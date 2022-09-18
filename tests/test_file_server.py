import pytest
from app.Connections.fs_server import FS_SERVER
from pathlib import Path
import uuid
from werkzeug.datastructures import FileStorage

# Create session wide connection to file server
@pytest.fixture(scope='session')
def file_server():
    return FS_SERVER()

@pytest.fixture(scope='session')
def uuid():
    uuid = '33e82c6e-a10f-40de-8a30-f2202865ba5f'
    return uuid

@pytest.fixture(scope='session')
def file():     
        # Create mock form data for file
        file_path = "./tests/files/example-cso-spills.csv"

        my_file = FileStorage(
            stream=open(file_path, "rb"),
            filename="cso-spills.csv",
            content_type="text/csv"
        )

        # Add file data to mock form data
        return my_file

def test_save_and_retrieve(file_server, uuid, file):
    """
    GIVEN a in memory csv file
    WHEN function is called
    THEN the file should be saved on the remote server and retrievable via the specified path
    """
    file_server.save_file_storage_object_as_csv(folder_name='CSO', file=file, unique_id=uuid)
    file_server.get_csv(folder_name='CSO', file_name=uuid)
    file_name = Path("./app/Local_File_Storage/CSO/", uuid)
    assert file_name.exists()


def test_delete_remote(file_server, uuid):
    """
    GIVEN a remote file path
    WHEN delete_csv_remote is called on the path
    THEN the file path should no longer be accesible
    """
    file_server.delete_csv_remote(file_name=uuid, folder_name='CSO')
    assert False == file_server.check_files_exists_on_remote(file_name=uuid, folder_name='CSO')
    
def test_delete_local(file_server, uuid):
    """
    GIVEN a local file path
    WHEN delete_csv_local is called on the path
    THEN the file path should no longer be accesible
    """
    file_name = Path("./app/Local_File_Storage/CSO/", uuid)
    file_server.delete_local_file(file_name=uuid, folder_name='CSO')
    if file_name.exists():
        assert False
    else:
        assert True
    