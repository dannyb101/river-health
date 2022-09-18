import os
import paramiko
from scp import SCPClient

class FS_SERVER:
    """
    Initalise class, and create SSh connection to remote file server
    Please note the only acceptable folder_names are (must be in all capitals):
    CSO, QUBE, NRFA, DO, BOD+NH3, OUTPUT, IMAGES, DOCS, BOD_GRAPH, NH3_GRAPH
    """
    def __init__(self):
        # Keypair needs to match the same public key given to the server
        self.key = paramiko.RSAKey.from_private_key_file("./app/Connections/fs_server_key/file_storage.keypair.key")
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # IP: this will need to be changed to whatever IP address your file server is located on
        # Username: this is the root username of the instance (E.G. Centos, Debian, Root etc)
        self.client.connect( hostname = "10.72.99.195", username = "centos", pkey = self.key )

    """
    Function to save_file_storage_object_as_csv to remote server
    Please see class for acceptable folder names
    file_name must be unique
    """
    def save_file_storage_object_as_csv(self, *, folder_name: str, file, unique_id):
        # Save CSV with Unique File name to local storage
        filepath = './app/Local_File_Storage/' + folder_name + '/' + file.filename
        file.save(filepath)
        unique_file_name = './app/Local_File_Storage/' + folder_name + '/' + unique_id
        os.rename(filepath, unique_file_name)

        # Send CSV from local storage to remote file server
        scp = SCPClient(self.client.get_transport())
        scp.put(unique_file_name, remote_path='/home/centos/' + folder_name)
        scp.close()

        # Delete local CSV
        self.delete_local_file(folder_name=folder_name, file_name=unique_id)

    """
    Function to convert dataframe to csv to remote server
    Please see class for acceptable folder names
    file_name must be unique
    """
    def save_dataframe_as_csv(self, *, folder_name: str, dataframe, unique_id):
        dataframe.to_csv('./app/Local_File_Storage/' + folder_name + '/' + unique_id)
        # Send CSV from local storage to remote file server
        scp = SCPClient(self.client.get_transport())
        scp.put('./app/Local_File_Storage/' + folder_name + '/' + unique_id, remote_path='/home/centos/' + folder_name)
        scp.close()

        # Delete local CSV
        self.delete_local_file(folder_name=folder_name, file_name=unique_id)

    """
    Function to save file to remote server
    Please see class for acceptable folder names
    file_name must be unique
    """
    def save_local_file_to_remote(self, *, folder_name: str, unique_id):
        scp = SCPClient(self.client.get_transport())
        scp.put('./app/Local_File_Storage/' + folder_name + '/' + unique_id, remote_path='/home/centos/' + folder_name)
        scp.close()

        # Delete local File
        self.delete_local_file(folder_name=folder_name, file_name=unique_id)


    """
    Function which retrieves file from remote server
    Saves file to local storage
    Returns file path to file in local storage
    """
    def get_csv(self, *, folder_name: str, file_name: str):
        scp = SCPClient(self.client.get_transport())
        remote_file_path = '/home/centos/' + folder_name + '/' + file_name
        local_file_path = "./app/Local_File_Storage/" + folder_name + '/' + file_name
        scp.get(remote_file_path, local_file_path)
        scp.close()
        return local_file_path

    """
    Function which retrieves graph from remote server
    Saves graph to templates folder
    Returns file path to file in local storage
    """
    def get_graph(self, *, folder_name: str, file_name: str):
        scp = SCPClient(self.client.get_transport())
        remote_file_path = '/home/centos/' + folder_name + '/' + file_name
        local_file_path = "./app/templates/graph_templates/" + folder_name + '/' + file_name + '.html'
        scp.get(remote_file_path, local_file_path)
        scp.close()
        return local_file_path

    """
    Function which deletes graph from local server
    Please use this after you have used the file in get_csv to avoid storing 
    unnecessary data in the application
    """
    def delete_local_graph(self, *, folder_name: str, file_name: str):
        local_file_path = "./app/templates/graph_templates/" + folder_name + '/' + file_name + '.html'
        os.remove(local_file_path)

    """
    Function which deletes file from remote server
    WARNING: This will permenantely delete file, no way to recover once function is run
    """
    def delete_csv_remote(self, *, folder_name: str, file_name: str):
        self.client.exec_command('rm ' + '/home/centos/' + folder_name + '/' + file_name)

    """
    Function which deletes file from local server
    Please use this after you have used the file in get_csv to avoid storing 
    unnecessary data in the application
    """
    def delete_local_file(self, *, folder_name: str, file_name: str):
        local_file_path = "./app/Local_File_Storage/" + folder_name + '/' + file_name
        os.remove(local_file_path)

    """
    Function which will check whether the file exists on remote
    Returns a boolean
    """
    def check_files_exists_on_remote(self, *, folder_name: str, file_name: str):
        sftp = self.client.open_sftp()
        try:
            if sftp.stat('/home/centos/' + folder_name + '/' + file_name):
                return True
        except:
            return False


