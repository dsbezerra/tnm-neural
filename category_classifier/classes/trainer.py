# coding=utf-8

import codecs
import pandas as pd
import urllib2
import json
import os

from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn import metrics

# API URL and endpoints
API_BASE_URL = "https://apitnm-tnmlicitacoes.rhcloud.com/api"
AUTH_ENDPOINT = '/adms/login'
NOTICES_ENDPOINT = '/editais'

# API Authorization token
admin_token = ''

# Admin credentials
login_credentials = {
    "email": "msteampro@gmail.com",
    "password": "c0b0l$cobol1"
}

# Default headers for urllib2.Request
default_headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Script working path
WORKING_PATH = os.getcwd()
APP_PATH = WORKING_PATH + '/category_classifier'

# Serialized trained neural network data paths
MULTINOMIAL_NB_PATH = APP_PATH + '/data/classifier/tnm_category_multinomial_nb.pkl'
VECTORIZER_PATH     = APP_PATH + '/data/classifier/tnm_category_vectorizer.pkl'

# Stop words CSV
STOP_WORDS_CSV_URI = "https://docs.google.com/spreadsheets/d/1JHwKWGSnzNDdLMO51efwDxw4EYWEXe562t7-3Zo363s/export?format=csv"

class Trainer:
        
    def __init__(self, data_table=None):
        if data_table:
            self.data_table = data_table

    # Save the current state of an object to disk
    def save_object_to_disk(classifier, file_path):
        joblib.dump(classifier, file_name);

    # Load the current state of an object from disk
    def load_object_from_disk(file_path):
        return joblib.load(file_path)

    # Load train data
    def load_data(self, path, header=None, names=None):
        if type(path) is not str:
            print "Path must be a string value!!"
            return 0

        if not names:
            names = ["database_id", "description"]

        try:
            file_path = os.path.abspath(path)
            self.data_table = pd.read_table(file_path, header=header, names=names)
            if not self.data_table.empty:
                print "Data loaded."

            else:
                print "Something is wrong."

        except IOError:
            print "There's no such file in this path!"

    # Train the network and test to see accuracy
    def train(self, nb_alpha=1.0, random_state=1, use_saved=True):
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

            if use_saved:
                self.vect = self.load_object_from_disk(VECTORIZER_PATH)
                self.nb = self.load_object_from_disk(MULTINOMIAL_NB_PATH)
            else:
                self.vect = CountVectorizer(decode_error="replace")
                self.nb = MultinomialNB(nb_alpha)
                
            # Vectorize the dataset
            # Transform training data into a dtm
            X_train_dtm = self.vect.fit_transform(X_train)

            # Print features used in classification
            #print ",\n".join(self.vect.get_feature_names())

            # Transform testing data (using fitted vocabulary) into a dtm
            X_test_dtm = self.vect.transform(X_test)

            # Evaluate Naive-Bayes model
            # Import and instantiate a Multinomial Naive Bayes model
            # Train model with X_train_dtm
            self.nb.fit(X_train_dtm, y_train)

            print "Training finished, using test data to check precision..."

            predicted = self.nb.predict(X_test_dtm)

            self.accuracy = metrics.accuracy_score(y_test, predicted)

            print "Predicted output precision: %s" % self.accuracy
            # Print vocabulary
            #print ",\n".join(vect.vocabulary_)
            
            return self.accuracy;
            
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
        
    # Authenticate user
    # Only used when training is for all data of database
    def authenticate(self):
        print "Authenticating..."
        global admin_token
        url = API_BASE_URL + AUTH_ENDPOINT
        req = urllib2.Request(url=url,
                              data=json.dumps(login_credentials),
                              headers=default_headers)
        f = urllib2.urlopen(req)
        if f.getcode() == 200:
            json_response = json.loads(f.read())
            admin_token = json_response["id"]
            print "Authenticating finished."
        else:
            print f.info()
            print "Something wrong happended"

    # Fetch all notices from database
    def fetch_all(self):
        if not admin_token:
            print "No admin token found."
        else:
            print "Fetching all..."
            url = API_BASE_URL + NOTICES_ENDPOINT
            req = urllib2.Request(url=url,
                                  headers=default_headers)
            req.add_header("Authorization", admin_token)
            f = urllib2.urlopen(req)
            if f.getcode() == 200:
                print "Fetching all finished."
                return json.JSONDecoder().decode(f.read().decode('utf-8'))
            else:
                return False

    # Convert input data to a tsv format
    def convert_input_to_tsv_file(self, array, file_path):
        if not file_path:
            print "Invalid file path!"
            return

        abs_path = os.path.abspath(file_path)
        
        with codecs.open(abs_path, "w", encoding="utf-8") as record_file:
            for item in array:
                record_file.write("%s\t%s\n" % (item["segmentoId"], item["objeto"].replace('\n', ' ').replace('\r', ' ').strip()))

        return abs_path
    
    def get_accuracy(self):
        return self.accuracy

    def get_stopwords(self):
        return self.stop_words


trainer = Trainer()
trainer.authenticate()
input = trainer.fetch_all()

trainer.convert_input_to_tsv_file(input, "all.tsv")

trainer.load_data("all.tsv")
print trainer.data_table
