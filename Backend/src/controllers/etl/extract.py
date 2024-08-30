import time
from sqlalchemy.orm import Session

from src.utils.datetime_parser import to_iso
from src.models.user_models.user import User
from src.models.file import File
from src.schemas.enums import ShipheroQueriesEnum, ETLLogProcessessEnum
from src.schemas.etl import ExtractFilters
from src.schemas.file import FileCreate
from src.controllers.file import FileController
from src.controllers.etl.log import ETLLogController
from src.controllers.shiphero.orders import OrdersController


class Extractor:
    """
    Shiphero data extractor
    """

    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user

    def extract(self,
                query: ShipheroQueriesEnum,
                filters: ExtractFilters | None = ExtractFilters()):
        go_to_next_page = True
        page_count = 0
        next_page = ''
        total_complexity = 0
        fails = 0
        request_interval = 10
        items = []
        filename = ''
        log_process = ETLLogProcessessEnum.EXTRACTION
        log_success = True
        log_description = None
        log_file_id = None

        while go_to_next_page:
            print(f'Extracting page {page_count+1}...')
            try:  # Extracting data
                if query == ShipheroQueriesEnum.ORDERS:
                    filename = 'orders_raw.json'
                    controller = OrdersController()
                    data = controller.extract(from_date=filters.from_date,
                                              limit=filters.limit_per_request,
                                              after=next_page)['data']['orders']

                for item in data['data']['edges']:
                    item = item['node']
                    item['extracted_at'] = to_iso()
                    items.append(item)
                total_complexity += data['complexity']
                page_info = data['data']['pageInfo']
                go_to_next_page = page_info['hasNextPage']
                next_page = page_info['endCursor']
                page_count += 1

            except Exception as e:
                fails += 1
                print(f"Extraction failed | Retrying in {request_interval}s")
                print(f'Extraction error: {str(e)}')

            print(f'Page {page_count} extracted.')
            if go_to_next_page:
                print(f'Wating {request_interval}s...')
                time.sleep(request_interval)

        if len(items) == 0:
            log_description = "Extraction completed - No data found"
        else:
            try:  # Saving extracted data in a cloud file
                description = f"Extraction completed - {query} count: {len(items)} | "
                description += f'Total complexity: {total_complexity} ({page_count} requests/{fails} fails)'
                print(description)
                print('Saving data in a file...')
                file_controller = FileController(db=self.db)
                file = FileCreate(filename=filename,
                                  content=items,
                                  description=description)
                data_file: File = file_controller.create(data=file,
                                                         user=self.user)
                log_file_id = data_file.id
                log_description = description
                print('Data successfully saved!')
            except Exception as e:
                log_success = False
                log_description = f'Failed to save data in a file: {str(e)}'

        try:  # Logging the extraction process
            etl_log_controller = ETLLogController(db=self.db, user=self.user)
            etl_log_controller.create_log(process=log_process,
                                          success=log_success,
                                          description=log_description,
                                          file_id=log_file_id)
        except Exception as e:
            print(f'Failed to log | Error: {str(e)}')
