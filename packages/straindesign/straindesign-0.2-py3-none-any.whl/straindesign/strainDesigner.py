import numpy as np
from scipy import sparse
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, List, Tuple
from cobra import Model, Metabolite, Reaction
from cobra.util.array import create_stoichiometric_matrix
from straindesign import StrainDesignMILP, SDModule, SDSolution, avail_solvers
from straindesign.fva import *
from straindesign.names import *
import straindesign.efmtool as efm
import jpype
from sympy import Rational, nsimplify, parse_expr, to_dnf
from sympy.core.numbers import One
import io

# import efmtool_link.efmtool4cobra as efm
# import efmtool_link.efmtool_intern as efm

def remove_irrelevant_genes(model,essential_reacs,gkis,gkos):
    # 1) Remove gpr rules from blocked reactions
    blocked_reactions = [reac.id for reac in model.reactions if reac.bounds == (0, 0)]
    for rid in blocked_reactions:
        model.reactions.get_by_id(rid).gene_reaction_rule = ''
    for g in model.genes[::-1]: # iterate in reverse order to avoid mixing up the order of the list when removing genes
        if not g.reactions:
            model.genes.remove(g)
    protected_genes = set()
    # 1. Protect genes that only occur in essential reactions
    for g in model.genes:
        if not g.reactions or {r.id for r in g.reactions}.issubset(essential_reacs):
            protected_genes.add(g)
    # 2. Protect genes that are essential to essential reactions
    for r in [model.reactions.get_by_id(s) for s in essential_reacs]:
        for g in r.genes:
            exp = r.gene_reaction_rule.replace(' or ',' | ').replace(' and ',' & ')
            exp = to_dnf(parse_expr(exp,{g.id:False}),force=True)
            if exp == False:
                protected_genes.add(g)
    # 3. Remove essential genes, and knockouts without impact from gko_costs
    [gkos.pop(pg.id) for pg in protected_genes if pg.id in gkos]
    # 4. Add all notknockable genes to the protected list
    [protected_genes.add(g) for g in model.genes if (g.id not in gkos) and (g.name not in gkos)] # support names or ids in gkos
    # genes with kiCosts are kept
    gki_ids = [g.id for g in model.genes if (g.id in gkis) or (g.name in gkis)] # support names or ids in gkis
    protected_genes = protected_genes.difference({model.genes.get_by_id(g) for g in gki_ids})
    protected_genes_dict = {pg.id: True for pg in protected_genes}
    # 5. Simplify gpr rules and discard rules that cannot be knocked out
    for r in model.reactions:
        if r.gene_reaction_rule:
            exp = r.gene_reaction_rule.replace(' or ',' | ').replace(' and ',' & ')
            exp = to_dnf(parse_expr(exp,protected_genes_dict),simplify=True,force=True)
            if exp == True:
                model.reactions.get_by_id(r.id).gene_reaction_rule = ''
            elif exp == False:
                print('Something went wrong during gpr rule simplification.')
            else:
                model.reactions.get_by_id(r.id).gene_reaction_rule = str(exp).replace(' & ',' and ').replace(' | ',' or ')
    # 6. Remove obsolete genes and protected genes
    for g in model.genes[::-1]:
        if not g.reactions or g in protected_genes:
            model.genes.remove(g)
    return gkos

def extend_model_gpr(model,gkos,gkis):
    # Split reactions when necessary
    reac_map = {}
    rev_reac = set()
    del_reac = set()
    for r in model.reactions:
        reac_map.update({r.id:{}})
        if not r.gene_reaction_rule:
            reac_map[r.id].update({r.id: 1.0})
            continue
        if r.gene_reaction_rule and r.bounds[0] < 0:
            r_rev = (r*-1)
            if r.gene_reaction_rule and r.bounds[1] > 0:
                r_rev.id = r.id+'_reverse_'+hex(hash(r))[8:]
            r_rev.lower_bound = np.max([0,r_rev.lower_bound])
            reac_map[r.id].update({r_rev.id: -1.0})
            rev_reac.add(r_rev)
        if r.gene_reaction_rule and r.bounds[1] > 0:
            reac_map[r.id].update({r.id: 1.0})
            r._lower_bound = np.max([0,r._lower_bound])
        else:
            del_reac.add(r)
    model.remove_reactions(del_reac)
    model.add_reactions(rev_reac)
    
    gene_names = set(g.name for g in model.genes)
    gene_names_exist = np.all([len(g.name) for g in model.genes])
    use_name_not_id = gene_names_exist and (gene_names.intersection(gkos) or gene_names.intersection(gkis))
   
    # All reaction rules are provided in dnf.
    for r in model.reactions:
        if r.gene_reaction_rule: # if reaction has a gpr rule
            dt = [s.strip() for s in r.gene_reaction_rule.split(' or ')]
            for i,p in enumerate(dt.copy()):
                ct = [s.strip() for s in p.replace('(','').replace(')','').split(' and ')]
                for j,g in enumerate(ct.copy()):
                    gene_met_id = 'g_'+g
                    # if gene is not in model, add gene pseudoreaction and metabolite
                    if gene_met_id not in model.metabolites.list_attr('id'):
                        model.add_metabolites(Metabolite(gene_met_id))
                        gene = model.genes.get_by_id(g)
                        w = Reaction(gene.id)
                        if use_name_not_id: # if gene name is available and used in gki_cost and gko_cost
                            w.id = gene.name
                        model.add_reaction(w)
                        w.reaction = '--> '+gene_met_id
                        w._upper_bound = np.inf
                    ct[j] = gene_met_id
                if len(ct) > 1:
                    ct_met_id = "_and_".join(ct)
                    if ct_met_id not in model.metabolites.list_attr('id'):
                        # if conjunct term is not in model, add pseudoreaction and metabolite
                        model.add_metabolites(Metabolite(ct_met_id))
                        w = Reaction("R_"+ct_met_id)
                        model.add_reaction(w)
                        w.reaction = ' + '.join(ct)+'--> '+ct_met_id
                        w._upper_bound = np.inf
                    dt[i] = ct_met_id
                else:
                    dt[i] = gene_met_id
            if len(dt) > 1:
                dt_met_id = "_or_".join(dt)
                if dt_met_id not in model.metabolites.list_attr('id'):
                    model.add_metabolites(Metabolite(dt_met_id))
                    for k,d in enumerate(dt):
                        w = Reaction("R"+str(k)+"_"+dt_met_id)
                        model.add_reaction(w)
                        w.reaction = d+' --> '+dt_met_id
                        w._upper_bound = np.inf
            else:
                dt_met_id = dt[0]
            r.add_metabolites({model.metabolites.get_by_id(dt_met_id): -1.0})
    return reac_map

def extend_model_regulatory(model, regcost, kocost):
    for reg_name, vals in regcost.items():
        lhs = vals['lhs']
        eqsign = vals['eqsign'] 
        rhs = vals['rhs']
        cost = vals['cost']
        reg_pseudomet_name = 'met_'+reg_name
        # add pseudometabolite
        m = Metabolite(reg_pseudomet_name)
        model.add_metabolites(m)
        # add pseudometabolite to stoichiometries
        for l,w in lhs.items():
            r = model.reactions.get_by_id(l)
            r.add_metabolites({m: w})
        # add pseudoreaction that defines the bound
        s = Reaction("bnd_"+reg_name)
        model.add_reaction(s)
        s.reaction = reg_pseudomet_name + ' --> '
        if eqsign == '=':
            s._lower_bound = -np.inf
            s._upper_bound = rhs
            s._lower_bound = rhs
        elif eqsign == '<=':
            s._lower_bound = -np.inf
            s._upper_bound = rhs
        elif eqsign == '>=':
            s._upper_bound = np.inf
            s._lower_bound = rhs
        # add knockable pseudoreaction and add it to the kocost list
        t = Reaction(reg_name)
        model.add_reaction(t)
        t.reaction = '--> '+reg_pseudomet_name
        t._upper_bound =  np.inf
        t._lower_bound = -np.inf
        kocost.update({reg_name:cost})
    return kocost

def preprocess_regulatory(model,reg_cost,has_gene_names):
    keywords = set(model.reactions.list_attr('id')+model.genes.list_attr('name')+model.genes.list_attr('id'))
    if '' in keywords:
        keywords.remove('')
    if has_gene_names:
        g_id_name_dict = {k:v for k,v in zip(model.genes.list_attr('id'),model.genes.list_attr('name'))}
    for k,v in reg_cost.copy().items():
    # generate name for regulatory pseudoreaction
        try:
            constr = parse_constraints(k,keywords)[0]
        except:
            raise Exception('Regulatory constraints could not be parsed. Please revise.')
        reacs_dict = constr[0]
        if has_gene_names:
            [reacs_dict.update({g_id_name_dict[l]:reacs_dict.pop(l)}) \
                for l in reacs_dict.copy().keys() if l in g_id_name_dict]
        eqsign = constr[1]
        rhs = constr[2]
        reg_name = ''
        for l,w in reacs_dict.items():
            if w<0:
                reg_name += 'n'+str(w)+'_'+l
            else:
                reg_name += 'p'+str(w)+'_'+l
            reg_name += '_'
        if eqsign == '=':
            reg_name += 'eq_'
        elif eqsign == '<=':
            reg_name += 'le_'
        elif eqsign == '>=':
            reg_name += 'ge_'
        reg_name += str(rhs)
        reg_cost.pop(k)
        reg_cost.update({reg_name:{'str' : k,'lhs' : reacs_dict, 'eqsign' : eqsign, 'rhs' : rhs, 'cost': v}})
    return reg_cost

def remove_blocked_reactions(model) -> List:
    blocked_reactions = [reac for reac in model.reactions if reac.bounds == (0, 0)]
    model.remove_reactions(blocked_reactions)
    return blocked_reactions

def remove_ext_mets(model):
    external_mets = [i for i,cpts in zip(model.metabolites,model.metabolites.list_attr("compartment")) if cpts == 'External_Species']
    model.remove_metabolites(external_mets)
    stoich_mat = create_stoichiometric_matrix(model)
    obsolete_reacs = [reac for reac,b_rempty in zip(model.reactions,np.any(stoich_mat,0)) if not b_rempty]
    model.remove_reactions(obsolete_reacs)

def remove_conservation_relations(model):
    stoich_mat = create_stoichiometric_matrix(model, array_type='lil')
    basic_metabolites = efm.basic_columns_rat(stoich_mat.transpose().toarray(), tolerance=0)
    dependent_metabolites = [model.metabolites[i].id for i in set(range(len(model.metabolites))) - set(basic_metabolites)]
    # print("The following metabolites have been removed from the model:")
    # print(dependent_metabolites)
    for m in dependent_metabolites:
        model.metabolites.get_by_id(m).remove_from_model()
    
# replace all stoichiometric coefficients with rationals.
def stoichmat_coeff2rational(model):
    num_reac = len(model.reactions)
    for i in range(num_reac):
        for k, v in model.reactions[i]._metabolites.items():
            if type(v) is float or type(v) is int:
                if type(v) is int or v.is_integer():
                    # v = int(v)
                    # n = int2jBigInteger(v)
                    # d = BigInteger.ONE
                    v = Rational(v) # for simplicity and actually slighlty faster (?)
                else:
                    rational_conversion='base10' # This was formerly in the function parameters 
                    v = nsimplify(v, rational=True, rational_conversion=rational_conversion)
                    # v = sympy.Rational(v)
                model.reactions[i]._metabolites[k] = v # only changes coefficient in the model, not in the solver
            elif not isinstance(v,Rational):
                raise TypeError

# replace all stoichiometric coefficients with ints and floats
def stoichmat_coeff2float(model):
    num_reac = len(model.reactions)
    for i in range(num_reac):
        for k, v in model.reactions[i]._metabolites.items():
            if v.is_Float or v.is_Rational or v.is_Integer:
                model.reactions[i]._metabolites[k] = float(v)
            else:
                raise Exception('unknown data type')
            
def modules_coeff2rational(sd_modules):
    for i,module in enumerate(sd_modules):
        for param in [CONSTRAINTS,INNER_OBJECTIVE, OUTER_OBJECTIVE, PROD_ID]:
            if param in module and module[param] is not None:
                if param == CONSTRAINTS:
                    for constr in module[CONSTRAINTS]:
                        for reac in constr[0].keys():
                            constr[0][reac] = nsimplify(constr[0][reac])
                if param in [INNER_OBJECTIVE, OUTER_OBJECTIVE, PROD_ID]:
                    for reac in module[param].keys():
                        module[param][reac] = nsimplify(module[param][reac])
    return sd_modules

def modules_coeff2float(sd_modules):
    for i,module in enumerate(sd_modules):
        for param in [CONSTRAINTS,INNER_OBJECTIVE, OUTER_OBJECTIVE, PROD_ID]:
            if param in module and module[param] is not None:
                if param == CONSTRAINTS:
                    for constr in module[CONSTRAINTS]:
                        for reac in constr[0].keys():
                            constr[0][reac] = float(constr[0][reac])
                if param in [INNER_OBJECTIVE, OUTER_OBJECTIVE, PROD_ID]:
                    for reac in module[param].keys():
                        module[param][reac] = float(module[param][reac])
    return sd_modules

# compression function (mostly copied from efmtool)
def compress_model(model):
    for r in model.reactions:
        r.gene_reaction_rule = ''
    num_met = len(model.metabolites)
    num_reac = len(model.reactions)
    old_reac_ids = [r.id for r in model.reactions]
    stoich_mat = efm.DefaultBigIntegerRationalMatrix(num_met, num_reac)
    reversible = jpype.JBoolean[:]([r.reversibility for r in model.reactions])
    # start_time = time.monotonic()
    flipped = []
    for i in range(num_reac):
        if model.reactions[i].upper_bound <= 0: # can run in backwards direction only (is and stays classified as irreversible)
            model.reactions[i] *= -1
            flipped.append(i)
            # print("Flipped", model.reactions[i].id)
        # have to use _metabolites because metabolites gives only a copy
        for k, v in model.reactions[i]._metabolites.items():
            n, d = efm.sympyRat2jBigIntegerPair(v)
            stoich_mat.setValueAt(model.metabolites.index(k.id), i, efm.BigFraction(n, d))
    # compress
    smc = efm.StoichMatrixCompressor(efm.subset_compression)
    reacNames = jpype.JString[:](model.reactions.list_attr('id'))
    comprec = smc.compress(stoich_mat, reversible, jpype.JString[num_met], reacNames,None)
    subset_matrix= efm.jpypeArrayOfArrays2numpy_mat(comprec.post.getDoubleRows())
    del_rxns = np.logical_not(np.any(subset_matrix, axis=1)) # blocked reactions
    for j in range(subset_matrix.shape[1]):
        rxn_idx = subset_matrix[:, j].nonzero()[0]
        r0 = rxn_idx[0]
        model.reactions[r0].subset_rxns = []
        model.reactions[r0].subset_stoich = []
        for r in rxn_idx: # rescale all reactions in this subset
            # !! swaps lb, ub when the scaling factor is < 0, but does not change the magnitudes
            factor = efm.jBigFraction2sympyRat(comprec.post.getBigFractionValueAt(r, j))
            # factor = jBigFraction2intORsympyRat(comprec.post.getBigFractionValueAt(r, j)) # does not appear to make a speed difference
            model.reactions[r] *=  factor #subset_matrix[r, j]
            # factor = abs(float(factor)) # context manager has trouble with non-float bounds
            if model.reactions[r].lower_bound not in (0, -float('inf')):
                model.reactions[r].lower_bound/= abs(subset_matrix[r, j]) #factor
            if model.reactions[r].upper_bound not in (0, float('inf')):
                model.reactions[r].upper_bound/= abs(subset_matrix[r, j]) #factor
            model.reactions[r0].subset_rxns.append(r)
            if r in flipped:
                model.reactions[r0].subset_stoich.append(-factor)
            else:
                model.reactions[r0].subset_stoich.append(factor)
        for r in rxn_idx[1:]: # merge reactions
            # rename main reaction
            if len(model.reactions[r0].id)+len(model.reactions[r].id) < 220 and model.reactions[r0].id[-3:] != '...':
                model.reactions[r0].id += '*'+model.reactions[r].id # combine names
            elif not model.reactions[r0].id[-3:] == '...':
                model.reactions[r0].id += '...'
            # !! keeps bounds of reactions[rxn_idx[0]]
            model.reactions[r0] += model.reactions[r]
            if model.reactions[r].lower_bound > model.reactions[r0].lower_bound:
                model.reactions[r0].lower_bound = model.reactions[r].lower_bound
            if model.reactions[r].upper_bound < model.reactions[r0].upper_bound:
                model.reactions[r0].upper_bound = model.reactions[r].upper_bound
            del_rxns[r] = True
    # print(time.monotonic() - start_time) # 11 seconds in iJO1366
    del_rxns = np.where(del_rxns)[0]
    for i in range(len(del_rxns)-1, -1, -1): # delete in reversed index order to keep indices valid
        model.reactions[del_rxns[i]].remove_from_model(remove_orphans=True)
    subT = np.zeros((num_reac, len(model.reactions)))
    rational_map = {}
    for j in range(subT.shape[1]):
        subT[model.reactions[j].subset_rxns, j] = [float(v) for v in model.reactions[j].subset_stoich]
        # rational_map is a dictionary that associates the new reaction with a dict of its original reactions and its scaling factors
        rational_map.update({model.reactions[j].id: {old_reac_ids[i]: v for i,v in zip(model.reactions[j].subset_rxns,model.reactions[j].subset_stoich)}})
    # for i in flipped: # adapt so that it matches the reaction direction before flipping
    #         subT[i, :] *= -1
    return sparse.csc_matrix(subT), rational_map

def compress_model_parallel(model, protected_rxns=[]):
    # lump parallel reactions
    # 
    # - exclude lumping of reactions with inhomogenous bounds
    # - exclude protected reactions
    old_num_reac = len(model.reactions)
    old_objective = [r.objective_coefficient for r in model.reactions]
    old_reac_ids = [r.id for r in model.reactions]
    stoichmat_T = create_stoichiometric_matrix(model,'lil').transpose()
    factor = [d[0] if d else 1.0 for d in stoichmat_T.data]
    A = (sparse.diags(factor)@stoichmat_T)
    lb = [r.lower_bound for r in model.reactions]
    ub = [r.upper_bound for r in model.reactions]
    fwd = sparse.lil_matrix([1. if (np.isinf(u) and f>0 or np.isinf(l) and f<0) else 0. for f,l,u in zip(factor,lb,ub)]).transpose()
    rev = sparse.lil_matrix([1. if (np.isinf(l) and f>0 or np.isinf(u) and f<0) else 0. for f,l,u in zip(factor,lb,ub)]).transpose()
    inh = sparse.lil_matrix([i+1 if not ((np.isinf(ub[i]) or ub[i] == 0) and (np.isinf(lb[i]) or lb[i] == 0)) \
                                 else 0 for i in range(len(model.reactions))]).transpose()
    A = sparse.hstack((A,fwd,rev,inh),'csr')
    # find equivalent/parallel reactions
    subset_list = []
    prev_found = []
    protected = [True if r.id in protected_rxns else False for r in model.reactions]
    hashes = [hash((tuple(A[i].indices),tuple(A[i].data))) for i in range(A.shape[0])]
    for i in range(A.shape[0]):
        if i in prev_found: # if reaction was already found to be identical to another one, skip.
            continue
        if protected[i]: # if protected, add 1:1 relationship, skip.
            subset_list += [[i]]
            continue
        subset_i = [i]
        for j in range(i+1,A.shape[0]): # otherwise, identify parallel reactions
            if not protected[j] and j not in prev_found:
                # if np.all(A[i].indices == A[j].indices) and np.all(A[i].data == A[j].data):
                if hashes[i] == hashes[j]:
                    subset_i += [j]
                    prev_found += [j]
        if subset_i:
            subset_list += [subset_i]
    # lump parallel reactions (delete redundant)
    del_rxns = [False]*len(model.reactions)
    for rxn_idx in subset_list:
        for i in range(1, len(rxn_idx)):
            if len(model.reactions[rxn_idx[0]].id)+len(model.reactions[rxn_idx[i]].id) < 220  and model.reactions[rxn_idx[0]].id[-3:] != '...':
                model.reactions[rxn_idx[0]].id += '*'+model.reactions[rxn_idx[i]].id # combine names
            elif not model.reactions[rxn_idx[0]].id[-3:] == '...':
                model.reactions[rxn_idx[0]].id += '...'
            del_rxns[rxn_idx[i]] = True
    del_rxns = np.where(del_rxns)[0]
    for i in range(len(del_rxns)-1, -1, -1): # delete in reversed index order to keep indices valid
        model.reactions[del_rxns[i]].remove_from_model(remove_orphans=True)
    # create compression map
    rational_map = {}
    subT = np.zeros((old_num_reac, len(model.reactions)))
    for i in range(subT.shape[1]):
        for j in subset_list[i]:
            subT[j,i] = 1
        # rational_map is a dictionary that associates the new reaction with a dict of its original reactions and its scaling factors
        rational_map.update({model.reactions[i].id: {old_reac_ids[j]: One() for j in subset_list[i]}})
        
    new_objective = old_objective@subT
    for r,c in zip(model.reactions,new_objective):
        r.objective_coefficient = c
    return sparse.csc_matrix(subT), rational_map


class StrainDesigner(StrainDesignMILP):
    def __init__(self, model: Model, sd_modules: List[SDModule], *args, **kwargs):
        allowed_keys = {SOLVER, MAX_COST, 'M', 'compress',KOCOST,KICOST,GKOCOST,GKICOST,REGCOST}
        # set all keys that are not in kwargs to None
        for key in allowed_keys:
            if key not in dict(kwargs).keys() and key not in {GKOCOST,GKICOST}:
                kwargs[key] = None
        # check all keys passed in kwargs
        for key, value in dict(kwargs).items():
            if key in allowed_keys:
                setattr(self,key,value)
            else:
                raise Exception("Key " + key + " is not supported.")
            if key == KOCOST:
                self.uncmp_ko_cost = value
            if key == KICOST:
                self.uncmp_ki_cost = value
            if key == GKOCOST:
                self.uncmp_gko_cost = value
            if key == GKICOST:
                self.uncmp_gki_cost = value
            if key == REGCOST:
                self.uncmp_reg_cost = value
        if (GKOCOST in kwargs or GKICOST in kwargs) and hasattr(model,'genes') and model.genes:
            self.gene_sd = True
            if np.any([len(g.name) for g in model.genes]):
                self.has_gene_names = True
            else:
                self.has_gene_names = False
            if GKOCOST not in kwargs or not kwargs[GKOCOST]:
                if self.has_gene_names: # if gene names are defined, use them instead of ids
                    self.uncmp_gko_cost = {k:1.0 for k in model.genes.list_attr('name')}
                else:
                    self.uncmp_gko_cost = {k:1.0 for k in model.genes.list_attr('id')}
            if GKICOST not in kwargs or not kwargs[GKICOST]:
                self.uncmp_gki_cost = {}
        else:
            self.gene_sd = False
            self.has_gene_names = False
        if not kwargs[KOCOST] and not self.gene_sd:
            self.uncmp_ko_cost = {k:1.0 for k in model.reactions.list_attr('id')}
        elif not kwargs[KOCOST]:
            self.uncmp_ko_cost = {}
        if not kwargs[KICOST]:
            self.uncmp_ki_cost = {}
        if not kwargs[REGCOST]:
            self.uncmp_reg_cost = {}
        # put module in list if only one module was provided
        if "SDModule" in str(type(sd_modules)):
            sd_modules = [sd_modules]
        self.orig_sd_modules = sd_modules
        # check that at most one bilevel module is provided
        bilvl_modules = [i for i,m in enumerate(sd_modules) \
                    if m[MODULE_TYPE] in [OPTKNOCK,ROBUSTKNOCK,OPTCOUPLE]]
        if len(bilvl_modules) > 1:
            raise Exception("Only one of the module types 'OptKnock', 'RobustKnock' and 'OptCouple' can be defined per "\
                                "strain design setup.")
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()): # suppress standard output from copying model
            self.orig_model = model.copy()
        self.orig_ko_cost   = self.uncmp_ko_cost
        self.orig_ki_cost   = self.uncmp_ki_cost
        self.orig_reg_cost  = self.uncmp_reg_cost
        self.compress        = kwargs['compress']
        self.M               = kwargs['M']
        self.uncmp_reg_cost = preprocess_regulatory(model,self.uncmp_reg_cost,self.has_gene_names)
        if self.gene_sd:
            self.orig_gko_cost   = self.uncmp_gko_cost
            self.orig_gki_cost   = self.uncmp_gki_cost
            # ensure that gene and reaction kos/kis do not overlap
            g_itv = {g for g in list(self.uncmp_gko_cost.keys())+list(self.uncmp_gki_cost.keys())}
            r_itv = {r for r in list(self.uncmp_ko_cost.keys())+list(self.uncmp_ki_cost.keys())}
            if np.any([np.any([True for g in model.reactions.get_by_id(r).genes if g in g_itv]) for r in r_itv]) or \
                np.any(set(self.uncmp_gko_cost.keys()).intersection(set(self.uncmp_gki_cost.keys()))) or \
                np.any(set(self.uncmp_ko_cost.keys()).intersection(set(self.uncmp_ki_cost.keys()))):
                raise Exception('Specified gene and reaction knock-out/-in costs contain overlap. '\
                                'Make sure that metabolic interventions are enabled either through reaction or '\
                                'through gene interventions and are defined either as knock-ins or as knock-outs.')
        # 1) Preprocess Model
        print('Preparing strain design computation.')
        if self.solver is None:
            if CPLEX in avail_solvers:
                self.solver = CPLEX
            elif GUROBI in avail_solvers:
                self.solver = GUROBI
            elif SCIP in avail_solvers:
                self.solver = SCIP
            else:
                self.solver = GLPK
        elif self.solver not in avail_solvers:
            raise Exception("Selected solver is not installed / set up correctly.")
        else:
            self.solver = self.solver
        print('  Using '+self.solver+' for solving LPs during preprocessing.')
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()): # suppress standard output from copying model
            cmp_model = model.copy()
        # remove external metabolites
        remove_ext_mets(cmp_model)
        # replace model bounds with +/- inf if above a certain threshold
        bound_thres = 1000
        if any([any([abs(b)>=bound_thres for b in r.bounds]) for r in cmp_model.reactions]):
            print('  Removing reaction bounds when larger than the threshold of '+str(bound_thres)+'.')
            for i in range(len(cmp_model.reactions)):
                if cmp_model.reactions[i].lower_bound <= -bound_thres:
                    cmp_model.reactions[i].lower_bound = -np.inf
                if cmp_model.reactions[i].upper_bound >=  bound_thres:
                    cmp_model.reactions[i].upper_bound =  np.inf
        # FVAs to identify blocked, irreversible and essential reactions, as well as non-bounding bounds
        print('  FVA to identify blocked reactions and irreversibilities.')
        flux_limits = fva(cmp_model,solver=kwargs[SOLVER])
        if kwargs[SOLVER] in ['scip','glpk']:
            tol = 1e-10 # use tolerance for tightening problem bounds
        else:
            tol = 0.0
        for (reac_id, limits) in flux_limits.iterrows():
            r = cmp_model.reactions.get_by_id(reac_id)
            # modify _lower_bound and _upper_bound to make changes permanent
            if r.lower_bound < 0.0 and limits.minimum - tol > r.lower_bound:
                r._lower_bound = -np.inf
            if limits.minimum >= tol:
                r._lower_bound = np.max([0.0,r._lower_bound])
            if r.upper_bound > 0.0 and limits.maximum + tol < r.upper_bound:
                r._upper_bound = np.inf
            if limits.maximum <= -tol:
                r._upper_bound = np.min([0.0,r._upper_bound])
        print('  FVA(s) to identify essential reactions.')
        essential_reacs = set()
        for m in sd_modules:
            if m[MODULE_TYPE] != SUPPRESS:  # Essential reactions can only be determined from desired
                                            # or opt-/robustknock modules
                flux_limits = fva(cmp_model,solver=kwargs[SOLVER],constraints=m[CONSTRAINTS])
                for (reac_id, limits) in flux_limits.iterrows():
                    if np.min(abs(limits)) > tol and np.prod(np.sign(limits)) > 0: # find essential
                        essential_reacs.add(reac_id)
        # remove ko-costs (and thus knockability) of essential reactions
        [self.uncmp_ko_cost.pop(er) for er in essential_reacs if er in self.uncmp_ko_cost]
        # If computation of gene-gased intervention strategies, (optionally) compress gpr are rules and extend stoichimetric network with genes
        if self.gene_sd:
            if kwargs['compress'] is True or kwargs['compress'] is None:
                num_genes = len(cmp_model.genes)
                num_gpr   = len([True for r in model.reactions if r.gene_reaction_rule])
                print('Preprocessing GPR rules ('+str(num_genes)+' genes, '+str(num_gpr)+' gpr rules).')
                # removing irrelevant genes will also remove essential reactions from the list of knockable genes
                self.uncmp_gko_cost = remove_irrelevant_genes(cmp_model, essential_reacs, self.uncmp_gki_cost, self.uncmp_gko_cost)
                if len(cmp_model.genes) < num_genes or len([True for r in model.reactions if r.gene_reaction_rule]) < num_gpr:
                    num_genes = len(cmp_model.genes)
                    num_gpr   = len([True for r in cmp_model.reactions if r.gene_reaction_rule])
                    print('  Simplifyied to '+str(num_genes)+' genes and '+\
                        str(num_gpr)+' gpr rules.')
            print('  Extending metabolic network with gpr associations.')
            reac_map = extend_model_gpr(cmp_model,self.uncmp_gko_cost, self.uncmp_gki_cost)
            for i,m in enumerate(sd_modules):
                for p in [CONSTRAINTS, INNER_OBJECTIVE, OUTER_OBJECTIVE, PROD_ID]:
                    if p in m and m[p] is not None:
                        if p == CONSTRAINTS:
                            for c in m[p]:
                                for k in list(c[0].keys()):
                                    v = c[0].pop(k)
                                    for n,w in reac_map[k].items():
                                        c[0][n] = v*w
                        if p in [INNER_OBJECTIVE, OUTER_OBJECTIVE, PROD_ID]:
                            for k in list(m[p].keys()):
                                v = m[p].pop(k)
                                for n,w in reac_map[k].items():
                                    m[p][n] = v*w
            self.uncmp_ko_cost.update(self.uncmp_gko_cost)
            self.uncmp_ki_cost.update(self.uncmp_gki_cost)
        self.uncmp_ko_cost = extend_model_regulatory(cmp_model,self.uncmp_reg_cost,self.uncmp_ko_cost)
        self.cmp_ko_cost = self.uncmp_ko_cost
        self.cmp_ki_cost = self.uncmp_ki_cost
        # Compress model
        self.cmp_mapReac = []
        if  kwargs['compress'] is True or kwargs['compress'] is None: # If compression is activated (or not defined)
            print('Compressing Network ('+str(len(cmp_model.reactions))+' reactions).')
            # compress network by lumping sequential and parallel reactions alternatingly. 
            # Exclude reactions named in strain design modules from parallel compression
            no_par_compress_reacs = set()
            for m in sd_modules:
                for p in [CONSTRAINTS, INNER_OBJECTIVE, OUTER_OBJECTIVE, PROD_ID]:
                    if p in m and m[p] is not None:
                        param = m[p]
                        if p == CONSTRAINTS:
                            for c in param:
                                for k in c[0].keys():
                                    no_par_compress_reacs.add(k)
                        if p in [INNER_OBJECTIVE, OUTER_OBJECTIVE, PROD_ID]:
                            for k in param.keys():
                                    no_par_compress_reacs.add(k)
            # Remove conservation relations.
            print('  Removing blocked reactions.')
            blocked_reactions = remove_blocked_reactions(cmp_model)
            # remove blocked reactions from ko- and ki-costs
            [self.cmp_ko_cost.pop(br.id) for br in blocked_reactions if br.id in self.cmp_ko_cost]
            [self.cmp_ki_cost.pop(br.id) for br in blocked_reactions if br.id in self.cmp_ki_cost]
            print('  Translating stoichiometric coefficients to rationals.')
            stoichmat_coeff2rational(cmp_model)
            sd_modules = modules_coeff2rational(sd_modules)
            print('  Removing conservation relations.')
            remove_conservation_relations(cmp_model)
            odd = True
            run = 1
            while True:
                # np.savetxt('Table.csv',create_stoichiometric_matrix(cmp_model),'%i',',')
                if odd:
                    print('  Compression '+str(run)+': Applying compression from EFM-tool module.')
                    subT, reac_map_exp = compress_model(cmp_model)
                    for new_reac, old_reac_val in reac_map_exp.items():
                        old_reacs_no_compress = [r for r in no_par_compress_reacs if r in old_reac_val]
                        if old_reacs_no_compress:
                            [no_par_compress_reacs.remove(r) for r in old_reacs_no_compress]
                            no_par_compress_reacs.add(new_reac)                            
                else:
                    print('  Compression '+str(run)+': Lumping parallel reactions.')
                    subT, reac_map_exp = compress_model_parallel(cmp_model, no_par_compress_reacs)
                remove_conservation_relations(cmp_model)
                if subT.shape[0] > subT.shape[1]:
                    print('  Reduced to '+str(subT.shape[1])+' reactions.')
                    # store the information for decompression in a Tuple
                    # (0) compression matrix, (1) reac_id dictornary {cmp_rid: {orig_rid1: factor1, orig_rid2: factor2}}, 
                    # (2) linear (True) or parallel (False) compression (3,4) ko and ki costs of expanded network
                    self.cmp_mapReac += [{"reac_map_exp":reac_map_exp,
                                          "odd":odd,
                                          KOCOST:self.cmp_ko_cost,
                                          KICOST:self.cmp_ki_cost}]
                    # compress information in strain design modules
                    if odd:
                        for new_reac, old_reac_val in reac_map_exp.items():
                            for i,m in enumerate(sd_modules):
                                for p in [CONSTRAINTS, INNER_OBJECTIVE, OUTER_OBJECTIVE, PROD_ID,MIN_GCP]:
                                    if p in m and m[p] is not None:
                                        param = m[p]
                                        if p == CONSTRAINTS:
                                            for j,c in enumerate(m[p]):
                                                if np.any([k in old_reac_val for k in c[0].keys()]):
                                                    lumped_reacs = [k for k in c[0].keys() if k in old_reac_val]
                                                    c[0][new_reac] = np.sum([c[0].pop(k)*old_reac_val[k] for k in lumped_reacs])
                                        if p in [INNER_OBJECTIVE, OUTER_OBJECTIVE, PROD_ID]:
                                            if np.any([k in old_reac_val for k in param.keys()]):
                                                lumped_reacs = [k for k in param.keys() if k in old_reac_val]
                                                m[p][new_reac] = np.sum([param.pop(k)*old_reac_val[k] for k in lumped_reacs if k in old_reac_val])
                                        # if p == MIN_GCP:
                                        #     m[p] = m[p]
                                        #     print('lol')
                    # compress ko_cost and ki_cost
                    # ko_cost of lumped reactions: when reacs sequential: lowest of ko costs, when parallel: sum of ko costs
                    # ki_cost of lumped reactions: when reacs sequential: sum of ki costs, when parallel: lowest of ki costs
                    if self.cmp_ko_cost:
                        ko_cost_new = {}
                        for r in cmp_model.reactions.list_attr('id'):
                            if np.any([s in self.cmp_ko_cost for s in reac_map_exp[r]]):
                                if odd and not np.any([s in self.cmp_ki_cost for s in reac_map_exp[r]]):
                                    ko_cost_new[r] = np.min([self.cmp_ko_cost[s] for s in reac_map_exp[r] if s in self.cmp_ko_cost])
                                elif not odd:
                                    ko_cost_new[r] = np.sum([self.cmp_ko_cost[s] for s in reac_map_exp[r] if s in self.cmp_ko_cost])
                        self.cmp_ko_cost = ko_cost_new
                    if self.cmp_ki_cost:
                        ki_cost_new = {}
                        for r in cmp_model.reactions.list_attr('id'):
                            if np.any([s in self.cmp_ki_cost for s in reac_map_exp[r]]):
                                if odd:
                                    ki_cost_new[r] = np.sum([self.cmp_ki_cost[s] for s in reac_map_exp[r] if s in self.cmp_ki_cost])
                                elif not odd and not np.any([s in self.cmp_ko_cost for s in reac_map_exp[r]]):
                                    ki_cost_new[r] = np.min([self.cmp_ki_cost[s] for s in reac_map_exp[r] if s in self.cmp_ki_cost])
                        self.cmp_ki_cost = ki_cost_new
                    if odd:
                        odd = False
                    else:
                        odd = True
                    run += 1
                else:
                    print('  Last step could not reduce size further ('+str(subT.shape[0])+' reactions).')
                    print('  Network compression completed. ('+str(run-1)+' compression iterations)')
                    print('  Translating stoichiometric coefficients back to float.')
                    stoichmat_coeff2float(cmp_model)
                    sd_modules = modules_coeff2float(sd_modules)
                    break

        # An FVA to identify essentials before building and launching MILP (not sure if this has an effect)
        print('  FVA(s) in compressed model to identify essential reactions.')
        essential_reacs = set()
        for m in sd_modules:
            if m[MODULE_TYPE] != SUPPRESS:  # Essential reactions can only be determined from desired
                                            # or opt-/robustknock modules
                flux_limits = fva(cmp_model,solver=kwargs[SOLVER],constraints=m[CONSTRAINTS])
                for (reac_id, limits) in flux_limits.iterrows():
                    if np.min(abs(limits)) > tol and np.prod(np.sign(limits)) > 0: # find essential
                        essential_reacs.add(reac_id)
        # remove ko-costs (and thus knockability) of essential reactions
        [self.cmp_ko_cost.pop(er) for er in essential_reacs if er in self.cmp_ko_cost]
        essential_kis = set(self.cmp_ki_cost[er] for er in essential_reacs if er in self.cmp_ki_cost)
        # Build MILP
        kwargs1 = kwargs
        kwargs1[KOCOST] = self.cmp_ko_cost
        kwargs1[KICOST] = self.cmp_ki_cost
        kwargs1['essential_kis'] = essential_kis
        kwargs1.pop('compress')
        if GKOCOST in kwargs1:
            kwargs1.pop(GKOCOST)
        if GKICOST in kwargs1:
            kwargs1.pop(GKICOST)
        if REGCOST in kwargs1:
            kwargs1.pop(REGCOST)
        print("Finished preprocessing:")
        print("  Model size: "+str(len(cmp_model.reactions))+" reactions, "+str(len(cmp_model.metabolites))+" metabolites")
        print("  "+str(len(self.cmp_ko_cost)+len(self.cmp_ki_cost)-len(essential_kis))+" targetable reactions")
        super().__init__(cmp_model,sd_modules, *args, **kwargs1)

    def expand_sd(self,sd):
        # expand mcs by applying the compression steps in the reverse order
        cmp_map = self.cmp_mapReac[::-1]
        for exp in cmp_map:
            reac_map_exp = exp["reac_map_exp"] # expansion map
            ko_cost      = exp[KOCOST]
            ki_cost      = exp[KICOST]
            par_reac_cmp = not exp["odd"] # if parallel or sequential reactions were lumped
            for r_cmp,r_orig in reac_map_exp.items():
                if len(r_orig) > 1:
                    for m in sd.copy():
                        if r_cmp in m:
                            val = m[r_cmp]
                            del m[r_cmp]
                            if val < 0: # case: KO
                                if par_reac_cmp:
                                    new_m = m.copy()
                                    for d in r_orig:
                                        if d in ko_cost:
                                            new_m[d] = val
                                    sd += [new_m]
                                else:
                                    for d in r_orig:
                                        if d in ko_cost:
                                            new_m = m.copy()
                                            new_m[d] = val
                                            sd += [new_m]
                            elif val > 0: # case: KI
                                if par_reac_cmp:
                                    for d in r_orig:
                                        if d in ki_cost:
                                            new_m = m.copy()
                                            new_m[d] = val
                                            # other reactions do not need to be knocked in
                                            for f in [e for e in r_orig if (e in ki_cost) and e != d]:
                                                new_m[f] = 0.0
                                            sd += [new_m]
                                else:
                                    new_m = m.copy()
                                    for d in r_orig:
                                        if d in ki_cost:
                                            new_m[d] = val
                                    sd += [new_m]
                            elif val == 0: # case: KI that was not introduced
                                new_m = m.copy() # assume that none of the expanded
                                for d in r_orig: # reactions are inserted, neither
                                    if d in ki_cost: # parallel, nor sequential
                                        new_m[d] = val
                                sd += [new_m]
                            sd.remove(m)
        # eliminate mcs that are too expensive
        if self.max_cost:
            costs = [np.sum([self.uncmp_ko_cost[k] if v<0 else self.uncmp_ki_cost[k] for k,v in m.items()]) for m in sd]
            sd = [sd[i] for i in range(len(sd)) if costs[i] <= self.max_cost+1e-8]
        # mark regulatory interventions with true or false
        for s in sd:
            for k,v in self.uncmp_reg_cost.items():
                if k in s:
                    s.pop(k)
                    s.update({v['str']:True})
                else:
                    s.update({v['str']:False})
        return sd

    # function wrappers for compute, compute_optimal and enumerate
    def enumerate(self, *args, **kwargs):
        cmp_sd_solution = super().enumerate(*args, **kwargs)
        if cmp_sd_solution.status in [OPTIMAL,TIME_LIMIT_W_SOL]:
            sd = self.expand_sd(cmp_sd_solution.get_reaction_sd_mark_no_ki())
        else:
            sd = []
        solutions = self.build_full_sd_solution(sd, cmp_sd_solution)
        print(str(len(sd)) +' solutions found.')
        return solutions
    
    def compute_optimal(self, *args, **kwargs):
        cmp_sd_solution = super().compute_optimal(*args, **kwargs)
        if cmp_sd_solution.status in [OPTIMAL,TIME_LIMIT_W_SOL]:
            sd = self.expand_sd(cmp_sd_solution.get_reaction_sd_mark_no_ki())
        else:
            sd = []
        solutions = self.build_full_sd_solution(sd, cmp_sd_solution)
        print(str(len(sd)) +' solutions found.')
        return solutions
    
    def compute(self, *args, **kwargs):
        cmp_sd_solution = super().compute(*args, **kwargs)
        if cmp_sd_solution.status in [OPTIMAL,TIME_LIMIT_W_SOL]:
            sd = self.expand_sd(cmp_sd_solution.get_reaction_sd_mark_no_ki())
        else:
            sd = []
        solutions = self.build_full_sd_solution(sd, cmp_sd_solution)
        print(str(len(sd)) +' solutions found.')
        return solutions
    
    def build_full_sd_solution(self, sd, sd_solution_cmp):
        sd_setup = {}
        sd_setup[MODEL_ID]          = sd_solution_cmp.sd_setup.pop(MODEL_ID)
        sd_setup[MAX_SOLUTIONS]     = sd_solution_cmp.sd_setup.pop(MAX_SOLUTIONS)
        sd_setup[MAX_COST]          = sd_solution_cmp.sd_setup.pop(MAX_COST)
        sd_setup[TIME_LIMIT]        = sd_solution_cmp.sd_setup.pop(TIME_LIMIT)
        sd_setup[SOLVER]            = sd_solution_cmp.sd_setup.pop(SOLVER)
        sd_setup[SOLUTION_APPROACH] = sd_solution_cmp.sd_setup.pop(SOLUTION_APPROACH)
        sd_setup[MODULES] = self.orig_sd_modules
        sd_setup[KOCOST]  = self.orig_ko_cost
        sd_setup[KICOST]  = self.orig_ki_cost
        sd_setup[REGCOST] = self.orig_reg_cost
        if self.gene_sd:
            sd_setup[GKOCOST] = self.orig_gko_cost
            sd_setup[GKICOST] = self.orig_gki_cost
        return SDSolution(self.orig_model,sd,sd_solution_cmp.status,sd_setup)