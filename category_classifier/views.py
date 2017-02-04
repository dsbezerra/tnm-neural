import json
import uuid
import os

from .classes import CategoryClassifier
from .classes import Trainer

from django.http import HttpResponse
from django.http import JsonResponse

# Empty responses are intentionally

# Test
def index(request):
    return HttpResponse('Hello!')

# Process input and responds with predicted data
def process(request):
    if request.method != "POST":
        return HttpResponse()
    
    if request.body:
        json_body = json.loads(request.body)
        category_classifier = CategoryClassifier(json_body['input'])
        results = category_classifier.run()
        
        #print results
        
        if results:            
            return JsonResponse(results)


    return HttpResponse('Hello!')

# Train current network with the new input data
def train(request):
    if request.method != "POST":
        return HttpResponse()

    if request.body:
        json_body = json.loads(request.body)

        if not json_body:
            return JsonResponse({
                'success': False,
                'message': 'Invalid request.'
            })
        
        task_id = uuid.uuid4()
        
        trainer = Trainer()

        file_path = "../data/%s.tsv" % (str(task_id))
        
        output_path = trainer.convert_input_to_tsv_file(json_body['input'], file_path)

        if output_path:
            trainer.load_data(output_path)
            accuracy = trainer.train()

            # Remove .tsv from disk
            os.remove(output_path)

            return JsonResponse({
                'success': True,
                'data': {
                    '_id': task_id,
                    'accuracy': accuracy,
                }                
            })
            
        else:
            return JsonResponse({
                'success': False,
                'message': 'Could not find data table.'
            })
    else:
        return HttpResponse();
            
