# -*- coding: utf-8 -*-
"""
This script will fit a CNN to our webscrapped data saved in "RYANDATA_filt.csv'

The titles from the csv need to be converted into sparse matrices that reprsent
    the number of occurances of each word from the global bag of words present
    in each of the titles.
    
The topics from the csv need to be converted into a sparse matrix with number
     of columns equal to the number of unique topics.
     
Once fit it saves the model:      model.json
    Also saves the label encoder: LabelEncoder.npy
    and the vectorizer:           Vectorizer.pkl
    
To test the model run keras_eval.py
    The testing data needs to be input as a list of strings, which is converted
    to a data frame, then the sparse matrix.

@author: Gary
"""

import pandas as pd
import numpy as np
import string

#========================= Read in the Data ===================================
data = pd.read_csv('RYANDATA_filt.csv')
data.columns = ['num','topic','authors','title','Journals','Years','Vol_Isue','DOI']

papers = pd.DataFrame(data['title'])
topic = pd.DataFrame(data['topic'])
author = pd.DataFrame(data['authors'])
print("Number of Papers: " + str(len(papers)))
topic['topic'].unique()

#========================= Formatting Data ====================================
# Convert the data in the a sparse matrix.
# X is size Number of Articles by Number of Words in bag
# Y is size Number of Articles by Number of Unique Topics
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.externals import joblib

feat = ['topic']
for x in feat:
    le = LabelEncoder()
    le.fit(list(topic[x].values))

np.save('../Models/keras_LabelEncoder.npy',le.classes_)
print('Saved Label Encoder: LabelEncoder.npy')

data['everything'] = pd.DataFrame(data['title'])
print(data['everything'].head(5))

def change(t):
    t = t.split()
    return ' '.join([(i) for (i) in t if i not in stop])

from nltk.corpus import stopwords
stop = list(stopwords.words('english'))
stop_c = [string.capwords(word) for word in stop]
for word in stop_c:
    stop.append(word)

data['everything'].apply(change)

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

#from sklearn.feature_extraction.text import TfidfVectorizer
#vectorizer = TfidfVectorizer(min_df=1, max_features=70000, strip_accents='unicode',lowercase =True,
#                            analyzer='word', token_pattern=r'\w+', use_idf=True, 
#                            smooth_idf=True, sublinear_tf=True, stop_words = 'english')
#vectors = vectorizer.fit_transform(data['everything'])
#vectors.shape

vect = CountVectorizer()
vect.fit(data['everything'])
joblib.dump(vect,'../Models/keras_Vectorizer.pkl')
print('Saved Vectorizer: Vectorizer.pkl')

vectors = vect.transform(data['everything'])

encoder = OneHotEncoder(sparse = True)
topic = encoder.fit_transform(topic)

X_train, X_test, y_train, y_test = train_test_split(vectors,
                                                    topic,#topic['topic'],
                                                    test_size=0.1,
                                                    random_state = 0)

input_dim = X_train.shape[1]  # Number of features
num_words = X_train.shape[1]

#========================= Fit the Neural net =================================
# Have 3 layers, first layer with 500 units, next two with 100 each.
# Output layer needs to have the same number of units as Num Topics
from keras.models import Sequential
from keras import layers
from keras.layers import LSTM, Dense, Dropout, Masking, Embedding

model = Sequential()
model.add(layers.Dense(500, input_dim=input_dim, activation='relu'))
model.add(Dropout(0.5))
model.add(layers.Dense(100, input_dim=input_dim, activation='relu'))
model.add(Dropout(0.5))
model.add(layers.Dense(100, input_dim=input_dim, activation='relu'))
model.add(Dropout(0.5))
model.add(layers.Dense(27, activation='sigmoid'))

model.compile(loss='binary_crossentropy', 
    optimizer='adam', 
    metrics=['accuracy'])
model.summary()

history = model.fit(X_train, y_train,
                    epochs=500,
                    verbose=2,
                    validation_data=(X_test, y_test),
                    batch_size=3000)

loss, accuracy = model.evaluate(X_train, y_train, verbose=False)
print("Training Accuracy: {:.4f}".format(accuracy))
loss, accuracy = model.evaluate(X_test, y_test, verbose=False)
print("Testing Accuracy:  {:.4f}".format(accuracy))

import matplotlib.pyplot as plt
# Plot training & validation accuracy values
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

#========================= Save the Model =====================================
from keras.models import model_from_json
model_json = model.to_json()
with open("../Models/keras_model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("../Models/keras_model.h5")
print("Saved model to disk: model.h5")
import os
if os.path.isfile('../Models/keras_LabelEncoder.npy'):
    print('Saved Label Encoder: LabelEncoder.npy')
else:
    print('NO LABEL ENCODER SAVED')
    
if os.path.isfile('../Models/keras_LabelEncoder.npy'):
    print('Saved Vectorizer: Vectorizer.pkl')
else:
    print('NO VECTORIZER SAVED')
    
















