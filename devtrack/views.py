from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import Request
from rest_framework.decorators import api_view

# Create your views here.


@api_view(["POST"])
def create_reporter(req: Request):
    return Response({"message": "created"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def list_reporters(req: Request):
    pass


@api_view(["GET"])
def get_reporter(req: Request):
    pass


@api_view(["POST"])
def create_issue(req: Request):
    pass


@api_view(["GET"])
def list_issues(req: Request):
    pass


@api_view(["GET"])
def get_issue(req: Request):
    pass


@api_view(["GET"])
def get_issue_by_status(req: Request):
    pass
