from flask import jsonify, make_response

class Response:
    def __init__(self, status_code, response_message, data=None):
        self.status_code = status_code
        self.response_message = response_message
        self.data = data or {}
        
        self.flask = make_response(jsonify(self.to_dict()), self.status_code)
    
    def to_dict(self):
        return {"response": self.response_message} | self.data
    
    def build(self):
        return self.flask


# Responses
class Responses:
    # 2** Success
    class OK_200(Response):
        def __init__(self, data=None):
            super().__init__(200, "ok", data)

    class Created_201(Response):
        def __init__(self, data=None):
            super().__init__(201, "created", data)
    
    class Accepted_202(Response):
        def __init__(self, data=None):
            super().__init__(202, "accepted", data)

    # 3** Redirection
    class Moved_Permanently_301(Response):
        def __init__(self, new_url="/", data=None):
            data = data or {}
            data.update({"new_url": new_url})
            super().__init__(301, "moved_permanently", data)

    class Found_302(Response):
        def __init__(self, new_url="/", data=None):
            data = data or {}
            data.update({"new_url": new_url})
            super().__init__(302, "found", data)

    class Temporary_Redirect_307(Response):
        def __init__(self, new_url="/", data=None):
            data = data or {}
            data.update({"new_url": new_url})
            super().__init__(307, "temporary_redirect", data)

    class Permanent_Redirect_308(Response):
        def __init__(self, new_url="/", data=None):
            data = data or {}
            data.update({"new_url": new_url})
            super().__init__(308, "permanent_redirect", data)

    # 4** Client Errors
    class Bad_Request_400(Response):
        def __init__(self, details="<detailed error message>", data=None):
            data = data or {}
            data.update({"details": details})
            super().__init__(400, "bad_request", data)

    class Unauthorized_401(Response):
        def __init__(self, details="This endpoint requires authentication", data=None):
            data = data or {}
            data.update({"details": details})
            super().__init__(401, "unauthorized", data)

    class Forbidden_403(Response):
        def __init__(self, details="<detailed error message>", data=None):
            data = data or {}
            data.update({"details": details})
            super().__init__(403, "forbidden", data)

    class Not_Found_404(Response):
        def __init__(self, details="<type of resource. this varies by endpoint>", data=None):
            data = data or {}
            data.update({"details": details})
            super().__init__(404, "resource_not_found", data)

    class Im_A_Teapot_418(Response): # sue me.
        def __init__(self, data=None):
            data = data or {}
            data.update({"details": "The server refuses to brew coffee because it is a teapot."})
            super().__init__(418, "im_a_teapot", data)

    class Too_Many_Requests_429(Response):
        def __init__(self, data=None):
            super().__init__(429, "too_many_requests", data)

    class Unavailable_For_Legal_Reasons_451(Response): # gotta catch em all.
        def __init__(self, details="The requested resource is unavailable due to legal reasons.", data=None):
            data = data or {}
            data.update({"details": details})
            super().__init__(451, "unavailable_for_legal_reasons", data)

    # 5** Server Errors
    class Internal_Server_Error_500(Response):
        def __init__(self, details="An unexpected error occurred. Try again later.", data=None):
            data = data or {}
            data.update({"details": details})
            super().__init__(500, "internal_server_error", data)
    
    resps = {
        200: OK_200,
        201: Created_201,
        202: Accepted_202,
        301: Moved_Permanently_301,
        302: Found_302,
        307: Temporary_Redirect_307,
        308: Permanent_Redirect_308,
        400: Bad_Request_400,
        401: Unauthorized_401,
        403: Forbidden_403,
        404: Not_Found_404,
        418: Im_A_Teapot_418,
        429: Too_Many_Requests_429,
        451: Unavailable_For_Legal_Reasons_451,
        500: Internal_Server_Error_500
    }
    
    def get(code: int, *args):
        try:   
            return Responses.resps[code](*args)
        except KeyError:
            return Response(500, "internal_server_error", {"details": "Invalid response code requested."})