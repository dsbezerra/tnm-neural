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
    else:

        print request.body

        if request.body and request.content_type == 'application/json':
            json_body = json.loads(request.body)
            category_classifier = CategoryClassifier(json_body['input'])
            results = category_classifier.run()

            if results:
                # TODO(diego): Use database to save predicted values and to control duplication
                # If array with more than one record, use Bulk from mongo to perform an efficient
                # insert into database, otherwise just use a normal insert operation. 
                
                # For now just send the information back to client

                return JsonResponse(results)
            return HttpResponse()
        else:
            return HttpResponse()
