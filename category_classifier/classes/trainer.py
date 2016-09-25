# coding=utf-8

import os
import pandas as pd
import urllib2

from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

STOP_WORDS_CSV_URI = "https://docs.google.com/spreadsheets/d/1JHwKWGSnzNDdLMO51efwDxw4EYWEXe562t7-3Zo363s/export?format=csv"

class Trainer:
        
    def __init__(self, data_table=None):
        if data_table:
            self.data_table = data_table

    # Load train data
    def load_data(self, path, header=None, names=None):
        if type(path) is not str:
            print "Path must be a string value!!"
            return 0

        if not names:
            names = ["category_name", "id", "database_id", "description"]

        try:
            root_path = os.getcwd() + '\\category_classifier\\'
            self.data_table = pd.read_table(root_path + path, header=header, names=names)
            if not self.data_table.empty:
                print "Data loaded."

            else:
                print "Something is wrong."

        except IOError:
            print "There's no such file in this path!"

    # Train the network and test to see accuracy
    def train(self, nb_alpha=1.0, random_state=1):
        data_table = self.data_table
        data_size = len(data_table)
        if data_size > 0:
            print "Training network..."

            X = data_table.description
            y = data_table.database_id

            X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=random_state)
            
            #print X_train.shape
            #print X_test.shape
            #print y_train.shape
            #print y_test.shape

            # Vectorize the dataset
            self.vect = CountVectorizer(decode_error="replace")
            # Transform training data into a dtm
            X_train_dtm = self.vect.fit_transform(X_train)

            # Print features used in classification
            #print ",\n".join(self.vect.get_feature_names())

            # Transform testing data (using fitted vocabulary) into a dtm
            X_test_dtm = self.vect.transform(X_test)

            # Evaluate Naive-Bayes model
            # Import and instantiate a Multinomial Naive Bayes model
            self.nb = MultinomialNB(nb_alpha)
            # Train model with X_train_dtm
            self.nb.fit(X_train_dtm, y_train)

            print "Training finished, using test data to check precision..."

            predicted = self.nb.predict(X_test_dtm)

            self.accuracy = metrics.accuracy_score(y_test, predicted)

            print "Predicted output precision: %s" % self.accuracy
            # Print vocabulary
            #print ",\n".join(vect.vocabulary_)
            
        else:
            print "There's no data to be trained!"

    def fetch_stopwords(self):
        req = urllib2.Request(url=STOP_WORDS_CSV_URI)
        res = urllib2.urlopen(req)

        if res.getcode() == 200 and res.info().gettype() == "text/csv":
            self.stop_words = []
            words_section = False
            while(True):
                row = res.readline()
                
                if row == '':
                    break

                if words_section:
                    # Get columns from row splitting by comma
                    columns = row.split(',')
                    # Add to stop words if it doesn't contribute to the network
                    if columns[1] == "Não":
                        self.stop_words.append(columns[0]) 
                        # Skip the rest of loop
                        continue

                if row.startswith("BEGIN"):
                    words_section = True
            
            return self.stop_words

        else:
            print "Failed to fetch stop words."
            return 0

    def get_accuracy(self):
        return self.accuracy

    def get_stopwords(self):
        return self.stop_words
