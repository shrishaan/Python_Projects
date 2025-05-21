import numpy as np
import nltk
import string
import random
import os

import nltk
nltk.download('punkt')
nltk.download('all')  
nltk.download('wordnet')

# Load and preprocess chatbot data
file_path = 'chatbot.txt'
if not os.path.exists(file_path):
    print("Error: 'chatbot.txt' file not found.")
    exit()

with open(file_path, 'r', errors='ignore') as f:
    raw_doc = f.read().lower()

# Tokenization
sent_tokens = nltk.sent_tokenize(raw_doc)
word_tokens = nltk.word_tokenize(raw_doc)

lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Greetings
GREET_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey")
GREET_RESPONSES = ["Hello", "Hi", "Greetings", "Sup?", "What's up?", "Hey", "*nods*", "I'm glad you are talking to me."]

def greet(sentence):
    for word in sentence.split():
        if word.lower() in GREET_INPUTS:
            return random.choice(GREET_RESPONSES)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf[:-1])
    idx = vals.argsort()[0][-1]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-1]
    if req_tfidf == 0:
        robo_response = "I am sorry! I don't understand you."
    else:
        robo_response = sent_tokens[idx]
    sent_tokens.pop()
    return robo_response

def chat():
    print("BOT: My name is Sins. Let's have a conversation! If you want to exit any time, just type Bye!")

    flag = True
    while flag:
        user_response = input().lower()
        if user_response != 'bye':
            if user_response in ['thanks', 'thank you']:
                print("BOT: You are welcome...")
                flag = False
            else:
                greeting = greet(user_response)
                if greeting is not None:
                    print("BOT:", greeting)
                else:
                    print("BOT:", response(user_response))
        else:
            flag = False
            print("BOT: Bye! Take care.")

if __name__ == "__main__":
    chat()
