import json
import requests
from sqlalchemy.orm import Session

from src.config.settings import Settings
from src.schemas.file import FileCreate
from src.models.file import File
from src.models.user_models.user import User
from src.utils.id_generator import generate_id

settings = Settings()
GITHUB_TOKEN = settings.GITHUB_TOKEN
TIMEOUT = 10


class FileController:
    """
    Manage data files
    """

    def __init__(self, db: Session):
        self.db = db
        self.headers = {
            'Content-Type': 'application/vnd.github+json',
            'Authorization': f'Bearer {GITHUB_TOKEN}',
        }
        self.url = 'https://api.github.com/gists'

    def get_file_extension(self, filename: str):
        """Get file extension from filename"""
        return filename.split('.')[-1]

    def create(self, data: FileCreate, user: User):
        """Save data to file"""
        try:
            file_ext = self.get_file_extension(data.filename)
            if file_ext == 'json':
                data.content = json.dumps(data.content)
            payload = {
                "description": data.description,
                'public': False,
                'files': {
                    data.filename: {"content": data.content}
                }
            }
            response = requests.post(self.url,
                                     data=json.dumps(payload),
                                     headers=self.headers,
                                     timeout=TIMEOUT)
            if response.status_code != 201:
                raise Exception('File storage API failure')
            response = response.json()

            file_detail = list(response['files'].values())[0]
            file = File(file_id=response['id'],
                        filename=file_detail['filename'],
                        url=file_detail['raw_url'],
                        description=data.description)
            file.id = generate_id(self.db, 'ff', File)
            file.user_id = user.id
            self.db.add(file)
            self.db.commit()
            self.db.refresh(file)
            return file

        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e

    def read(self, file_id: str):
        """Retrieve a file"""
        try:
            file: File = self.db.query(File).filter(
                File.id == file_id, File.deleted == False).first()
            if not file:
                raise Exception('File not found.')
            response = requests.get(self.url + f'/{file.file_id}',
                                    headers=self.headers,
                                    timeout=TIMEOUT)
            if response.status_code != 200:
                raise Exception('File storage API failure')
            return file
        except Exception as e:
            raise Exception(str(e)) from e

    def read_content(self, file_id: str):
        """Read a file's content"""
        try:
            file = self.read(file_id)
            response = requests.get(file.url, timeout=TIMEOUT)
            if response.status_code != 200:
                raise Exception('File storage API failure')

            file_ext = self.get_file_extension(file.filename)
            if file_ext == 'json':
                return response.json()
            return response.text
        except Exception as e:
            raise Exception(str(e)) from e

    def delete(self, file_id: str):
        """Delete a file"""
        try:
            file = self.read(file_id)
            response = requests.delete(self.url + f'/{file.file_id}',
                                       headers=self.headers,
                                       timeout=TIMEOUT)
            if response.status_code != 204:
                raise Exception('Failed to delete file')
            file.deleted = True
            self.db.commit()
            self.db.refresh(file)
            return file
        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e
