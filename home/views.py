import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import schedule_daily_task

# Create your views here.
@csrf_exempt
def schedule_task_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)
    
    try:
        data = json.loads(request.body)

        name = data["name"]
        task_path = "home.tasks.call_url_task"
        end_point = data.get("endpoint")
        hour = int(data.get("hour", 0))
        minute = int(data.get("minute", 0))
        args = data.get("args", [])
        kwargs = data.get("kwargs", {})
        enabled = data.get("enabled", True)
        timezone = data.get("timezone", "Asia/Qatar")

        task = schedule_daily_task(
            name=name,
            task_path=task_path,
            hour=hour,
            minute=minute,
            args=[end_point],
            kwargs=kwargs,
            enabled=enabled,
            timezone=timezone
        )

        return JsonResponse({
            "status": "scheduled",
            "task_id": task.id,
            "task_name": task.name
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=400)
