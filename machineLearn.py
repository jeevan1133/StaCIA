import nltk
qFile = open("qList", 'r')
ClubNames = ["Cal Poly Game Design Club", "Association for Computing Machinery", "Women Involved in Software and Hardware", "Cal Poly Linux Users Group", "White Hat", "Cal Poly App Dev Club", "Cal Poly Robotics Club", "SLO Hacks", "CPGD", "ACM", "WISH", "CPLUG"]

OfficerRoles = ["President", "Vice President", "Secretary", "Treasurer"]

CSCorSTAT = ["CSC", "STAT", "Computer Science", "Statistics"]

Day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

STATCLASSNAME = ["STAT 150", "STAT 301", "STAT 302", "STAT305"]

TutorName = ["Nicole Anderson-Au", "Austin Shin", "Cole Cummins", "James Asbury", "Jeremy Berchtold", "Jiwon Lee", "Nathan Lui"]

StatYear = ["2017-2018", "2018-2019"]

StatTutorType = ["General", "Private"]
CSCClass = ["101", "202", "203", "225", "141", "357", "123" "234", "349"]

hasTwo = False
varDict = {
   "CSSESTATClubOrgName": ClubNames,
   "OfficerRole": OfficerRoles,
   "CSCorSTAT": CSCorSTAT,
   "Day": Day,
   "STATCLASSNAME": STATCLASSNAME,
   "TutorName": TutorName,
   "STATTutorType": StatTutorType,
   "StatYear": StatYear,
   "CSCClass": CSCClass
}
def getQuestionWords(question):
  return [m[0] for m in nltk.pos_tag(question) if m[1][0] == 'W']

def getSubjects(question):
  return [m[0] for m in nltk.pos_tag(question) if m[1][0] == 'N']

def getVerbs(question, count):
  return [m[0] for m in nltk.pos_tag(question) if m[1][0] == 'V'][:count]

def getPrepositions(question):
  return [m[0] for m in nltk.pos_tag(question) if m[1] == 'IN']

#extracts "meaningful" words
def run(inputQuestion):
  question = nltk.word_tokenize(inputQuestion)
  starting = question[0].lower()
  question = [m.lower() for m in question if m.lower() not in nltk.corpus.stopwords.words('english')]
  question.append(starting)
  l1 = getQuestionWords(question)
  l1.extend(getSubjects(question))
  l1.extend(getVerbs(question, 2))
  l1.extend(getPrepositions(question))
  nameSub = '' #holds the "name" if one is found
  rs = []
  for v in l1:
    if v in [m.lower() for m in nltk.corpus.names.words('male.txt')] or \
       v in [m.lower() for m in nltk.corpus.names.words('female.txt')]:
      rs.append('~NAME~')
      nameSub = v
    else:
      rs.append(v)
  retDict = {}
  for word in rs:
    retDict[word] = True
  return retDict
  #nameSub has first letter capitalized, note that this might not always be the case
  #nameSub = nameSub.capitalize()

def getImpTerms(inpStr):
   newList = []
   for val in varDict:
      for word in varDict[val]:
         if inpStr.find(word) > 0:
            newList.append((val, word))
   return newList
   
Questlist = []
lineList = qFile.readlines()
for line in lineList:
   rawQuest = line.split('|')[1]
   rawQuest = rawQuest.strip()
   wordList = run(rawQuest)
   Questlist.append((wordList, rawQuest))
findFEATURES = []
classifier = nltk.NaiveBayesClassifier.train(Questlist)
testStr = input("Please input string: ")

while testStr != "quit":
   print(getImpTerms(testStr))
   print(classifier.classify(run(testStr)))
   testStr = input("Please input string: ")
   
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
