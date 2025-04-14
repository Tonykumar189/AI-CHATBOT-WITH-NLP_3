import random
import json
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Download required NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Sample intents
intents = {
    "intents": [
        {"tag": "greeting", "patterns": ["Hi", "Hello", "Hey"], "responses": ["Hello!", "Hi there!", "Greetings!"]},
        {"tag": "goodbye", "patterns": ["Bye", "See you", "Goodbye"], "responses": ["See you later!", "Goodbye!"]},
        {"tag": "thanks", "patterns": ["Thanks", "Thank you"], "responses": ["You're welcome!", "No problem!"]},
        {"tag": "name", "patterns": ["What is your name?", "Who are you?"], "responses": ["I'm CodTechBot, your assistant."]}
    ]
}

# Preprocessing
lemmatizer = WordNetLemmatizer()
all_words = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

# Lemmatization and removing duplicates
ignore_words = ['?', '.', '!']
all_words = [lemmatizer.lemmatize(w.lower()) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# Training data
X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    bag = [0] * len(all_words)
    pattern_words = [lemmatizer.lemmatize(w.lower()) for w in pattern_sentence]
    for word in pattern_words:
        for i, w in enumerate(all_words):
            if w == word:
                bag[i] = 1
    X_train.append(bag)
    y_train.append(tags.index(tag))

# Model
model = MultinomialNB()
model.fit(X_train, y_train)

# Chat function
def bag_of_words(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(w.lower()) for w in sentence_words]
    bag = [0] * len(all_words)
    for s in sentence_words:
        for i, w in enumerate(all_words):
            if w == s:
                bag[i] = 1
    return np.array(bag)

def chat():
    print("CodTechBot is online! (type 'quit' to stop)")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            print("CodTechBot: Goodbye!")
            break
        bow = bag_of_words(inp)
        result = model.predict([bow])[0]
        tag = tags[result]

        for intent in intents['intents']:
            if intent["tag"] == tag:
                print("CodTechBot:", random.choice(intent["responses"]))

# Start the chatbot
chat()
