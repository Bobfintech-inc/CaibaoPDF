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


def get_caibao_files(limit=0) -> Generator[CaibaoFile, None, None]:

    # Step 1: Identify the company with the higher priority and code
    highest_priority_companies = (
        Company.objects.all()
    )
    for highest_priority_company in highest_priority_companies:
        logger.debug(f'running for company {highest_priority_company}')

        if limit > 0:
            # Step 2: Retrieve CaibaoFile records for this company where the related Task is null
            caibao_files = CaibaoFile.objects.filter(
                company=highest_priority_company, tasks__isnull=True
            ).order_by("created_at")[:limit]
        else:
            caibao_files = CaibaoFile.objects.filter(
                company=highest_priority_company, tasks__isnull=True
            ).order_by("created_at")

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
