import json
import requests
from sqlalchemy.orm import Session

from src.config.settings import Settings
from src.schemas.file import FileCreate
from src.models.file import File
from src.models.user_models.user import User

settings = Settings()
GITHUB_TOKEN = settings.GITHUB_TOKEN


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
            file = File()
            file.user_id = user.id
            self.db.add(file)
            self.db.flush()
            data.filename = f"{file.id}_{data.filename}"

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
                                     headers=self.headers)
            if response.status_code != 201:
                raise Exception('File storage API failure')
            response = response.json()

            file_detail = list(response['files'].values())[0]
            file.file_id = response['id']
            file.filename = file_detail['filename']
            file.url = file_detail['raw_url']
            if data.description not in [None, ""]:
                file.description = data.description
            self.db.commit()
            self.db.refresh(file)
            return file

        except Exception as e:
            print(e)
            self.db.rollback()
            raise Exception(str(e)) from e

    def read(self, file_id: int):
        """Retrieve a file"""
        try:
            file: File = self.db.query(File).filter(
                File.id == file_id, File.deleted == False).first()
            if not file:
                raise Exception('File not found.')
            response = requests.get(self.url + f'/{file.file_id}',
                                    headers=self.headers)
            if response.status_code != 200:
                raise Exception('File storage API failure')
            return file
        except Exception as e:
            raise Exception(str(e)) from e

    def read_content(self, file_id: int):
        """Read a file's content"""
        try:
            file = self.read(file_id)
            response = requests.get(file.url)
            if response.status_code != 200:
                raise Exception('File storage API failure')

            file_ext = self.get_file_extension(file.filename)
            if file_ext == 'json':
                return response.json()
            return response.text
        except Exception as e:
            raise Exception(str(e)) from e

    def delete(self, file_id: int):
        """Delete a file"""
        try:
            file = self.read(file_id)
            response = requests.delete(self.url + f'/{file.file_id}',
                                       headers=self.headers)
            if response.status_code != 204:
                raise Exception('Failed to delete file')
            file.deleted = True
            self.db.commit()
            self.db.refresh(file)
            return file
        except Exception as e:
            self.db.rollback()
            raise Exception(str(e)) from e
