import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
qFile = open("Questions.txt", 'r')
#extracts "meaningful" words
def run(inputQuestion):
  ensw = stopwords.words("english")
  rs = [word for word in word_tokenize(inputQuestion) if word not in ensw] 
  retDict = {}
  if ("[" in rs):
     rs.remove("[")
  if ("]" in rs):
     rs.remove("]")
  if ("?" in rs):
     rs.remove("?")
  for word in rs:
    retDict[word] = True
  return retDict
  #nameSub has first letter capitalized, note that this might not always be the case
  #nameSub = nameSub.capitalize()

#def getImpTerms(inpStr):
#   newList = []
#   for val in varDict:
#      for word in varDict[val]:
#         if inpStr.find(word) > 0:
#            newList.append((val, word))
#   return newList
   
def classTrain():
   Questlist = []
   lineList = qFile.readlines()
   for line in lineList:
      rawQuest = line.split('|')[1]
      rawQuest = rawQuest.strip()
      wordList = run(rawQuest)
      Questlist.append((wordList, rawQuest))
   classifier = nltk.NaiveBayesClassifier.train(Questlist)
   return classifier

def getInp():
   classifier = classTrain()
   testStr = input("Please input string: ")
   while testStr != "quit":
      #print(getImpTerms(testStr))
      #print(run(testStr))
      print(classifier.classify(run(testStr)))
      testStr = input("Please input string: ")

#classTrain()   








#splStr = testStr.split(' ')
#newList = []
#for word in splStr:
#   for val in varDict:
#      if word in varDict[val]:
#         newList.append((val, word))
#print(run(testStr))
#print(newList)
#print(classifier.classify(run(testStr)))

#   for i in range(len(rqSplit)):
#      nameList = []
#      print(rqSplit[i])
#      if (rqSplit[i][0] == '['):
#         offSet = 1
#         if (rqSplit[i][len(rqSplit[i])-1] == '?' or rqSplit[i][len(rqSplit[i])-1] == '.'):
#            offSet = 2
#         for name in varDict[rqSplit[i][1:len(rqSplit[i])-offSet]]:
#            nameList = list(rqSplit)
#            nameList[i] = name
#            for j in range(i, len(nameList)):
#               if (nameList[j][0] == '['):
#                  offSet = 1
#                  if (rqSplit[j][len(rqSplit[j])-1] == '?' or rqSplit[j][len(rqSplit[j])-1] == '.'):
#                     offSet = 2
#                  for var in varDict[nameList[j][1:len(nameList[j])-offSet]]:
#                     nameList[j] = var
#                     Questlist.append(' '.join(nameList)) 
#                     hasTwo = True
#            if hasTwo == False:
#               Questlist.append(' '.join(nameList))
#               hasTwo = False
#print(Questlist)
