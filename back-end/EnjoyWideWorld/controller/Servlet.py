# Abstract up the exception-handling code
# in this abstract class.
# ZHOU Kunpeng, 22 Dec 2018

from django.http import JsonResponse
import json
import traceback

# Usage:
# First create a facade method for Django's need.
# Implement this abstract class, override the _action() function.
# In the facade method above, create an instance of the implmented class, 
# and return instance.execute(request).

# Example:
# def servlet(request):
#     return ServletImpl().execute(request)
# class ServletImpl(servlet.AttribServlet):
#     def _action(self, request, response):
#         # do something ...

class AttribServlet():
    # the one who really deals with requests. 
    # Problem: it cannot be passed to django. User has to manually write a function 
    #   that calls return Extend()._execute(request)
    def execute(self, request):
        # preset success
        response = {}
        response['success'] = 1

        try:
            # AttribServlet accepts only GET and POST
            if request.method == "GET":
                self._action(request.GET, response)
            elif request.method == "POST":
                self._action(request.POST, response)
            else:
                raise Exception("ERROR: request method should be GET or POST")

        # print exception content and set success to 0
        except Exception as e:
            response['success'] = 0
            response['error'] = str(e)
            traceback.print_exc()
            print(e)

        # pack up json and return
        return JsonResponse(response)

    # request: a dictionary containing all informations sent by client
    #   NOTE should use request.get('xxx') to read attributes. 
    #        If using request['xxx'], might raise error if xxx does not exist, 
    #        which may not be desired.
    # response: a dictionary containing all informations responded to client
    def _action(self, request, response):
        pass
