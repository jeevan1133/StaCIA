import os, sys, random, requests
from bs4 import BeautifulSoup
import re

def getSkillsTaught():
   url = "http://tutoring.csc.calpoly.edu"
   myRequest = requests.get(url)
   soup = BeautifulSoup(myRequest.text,"html.parser")
   i = 0
   for Row in soup.find_all("li"):
      if (i<15):
         i+=1
         continue
      if (Row.text == "CP Home"):
         break
      print(Row.text)
   
def getWontDo():
   url = "http://tutoring.csc.calpoly.edu"
   myRequest = requests.get(url)
   soup = BeautifulSoup(myRequest.text,"html.parser")
   i = 0
   for Row in soup.find_all("p"):
      if (i==2):
         print(Row.text)
         break
      i+=1
      
def getClassesInfo():
   url = "http://tutoring.csc.calpoly.edu"
   myRequest = requests.get(url)
   soup = BeautifulSoup(myRequest.text,"html.parser")
   i = 0
   for Row in soup.find_all("p"):
      if (i==0):
         print(Row.text)
         break
      i+=1

def getTutorNames():
   url = "http://tutoring.csc.calpoly.edu/tutors/"
   myRequest = requests.get(url)
   soup = BeautifulSoup(myRequest.text, "html.parser")
   for Row in soup.find_all("h1", {"id":"head-tutor"}):
      print(Row.text) 
   for Row in soup.find_all("h2"):
      print(Row.text)

def getGameDesignDescript():
   url = "http://www.cpgd.org/"
   myRequest = requests.get(url)
   soup = BeautifulSoup(myRequest.text, "html.parser")
   i = 0
   for Row in soup.find_all("div", {"class":"widget-content"}):
      if (i ==1):
         print(Row.text)
         break
      i+=1

def getCPGDOfficers():
   url = "http://www.cpgd.org/"
   myRequest = requests.get(url)
   soup = BeautifulSoup(myRequest.text, "html.parser")
   for Row in soup.find_all("div", {"class":"widget TextList", "data-version":"1", "id":"TextList1"}):
      print(Row.text)

def getPolyAppDevOfficers():
   url = "http://www.polyappdev.club"
   myRequest = requests.get(url)
   i = 0
   soup = BeautifulSoup(myRequest.text, "html.parser")
   for Row in soup.find_all("div", {"class":"col-lg-3 col-md-6 text-center"}):
      if (i<5):
         i+=1
         continue
      print(Row.text)

def getPolyAppDevContact():
   url = "http://www.polyappdev.club"
   myRequest = requests.get(url)
   i = 0
   soup = BeautifulSoup(myRequest.text, "html.parser")
   for Row in soup.find_all("div", {"class":"col-lg-12 text-center"}):
      if (i==6):
         print(Row.text)
      i+=1
      
def getRoboticsDescript():
   url = "http://calpolyrobotics.com"
   myRequest = requests.get(url)
   i = 0
   soup = BeautifulSoup(myRequest.text, "html.parser")
   for Row in soup.find_all("p", {"style":"white-space:pre-wrap;"}):
      print(Row.text)
      i+=1

def getRoboticsOfficers():
   url = "http://calpolyrobotics.com/contact"
   myRequest = requests.get(url)
   i = 0
   soup = BeautifulSoup(myRequest.text, "html.parser")
   for Row in soup.find_all("div", {"class":"sqs-block html-block sqs-block-html sqs-col-6 span-6 float float-right", "data-block-type":"2", "id":"block-yui_3_17_2_7_1514424451520_11041"}):
      print(Row.text)

def getRoboticsLocation():
   url = "http://calpolyrobotics.com/contact"
   myRequest = requests.get(url)
   i = 0
   soup = BeautifulSoup(myRequest.text, "html.parser")
   for Row in soup.find_all("div", {"class":"footer-inner"}):
      print(Row.text)


