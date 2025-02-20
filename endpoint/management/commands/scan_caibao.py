from django.core.management.base import BaseCommand
from endpoint.models import CaibaoFile, Company
from utils.utils import batch_data
import os, logging
import fnmatch
from filehash import FileHash
from tqdm import tqdm
import concurrent.futures

from django.conf import settings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "扫描指定目录下的财报文件并将其添加到数据库，目录结构为 路径/公司/财报.pdf"

    def add_arguments(self, parser):

        parser.add_argument(
            "--include",
            type=str,
            default="*",
            help="Pattern to include files (default: all files)",
        )
        parser.add_argument(
            "--flush",
            type=bool,
            default=True,
            help="Flush the database before adding new files",
        )
        
        parser.add_argument(
            "--batch-size",
            type=int,
            default=100,
            help="The number of files to process in each batch"
        )
        
        parser.add_argument(
            "--max-workers",
            type=int,
            default=8,
            help="The maximum number of workers to use for processing files"
        )


    def iter_caibao_files(self, directory, pattern):
        for root, dirs, files in os.walk(directory):
            filtered_files = [os.path.join(root, file) for file in files]
            for file_path in fnmatch.filter(filtered_files, pattern):
                yield os.path.relpath(file_path, os.getcwd())

    def handle(self, *args, **kwargs):
        # 在此处添加您的数据初始化逻辑
        if kwargs["flush"]:
            CaibaoFile.objects.all().delete()
            Company.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("数据库已清空"))

        # Get the directory and pattern from options
        directory = settings.CAIBAO_ROOT
        pattern = kwargs["include"]

        # Validate the directory path
        if not os.path.isdir(directory):
            raise ValueError(f"The directory '{directory}' does not exist.")

        total_files = len(list(self.iter_caibao_files(directory, pattern)))
        
        for file_paths in batch_data(
            tqdm(
                self.iter_caibao_files(directory, pattern),
                total=total_files,
            ),
            kwargs['batch_size'],
        ):

            with concurrent.futures.ProcessPoolExecutor(max_workers=kwargs['max_workers']) as executor:
                futures = {
                    executor.submit(process_file, file_path): file_path
                    for file_path in file_paths
                }
                for future in concurrent.futures.as_completed(futures):
                    file_path = futures[future]
                    try:
                        future.result()  # Retrieve result or raise exception
                    except Exception as e:
                        self.stderr.write(
                            self.style.ERROR(f"Error processing {file_path}: {e}")
                        )

        self.stdout.write(self.style.SUCCESS("数据库已初始化并添加数据"))

def get_or_create_company(file_path):
    # TODO: adjust for folder pattern
    company_str = file_path.split("/")[-2]
    code, company_name = company_str.split("_")
    return Company.objects.get_or_create(name=company_name, code=code)

def process_file(file_path):
    try:
        file_hasher = FileHash("sha256")
        company,_ = get_or_create_company(file_path)
        hash_digest = file_hasher.hash_file(file_path)
        CaibaoFile(file_path=file_path, hash_digest=hash_digest, company=company).save()
    except Exception as e:
        logger.exception(e)
        # self.stdout.write(self.style.SUCCESS(f"File {file_path} added to the database"))
