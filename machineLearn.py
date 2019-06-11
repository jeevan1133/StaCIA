import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def run(inputQuestion,variables_dict=None):
  #ensw = stopwords.words("english")
  vars_to_replace = re.findall(r'\[(.*?)\]', inputQuestion)
  rs = [word for word in word_tokenize(inputQuestion)] # if word not in ensw] 
  if ("[" in rs):
     rs.remove("[")
  if ("]" in rs):
     rs.remove("]")  
  for v in var:
     rs.extend(variables_dict.get(v))
      
  return {word: True for word in rs}
  
  
def classTrain(variables_dict):
   qFile = open("Questions.txt", 'r')
   Questlist = []
   lineList = qFile.readlines()
   for line in lineList:
      rawQuest = line.split('|')[1]
      rawQuest = rawQuest.strip()
      wordList = run(rawQuest, variables_dict)
      Questlist.append((wordList, rawQuest))
      
   qFile.close()
  
   for _ in range(5):
      random.shuffle(Questlist)
      classifier = nltk.NaiveBayesClassifier.train(Questlist)
   return classifier
  
