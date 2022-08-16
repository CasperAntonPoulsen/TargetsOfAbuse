import requests
import json
import pandas as pd
import re
import spacy
import time
import numpy as np

def findTokenOffsets(sentence):
    # This function only works with grammatically correct english
    # where there are spaces after commas, colons and semi-colons.
    sentenceSplit = sentence.split(" ")
    offsets = [0]
    for idx, char in enumerate(sentence):
        if char == " ":
            offsets.append(idx+1)

    return {offsets[i]:sentenceSplit[i] for i in range(len(sentenceSplit))}

def createTarget(dbEntry):

    targetString = ""

    tokenOffsets = findTokenOffsets(dbEntry["@text"])


    for offset in list(tokenOffsets.keys()):
        for word in dbEntry["Resources"]:

            # Is the current offset the same as the current entry
            if int(word["@offset"]) == offset:
                if targetString == "":
                    targetString = targetString + word["@surfaceForm"]
                else:
                    targetString = targetString + " " + word["@surfaceForm"]

            # Has it already been marked?
            elif targetString.split(" ")[-1] != "*":
                if targetString != "":
                    targetString = targetString + " *"


    return targetString

def createSource(nlp, dbEntry):
    doc = nlp(dbEntry["@text"])

    sourceString = ""

    for token in doc:
        sourceString = sourceString + token.text + " " + token.pos_ + " "

    return sourceString[:-1]


if __name__ == "__main__":

    print("loading file")

    with open("db_spotlight_05.json", "r", encoding="utf-8") as file:
        db_spotlight_05 = [line.strip() for line in file.readlines()]

    print("file loaded")
    print("starting data annotation")

    nlp = spacy.load("da_core_news_sm")
    annotatedData = []
    counter = 0
    errorCounter = 0
    nEntries = len(db_spotlight_05)

    for entry in db_spotlight_05:
        counter += 1
        percentageDone = np.round((counter/nEntries)*100, 2)
        print(str(counter) + " / " + str(nEntries) + "   " + str(percentageDone) + "%", end="\r")

        try:
            dbEntry = json.loads(entry)
        
        # Failed dbpedia spotlight request
        except json.JSONDecodeError:
            continue
        
        
        
        try:
            annotatedData.append({
                                    "source":createSource(nlp, dbEntry),
                                    "target":createTarget(dbEntry)
                                })
        # No targets
        except KeyError:

            continue
    print("finished data annotation")
    dfAnnotatedData = pd.DataFrame(annotatedData)

    cleanedTargets = []

    for target in dfAnnotatedData["target"]:
        
        if target.split(" ")[-1] == "*":
            cleanedTargets.append(target[:-2])
        else:
            cleanedTargets.append(target)

    dfAnnotatedData["cleaned_target"]= cleanedTargets


    validationSplit = int(len(dfAnnotatedData)*0.8)


    dfAnnotatedDataShuffled = dfAnnotatedData.sample(frac=1)

    train_set = dfAnnotatedDataShuffled.iloc[:validationSplit]
    validation_set = dfAnnotatedDataShuffled.iloc[validationSplit:]
    print("writing training set")
    with open("src_train_dbpedia_spotlight05_da.txt", "w+", encoding="utf-8") as srcfile:
        with open("tgt_train_dbpedia_spotlight05_da.txt", "w+", encoding="utf-8") as tgtfile:

            for idx, row in train_set.iterrows():
                srcfile.write(row[0]+ "\n")
                tgtfile.write(row[2]+ "\n")

    print("writing validation set")
    with open("src_valid_dbpedia_spotlight05_da.txt", "w+", encoding="utf-8") as srcfile:
        with open("tgt_valid_dbpedia_spotlight05_da.txt", "w+", encoding="utf-8") as tgtfile:

            for idx, row in validation_set.iterrows():
                srcfile.write(row[0]+ "\n")
                tgtfile.write(row[2]+ "\n")