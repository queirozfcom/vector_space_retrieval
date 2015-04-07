# Vector-space Retrieval
Simple implementation of an Information Retrieval (IR) System based upon the vector space model.

> This project is structured as seen in [PyImports](https://github.com/cod3monk3y/PyImports), by cod3monk3y.

## Project Structure

This is a python project. It is split among 4 modules: `inverted_index`, `indexer`, `query_processor` and `search`.

XML files representing articles and journal entries on **Cystic Fibrosis** can be found under `vsr/data`.

- **INVERTED_INDEX**

This module builds an *inverted index* based upon the XML files containing article data.

These XML files are parsed, tokenized and used to build an inverted index. The inverted index is then used to build a **document-term matrix**, linking every document to the list of tokens found in that document.

The output from this module is saved at `vsr/inverted_index/output.csv`

- **INDEXER**

This module uses the inverted index built in the previous module and creates a *document-term matrix*.

It is saved in `vsr/indexer/output.csv`


- **QUERY_PROCESSOR**

Akin to the previous module, this module creates another *document-term matrix*, but uses queries rather than documents. Additionaly, the expected results are also formated in CSV format to enable future comparison.

Output files: `vsr/query_processor/expected_query_results.csv` and `vsr/query_processor/queries.csv`.

- **SEARCH**

This module uses as input the files generated in the two previous modules, as well as an XML file that contains a list of queries with *expected results*. This module runs the quries against the documents and saves the output in these two files (they have the same data, but the second file is easier to read):
 - `vsr/search/actual_results.csv`
 - `vsr/search/actual_results_only_doc_ids.csv`


## Project dependencies

This project was built using Python version 2.7, on Ubuntu 14.04. The following python dependencies are needed to run it:

 - scipy
 - numpy
 - nltk
 - toolz

> Look at [Getting Started with Python NLTk on Ubuntu](http://queirozf.com/entries/getting-started-with-python-nltk-on-ubuntu) for more info on how to install these.

## Running the scripts

> The scripts should be run in this order!

Since the project is structured as *python modules*, please use the `-m` modifier when running them. 
In other words:

 - `vector_space_retrieval$ python -m vsr.inverted_index.main` - for module **inverted_index**
 - `vector_space_retrieval$ python -m vsr.index.main` - for module **indexer**
 - `vector_space_retrieval$ python -m vsr.query_processor.main` - for module **query_processor**
 - `vector_space_retrieval$ python -m vsr.search.main` - for module **search**

## Other

- `.out` files - These are [pickle](https://docs.python.org/2/library/pickle.html) dumps of some key data structures used in this project. useful for debugging purposes.
- `vsr/common` - Helper files used by the whole project
- `vsr/data` - Raw data used in this project.
- `logs/` - Log files. Useful for debugging purposes.
- `.cfg` files - Config files. Each module has one config file.
  - Please note that the same options (section [Params]) should be set across the modules, in order to prevent inconsistencies.


