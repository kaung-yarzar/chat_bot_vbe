

import warnings
warnings.filterwarnings('ignore')

import nltk

nltk.download('wordnet')
nltk.download('punkt_tab')
nltk.download('stopwords')

from nltk.stem import WordNetLemmatizer

import numpy

import streamlit as st

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from pymongo import MongoClient





client = MongoClient('mongodb://kelo:11MRAg3FVeaA3QeS@cluster0-shard-00-00.g1sch.mongodb.net:27017,cluster0-shard-00-01.g1sch.mongodb.net:27017,cluster0-shard-00-02.g1sch.mongodb.net:27017/?ssl=true&replicaSet=atlas-i75tpn-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')
db = client['tumltaproject']
collection = db['training_data']

data = collection.find()

sentences = ""
for doc in data:
    text_value = doc.get("text", "")
    sentences += text_value + "\n"


client.close()



# file = open('data.txt', 'r')
# sentences = file.read()



import nltk
sen = nltk.sent_tokenize(sentences) # make sentences


words = nltk.word_tokenize(sentences) # make words

##from nltk.corpus import wordnet as wn
wnlem = nltk.stem.WordNetLemmatizer()

def perfom_lemmatization(tokens):
  return[wnlem.lemmatize(token) for token in tokens]

import string
pr = dict((ord(punctuation),None) for punctuation in string.punctuation)

# To process data

def get_processed_text(document):
  return perfom_lemmatization(nltk.wordpunct_tokenize(document.lower().translate(pr)))




greeting_inputs=('hey', 'hello')
greeting_responses =['hey', 'hello']

import random
# generating greeting responses
def generate_greeting_responses(greeting):
  for token in greeting.split():
    if token.lower() in greeting_inputs:
      return random.choice(greeting_responses)

# for generating responses


def generate_response(user_input):
  bot_response = ''
  sen.append(user_input)

  word_vectorizer = TfidfVectorizer(tokenizer=get_processed_text, stop_words='english')
  word_vectors = word_vectorizer.fit_transform(sen)
  similar_vector_values = cosine_similarity(word_vectors[-1], word_vectors)
  similar_sentence_number = similar_vector_values.argsort()[0][-2]


  match_vector = similar_vector_values.flatten()
  match_vector.sort()
  vector_matched = match_vector[-2]


  if vector_matched == 0:
    bot_response = bot_response + 'I am sorry. I am not trained for this data'
    return bot_response

  else:
    if '?' in sen[similar_sentence_number]:
      bot_response = bot_response + sen[similar_sentence_number + 1]

    else:
      bot_response = bot_response + sen[similar_sentence_number]

    return bot_response



# continue_flat = True
# print("Hello I am chat bot for Students. You can ask me anything about Technological University Meiktila")
# while(continue_flat == True):
#   human = input()
#   human = human.lower()



#   #for closing
#   if human != 'bye':
#     if human == 'thanks' or human == 'thankyou':
#       continue_flat = False
#       print('Most welcome from bot')
#     else:
#       if generate_greeting_responses(human) != None:
#         print('bot : ' +generate_greeting_responses(human))
#       else:
#         print('Bot : ', end = '')
#         print(generate_response(human))
#         sen.remove(human)

#   else:
#       continue_flat = False
#       print('Bot : goodbye')


# prompt = st.chat_input("Say something")
# if prompt:
#     st.write(f"User has sent the following prompt: {human}")




st.title("Welcome to TU Meiktila")

# with st.chat_message("bot", avatar="🦖"):
#   st.markdown('Hello Student Information Chat Bot. Feel Free to ask me..')


# user_prompt = st.chat_input("Say something")
# if user_prompt:
#     with st.chat_message("user", avatar="🧑‍💻"):
#       st.markdown(user_prompt)
 


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar= message["avatar"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar" : "🧑‍💻"}) 
if prompt != None:
  response = f"Echo: {generate_response(prompt)}"
  # Display assistant response in chat message container
  with st.chat_message("assistant", avatar="🤖"):
      # st.markdown(response)
      if 'https' in response:
         st.image(response)
      else:   
        st.markdown(response)
  # Add assistant response to chat history
  st.session_state.messages.append({"role": "assistant", "content": response, "avatar" : "🤖"})
