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
hasVar = False
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
   
Questlist = []
lineList = qFile.readlines()
for line in lineList:
   rawQuest = line.split('|')[1]
   rawQuest = rawQuest.strip()
   rqSplit = rawQuest.split(' ')
   for i in range(len(rqSplit)):
      nameList = []
      print(rqSplit[i])
      if (rqSplit[i][0] == '['):
         hasVar = True
         offSet = 1
         if (rqSplit[i][len(rqSplit[i])-1] == '?' or rqSplit[i][len(rqSplit[i])-1] == '.'):
            offSet = 2
         for name in varDict[rqSplit[i][1:len(rqSplit[i])-offSet]]:
            nameList = list(rqSplit)
            nameList[i] = name
            for j in range(i, len(nameList)):
               if (nameList[j][0] == '['):
                  offSet = 1
                  if (rqSplit[j][len(rqSplit[j])-1] == '?' or rqSplit[j][len(rqSplit[j])-1] == '.'):
                     offSet = 2
                  for var in varDict[nameList[j][1:len(nameList[j])-offSet]]:
                     nameList[j] = var
                     Questlist.append(' '.join(nameList)) 
                     hasTwo = True
            if hasTwo == False:
               Questlist.append(' '.join(nameList))
               hasTwo = False
      else:
         Questlist.append(' '.join(rqSplit))
print(Questlist)
