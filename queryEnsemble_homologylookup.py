#!/Users/thor/Library/Enthought/Canopy_64bit/User/bin/python
# NOTE: above is for laptop only, typical directive is #!/usr/bin/python
import requests, sys
import re
import time
import random
import argparse

def listOfGeneNames(l):
    filedata = []
    fileDict = dict()
    with open(l) as inputdatafile:
        for dline in inputdatafile:
            filedata.append(dline.rstrip())
    for i in filedata:
        isplit = i.split(',')
        k = isplit[0]
        v = isplit[1]
        fileDict[k] = v
    return fileDict
def lookupEnsembleID(ugeneID, ensQuery):
    uniqueID = ugeneID
    n = random.random() + 0.5
    time.sleep(n)
    server = "https://rest.ensembl.org/"
    lookupIDstring = "xrefs/symbol/"
    speciesString = "armadillo/"
    idName = ensQuery
    ext1 = "?content-type=application/json"
    q = server+lookupIDstring+speciesString+idName+ext1
    r = requests.get(q, headers={ "Content-Type" : "application/json"})
    if not r.ok:
        print q
        print ensQuery+"\t"+"MATCH ERROR"
        return (uniqueID, (ensQuery, "MATCH ERROR"))
        # r.raise_for_status()
        # sys.exit()
    else:
        decoded = r.json()
        if not decoded:
            return (uniqueID, (ensQuery, "NO MATCH"))
        else:
            res = decoded[0]
            ensembleName = res["id"]
            return (uniqueID, (ensQuery, ensembleName))

def checkGeneWithEnsemble(g_id, g):
    geneResultCheck = lookupEnsembleID(g_id, g)
    if geneResultCheck[1][1] == "MATCH ERROR":
        return 0
    elif geneResultCheck[1][1] == "NO MATCH":
        return 0
    else:
        if geneResultCheck[1][1] == g:
            return 1
        else:
            return 0

def lookupEnsembleHomology_NoSequence(ugeneID, ensQuery):
    uniqueID = ugeneID
    noHomologyString = "NOMATCH_HOMOLOGY"
    n = random.random() + 0.5
    time.sleep(n)
    server = "https://rest.ensembl.org/"
    lookupIDstring = "homology/symbol/"
    speciesString = "armadillo/"
    idName = ensQuery
    # ?content-type=application/json;format=condensed;target_species=human;type=orthologues
    ext1 = "?content-type=application/json;format=condensed;"
    targetSpecies = "target_species=human;"
    ext2 = "type=orthologues"
    q = server+lookupIDstring+speciesString+idName+ext1+targetSpecies+ext2
    r = requests.get(q, headers={ "Content-Type" : "application/json"})
    if not r.ok:
        print ensQuery+"\t"+"MATCH ERROR OR NO MATCH"
        return (uniqueID, (ensQuery, "MATCH_ERROR"))
        # r.raise_for_status()
        # sys.exit()
    else:
        decoded = r.json()
        if not decoded:
            return (uniqueID, (ensQuery, "NO MATCH"))
        elif "error" in decoded:
            return (uniqueID, (ensQuery, "NO MATCH")) # alternative output to above
        else:
            res = ""
            try: 
                res = decoded["data"][0]["homologies"][0]["id"]
            except IndexError:
                res = noHomologyString
            # optional: run error check here, error check
            # re-queries with ID to verify gene ID matches Ensemble ID
            # and throws error if it does not
            # comment out to skip
            ensQuery = decoded["data"][0]["id"]
            errorCheck = checkGeneWithEnsemble(uniqueID, decoded["data"][0]["id"])
            if not errorCheck:
                print "####"
                print "Warning! Gene name did not match ensemble check"
                print decoded
                print decoded["data"][0]["id"]
                print res
                print "####"
            return (uniqueID, (ensQuery, res))
def main():
    parser = argparse.ArgumentParser(description='Parse Ensemble Data')
    parser.add_argument('-i', '--input', dest='input', help='Input gene list to query Ensemble REST database')
    args = parser.parse_args()
    mFileIn = args.input
    aDict = listOfGeneNames(mFileIn)
    aResult = []
    for k,v in aDict.items():
        aResultItem = lookupEnsembleHomology_NoSequence(k,v)
        aResult.append(aResultItem)
    print "###" + "RESULTS"
    for i in aResult:
        s = i[0] + "," + i[1][0] + "," + i[1][1]
        print s
if __name__ == "__main__":
        main()
