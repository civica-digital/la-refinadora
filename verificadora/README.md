# Verificadora

### License

This code is open source under the PENDING license. See the LICENSE.md file for
full details.

### Verificadora

Datasets can be validated using the different plugins. to run the code:

`python3 verificadora.py --dataset text.csv --resources resources.json`

Where `test.csv` is the file to be checked and `resources.json` is a file with the form:

	"resources": [
		"plugin1.py",
		"plugin2.py
	]

which will return a json of the form:

	{  
	   "detail":{  
	      "general-file-check.py":{  
	         "validators":{  
	            "separator":{  
	               "status":"Pass",
	               "reason":"Coma"
	            },
	            "utf-8":{  
	               "status":"Pass",
	               "reason":"Se detectó la codificación UTF-8"
	            }
	         },
	         "status":"Pass"
	      }
	   },
	   "status":"Pass"
	}


#### Plugin (Resources)

The directory Plugins contains the specific validations the file will be checked to.

Each verification requires to have two calls:

- Call without any files: In which case the plugin will answer with a json with the requirements of the verificator with the form:

		{  
		   "status":"general-file-check",
		   "response":{  
		      "raw":"true",
		      "unit":"row",
		      "number":"5",
		      "sampling":"random"
		   }
		}

- Call with `--dataset file.csv`, which in turn will return a status response of the form:

		{  
		   "status":"Pass",
		   "validators":{  
		      "separator":{  
		         "status":"Pass",
		         "reason":"Coma"
		      },
		      "utf-8":{  
		         "status":"Pass",
		         "reason":"UTF-8 encoding detected"
		      }
		   }
		}


#### Recommended Plugin Pseudocode Structure

It is recommended that the plugin structure will be as follows:

A method to do the actual subverifications done by the plugin.
A method to each subverification
A method that calls all subverifications
A method that constructs all subverifications
A method that returns the response json, according to the input parameters.


#### Configuration

Pending to changes by Mike.
