import os
import time
import logging
import signal
import sys
from contextlib import contextmanager

from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
import requests
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout, TooManyRedirects

from endpoint.models import Task, TaskStatus
from utils.utils import get_task_id
from endpoint.tasks import get_caibao_files, get_call_back_url, get_available_endpoint

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the OCR submission daemon as a long-running process'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.running = True
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=0,
            help='Maximum number of files to process in each iteration',
        )
        parser.add_argument(
            '--sleep-interval',
            type=int,
            default=60,
            help='Time to sleep between iterations (in seconds)',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Increase output verbosity',
        )

    def handle(self, *args, **options):
        limit = options['limit']
        sleep_interval = options['sleep_interval']
        verbose = options['verbose']
        
        if verbose:
            logger.setLevel(logging.DEBUG)
        
        self.stdout.write(self.style.SUCCESS(f'Starting OCR submission daemon (limit={limit}, interval={sleep_interval}s)'))
        
        try:
            self.run_daemon(limit, sleep_interval)
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('OCR submission daemon stopped by user'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'OCR submission daemon crashed: {e}'))
            logger.exception("Fatal error in OCR daemon")
            sys.exit(1)
    
    def handle_shutdown(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self.stdout.write(self.style.WARNING(f'Received signal {signum}, shutting down gracefully...'))
        self.running = False
    
    def sleep_with_interrupt(self, sleep_interval):
        """Sleep for the given interval while still responding to shutdown signals."""
        for _ in range(sleep_interval):
            if not self.running:
                break
            time.sleep(1)
    
    @contextmanager
    def open_file_safely(self, file_path):
        """Safely open and close files to prevent resource leaks."""
        file_obj = None
        try:
            file_obj = open(file_path, "rb")
            yield file_obj
        finally:
            if file_obj:
                file_obj.close()
    
    def process_caibao_file(self, caibao_file, ocr_endpoint):
        """Process a single CaibaoFile for OCR submission."""
        task_id = get_task_id(caibao_file.hash_digest)
        file_name = os.sep.join(caibao_file.file_path.split(os.sep)[-2:])
        
        params = {
            "taskId": task_id, 
            "callback": get_call_back_url(), 
            "async": True, 
            "outformat": settings.OCR_OUTPUT_FORMAT
        }
        
        logger.info(f'Submitting file: {caibao_file.file_path}, payload: {params}')
        
        with self.open_file_safely(caibao_file.file_path) as file_obj:
            files = {"file": (file_name, file_obj)}
            
            try:
                response = requests.post(ocr_endpoint.url, params=params, files=files)
                response.raise_for_status()
                data = response.json()
                logger.info(f"OCR service response: {data}")
                
                if data['status'] in ('create', 'waitting', 'running', 'success', 'existed'):
                    task, created = Task.objects.update_or_create(
                        task_id=task_id,
                        source_file=caibao_file,
                        endpoint=ocr_endpoint,
                        defaults={
                            "status": TaskStatus.RUNNING,
                            "message": data.get("message", ""),
                            "biz_type": data.get("bizType", ""),
                            "file_name": file_name,
                        },
                    )
                    logger.info(f'Task {task} {"created" if created else "updated"}')
                    return task
                elif data['status'] == 'full':
                    logger.warning(f"OCR service is full: {data}")
                    return None
                else:  # 'error' or other status
                    logger.error(f"OCR service error: {data}")
                    return None
                    
            except HTTPError as e:
                logger.exception(f"HTTP error when submitting to OCR service: {e}")
            except (RequestException, ConnectionError, Timeout, TooManyRedirects) as e:
                logger.exception(f"Connection error when submitting to OCR service: {e}")
            
            return None
    
    def file_loop(self, sleep_interval, caibao_file):
        while self.running:
            try:
                # Check for available endpoint first
                ocr_endpoint = get_available_endpoint()
                if not ocr_endpoint:
                    msg = f"No OCR endpoint available, waiting for {sleep_interval} seconds"
                    logger.warning(msg)
                    self.stdout.write(self.style.WARNING(msg))
                    self.sleep_with_interrupt(sleep_interval)
                    continue

                with transaction.atomic():
                    # Recheck endpoint availability for each file
                    ocr_endpoint = get_available_endpoint()
                    if not ocr_endpoint:
                        msg = "OCR endpoint no longer available"
                        logger.warning(msg)
                        self.stdout.write(self.style.WARNING(msg))
                        continue
                    
                    task = self.process_caibao_file(caibao_file, ocr_endpoint)
                    
                    if task:
                        ocr_endpoint.current_load += 1
                        saved_endpoint = ocr_endpoint.save()
                        logger.info(f'endpoint info saved {saved_endpoint}')
                        break
                    else:
                        raise Exception('creating task failed')
                    
                        
            except Exception as e:
                logger.exception(f"Error processing file {caibao_file}: {e}")
                logger.warning(f'retrying file {caibao_file}')
        
        
    def run_daemon(self, limit, sleep_interval):
        """
        Long-running daemon that continuously processes files for OCR submission.
        """

        for caibao_file in get_caibao_files(limit):
            if not self.running:
                logger.info(f'exiting')
                break
            else:
                self.file_loop(sleep_interval, caibao_file)

        self.stdout.write(self.style.SUCCESS("OCR daemon shutdown complete"))