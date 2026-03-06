# tasks.py
import requests
from celery import shared_task


@shared_task(bind=True, autoretry_for=(requests.exceptions.RequestException,),
             retry_backoff=30, retry_kwargs={"max_retries": 5})
def call_url_task(self, url, method="GET", payload=None, headers=None, timeout=15):
    """
    Calls a given URL.

    Parameters
    ----------
    url : str
    method : GET | POST
    payload : dict (optional JSON body)
    headers : dict (optional headers)
    timeout : request timeout
    """

    payload = payload or {}
    headers = headers or {}

    if method.upper() == "POST":
        response = requests.post(url, json=payload, headers=headers, timeout=timeout)
    else:
        response = requests.get(url, headers=headers, timeout=timeout)

    return {
        "status_code": response.status_code,
        "response": response.text[:500]
    }