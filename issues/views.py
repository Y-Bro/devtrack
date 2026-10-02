import json
from os import path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.request import Request

from issues.models import (
    CriticalIssue,
    Issue,
    LowPriorityIssue,
    Priority,
    Reporter,
    Status,
    Team,
)

# Create your views here.

ISSUE_CLASSES = {Priority.CRITICAL: CriticalIssue, Priority.LOW: LowPriorityIssue}


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
    next_id = len(reportersList) + 1

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
    body = req.data

    missing = [
        f
        for f in ("title", "description", "status", "priority", "reporter_id")
        if f not in body
    ]

    if missing:
        missing_fields = ", ".join(missing)
        return Response(
            {"error": f"Missing fields: {missing_fields}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    issueList = _open_file_to_read("issues")
    id = len(issueList) + 1

    priority = body["priority"]

    issue_cls = (
        ISSUE_CLASSES.get(priority, Issue) if isinstance(priority, str) else Issue
    )

    issue = issue_cls(
        id,
        body["title"],
        body["description"],
        body["status"],
        priority,
        body["reporter_id"],
    )

    try:
        issue.validate()
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    reporterList = _open_file_to_read("reporters")

    if not any(r["id"] == body["reporter_id"] for r in reporterList):
        return Response(
            {
                "error": f"Reporter with reporter_id: {body["reporter_id"]} does not exist"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    issueList.append(issue.to_dict())

    _open_file_to_write("issues", issueList)

    return Response(
        {"message": f"created: {issue.describe()}", "data": issue.to_dict()},
        status=status.HTTP_201_CREATED,
    )


ENUM_FILTERS = {"status": Status, "priority": Priority}


def _get_filter_error(query_params):
    for name, value in query_params.items():
        if name not in Issue.FILTER_FIELDS:
            allowed = ", ".join(Issue.FILTER_FIELDS)
            return f"Invalid filter '{name}'. Allowed filters: {allowed}"

        if name in ENUM_FILTERS and value not in ENUM_FILTERS[name]:
            return ENUM_FILTERS[name].invalid_message(name, value)

        if name == "reporter_id" and not value.isdigit():
            return f"Invalid reporter_id '{value}'. It must be a positive integer"

    return None


def list_issues(req: Request):
    error = _get_filter_error(req.query_params)
    if error:
        return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

    status_filter = req.query_params.get("status")
    priority_filter = req.query_params.get("priority")
    reporter_filter = req.query_params.get("reporter_id")

    matching_issues = []

    listIssues = _open_file_to_read("issues")

    for issue in listIssues:
        if status_filter is not None and issue["status"] != status_filter:
            continue
        if priority_filter is not None and issue["priority"] != priority_filter:
            continue
        if reporter_filter is not None and issue["reporter_id"] != int(reporter_filter):
            continue
        matching_issues.append(issue)

    return Response(
        {"message": "ok", "data": matching_issues}, status=status.HTTP_200_OK
    )


def get_issue(req: Request, id: int):
    try:
        issue_id = int(id)
    except ValueError:
        return Response(
            {"error": "id must be an integer"}, status=status.HTTP_400_BAD_REQUEST
        )

    issueList = _open_file_to_read("issues")

    issue = next((i for i in issueList if i["id"] == issue_id), None)

    if issue is None:
        return Response(
            {"error": "Issue does not exist"}, status=status.HTTP_404_NOT_FOUND
        )

    return Response({"message": "ok", "data": issue}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def route_reporters_root(req: Request):

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
