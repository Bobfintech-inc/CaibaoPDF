# your_app/tasks.py

from typing import Generator
from rest_framework.reverse import reverse
import os
from celery import shared_task
import requests
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout, TooManyRedirects

from .models import Task, Company, CaibaoFile
from django.conf import settings
from django.db.models import Max
import logging
logger = logging.getLogger(__name__)


class FakeResponse:

    def json(self):
        return {
            "taskId": "test2",
            "status": "waitting",
            "message": "Task accepted",
            "bizType": "pdf2text",
            "fileName": None,
        }

    @property
    def status_code(self):
        return 200


def fake_invoke(url, params, files):
    return FakeResponse()


def get_files_to_submit():
    # Get all files that have not been submitted
    Company.objects.joined()
    files = CaibaoFile.objects.filter(task_id__isnull=True)
    return files


def get_caibao_files(limit=10) -> Generator[CaibaoFile, None, None]:
    # Step 1: Identify the company with the higher priority and code
    highest_priority_company = (
        Company.objects.all().order_by("code").first()
    )

    if highest_priority_company is None:
        raise ValueError("No companies found")

    # Step 2: Retrieve CaibaoFile records for this company where the related Task is null
    caibao_files = CaibaoFile.objects.filter(
        company=highest_priority_company, tasks__isnull=True
    ).order_by("created_at")[:limit]

    # Step 3: Yield each CaibaoFile record
    for caibao_file in caibao_files:
        yield caibao_file


def get_call_back_url():
    callback_url = reverse("task-status-update")
    return f"http://{settings.SITE_DOMAIN}{callback_url}"


@shared_task
def submit_ocr_task(limit=10):

    url = os.environ.get("OCR_API_URL")
    for caibao_file in get_caibao_files(limit):
        
        
        params = {"testId": caibao_file.hash_digest, "callback": get_call_back_url()}
        files = {
            "file": (
                os.sep.join(caibao_file.file_path.split(os.sep)[-2:]),
                open(caibao_file.file_path, "rb"),
            ),
        }
        logger.info(f'{caibao_file.file_path} submit, payload {params}')
        try:
            response = requests.post(url, params=params, files=files)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            logger.info(data)
            task, created = Task.objects.update_or_create(
                task_id=caibao_file.hash_digest,
                source_file=caibao_file,
                defaults={
                    "status": data["status"],
                    "message": data.get("message", ""),
                    "biz_type": data.get("bizType", ""),
                    "file_name": data.get("fileName", ""),
                },
            )

        except HTTPError as e:
            logger.exception(e)
        except (RequestException, ConnectionError, Timeout, TooManyRedirects) as e:
            logger.exception(e)
