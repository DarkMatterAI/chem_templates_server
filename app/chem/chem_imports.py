import json 

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import Descriptors
from rdkit.Chem import QED
from rdkit.Contrib.SA_Score import sascorer
from rdkit.Chem.FilterCatalog import FilterCatalog, FilterCatalogParams
from rdkit.Chem.Lipinski import RotatableBondSmarts

from chem_templates.filter import Filter, RangeFunctionFilter, CatalogFilter, FilterResult, Template, SimpleSmartsFilter
from chem_templates.chem import Molecule, Catalog
from chem_templates.utils import flatten_list, deduplicate_list
from chem_templates.building_blocks import REACTION_GROUP_DICT, Synthon, molecule_to_synthon, ReactionUniverse 
from chem_templates.assembly import (
                                    build_assembly_from_dict, 
                                    AssemblyInputs, 
                                    SynthonPool, 
                                    AssemblyPool,
                                    build_synthesis_scheme, 
                                    build_fragment_assembly_scheme
                                    )

def to_mol(smile):
    try:
        mol = Chem.MolFromSmiles(smile)
    except:
        mol = None
        
    return mol

def smart_to_mol(smarts):
    try:
        mol = Chem.MolFromSmarts(smarts)
    except:
        mol = None
        
    return mol

def find_bond_groups(mol):
    """
    Find groups of contiguous rotatable bonds and return them sorted by decreasing size

    https://www.rdkit.org/docs/Cookbook.html
    """
    rot_atom_pairs = mol.GetSubstructMatches(RotatableBondSmarts)
    rot_bond_set = set([mol.GetBondBetweenAtoms(*ap).GetIdx() for ap in rot_atom_pairs])
    rot_bond_groups = []
    while (rot_bond_set):
        i = rot_bond_set.pop()
        connected_bond_set = set([i])
        stack = [i]
        while (stack):
            i = stack.pop()
            b = mol.GetBondWithIdx(i)
            bonds = []
            for a in (b.GetBeginAtom(), b.GetEndAtom()):
                bonds.extend([b.GetIdx() for b in a.GetBonds() if (
                    (b.GetIdx() in rot_bond_set) and (not (b.GetIdx() in connected_bond_set)))])
            connected_bond_set.update(bonds)
            stack.extend(bonds)
        rot_bond_set.difference_update(connected_bond_set)
        rot_bond_groups.append(tuple(connected_bond_set))
    return tuple(sorted(rot_bond_groups, reverse = True, key = lambda x: len(x)))

def max_ring_size(mol):
    'size of largest ring'
    ring_info = mol.GetRingInfo()
    return max((len(r) for r in ring_info.AtomRings()), default=0)

def min_ring_size(mol):
    'size of smallest ring'
    ring_info = mol.GetRingInfo()
    return min((len(r) for r in ring_info.AtomRings()), default=0)

def loose_rotbond(mol):
    'number of rotatable bonds, includes things like amides and esters'
    return rdMolDescriptors.CalcNumRotatableBonds(mol, False)

def rot_chain_length(mol):
    'Length of longest contiguous rotatable bond chain'
    output = find_bond_groups(mol)
    output = len(output[0]) if output else 0
    return output

def num_compounds(mol):
    'number of molecules in mol'
    smile = Chem.MolToSmiles(mol)
    return smile.count('.')+1


PROP_FUNCS = {
    'Number of Compounds' : num_compounds,
    'TPSA' : rdMolDescriptors.CalcTPSA,
    'LogP' : Descriptors.MolLogP,
    
    'Molecular Weight' : rdMolDescriptors.CalcExactMolWt,
    'Heavy Atom Count' : rdMolDescriptors.CalcNumHeavyAtoms,
    'Atom Count' : rdMolDescriptors.CalcNumAtoms,
    'Heteroatom Count' : rdMolDescriptors.CalcNumHeteroatoms,
    'Spiro Atom Count' : rdMolDescriptors.CalcNumSpiroAtoms,
    'Bridgehead Atom Count' : rdMolDescriptors.CalcNumBridgeheadAtoms,
    'Stereocenter Count' : rdMolDescriptors.CalcNumAtomStereoCenters,
    
    'Hydrogen Bond Donors' : rdMolDescriptors.CalcNumHBD,
    'Hydrogen Bond Acceptors' : rdMolDescriptors.CalcNumHBA,
    
    'Formal Charge' : Chem.rdmolops.GetFormalCharge,
    
    'Rotatable Bonds' : rdMolDescriptors.CalcNumRotatableBonds,
    'Loose Rotatable Bonds' : loose_rotbond,
    'Rotatable Chain Length' : rot_chain_length,
    
    'Max Ring Size' : max_ring_size,
    'Min Ring Size' : min_ring_size,
    
    'Ring Count' : rdMolDescriptors.CalcNumRings,
    'Ring Count (Aromatic)' : rdMolDescriptors.CalcNumAromaticRings,
    'Ring Count (Saturated)' : rdMolDescriptors.CalcNumSaturatedRings,
    'Ring Count (Aliphatic)' : rdMolDescriptors.CalcNumAliphaticRings,
    
    'Heterocycle Count' : rdMolDescriptors.CalcNumHeterocycles,
    'Heterocycle Count (Aromatic)' : rdMolDescriptors.CalcNumAromaticHeterocycles,
    'Heterocycle Count (Saturated)' : rdMolDescriptors.CalcNumSaturatedHeterocycles,
    'Heterocycle Count (Aliphatic)' : rdMolDescriptors.CalcNumAliphaticHeterocycles,
    
    'Carbocycles (Aromatic)' : rdMolDescriptors.CalcNumAromaticCarbocycles,
    'Carbocycles (Saturated)' : rdMolDescriptors.CalcNumSaturatedCarbocycles,
    'Carbocycles (Aliphatic)' : rdMolDescriptors.CalcNumAliphaticCarbocycles,
    
    'Amide Bond Count' : rdMolDescriptors.CalcNumAmideBonds,
    'Fraction SP3' : rdMolDescriptors.CalcFractionCSP3,
    'QED' : QED.qed,
    'SA Score' : sascorer.calculateScore,
    'Molar Refractivity' : Descriptors.MolMR,
    'Radical Count' : Descriptors.NumRadicalElectrons
}

PROPERTY_NAMES = list(PROP_FUNCS.keys())

FILTER_CATALOGUES = {
    'PAINS' : FilterCatalog(FilterCatalogParams.FilterCatalogs.PAINS),
    'PAINS_A' : FilterCatalog(FilterCatalogParams.FilterCatalogs.PAINS_A),
    'PAINS_B' : FilterCatalog(FilterCatalogParams.FilterCatalogs.PAINS_B),
    'PAINS_C' : FilterCatalog(FilterCatalogParams.FilterCatalogs.PAINS_C),
    'BRENK' : FilterCatalog(FilterCatalogParams.FilterCatalogs.BRENK),
    'NIH' : FilterCatalog(FilterCatalogParams.FilterCatalogs.NIH),
    'ZINC' : FilterCatalog(FilterCatalogParams.FilterCatalogs.ZINC),
}

CATALOG_NAMES = list(FILTER_CATALOGUES.keys())

property_filter_description = '''property filters compute the `value` of some `property_name`. The `value` is then 
compared to `min_val` and `max_val`. If `min_val <= value <= max_val` (note this is inclusive), 
the property filter evaluates to `True`. Otherwise, the property filter evaluates to `False`.

If `min_val=None` or `max_val=None`, that bound is ignored. If both bounds are `None`, the 
property filter is ignored
'''

property_function_descriptions = {
    'Number of Compounds' : "counts the number of compounds in the input, denoted by `.` separation",
    'TPSA' : "TPSA value for the input",
    'LogP' : "cLogP for the input",
    
    'Molecular Weight' : "molecular weight of the input",
    'Heavy Atom Count' : "counts the number of heavy atoms in the input",
    'Atom Count' : "counts the total number of atoms in the input (including hydrogens)",
    'Heteroatom Count' : "counts the number of heteroatoms in the input",
    'Spiro Atom Count' : "counts the number of spirocarbons in the input",
    'Bridgehead Atom Count' : "counts the number of bridgehead atoms in the input",
    'Stereocenter Count' : "counts the number of stereocenters in the input",
    
    'Hydrogen Bond Donors' : "counts the number of hydrogen bond donors in the input",
    'Hydrogen Bond Acceptors' : "counts the number of hydrogen bond acceptors in the input",
    
    'Formal Charge' : "computes the overall formal charge of the input",
    
    'Rotatable Bonds' : "counts the number of rotatable bonds in the input",
    'Loose Rotatable Bonds' : "counts the number of rotatable bonds in the input, using looser criteria that includes things like amides and esters", 
    'Rotatable Chain Length' : "counts the length of the longest contiguous chain of rotatable bonds in the input",
    
    'Max Ring Size' : "computes the size of the largest ring in the input",
    'Min Ring Size' : "computes the size of the smallest ring in the input",
    
    'Ring Count' : "counts the number of rings in the input",
    'Ring Count (Aromatic)' : "counts the number of aromatic rings in the input",
    'Ring Count (Saturated)' : "counts the number of saturated rings in the input",
    'Ring Count (Aliphatic)' : "counts the number of aliphatic rings in the input",
    
    'Heterocycle Count' : "counts the number of heterocycles in the input",
    'Heterocycle Count (Aromatic)' : "counts the number of aromatic heterocycles in the input",
    'Heterocycle Count (Saturated)' : "counts the number of saturated heterocycles in the input",
    'Heterocycle Count (Aliphatic)' : "counts the number of aliphatic heterocycles in the input",
    
    'Carbocycles (Aromatic)' : "counts the number of aromatic carbocycles in the input",
    'Carbocycles (Saturated)' : "counts the number of saturated carbocycles in the input",
    'Carbocycles (Aliphatic)' : "counts the number of aliphatic carbocycles in the input",
    
    'Amide Bond Count' : "counts the number of amide bonds in the input",
    'Fraction SP3' : "computes the fraction SP3 of the input",
    'QED' : "computes the QED score of the input",
    'SA Score' : "computes the SA score of the input",
    'Molar Refractivity' : "computes the molar refractivity of the input",
    'Radical Count' : "counts the number of radical electrons in the input"
}

catalog_filter_description = '''catalog filters compare the input structure 
to preset filter catalogues in the RDKit library designed to screen undesirable compounds. 
If an input matches a filter catalog, the filter evaluates to `False`.
'''

catalog_descriptions = {
    'PAINS' : 'Pan assay interference patterns, doi:10.1021/jm901137j',
    'PAINS_A' : 'Pan assay interference patterns subset A, doi:10.1021/jm901137j',
    'PAINS_B' : 'Pan assay interference patterns subset B, doi:10.1021/jm901137j',
    'PAINS_C' : 'Pan assay interference patterns subset C, doi:10.1021/jm901137j',
    'BRENK' : 'filters unwanted functionality due to potential tox reasons or unfavorable pharmacokinetics, doi:10.1002/cmdc.200700139',
    'NIH' : 'annotated compounds with problematic functional groups, doi:10.1039/C4OB02287D',
    'ZINC' : 'Filtering based on drug-likeness and unwanted functional groups, http://blaster.docking.org/filtering/',
}

smarts_filter_description = '''Smarts filters screen inputs against a given smarts string to 
count the number of matches against the smarts pattern. The match count is then 
compared to `min_val` and `max_val`. If `min_val <= value <= max_val` (note this is inclusive), 
the smarts filter evaluates to `True`. Otherwise, the smarts filter evaluates to `False`.

If `min_val=None` or `max_val=None`, that bound is ignored. If both bounds are `None`, the 
smarts filter is ignored

To exclude all inputs that match a smarts string, set `min_val=None` and `max_val=0`
'''

FILTER_DESCRIPTIONS = {
    'property_filters' : {
        'overview' : property_filter_description,
        'example_format' : {"Number of Compounds" : {'min_val' : 120, 'max_val' : 450},
                            "TPSA" : {'min_val' : 20, 'max_val' : None}},
        'decriptions' : property_function_descriptions
    },
    'catalog_filters' : {
        'overview' : catalog_filter_description,
        'example_format' :  {"PAINS" : {'include' : False},
                            "PAINS_A" : {'include' : True}},
        'descriptions' : catalog_descriptions
    },
    'smarts_filters' : {
        'overview' : smarts_filter_description,
        'example_format' : {'C=CC(=O)[!#7;!#8]' : {'min_val' : None, 'max_val' : 0}}
    }
}


BASE_TEMPLATE = {
    'template_name' : None,
    'property_filters' : {
                        "Number of Compounds" :             {'min_val' : None, 'max_val' : None},
                        "TPSA" :                            {'min_val' : None, 'max_val' : None},
                        "LogP" :                            {'min_val' : None, 'max_val' : None},
                        "Molecular Weight" :                {'min_val' : None, 'max_val' : None},
                        "Heavy Atom Count" :                {'min_val' : None, 'max_val' : None},
                        "Atom Count" :                      {'min_val' : None, 'max_val' : None},
                        "Heteroatom Count" :                {'min_val' : None, 'max_val' : None},
                        "Spiro Atom Count" :                {'min_val' : None, 'max_val' : None},
                        "Bridgehead Atom Count" :           {'min_val' : None, 'max_val' : None},
                        "Stereocenter Count" :              {'min_val' : None, 'max_val' : None},
                        "Hydrogen Bond Donors" :            {'min_val' : None, 'max_val' : None},
                        "Hydrogen Bond Acceptors" :         {'min_val' : None, 'max_val' : None},
                        "Formal Charge" :                   {'min_val' : None, 'max_val' : None},
                        "Rotatable Bonds" :                 {'min_val' : None, 'max_val' : None},
                        "Loose Rotatable Bonds" :           {'min_val' : None, 'max_val' : None},
                        "Rotatable Chain Length" :          {'min_val' : None, 'max_val' : None},
                        "Max Ring Size" :                   {'min_val' : None, 'max_val' : None},
                        "Min Ring Size" :                   {'min_val' : None, 'max_val' : None},
                        "Ring Count" :                      {'min_val' : None, 'max_val' : None},
                        "Ring Count (Aromatic)" :           {'min_val' : None, 'max_val' : None},
                        "Ring Count (Saturated)" :          {'min_val' : None, 'max_val' : None},
                        "Ring Count (Aliphatic)" :          {'min_val' : None, 'max_val' : None},
                        "Heterocycle Count" :               {'min_val' : None, 'max_val' : None},
                        "Heterocycle Count (Aromatic)" :    {'min_val' : None, 'max_val' : None},
                        "Heterocycle Count (Saturated)" :   {'min_val' : None, 'max_val' : None},
                        "Heterocycle Count (Aliphatic)" :   {'min_val' : None, 'max_val' : None},
                        "Carbocycles (Aromatic)" :          {'min_val' : None, 'max_val' : None},
                        "Carbocycles (Saturated)" :         {'min_val' : None, 'max_val' : None},
                        "Carbocycles (Aliphatic)" :         {'min_val' : None, 'max_val' : None},
                        "Amide Bond Count" :                {'min_val' : None, 'max_val' : None},
                        "Fraction SP3" :                    {'min_val' : None, 'max_val' : None},
                        "QED" :                             {'min_val' : None, 'max_val' : None},
                        "SA Score" :                        {'min_val' : None, 'max_val' : None},
                        "Molar Refractivity" :              {'min_val' : None, 'max_val' : None},
                        "Radical Count" :                   {'min_val' : None, 'max_val' : None},
                        },
    'catalog_filters' : {
                        "PAINS" : {'include' : False},
                        "PAINS_A" : {'include' : False},
                        "PAINS_B" : {'include' : False},
                        "PAINS_C" : {'include' : False},
                        "BRENK" : {'include' : False},
                        "NIH" : {'include' : False},
                        "ZINC" : {'include' : False},
                        },
    'smarts_filters' : {
                        'example_smarts' : {'min_val' : None, 'max_val' : None},
                        }
}


REACTION_MECHANISM_DICT = {
                        'O-acylation' : True,
                        'Olefination' : True,
                        'Condensation_of_Y-NH2_with_carbonyl_compounds' : True,
                        'Amine_sulphoacylation' : True,
                        'C-C couplings' : True,
                        'Radical_reactions' : True,
                        'N-acylation' : True,
                        'O-alkylation_arylation' : True,
                        'Metal organics C-C bong assembling' : True,
                        'S-alkylation_arylation' : True,
                        'Alkylation_arylation_of_NH-lactam' : True,
                        'Alkylation_arylation_of_NH-heterocycles' : True,
                        'Amine_alkylation_arylation' : True
                    }

SYNTHON_NODE_SCHEMA = {
                        'name' : '', 
                        'node_type' : 'synthon_node', 
                        'n_func' : [],
                        'template_config' : None,
                        'reaction_mechanisms' : REACTION_MECHANISM_DICT,
                        'incoming_node' : None,
                        'next_node' : None
                    }

SYNTHON_LEAF_NODE_SCHEMA = {
                        'name' : '',
                        'node_type' : 'synthon_leaf_node',
                        'n_func' : [],
                        'template_config' : None
                    }

FRAGMENT_NODE_SCHEMA = {
                            'name' : '',
                            'node_type' : 'fragment_node',
                            'template_config' : None,
                            'children' : []
                        }

FRAGMENT_LEAF_NODE_SCHEMA = {
                                'name' : '',
                                'node_type' : 'fragment_leaf_node',
                                'mapping_idxs' : [],
                                'template_config' : None
                            }

bb_assembly_overview = '''Building block assembly attempts to fuse building block compounds 
based on a defined set of allowed reactions. Building block assemblies are made from 
leaf nodes (`synthon_leaf_node`) and reaction nodes (`synthon_node`)

leaf nodes have the following schema:

{
    'name' : '',
    'node_type' : 'synthon_leaf_node',
    'n_func' : [],
    'template_config' : None
}

`n_func` is a list of integers defining how many reactive functional groups a building block 
molecule is allowed to have

`template_config` is an optional template for filtering building blocks

reaction nodes have the following schema:

{
    'name' : '', 
    'node_type' : 'synthon_node', 
    'n_func' : [],
    'template_config' : None,
    'reaction_mechanisms' : {'C-C couplings' : True},
    'incoming_node' : None,
    'next_node' : None
}

`reaction_mechanisms` is a dictionary defining what reaction mechanisms are allowed. See the 
node schema below for the full list.

`incoming_node` and `next_node` are expected to be either leaf nodes or reaction nodes.

Example:

Here is an example schema for fusing two building blocks. 

Note: all `name` attributes must be unique

block1 = {
            'name' : 'building_block_1',
            'node_type' : 'synthon_leaf_node',
            'n_func' : [1],
            'template_config' : template_config_1
        }

block2 = {
            'name' : 'building_block_2',
            'node_type' : 'synthon_leaf_node',
            'n_func' : [1],
            'template_config' : template_config_2
        }

product = {
            'name' : 'product', 
            'node_type' : 'synthon_node', 
            'n_func' : [0],
            'template_config' : template_config_3,
            'reaction_mechanisms' : {
                                        'O-acylation' : True,
                                        'Olefination' : True,
                                        'Condensation_of_Y-NH2_with_carbonyl_compounds' : True,
                                        'Amine_sulphoacylation' : True,
                                        'C-C couplings' : True,
                                        'Radical_reactions' : True,
                                        'N-acylation' : True,
                                        'O-alkylation_arylation' : True,
                                        'Metal organics C-C bong assembling' : True,
                                        'S-alkylation_arylation' : True,
                                        'Alkylation_arylation_of_NH-lactam' : True,
                                        'Alkylation_arylation_of_NH-heterocycles' : True,
                                        'Amine_alkylation_arylation' : True
                                    },
            'incoming_node' : block1,
            'next_node' : block2
        }
'''

BUILDING_BLOCK_ASSEMBLY_DESCRIPTION = {
    'overview' : bb_assembly_overview,
    'leaf_node_schema' : SYNTHON_LEAF_NODE_SCHEMA,
    'node_schema' : SYNTHON_NODE_SCHEMA
}


fragment_assembly_overview = '''Fragment assembly attempts to fuse molecular fragments 
based on dummy atom mapping. Fragment assemblies are made from leaf nodes 
(`fragment_leaf_node`) and fusion nodes (`fragment_node`)

leaf nodes have the following schema:

{
    'name' : '',
    'node_type' : 'fragment_leaf_node',
    'mapping_idxs' : [],
    'template_config' : None
}

`mapping_idxs` is a list of ints defining the expected mapped dummy atoms. For example, 
`mapping_idxs=[1,2]` would require fragments of the form `[*:1]R[*:2]`

Fusion nodes have the following schema:

{
    'name' : '',
    'node_type' : 'fragment_node',
    'template_config' : None,
    'children' : []
}

`children` is a list of `fragment_leaf_node` or `fragment_node` schemas that feed into 
the fusion node.

Example:

Here is an example schema for fusing fragments in the form of `[scaffold]-[linker]-[r_group]` 

Note: all `name` attributes must be unique


r1_schema = {
                'name' : 'R1',
                'node_type' : 'fragment_leaf_node',
                'mapping_idxs' : [1],
                'template_config' : template_config_1
            }

linker_schema = {
                'name' : 'linker',
                'node_type' : 'fragment_leaf_node',
                'mapping_idxs' : [1, 2],
                'template_config' : template_config_2
            }

scaffold_schema = {
                'name' : 'scaffold',
                'node_type' : 'fragment_leaf_node',
                'mapping_idxs' : [2],
                'template_config' : template_config_3
            }

fused_molecule = {
                    'name' : 'full_molecule',
                    'node_type' : 'fragment_node',
                    'template_config' : template_config_4,
                    'children' : [r1_schema, linker_schema, scaffold_schema]
                }
'''


FRAGMENT_ASSEMBLY_DESCRIPTION = {
    'overview' : fragment_assembly_overview,
    'leaf_node_schema' : FRAGMENT_LEAF_NODE_SCHEMA,
    'node_schema' : FRAGMENT_NODE_SCHEMA
}

