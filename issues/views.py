from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request

from issues.models import Reporter

# Create your views here.


def create_reporter(req: Request):
    report = Reporter()
    return Response({"message": "created"}, status=status.HTTP_201_CREATED)


def list_reporters(req: Request):
    return Response({"message": "ok"}, status=status.HTTP_200_OK)


def get_reporter(req: Request, id: int):
    return Response({"message": "ok", "id": id}, status=status.HTTP_200_OK)


def create_issue(req: Request):
    return Response({"message": "created"}, status=status.HTTP_201_CREATED)


def list_issues(req: Request):
    return Response({"message": "ok"}, status=status.HTTP_200_OK)


def get_issue(req: Request, id: int):
    return Response({"message": "ok"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_issue_by_status(req: Request):
    return Response({"message": "ok"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def route_reporters_root(req: Request):

    print(req.query_params)

    method = req.method
    if method == "POST":
        return create_reporter(req)
    if "id" in req.query_params:
        return get_reporter(req, req.query_params["id"])
    return list_reporters(req)


@api_view(["GET", "POST"])
def route_issues_root(req: Request):
    method = req.method
    if method == "POST":
        return create_issue(req)
    if "id" in req.query_params:
        return get_issue(req, req.query_params["id"])
    return list_issues(req)
