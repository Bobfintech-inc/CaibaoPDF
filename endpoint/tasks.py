# your_app/tasks.py

from typing import Generator
from rest_framework.reverse import reverse
import os
from celery import shared_task
import requests
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout, TooManyRedirects

from .models import Task, Company, CaibaoFile, TaskStatus
from django.conf import settings
from django.db.models import Max
import logging

from utils.utils import get_task_id
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


def is_enough_tasks_running(limit):
    return Task.objects.filter(status='running').count() >= limit


@shared_task
def submit_ocr_task(limit=10):
    
    task_cap = 3
    if is_enough_tasks_running(task_cap):
        logger.info(f'{task_cap} tasks already running')
        return
    
    url = os.environ.get("OCR_API_URL").strip()
    tasks_created = []
    for caibao_file in get_caibao_files(limit):
        try:
            task_id = get_task_id()
            params = {"testId": task_id, "callback": get_call_back_url(), "async": True, "outformat": "md"}
            files = {
                "file": (
                    os.sep.join(caibao_file.file_path.split(os.sep)[-2:]),
                    open(caibao_file.file_path, "rb"),
                ),
            }
            logger.info(f'{caibao_file.file_path} submit, payload {params}')

            response = requests.post(url, params=params, files=files)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            logger.info(data)
            match data['status']:
                case 'create' | 'waitting' | 'running' | 'success' | 'existed':
                    task, created = Task.objects.update_or_create(
                        task_id=task_id,
                        source_file=caibao_file,
                        defaults={
                            "status": TaskStatus.RUNNING,
                            "message": data.get("message", ""),
                            "biz_type": data.get("bizType", ""),
                            "file_name": data.get("fileName", ""),
                        },
                    )
                    tasks_created.append(task)
                    logger.info(f'task {task} ' + ('created' if created else 'updated'))
                case 'full':
                    logger.warning(data)
                    break
                case 'error':
                    logger.error(data)
                    break


        except HTTPError as e:
            logger.exception(e)
        except (RequestException, ConnectionError, Timeout, TooManyRedirects) as e:
            logger.exception(e)

    logger.info(f'submit ocr task existing, {len(tasks_created)} tasks created')