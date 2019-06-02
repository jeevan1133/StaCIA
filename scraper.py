import os, sys, random, requests
from bs4 import BeautifulSoup




def getSkillsTaught():
   url = "http://tutoring.csc.calpoly.edu/"
   myRequest = requests.get(url)
   i = 0
   soup = BeautifulSoup(myRequest.text,"html.parser")
   for Row in soup.find_all("li"):
      if (i<15):
         i+=1
         continue
      if (Row.text == "CP Home"):
         break
      print(Row.text)
