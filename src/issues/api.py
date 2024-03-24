from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from issues.models import Issue


def get_issues(request: HttpRequest) -> JsonResponse:
    # issues = Issue.objects.create()
    # issues = Issue.objects.update()
    # issues = Issue.objects.get()
    # issues = Issue.objects.delete()
    # issues = Issue.objects.all()
    issues: list[Issue] = Issue.objects.all()  # noqa

    results: list[dict] = [
        {
            "id": issue.id,
            "title": issue.title,
            "body": issue.body,
            "senior_id": issue.senior_id,
            "junior_id": issue.junior_id,
        }
        for issue in issues
    ]
    return JsonResponse(data={"results": results})


def create_issue(request):
    if request.method == "POST":
        data = request.POST
        try:
            new_issue = Issue.objects.create(  # noqa
                title=data.get("title", ""),
                junior_id=data.get("junior_id", None),
                senior_id=data.get("senior_id", None),
            )
            return JsonResponse({"message": "Задача успешно создана"}, status=201)
        except Exception as e:
            return JsonResponse(
                {"error": f"Ошибка при создании задачи: {str(e)}"}, status=500
            )
    else:
        return JsonResponse({"error": "Метод не разрешен"}, status=405)
