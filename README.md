# Vector-space Retrieval
Simple implementation of an Information Retrieval (IR) System based upon the vector space model.

> This project is structured as seen in [PyImports](https://github.com/cod3monk3y/PyImports), by cod3monk3y.

## Quick Start

Clone repo and run `$ python -m vsr` from the repository root. Outputs are under modules/*module_name*/output.

## Project Structure

 This is a python project. It is split among 5 modules: `inverted_index`, `indexer`, `query_processor`, `search` and `metrics`

 XML files representing articles and journal entries on **Cystic Fibrosis** can be found under `vsr/data`.

- **Module 'inverted_index'**

 This module builds an *inverted index* based upon the XML files containing article data.

 These XML files are parsed, tokenized and used to build an inverted index. The inverted index is then used to build a **document-term matrix**, linking every document to the list of tokens found in that document.

 The output from this module is saved at `vsr/modules/inverted_index/output/output.csv`

- **Module 'indexer'**

 This module uses the inverted index built in the previous module and creates a *document-term matrix*.

 It is saved in `vsr/modules/indexer/output/output.csv`

 Additionaly, a file in `vsr/modules/indexer/modelo.txt` is included, with specific instructions (in Portuguese) on how to read file `output.csv`.


- **Module 'query_processor**

 Akin to the previous module, this module creates another *document-term matrix*, but uses queries rather than documents. Additionaly, the expected results are also formated in CSV format to enable future comparison.

 Output files:
 - `vsr/modules/query_processor/output/expected_query_results.csv`
 - `vsr/modules/query_processor/output/expected_query_results_only_doc_ids.csv` (same info, lighter format) 
 - `vsr/modules/query_processor/output/queries.csv`.

- **Module 'search'**

 This module uses as input the files generated in the two previous modules, as well as an XML file that contains a list of queries with *expected results*. This module runs the quries against the documents and saves the output in these two files (they have the same data, but the second file is easier to read):
 - `vsr/modules/search/output/actual_results.csv`
 - `vsr/modules/search/output/actual_results_only_doc_ids.csv` (same info, lighter format)

- **Module 'metrics'**

 This module is responsible for comparing results (actual results vs expected results) and extract all sorts of metrics from them, including precision, recall, f1 score, mean average precision, discounted cumulative gain, precision at 10 results (precision@10) and 11-point precision vs recall graph.

 All results are located under `vsr/modules/metrics/output`, including a png image.

## Project dependencies

This project was built using Python version 2.7, on Ubuntu 14.04. The following python dependencies are needed to run it:

 - scipy
 - numpy
 - nltk
 - toolz
 - matplotlib

> Look at [Getting Started with Python NLTk on Ubuntu](http://queirozf.com/entries/getting-started-with-python-nltk-on-ubuntu) for more info on how to install these if you're using the Ubuntu OS.

## Running the scripts

### Run all scripts together

Just run `$ python -m vsr` from the repository root - this is the recommended approach.

### Run each script separately

> The scripts should be run in this order!

Since the project is structured as *python modules*, please use the `-m` modifier when running them. 
In other words:

 - `$ python -m vsr.modules.inverted_index` - for module **inverted_index**
 - `$ python -m vsr.modules.indexer` - for module **indexer**
 - `$ python -m vsr.modules.query_processor` - for module **query_processor**
 - `$ python -m vsr.modules.search` - for module **search**
 - `$ python -m vsr.modules.metrics` - for module **metrics**

## Other

- `.out` files - These are [pickle](https://docs.python.org/2/library/pickle.html) dumps of some key data structures used in this project. useful for debugging purposes.
- `vsr/common` - Helper files used by the whole project
- `vsr/data` - Raw data used in this project.
- `logs/` - Log files. Useful for debugging purposes.
- `.cfg` files - Config files. Each module has one config file.
  - Please note that, when running each module individually the same options (section [Params]) should be set across the modules, in order to prevent inconsistencies.

### Sample graph

- Precision x Recall graph, when [Porter's Stemming Algorithm](http://tartarus.org/martin/PorterStemmer/) is used:
 
 ![precision_recall_graph_using_stemmer](http://i.imgur.com/34cA5fp.png "Precision x Recall Graph")

