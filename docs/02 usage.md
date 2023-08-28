# Usage

Overview on using the server

## API docs

API docs can be found at `http://{hostname}:{port}/docs`. For the default setup, this should be 
`http://localhost:7861/docs`

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


## Python Query

Example of how to send queries to the server with the python `requests` library.

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

