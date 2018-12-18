# Abstract up the exception-handling code
# in this abstract class.
# (might be problematic: how to import a class in the package of previous level?)
# NOTE do not implememnt for now.
# ZHOU Kunpeng, 18 Dec 2018

from django.http import HttpResponse
import json

class AttribServlet():
    # the one who really deals with requests.
    def execute(self, request):
        response = {}

        try:
            if request.method == "GET":
                action(request.GET, response)
            elif request.method == "POST":
                action(request.POST, response)
            else
                raise Exception("ERROR: request method should be GET or POST")

        except Exception as e:
            response['success'] = 0
            response['error'] = e
            print(e)

        finally:
            # pack up json and return
            return HttpResponse(json.dumps(response), content_type="application/json")

    # request: a dictionary containing all informations sent by client
    # response: a dictionary containing all informations responded to client
    def action(self, request, response):
        pass
