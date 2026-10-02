import json
from os import path
import traceback
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request

from issues.models import Reporter

# Create your views here.


def _open_file_to_read(filename):
    if filename not in ("reporters", "issues"):
        raise ValueError("No file exists")

    file_path = path.join(path.dirname(__file__), "files", f"{filename}.json")

    with open(file_path, "r") as file:
        return json.load(file)


def _open_file_to_write(filename, data):
    if filename not in ("reporters", "issues"):
        raise ValueError("No file exists")

    file_path = path.join(path.dirname(__file__), "files", f"{filename}.json")

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def create_reporter(req: Request):
    body = req.data
    missing = [f for f in ("name", "email", "team") if f not in body]
    if missing:
        return Response(
            {"error": f"Missing fields: {', '.join(missing)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    reportersList = _open_file_to_read("reporters")
    next_id = max((r["id"] for r in reportersList), default=0) + 1

    reporter = Reporter(next_id, body["name"], body["email"], body["team"])
    try:
        reporter.validate()
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    reportersList.append(reporter.to_dict())
    _open_file_to_write("reporters", reportersList)

    return Response(
        {"message": "created", "data": reporter.to_dict()},
        status=status.HTTP_201_CREATED,
    )


def list_reporters(req: Request):

    reportersList = _open_file_to_read("reporters")
    return Response(
        {"success": "true", "data": reportersList}, status=status.HTTP_200_OK
    )


def get_reporter(req: Request, id: str):
    try:
        reporter_id = int(id)
    except ValueError:
        return Response(
            {"error": "id must be an integer"}, status=status.HTTP_400_BAD_REQUEST
        )

    reportersList = _open_file_to_read("reporters")
    reporter = next((r for r in reportersList if r["id"] == reporter_id), None)

    if reporter is None:
        return Response(
            {"error": "Reporter does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    return Response({"message": "ok", "data": reporter}, status=status.HTTP_200_OK)


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
