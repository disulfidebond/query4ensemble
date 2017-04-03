# query4ensemble

## Overview
This python script has two main functionalities.  It will either accept as input a list of genes with NCBI identifiers, and provide a matching list of ENSEMBL genes, or it will accept as input a list of genes with NCBI identifiers and provide a matching list of homologous genes with matching ENSEMBL identifiers.


## Usage
*python queryEnsemble_homologylookup.py [-i input] [OPTIONS]*
The script will output to STDOUT, but can be redirected as appropriate.  The output is formatted as three columns, in the format:

geneName[#],geneName|ENSEMBL,ENSEMBL|'NO MATCH'|NOMATCH_HOMOLOGY

where 
  geneName[#] is the NCBI gene name, and if applicable (see detailed usage), it is flagged to indicate multiple records are associated with it.
  geneName|ENSEMBL is the NCBI gene name, or an associated ENSEMBL identifier, see detailed usage for more information
  ENSEMBL identifier|'NO MATCH'|NOMATCH_HOMOLOGY is the ENSEMBL homologous gene name, or an identifier indicating why no match occurred, see detailed usage for more information
Usage Options are:
-i **input: the name of the input file.  Must be formatted as two comma-separated columns of gene names.  The list cannot have duplicate gene names, however if the *output* has more than one identifier associated with an NCBI gene name, it will be flagged with a "#".**

-g **genome: the genome of the organism that is being studied, either with homology or with queries to ENSEMBL.  Must be a recognized ENSEMBL name or identifier, such as "armadillo", or "Dasypus_novemcinctus"**

-H **homology: the target homologous organism with the specified genome using ENSEMBL queries.  Must be a recognized ENSEMBL name or identifier, such as "human" or "homo_sapiens"**

-v **verbose: True or False. Default is False.  If specified, must be set to true.  True will output errors and detailed information on what matched; the final output will be separated by a line of "####RESULTS"**

-t **type: required for Homology, ignored otherwise.  Indicates how to search for homologous matches.  Must be an integer of 1,2, or 3.**

  **1 -> strict will reject any searches that do not strictly match the homology term**
  
  **2 -> lenient will attempt to match a homology term, then attempt to match a term using a cross-ref lookup but add a warning tag**
  
  **3 -> lax will attempt to match a homology term, then automatically match the term using a cross reference lookup**
## Detailed Usage
The option to convert a list of NCBI gene names, such as from Differential Gene Expression, to ENSEMBL identifiers, can be used by simply not using the -H option.  If more than one ENSEMBL identifier is linked to an NCBI gene, the NCBI gene will be flagged with a hash "#".

To run a homology search, the options for input, genome name, -H and -t must be provided.  As the scripr progresses, it will attempt to use the genome name and the -H homology name with the REST ENSEMBL API.  Note that if either name is not recognized, the script will likely fail, and possibly crash.
If a homologous match is found, it will be returned as an entry in the third column of output.  The first two are the NCBI gene name, either an NCBI gene name or an ENSEMBL gene name, and then either an ENSEMBL gene name or a tag indicating success or failure.
If it fails to find a homologous match, then if type 1 was provided, it ends the query for that gene and continues.  If either type "-t" option 2 or 3 are provided, it then attempts to find a matching gene by looking up the ENSEMBL gene identifier first.  If this or the previous option succeeds, then the ENSEMBL gene ID is returned.  If this fails, and option 3 is not provided, it ends the query for that gene and continues.  If option 3 is provided, it then simply attempts to match the gene to the homologus organism, without specific respect to homology.  If this is successful, it then returns the matched gene with a hash "#" flag appended to the end of the ENSEMBL gene ID, which can be ignored, checked, or filtered later as appropriate.
  
