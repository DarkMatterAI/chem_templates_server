## Templates Overview

Templates have three categories of filter:
- Property Filters
- Catalog Filters 
- Smarts Filters

Property filters verify if the value of a certain property is within a specified range.

Catalog filters reject inputs that match a specific catalog (ie PAINS)

Smarts filters verify the number of matches to a specifc smarts string is within a specified range.

A complete list of properties and catalogs supported can be found at the `/filter_descriptions` endpoint.

## Template Format

Templates are specified as JSON objects:

```
{
  "template_name": null,
  "property_filters": {
    "Molecular Weight": {
      "min_val": null,
      "max_val": null
    }
  },
  "catalog_filters": {
    "PAINS": {
      "include": false
    },
  },
  "smarts_filters": {
    "example_smarts": {
      "min_val": null,
      "max_val": null
    }
  }
}
```

For `property_filters` and `smarts_filters`, at least one of `min_val, max_val` must be specified as an integer.

A `catalog_filters` can be included by setting `include=True`

`smarts_filters` must correspond to a syntactically valid SMARTS string.

A full JSON containing all available properties can be found at `/base_template` endpoint.

To validate a template and remove any unspecified filters, use the `/strip_template` endpoint.


## Template API

`/filter_descriptions` - descriptions of available filters

`/base_template` - template config showing all available filters

`/strip_template` - strips a template config of unused filters

`/eval_template_functional` - filters a set of `inputs` against a `template_config`

Full API docs can be found at `http://{hostname}:{port}/docs`.

Example of using the `eval_template_functional` with the python `requests` library 

```python
import requests
from concurrent.futures import ThreadPoolExecutor
from functools import partial

def send_filter_request(inputs, template_config, return_data=True):
    
    filter_results = requests.post('http://localhost:7861/eval_template_functional',
                               json={'inputs' : inputs, 'template_config' : template_config},
                               params={'return_data' : return_data})
    
    filter_results = filter_results.json()
    
    return filter_results

def send_filter_request_parallel(inputs, template_config, batch_size, n_concurrent, return_data=True):
    
    input_batches = [inputs[i:i+batch_size] for i in range(0, len(inputs), batch_size)]
    
    with ThreadPoolExecutor(n_concurrent) as p:
        func = partial(send_filter_request, template_config=template_config, return_data=return_data)
        results = p.map(func, input_batches)
        
    results = [item for sublist in results for item in sublist]
        
    return results

template_config = {
 "template_name": "my_template",
 "property_filters": {
  "LogP": {
   "min_val": None,
   "max_val": 5
  },
  "Molecular Weight": {
   "min_val": None,
   "max_val": 500
  },
  "Hydrogen Bond Donors": {
   "min_val": None,
   "max_val": 5
  },
  "Hydrogen Bond Acceptors": {
   "min_val": None,
   "max_val": 10
  }
 },
 "catalog_filters": {
  "PAINS": {
   "include": True
  },
 },
 "smarts_filters": {
   "[F,Cl,Br]": {
   "min_val": 1.0,
   "max_val": 3.0
  }
 }
}

inputs = ...
batch_size = 256
n_concurrent = 32

results = send_filter_request_parallel(inputs, template_config, batch_size, n_concurrent)
```

For best results, set `n_concurrent` to the number of workers the server has


## Template Stateful API

If a MongoDB connection is enabled, stateful endpoints supporting CRUD operations become available

`/create_template` - create template

`/get_template/{template_id}` - get template by ID

`/scroll_templates` - scroll saved templates

`/update_template/{template_id}` - update saved template

`/delete_template/{template_id}` - delete saved template

`/eval_template_stateful/{template_id}` - eval `inputs` against a saved template

Full API docs can be found at `http://{hostname}:{port}/docs`.

```python
import requests
from concurrent.futures import ThreadPoolExecutor
from functools import partial

template_config = {
 "template_name": "my_template",
 "property_filters": {
  "LogP": {
   "min_val": None,
   "max_val": 5
  },
  "Molecular Weight": {
   "min_val": None,
   "max_val": 500
  },
  "Hydrogen Bond Donors": {
   "min_val": None,
   "max_val": 5
  },
  "Hydrogen Bond Acceptors": {
   "min_val": None,
   "max_val": 10
  }
 },
 "catalog_filters": {
  "PAINS": {
   "include": True
  },
 },
 "smarts_filters": {
   "[F,Cl,Br]": {
   "min_val": 1.0,
   "max_val": 3.0
  }
 }
}

create_response = requests.post('http://localhost:7861/create_template', json=template_config)
template_id = response.json()['_id']
inputs = ...

eval_response = requests.post(f'http://localhost:7861/eval_template_stateful/{template_id}',
                                json={'inputs':inputs}, params={'return_data':True})
```