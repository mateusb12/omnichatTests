import json
from flask import Response


def createResponseWithAntiCorsHeaders(data):
    dump_response = json.dumps(data)
    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods": "*"
    }
    return Response(dump_response, headers=response_headers)