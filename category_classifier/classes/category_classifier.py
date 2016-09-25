import codecs
import json
import os
import sys
import uuid

from sklearn.externals import joblib

# Script working path
WORKING_PATH = os.getcwd()
APP_PATH = WORKING_PATH + '\\category_classifier'

# Serialized trained neural network data paths
MULTINOMIAL_NB_PATH = APP_PATH + '\\data\\classifier\\tnm_category_multinomial_nb.pkl'
VECTORIZER_PATH     = APP_PATH + '\\data\\classifier\\tnm_category_vectorizer.pkl'

# CATEGORIES
CATEGORIES_LIST_PATH = APP_PATH + '\\data\\category_list.json'

class CategoryClassifier:
    
    # Constructor
    def __init__(self, input=None):
        f = codecs.open(CATEGORIES_LIST_PATH, "r", encoding="utf-8")
        self.categories = json.loads(f.read())['categories']
        if input:
            self.input = input
        
    # Runs the neural network
    def run(self):
        if self.input:
            #print 'Running...'
            return self.process()
        else:
            return -1

    # Process input data
    def process(self):
        
        try:
        
            vect = joblib.load(  VECTORIZER_PATH  )
            nb   = joblib.load(MULTINOMIAL_NB_PATH)
			
            #print ",\n".join(vect.stop_words)
        
            if nb and vect:
                X_input_counts = vect.transform(self.input)
                Y_predicted    = nb.predict(X_input_counts)
                
                results = { 
                    '_id': uuid.uuid4(), # Test
                    'count': len(Y_predicted), 
                    'data': []
                }

                index = 0

                for y in Y_predicted:
                    result = { 
                        'output': self.categories[y], 
                        'tested_input': self.input[index]
                    }
                    
                    results['data'].append(result)
                    
                    index += 1

                self.output = results

                return self.output
            
            else:
                return -1

        except IOError:
            #print """Trained network not found!\n
            #         Please check if the files exists in specified paths."""
            return -1

    # Setters
    def set_input(self, input):
        self.input = input
    
    def set_output(self, output):
        self.output = output

    # Getters    
    def get_input(self):
        return self.input

    def get_output(self):
        return self.output
