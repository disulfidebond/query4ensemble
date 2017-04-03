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
        fileGenes = []
        i = i.replace('"', '')
        isplit = i.split(',')
        isplitItems = []
        if len(isplit) != 2:
            k = isplit[0]
            splitDivider = len(isplit) / 2
            for x in xrange(0, splitDivider):
                isplitItems.append(isplit[x])
            k += "#"
            for val in isplitItems:
                fileGenes.append(val)
            fileDict[k] = fileGenes
        else:
            iSplitList = []
            iSplitList.append(isplit[1])
            k = isplit[0]
            v = iSplitList
            fileDict[k] = v
    return fileDict

def lookupEnsembleHomologyErrorCheck(ugeneID, ensQuery, genomeName, queryName):
    n = random.random() + 0.5
    time.sleep(n)
    server = "https://rest.ensembl.org/"
    lookupIDstring = "homology/symbol/"
    speciesString = genomeName + "/"
    uniqueID = ugeneID
    idName = ensQuery
    ext1 = "?content-type=application/json;format=condensed;"
    targetSpecies = "target_species=" + queryName + ";"
    ext2 = "type=orthologues"
    q = server+lookupIDstring+speciesString+idName+ext1+targetSpecies+ext2
    # print(q)
    r = requests.get(q, headers={ "Content-Type" : "application/json"})
    if not r.ok:
        return (uniqueID, (ensQuery, 0))
    else:
        decoded = r.json()
        if not decoded:
            return (uniqueID, (ensQuery, 0))
        elif "error" in decoded:
            return (uniqueID, (ensQuery, 0)) # alternative output to above
        else:
            res = ""
            try:
                res = decoded["data"][0]["homologies"][0]["id"]
            except IndexError:
                return (uniqueID, (ensQuery, 0))
            if not res:
                return (uniqueID, (ensQuery, 0))
            else:
                return (uniqueID, (ensQuery, res))

def lookupEnsembleID(ugeneID, ensQuery, genomeName, verboseBool):
    if verboseBool:
        print("Checking")
        print(ensQuery)
    uniqueID = ugeneID
    n = random.random() + 0.5
    time.sleep(n)
    server = "https://rest.ensembl.org/"
    lookupIDstring = "xrefs/symbol/"
    # speciesString = "armadillo/"
    speciesString = genomeName + "/"
    idName = ensQuery
    ext1 = "?content-type=application/json"
    q = server+lookupIDstring+speciesString+idName+ext1
    r = requests.get(q, headers={ "Content-Type" : "application/json"})
    if not r.ok:
        if verboseBool:
            print(q)
            print(ensQuery+"\t"+"MATCH ERROR")
        else:
            print("Error")
        return (uniqueID, (ensQuery, 0))
        # rList.append([(uniqueID, (ensQuery, "MATCH ERROR"))])
        # r.raise_for_status()
        # sys.exit()
    else:
        decoded = r.json()
        if not decoded:
            if verboseBool:
                print("couldn't find match")
            # rList.append([(uniqueID, (ensQuery, "NO MATCH"))])
            return (uniqueID, (ensQuery, 0))
        else:
            res = decoded[0]
            ensembleName = res["id"]
            if verboseBool:
                print("Found match for")
                print(res)
            # rList.append([(uniqueID, (ensQuery, ensembleName))])
            return (uniqueID, (ensQuery, ensembleName)) # change to: if return True Below, check xref Ensemble, if return true, return gene, else return no match query
    # return rList


def lookupEnsembleHomology_NoSequence(ugeneID, ensQuery, queryName, genomeName, verboseBool, searchType):
    uniqueID = ugeneID
    returnItemsList = []
    for itm in ensQuery:
        print("looking up")
        print(itm)
        noHomologyString = "NOMATCH_HOMOLOGY"
        n = random.random() + 0.5
        time.sleep(n)
        server = "https://rest.ensembl.org/"
        lookupIDstring = "homology/symbol/"
        speciesString = genomeName + "/"

        idName = itm
        # ?content-type=application/json;format=condensed;target_species=human;type=orthologues
        ext1 = "?content-type=application/json;format=condensed;"
        targetSpecies = "target_species=" + queryName + ";"
        ext2 = "type=orthologues"
        q = server+lookupIDstring+speciesString+idName+ext1+targetSpecies+ext2
        r = requests.get(q, headers={ "Content-Type" : "application/json"})
        if not r.ok:
            if verboseBool:
                print("NO Homology Match!")
                print itm+"\t"+"MATCH ERROR OR NO MATCH"
            # return (uniqueID, (itm, "MATCH_ERROR"))
            if searchType > 1:
                print("Trying new search")
                l_itm = lookupEnsembleID(ugeneID, itm, queryName, verboseBool)
                print(l_itm)
                if not l_itm[1][1]:
                    l_itm_recheck = lookupEnsembleID(ugeneID, itm, genomeName, verboseBool)
                    l_itm_recheck_Final = lookupEnsembleHomologyErrorCheck(ugeneID, l_itm_recheck[1][0], genomeName, queryName)
                    if not l_itm_recheck_Final[1][1]:
                        new_l_itm = "NO MATCH"
                    else:
                        new_l_itm = l_itm[1][0] + "#"
                else:
                    new_l_itm = l_itm[1][1] + "#"
                l_itm = (l_itm[0], (l_itm[1][0], new_l_itm))
                returnItemsList.append(l_itm)
                continue
            else:
                returnItemsList.append((uniqueID, (itm, "MATCH_ERROR")))
                continue
        else:
            decoded = r.json()
            if not decoded:
                # return (uniqueID, (itm, "NO MATCH"))
                returnItemsList.append((uniqueID, (itm, "NO MATCH")))
                if verboseBool:
                    print("No Match for")
                    print(itm)
                continue
            elif "error" in decoded:
                # return (uniqueID, (itm, "NO MATCH")) # alternative output to above
                returnItemsList.append((uniqueID, (itm, "NO MATCH")))
                if verboseBool:
                    print("No Match for")
                    print(itm)
                continue
            else:
                res = ""
                try:
                    res = decoded["data"][0]["homologies"][0]["id"]
                except IndexError:
                    res = noHomologyString
                returnItemsList.append((uniqueID, (itm, res)))
                # optional: run error check here, error check
                # re-queries with ID to verify gene ID matches Ensemble ID
                # and throws error if it does not
                # comment out to skip
                new_itm = decoded["data"][0]["id"]
                if res == 'NOMATCH_HOMOLOGY':
                    print("retrying first option")
                    firstRetry = lookupEnsembleID(uniqueID, new_itm, queryName, verboseBool)
                    if firstRetry[1][1] == "MATCH ERROR" or "NO MATCH":
                        secondRetry = lookupEnsembleID(uniqueID, new_itm, genomeName, verboseBool)
                        print("retrying second option")
                        if secondRetry[1][1] == "MATCH ERROR" or "NO MATCH":
                            returnItemsList.append((uniqueID, (new_itm, "NO MATCH")))
                        else:
                            print("secondRetry")
                            print(secondRetry)
                            sys.exit()
                    else:
                        print(firstRetry)
                        sys.exit()
                else:
                    # return (uniqueID, (itm, res))
                    returnItemsList.append((uniqueID, (itm, res)))
    return returnItemsList
def main():
    parser = argparse.ArgumentParser(description='Parse Ensemble Data')
    parser.add_argument('-i', '--input', dest='input', help='Input gene list to query Ensemble REST database')
    parser.add_argument('-g', '--genome', dest='genome', help='name for target genome')
    # parser.add_argument('-q', '--query', dest='query', help='name for query against genome, or what you are searching against.   Ignored if homology is not selected.')
    parser.add_argument('-H', '--homology', dest='homology', help='homology lookup that target genome will be queried against')
    parser.add_argument('-v', '--verbose', dest='verbose', help='verbose True or False, will provide all errors as a header, proceeded by the line \"###Results\"')
    parser.add_argument('-t', '--type', dest='type', help='Only requried for homology, ignored otherwise\nArgument is an int: 3 types of searches,1,2,3\n1 -> strict will reject any searches that do not strictly match the homology term\n2 -> lenient will attempt to match a homology term, then attempt to match a term using a cross-ref lookup but add a warning tag \"#\"\n 3-> lax will attempt to match a homology term, then automatically match the term using a cross reference lookup\n\n')
    args = parser.parse_args()
    verboseBool = False
    queryName = ""
    genomeName = ""
#    if args.query:
#        queryName = args.query
    if args.verbose:
        verboseBool = True
    homologyLookup = False
    if args.homology:
        queryName = args.homology
        homologyLookup = True
    criteriaType = None
    if homologyLookup:
        try:
            criteriaType = int(args.type)
        except ValueError:
            print("It looks like you may have made a typo for the type of homology lookup")
            print("you entered")
            print(args.type)
            print("but only an argument of 1 2 or 3 can be used.  Please re-enter!")
    genomeName = args.genome
#    queryName = args.query
    if not genomeName:
        print("Sorry, a genome name must be provided! Please provide one and rerun")
    mFileIn = args.input
    if not mFileIn:
        print("Sorry, an input file must be provided!  Please provide one and rerun")
    aDict = listOfGeneNames(mFileIn)
    aResult = []
    if homologyLookup:
        print("Running homologylookup")
        for k,v in aDict.items():
            aResultItem = lookupEnsembleHomology_NoSequence(k,v, queryName, genomeName, verboseBool, criteriaType)
            aResult.append(aResultItem)
    else:
        for k,v in aDict.items():
            vList = v
            for vItem in vList:
                aResultItem = lookupEnsembleID(k, vItem, genomeName, verboseBool)
                aResult.append(aResultItem)
    if args.verbose:
        print("###Results")
        print(aResult)
        print('\n')
    if homologyLookup:
        print("true")
        for itm in aResult: # reformat Output, or set flag for lookupEnsembleID
            for l_of_itms in itm:
                # l_of_itms = itm
                s = str(l_of_itms[0]) + "," + str(l_of_itms[1][0]) + "," + str(l_of_itms[1][1])
                print s
    else:
        for itm in aResult: # reformat Output, or set flag for lookupEnsembleID
            l_of_itms = itm
            s = str(l_of_itms[0]) + "," + str(l_of_itms[1][0]) + "," + str(l_of_itms[1][1])
            print s
if __name__ == "__main__":
        main()
