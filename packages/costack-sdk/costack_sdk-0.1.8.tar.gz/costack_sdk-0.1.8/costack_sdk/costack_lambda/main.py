import json

class CostackRequest:
    def __init__(self, event):
        # initialie 
        self._header = None
        self._http_method = None
        self._body = None 
        self._is_base64_encoded = None 
        self._route_path = None 
        self._params = None 
        # build from the event input 
        self.build_from_event(event)

    @property
    def header(self):
        return self._header

    @property
    def http_method(self):
        return self._http_method

    @property
    def body(self):
        return self._body

    @property
    def is_base64_encoded(self):
        return self._is_base64_encoded

    @property
    def route_path(self):
        return self._route_path

    @property
    def params(self):
        return self._params

    def build_from_event(self, event):
        # parse the input event 
        http = event['requestContext']['http']
        self._http_method = http['method']
        self._header = event['headers']
        self._is_base64_encoded = event['isBase64Encoded']
        self._route_path = event["routeKey"].split()[1]
        # optional params
        self._params = event.get("queryStringParameters", None)
        if self._http_method.lower() == "get":
            # do nothing 
            pass 
        elif self._http_method.lower() == "post":
            self._body = event['body']
    
def costack_http(methods=[]):
    for m in methods:
        if m.lower() not in ["get", "post", "put"]:
            raise ValueError(f"unexpected http method {m}")
    def decorator(function):
        def wrapper(event, context):
            #parse the input event to a readable format 
            # check the method and make sure it matches 
            request = CostackRequest(event)
            if request.http_method not in methods:
                raise ValueError(f"unmatched http method {m} for function")
            result = function(request, context)
            return result
        return wrapper
    return decorator

@costack_http(methods=["GET", "POST"])
def simple_lambda(event, context):
    print(event.header)
    print(event.body)
    return event 

if __name__=="__main__":
    with open("sample_get.json", "r") as f:
        event = json.loads(f.read())
    res = simple_lambda(event,22)
    print(res)

