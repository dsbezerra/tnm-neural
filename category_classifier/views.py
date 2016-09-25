import json

from .classes import CategoryClassifier

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
