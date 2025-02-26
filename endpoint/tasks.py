# your_app/tasks.py
from django.db.models import F, ExpressionWrapper, FloatField
from django.db import transaction
from typing import Generator
from rest_framework.reverse import reverse
import os
from celery import shared_task
import requests
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout, TooManyRedirects

from .models import Task, Company, CaibaoFile, TaskStatus, OCREndpoint
from django.conf import settings
from django.db.models import Max
import logging

from utils.utils import get_task_id
logger = logging.getLogger(__name__)



def get_files_to_submit():
    # Get all files that have not been submitted
    Company.objects.joined()
    files = CaibaoFile.objects.filter(task_id__isnull=True)
    return files


def get_caibao_files(limit=10) -> Generator[CaibaoFile, None, None]:

    # Step 1: Identify the company with the higher priority and code
    highest_priority_companies = (
        Company.objects.all().order_by("code")
    )
    for highest_priority_company in highest_priority_companies:
        logger.debug(f'running for company {highest_priority_company}')

        # Step 2: Retrieve CaibaoFile records for this company where the related Task is null
        caibao_files = CaibaoFile.objects.filter(
            company=highest_priority_company, tasks__isnull=True
        ).order_by("created_at")[:limit]

        # Step 3: Yield each CaibaoFile record
        for caibao_file in caibao_files:
            logger.debug(f"yielding caibao {caibao_file}")
            yield caibao_file


def get_call_back_url():
    callback_url = reverse("task-status-update")
    return f"http://{settings.SITE_DOMAIN}{callback_url}"



def get_available_endpoint():
    endpoint = OCREndpoint.objects.filter(current_load__lt=F('capacity')).annotate(load_ratio=ExpressionWrapper(
            F('current_load') * 1.0 / F('capacity'), 
            output_field=FloatField()
        )).order_by('load_ratio').first()
    return endpoint

@shared_task
def submit_ocr_task(limit=10):
    logger.debug("start submit ocr task")
    tasks_created = []
    for caibao_file in get_caibao_files(limit):
        
        try:
            with transaction.atomic():
                
                task_id = get_task_id(caibao_file.hash_digest)
                params = {"taskId": task_id, "callback": get_call_back_url(), "async": True, "outformat": "md"}
                files = {
                    "file": (
                        os.sep.join(caibao_file.file_path.split(os.sep)[-2:]),
                        open(caibao_file.file_path, "rb"),
                    ),
                }
                logger.info(f'{caibao_file.file_path} submit, payload {params}')
                
                
                ocr_endpoint = get_available_endpoint()
                if not ocr_endpoint:
                    logger.warning("No ocr endpoint available at this time")
                    break
                
                try:
                    response = requests.post(ocr_endpoint.url, params=params, files=files)
                    
                    response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
                    data = response.json()
                    logger.info(data)
                    match data['status']:
                        case 'create' | 'waitting' | 'running' | 'success' | 'existed':
                            task, created = Task.objects.update_or_create(
                                task_id=task_id,
                                source_file=caibao_file,
                                endpoint=ocr_endpoint,
                                defaults={
                                    "status": TaskStatus.RUNNING,
                                    "message": data.get("message", ""),
                                    "biz_type": data.get("bizType", ""),
                                    "file_name": data.get("fileName", ""),
                                },
                            )
                            tasks_created.append(task)
                            logger.info(f'task {task} ' + ('created' if created else 'updated'))
                            ocr_endpoint.current_load += 1
                            ocr_endpoint.save()
                            if ocr_endpoint.current_load > ocr_endpoint.capacity:
                                logger.warning("No ocr endpoint available at this time")
                                break
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

        except Exception as e:
            logger.exception(e)

    logger.info(f'submit ocr task existing, {len(tasks_created)} tasks created')