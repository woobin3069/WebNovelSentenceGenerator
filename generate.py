import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import re

filename = r"output.txt"
raw_text = open(filename, 'r', encoding='utf-8').read()
data = raw_text.lower()
chars = sorted(list(set(data)))

char_to_int = dict((c, i) for i, c in enumerate(chars))
int_to_char = dict((i, c) for i, c in enumerate(chars))
n_chars = len(data)
VOCAB_SIZE = len(chars)

SEQ_LENGTH = 20
X = np.zeros((int(len(data)-SEQ_LENGTH), SEQ_LENGTH, VOCAB_SIZE))
y = np.zeros(int(len(data)-SEQ_LENGTH))
jk=[]
for i in range(0,int(len(data)-SEQ_LENGTH)):
    X_sequence = data[i:i+SEQ_LENGTH]
    X_sequence_ix = [char_to_int[value] for value in X_sequence]
    print(X_sequence_ix)
    input_sequence = np.zeros((SEQ_LENGTH, VOCAB_SIZE))
    for j in range(SEQ_LENGTH):
        input_sequence[j][X_sequence_ix[j]] = 1.
    X[i] = input_sequence
    print(X[i])
    y_sequence = data[i+SEQ_LENGTH]
    y_sequence_ix = [char_to_int[value] for value in y_sequence]
    jk.append(y_sequence_ix)
    
y = np_utils.to_categorical(jk,num_classes=1030)
print(X.shape)
print(y.shape)
filepath="weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
model.fit(X, y, epochs=50, batch_size=64, callbacks=callbacks_list)

sty='나 혼자 살아남았다. 흑막이 되어 분란을 일으켰으며 물심양면 용사들이 성장할 수 있도록 도와주었다.'
sty=re.sub('\W',' ',sty)
X = np.zeros((1, SEQ_LENGTH, VOCAB_SIZE))
jk=[]
for i in range(100):
    X_sequence = sty[i:i+SEQ_LENGTH]
    X_sequence_ix = [char_to_int[value] for value in X_sequence]
    #print(X_sequence_ix)
    input_sequence = np.zeros((SEQ_LENGTH, VOCAB_SIZE))
    for j in range(SEQ_LENGTH):
        input_sequence[j][X_sequence_ix[j]] = 1.
    X[0] = input_sequence
    l=model.predict(X)
    index = np.argmax(l)
    print(index)
    g=(int_to_char[index])
    sty=sty+g
    sty=sty[1:len(sty)]
    print(sty)
    print('\n')
