import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
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

ensw = stopwords.words("english")
#extracts "meaningful" words
def getImpTerms(inpStr):
   newList = []
   for val in varDict:
      for word in varDict[val]:
         if inpStr.find(word) > 0:
            newList.append((val, word))
   return newList

def run(inputQuestion):
  rs = [word for word in word_tokenize(inputQuestion) if word not in ensw]
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
url = "https://api.groupme.com/v3/groups?token=c7GHQhPX92iPvzNLOuLQOZpFh3e6krkgBYzfGMMp"
r = requests.get(url)
data = r.json()
import string
from random import *
min_char = 8
max_char = 12
allchar = string.ascii_letters + string.punctuation + string.digits
password = "".join(choice(allchar) for x in range(randint(min_char, max_char)))
data = {
   "bot_id"  :  "462a2b8d192fbe66e261cd8d05",
   "text"  :   "Hello world"
}
pars = {
   "limit"   :   1
   #"since_id": "462a2b8d192fbe66e261cd8d05"
}
messUrl = "https://api.groupme.com/v3/groups/51012574/messages?token=c7GHQhPX92iPvzNLOuLQOZpFh3e6krkgBYzfGMMp"
postUrl = "https://api.groupme.com/v3/bots/post"
r = 0
estVal = ""
while(True):
   r =requests.get(messUrl, params = pars)
   #print(r)
   if (r == 304):
      break
   r = r.json()
   #print(r)
   if (r["response"]["messages"][0]["text"]!=estVal):
      print("we out here")
      data["text"] = classifier.classify(run(r["response"]["messages"][0]["text"]))
      print(requests.post(url = postUrl, data=data))
      estVal = r["response"]["messages"][0]["text"]
