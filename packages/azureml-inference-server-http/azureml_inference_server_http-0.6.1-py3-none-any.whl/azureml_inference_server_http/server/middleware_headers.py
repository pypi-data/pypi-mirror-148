import os
import uuid

from flask import request


class WSGIRequest(object):
    def __init__(self, inner_app):
        if not inner_app:
            raise Exception("WSGI application was required but not provided")
        self._inner_app = inner_app

    def __call__(self, environ, start_response):
        """Sets request id and server version in header before returning to client"""
        request_id = environ.get("HTTP_X_MS_REQUEST_ID", str(uuid.uuid4()))
        x_request_id = environ.get("HTTP_X_REQUEST_ID", request_id)
        x_client_request_id = environ.get("HTTP_X_CLIENT_REQUEST_ID")
        server_ver = os.environ.get("HTTP_X_MS_SERVER_VERSION", "")
        environ["REQUEST_ID"] = request_id

        def request_start_response(status_string, headers_array, exc_info=None):
            if server_ver:
                headers_array.append(("x-ms-server-version", server_ver))
            headers_array.append(("x-ms-request-id", request_id))
            headers_array.append(("x-request-id", x_request_id))
            if x_client_request_id:
                headers_array.append(("x-client-request-id", x_client_request_id))
            # Office services have their own tracing field 'TraceId', we need to support it.
            if "TraceId" in request.headers:
                headers_array.append(("TraceId", request.headers["TraceId"]))
            start_response(status_string, headers_array, exc_info)

        return self._inner_app(environ, request_start_response)
