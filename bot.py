import requests
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from project3 import *
qFile = open("Question.txt", 'r')
from machineLearn.py import *
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
clf = classTrain()
messUrl = "https://api.groupme.com/v3/groups/51012574/messages?token=c7GHQhPX92iPvzNLOuLQOZpFh3e6krkgBYzfGMMp"
postUrl = "https://api.groupme.com/v3/bots/post"
r = 0
estVal = ""
while(True):
   r =requests.get(messUrl, params = pars)
   #print(r)
   r = r.json()
   #print(r)
   if (r["response"]["messages"][0]["text"]!=estVal):
      query = r["response"]["messages"[0]["text"]
      question = clf.classify(run(query))
      variables_to_substitute_for = re.findall(r'\[(.*?)\]', question)
      cond, args = get_variable_mapping(variables_to_substitute_for, variables, query)
      inpStr = get_answer_from_query(question, args)
      data["text"] = inpStr
      requests.post(url = postUrl, data=data)
      estVal = r["response"]["messages"][0]["text"]

