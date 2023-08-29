## Assembly Overview

Assembly endpoints attempt to assemble molecules either from building block molecules or molecular fragments.

Assemblies are structured as directed graphs, starting with leaf nodes and ending with an assembled molecule. 
Each node in the graph can be optionally assigned a template to filter molecules moving through the node.

## Building Blocks

Building block molecules are first converted to `synthons` based on a set of SMARTS. Molecules that fail to 
map to synthons are excluded from assembly. `synthons` are routed to leaf nodes of the assembly, either by 
explicit mapping or by matching the `template` and desired number of functional groups at a given leaf node. 
Synthon leaf nodes are sent to reaction nodes. A reaction node has a set of allowed reactions. If two synthons 
match one of the allowed reactions, they are fused based on the reaction schema. The fused molecule is then sent 
on to the next node.

### Building Blocks API

`/building_block/compute_synthons` - computes synthons (if possible) for the inputs

`/building_block/description` - overview of building block assembly schemas

`/building_block/reaction_mechanisms` - dict of allowed reaction mechanisms

`/building_block/2bb_assembly` - assembly for product molecules made from two building blocks

`/building_block/3bb_assembly` - assembly for product molecules made from three building blocks

`/building_block/custom_assembly` - assembly for custom building block schema

Full API docs can be found at `http://{hostname}:{port}/docs`.

### Building Block Examples

#### Two Building Block Assembly

For two building block assembly, we have two inputs (`building_block_1` and `building_block_2`), and one `product`.

An example request is shown below. `building_block_1` and `building_block_2` each contain a set of `inputs` and 
a `template_config`. The `inputs` will be sent to the specific node (block 1 or 2) and screened against the node's 
template. Inputs that pass the templates are sent on to the `product` node. 

The `product` node has a set of 
allowed reactions and a `template_config`. The `product` node screens the outputs from `building_block_1` 
and `building_block_2` for molecule pairs that fit an allowed reaction schema. If a match is found, the inputs 
are reacted into a fused molecule. The fused molecule is then checked against the `product` template.

The request input also contains a set of `unmapped_inputs`. Items in `unmapped_inputs` may be routed to 
either `building_block_1` or `building_block_2`, provided the item passes the template at each node.

```python
import requests
request_inputs = {
 "building_block_1": {
  "inputs": [{"input": "O=CC1CC2C(C1)C2(F)F", "data": {"ID": "EN300-7176480"}}],
  "template_config": bb1_template},
 "building_block_2": {
  "inputs": [{"input": "CC1CCCC(=CN(C)C)C1=O", "data": {"ID": "EN300-25308976"}},
             {"input": "N#Cc1cnn(-c2cccc(Br)c2)c1N", "data": {"ID": "EN300-110252"}}],
  "template_config": bb2_template},
 "product": {
  "reaction_mechanisms": {
                        'O-acylation' : True,
                        'Olefination' : True,
                        'Condensation_of_Y-NH2_with_carbonyl_compounds' : True,
                        'Amine_sulphoacylation' : True,
                        'C-C couplings' : True,
                        'Radical_reactions' : False,
                        'N-acylation' : False,
                        'O-alkylation_arylation' : False,
                        'Metal organics C-C bong assembling' : False,
                        'S-alkylation_arylation' : False,
                        'Alkylation_arylation_of_NH-lactam' : True,
                        'Alkylation_arylation_of_NH-heterocycles' : True,
                        'Amine_alkylation_arylation' : False
                        },
  "template_config": product_template},
 "unmapped_inputs": [{'input':'COc1ccc(C)c(CN)n1', 'data' : {'source' : 'unmaped'}}]
}

response = requests.post('http://localhost:7861/building_block/2bb_assembly',
                      json=request_inputs)
```

#### Three Building Block Assembly

Assembling molecules made of three building blocks works the same way, just with more inputs and 
an intermediate product node.

```python
import requests
request_inputs = {
  "building_block_1": {
    "inputs": [{"input": "CCOC(=O)c1c(N)ccnc1C(F)(F)F", "data": {"blah": "blee"}}],
    "template_config": bb1_template},
  "building_block_2": {
    "inputs": [{"input": "CCOC(=O)c1c(N)ccnc1C(F)(F)F","data": {"blah": "blee"}}],
    "template_config": bb2_template},
  "intermediate_product_1": {
    "reaction_mechanisms": {"N-acylation" : True, ...},
    "template_config": ip1_template},
  "building_block_3": {
    "inputs": [{"input": "COC(=O)C(C)N=C=O", "data": {"blah": "blee"}}],
    "template_config": bb3_template},
  "product": {
    "reaction_mechanisms": {"N-acylation" : True, ...},
    "template_config": product_template},
  "unmapped_inputs" : [{'input':'COc1ccc(C)c(CN)n1', 'data' : {'source' : 'unmaped'}}]}

response = requests.post('http://localhost:7861/building_block/3bb_assembly',
                      json=request_inputs)
```

#### Custom Building Block Assembly

It is also possible to create arbitrary assemblies using custom assembly schemas. Input nodes must follow the 
`synthon_leaf_node_schema` format. Reaction nodes must follow the `synthon_node_schema` format.

For leaf nodes:
- `name` - `str` name of node, used for mapping inputs
- `n_func` - `list[int]`. The number of reactive functional groups allowed at the node
- `template_config` - `dict`. Optional template applied at the node

```python
synthon_leaf_node_schema = {
                        'name' : '',
                        'node_type' : 'synthon_leaf_node',
                        'n_func' : [],
                        'template_config' : None
                    }
```

For reaction nodes:
- `name` - `str` name of node, used for mapping inputs
- `n_func` - `list[int]`. The number of reactive functional groups allowed at the node
- `template_config` - `dict`. Optional template applied at the node
- `reaction_mechanisms` - `dict`. Dict of allowed reaction mechanisms. See `/building_block/reaction_mechanisms` for a full list
- `incoming_node` - `dict`. The input node to the assembly. Must follow `synthon_leaf_node_schema` or `synthon_node_schema` format
- `next_node` - `dict`. The input node to the assembly. Must follow `synthon_leaf_node_schema` or `synthon_node_schema` format

```python
synthon_node_schema = {
                        'name' : '', 
                        'node_type' : 'synthon_node', 
                        'n_func' : [],
                        'template_config' : None,
                        'reaction_mechanisms' : {"N-acylation" : True, ...},
                        'incoming_node' : None,
                        'next_node' : None
                    }
```

For example, the following schema is equivalent to assembling three building blocks

```python
bb1_schema = {
                'name' : 'building_block_1',
                'node_type' : 'synthon_leaf_node',
                'n_func' : [1], # first block must have 1 functional group
                'template_config' : bb1_template
            }

bb2_schema = {
                'name' : 'building_block_2',
                'node_type' : 'synthon_leaf_node',
                'n_func' : [2], # second block must have 2 functional groups to connect [block1]-[block2]-[block3]
                'template_config' : bb3_template
            }

bb3_schema = {
                'name' : 'building_block_1',
                'node_type' : 'synthon_leaf_node',
                'n_func' : [1], # third block must have 1 functional group
                'template_config' : bb3_template
            }

ip1_schema = {
                        'name' : 'intermediate_product_1', 
                        'node_type' : 'synthon_node', 
                        'n_func' : [1], # should be 1 functional group left after fusing block1-block2
                        'template_config' : ip1_template,
                        'reaction_mechanisms' : {"N-acylation" : True, ...},
                        'incoming_node' : bb1_schema,
                        'next_node' : bb2_schema
                    }

product_schema = {
                        'name' : 'product', 
                        'node_type' : 'synthon_node', 
                        'n_func' : [0], # final product [block1]-[block2]-[block3] should have no functional groups left
                        'template_config' : product_template,
                        'reaction_mechanisms' : {"N-acylation" : True, ...},
                        'incoming_node' : ip1_schema,
                        'next_node' : bb3_schema
                    }

request_inputs = {
    'assembly_schema' : product_schema,
    "mapped_inputs": { # note that the keys here match the name attributes of the leaf nodes
        "building_block_1": [...],
        "building_block_2": [...],
        "building_block_3": [...]
    },
    "unmapped_inputs" : [...]
}

result = requests.post('http://localhost:7861/building_block/custom_assembly',
                        json=request_inputs)
```


## Fragment Assembly

Fragments are assembled by fusing dummy atoms - `[*]-R1 + [*]-R2 -> R1-R2`.

Fragments are first routed to the leaf nodes of the assembly, either by explicit mapping or by matching the `template` 
and desired number of dummy atoms at a given leaf node. Items from the leaf nodes are then sent to fusion nodes, which 
assemble fragments based on dummy atoms and mapping numbers. Mapping number configurations are explained in the 
fragment examples section

### Fragment API

`/fragment/description` - overview of fragment assembly schema

`/fragment/custom_assembly` - assembly for custom fragment schema

Full API docs can be found at `http://{hostname}:{port}/docs`.

### Fragment Examples

#### Custom Fragment Assembly

We can create arbitrary fragment assemblies using custom assembly schemas. Input nodes must follow the 
`fragment_leaf_node_schema` format. Fusion nodes must follow the `fragment_node_schema` format.

For leaf nodes:
- `name` - `str` name of node, used for mapping inputs
- `mapping_idxs` - `list[int]`. Mapping index values of dummy atoms
- `template_config` - `dict`. Optional template applied at the node

The `mapping_idxs` term defines how many dummy atoms are expected and how they should be mapped. For example, 
`mapping_idxs=[1,2]` would expect an input with two dummy atoms `[*]-R-[*]`. Internally, this would be converted 
to `[*:1]-R-[*:2]` and `[*:2]-R-[*:1]`. When this fragment encounters another fragment, they are fused on dummy 
atoms with matching mapping. ie `[*:2]-R1-[*:1] + [*:2]-R2-[*:3] -> [*:1]-R1-R2-[*:3]`

```python
fragment_leaf_node_schema = {
                                'name' : '',
                                'node_type' : 'fragment_leaf_node',
                                'mapping_idxs' : [],
                                'template_config' : None
                            }
```

For fusion nodes:
- `name` - `str` name of node, used for mapping inputs
- `template_config` - `dict`. Optional template applied at the node
- `children` - `list[dict]`. List of child nodes. Child nodes must follow `fragment_leaf_node_schema` or `fragment_node_schema` format

```python
fragment_node_schema = {
                            'name' : '',
                            'node_type' : 'fragment_node',
                            'template_config' : None,
                            'children' : []
                        }
```

The following example shows how to create a schema for assembling molecules following the `[scaffold]-[linker]-[r-group]` pattern.

```python
scaffold_schema = {
                        'name' : 'scaffold',
                        'node_type' : 'fragment_leaf_node',
                        'mapping_idxs' : [1],
                        'template_config' : scaffold_template
                    }

linker_schema = {
                        'name' : 'linker',
                        'node_type' : 'fragment_leaf_node',
                        'mapping_idxs' : [1, 2],
                        'template_config' : linker_template
                    }

rgroup_schema = {
                        'name' : 'rgroup',
                        'node_type' : 'fragment_leaf_node',
                        'mapping_idxs' : [2],
                        'template_config' : rgroup_template
                    }

# note the `mapping_idx` values dictate the `[scaffold]-[linker]-[r-group]` assembly pattern

product_schema = {
                    'name' : 'product',
                    'node_type' : 'fragment_node',
                    'template_config' : product_template,
                    'children' : [scaffold_schema, linker_schema, rgroup_schema]
                }

request_inputs = {
    'assembly_schema' : product_schema,
    "mapped_inputs": { # note that the keys here match the name attributes of the leaf nodes
        "scaffold": [...],
        "linker": [...],
        "rgroup": [...]
    },
    "unmapped_inputs" : [...]
}

result = requests.post('http://localhost:7861/fragment/custom_assembly',
                        json=request_inputs)
```


## Stateful Assembly API

If a MongoDB connection is enabled, stateful endpoints supporting CRUD operations become available

`/create_assembly_schema` - create saved assembly schema

`/get_assembly_schema/{assembly_schema_id}` - get assembly schema by id

`/scroll_assembly_schema` - scroll saved assembly schemas

`/update_assembly_schema/{assembly_schema_id}` - update saved assembly schema

`/delete_assembly_schema/{assembly_schema_id}` - delete saved assembly schema

`/building_block/2bb_assembly_stateful` - 2 building block assembly using saved templates

`/building_block/3bb_assembly_stateful` - 3 building block assembly using saved templates

`/building_block/custom_assembly_stateful` - custom building block assembly using saved assembly schema

`/fragment/custom_assembly_stateful` - custom fragment assembly using saved assembly schema

Full API docs can be found at `http://{hostname}:{port}/docs`.
