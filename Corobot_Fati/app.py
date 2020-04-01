import nltk
import numpy as np
import random
import string 
import re

texte = open('data/infos_corona.txt','r',errors = 'ignore', encoding = "utf8")
texte = texte.read()

texte = re.sub("n.c.a.", "nca", texte)

nltk.download('punkt')
nltk.download('wordnet')
phrases_tokens = nltk.sent_tokenize(texte)

for s in sorted(range(len(phrases_tokens)), reverse = True):
    if re.search(r"\?", phrases_tokens[s]):
        del phrases_tokens[s]


phrases_tokens = list(set(phrases_tokens)) 

from nltk.stem.snowball import FrenchStemmer
Stemmer = FrenchStemmer()
def user_stem(text_user):
    text_user = nltk.word_tokenize(text_user)
    liste_racine = []
    for i in range(len(text_user)):
        liste_racine.append(Stemmer.stem(text_user[i]))
    return " ".join(liste_racine)

def nettoyage(texte):
    texte = texte.lower()
    texte = re.sub(r"\ufeff", "", texte) 
    texte = re.sub(r"\n", " ", texte) 
    texte = re.sub(r"\'", " ", texte)
    texte = re.sub("n.c.a", "nca", texte)
    texte = re.sub("covid-19|virus|covid|sars-cov", "coronavirus", texte)
    texte = re.sub("coronacoronavirus", "", texte)
    texte = re.sub("mort(\w){0,3}|deces|deced(\w){1,5}", "deces", texte)
    texte = re.sub("mort(\w){1,5}|medic(\w){1,5}", "medical", texte)
    texte = re.sub(f"[{string.punctuation}]", " ",texte)
    texte = user_stem(texte)
    return texte

phrases_nettoyees = []
for i in range(len(phrases_tokens)):
    phrases_nettoyees.append(nettoyage(phrases_tokens[i]))

from stop_words import get_stop_words
from sklearn.feature_extraction.text import TfidfVectorizer

fr_stop_words = get_stop_words('french')

# entrainement de la matrice TF-IDF sur les infos
TfidfVec = TfidfVectorizer(stop_words = fr_stop_words)
tf_idf_chat = TfidfVec.fit(phrases_nettoyees)

from sklearn.metrics.pairwise import cosine_similarity
def chatbot(phrase_user):
    phrase_user = [phrase_user]
    tfidf_info = tf_idf_chat.transform(phrases_nettoyees)
    tfidf_user = tf_idf_chat.transform(phrase_user)
    similarite = cosine_similarity(tfidf_user, tfidf_info).flatten()
    index_max_sim = np.argmax(similarite)
    if (similarite[index_max_sim]==0):
        bot_rep = "Veuillez m'excuser, je n'ai pas trouvé cette information"
    else:
        bot_rep = phrases_tokens[index_max_sim]
    return bot_rep

user_hello = r"bonjour|salut|hey|coucou|bjr|slt|cc"
bot_hello = ["Bonjour, bienvenue su le chat", "Bonjour, je suis à votre écoute", "Bonjour, une question ?", "Bienvenu sur votre chatbot specialiste Coronavirus"]

def hello(sentence):
    for word in sentence.split():
        if word in user_hello :
            return random.choice(bot_hello)

print("Bonjour, \nJe suis Corobot, votre informateur spécialiste Covid-19. Comment puis-je vous renseigner ?\n\nPour quitter le chat, écrivez quit ")
flag = True
while flag == True:
    phrase_user = input(">")
    phrase_user = phrase_user.lower()
    if phrase_user != "quit":
        if phrase_user == 'merci':
            flag=False
            print("Au plaisir, \nAvant de vous laisser laisse-moi vous offrir quelques conseils :\nLavez-vous les mains, \nRestez chez vous et surtout \nPrennez soins de vous \n Corobot")
        else :
            if hello(phrase_user) != None :
                print(""+hello(phrase_user))
            else : 
                phrase_user = nettoyage(phrase_user)
                print(""+chatbot(phrase_user))
    else :
        flag = False
        print ("Avant de vous laisser laisse-moi vous offrir quelques conseils :\nLavez-vous les mains, Restez chez vous et surtout Prennez soins de vous \n Corobot")

#creer une application flask
from flask import Flask, render_template, request

app = flask(__name__)