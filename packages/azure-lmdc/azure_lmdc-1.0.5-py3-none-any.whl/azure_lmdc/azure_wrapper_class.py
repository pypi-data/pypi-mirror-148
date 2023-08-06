import os, uuid, sys, io
from typing import Tuple
from os.path import join, split, basename
from azure.storage.filedatalake import DataLakeServiceClient
from azure.core._match_conditions import MatchConditions
from azure.storage.filedatalake._models import ContentSettings
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv
from PIL import Image

class RequestResult:

    def __init__(self, status: bool, success_msg: str, erro: str):
        self.status = status
        self.success_msg = success_msg
        self.erro = erro

    @staticmethod
    def ofOk(success_msg: str = None):
        return RequestResult(True, success_msg, None)

    @staticmethod
    def ofError(err_msg: str = None):
        return RequestResult(False, None, err_msg)

    def printMsg(self):
        if self.status is True:
            print(self.success_msg)
        else:
            print(self.erro)

class Azure_wrapper:

    def __init__(self):
        """
        creates azure wrapper object to interact with the azure file system
        All attributes are received via environment variables
        :return: azure_wrapper objecy
        """

        # usar os.getenv para os atributos

        load_dotenv()

        # credenciais
        self.account_name = os.getenv("ACCOUNT_NAME")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.tenant_id = os.getenv("TENANT_ID")

        self.file_system_name = os.getenv("FILE_SYSTEM_NAME")
        self.__root = os.getenv("DIR_NAME")

        self.initialize_storage_account_ad()

    def get_root(self) -> str:
        """
        returns string containing the root directory of the file system

        :return: root of the file system as string
        """

        return self.__root

    def initialize_storage_account_ad(self) -> None:
        """
        initializes the connection with azure as a service client

        :return: None
        """
        try:
            global service_client

            credential = ClientSecretCredential(self.tenant_id, self.client_id, self.client_secret)

            service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
                "https", self.account_name), credential=credential)

        except Exception as e:
            print(e)

    def exist_path(self, path: str) -> bool:
        """
        checks the existence of a directory. Must be a full path
        :param path: full path of the directory to check if exists
        :return: true if directory exists, else returns false
        """
        try:

            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)

            full_path = join(self.__root, path)

            return file_system_client.get_directory_client(full_path).exists()

        except Exception as e:
            print(e)
            return False

    def upload(self, local_path: str, azure_path: str) -> RequestResult:
        """
        Uploads local file to azure with a specified name

        Parameters:
        
        local_path: (str)
            full path name of local file that will be uploaded
        azure_path: (str)
            full path name of the file when uploaded. Can be the same name of the local file
        
        Return:
            
        RequestResult: (RequestResult)
            RequestResult object created to identify success or failure of the upload operation

        """

        try:
            path_azure_base = os.path.split(azure_path)[0]
            if self.exist_path(path_azure_base) is False:
                return RequestResult.ofError(err_msg= f"path {path_azure_base} does not exist. Check full path.")

            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)

            dir_path = self.__root

            if path_azure_base != "":
                dir_path = join(self.__root, path_azure_base)

            directory_client = file_system_client.get_directory_client(dir_path)

            file_client = directory_client.get_file_client(basename(azure_path))

            local_file = open(local_path, 'rb')

            file_contents = local_file.read()

            file_client.upload_data(file_contents, overwrite=True)
            return RequestResult.ofOk("File uploaded")

        except Exception as e:
            print(e)
            return RequestResult.ofError(err_msg=f"upload local file {local_file} to {azure_path} Failed.")

    def download(self, azure_file_path: str, local_save_path: str = os.getcwd()) -> Tuple[str, RequestResult]:
        """
        downloads uploaded file to local machine

        Parameters:

        azure_file_path: (str)
            full path name of the uploaded file
        local_save_path: (str)
            full directory path, where the file will be downloaded
        
        Return:

            Tuple(local_file_name, ret2)

            local_file_name: (str)
                Full path name of the file which was to be downloaded
            RequestResult: (RequestResult)
                RequestResult object created to identify success or failure of the download operation
            
        """

        try:
            path_base_azure, azure_file_name = os.path.split(azure_file_path)
            if self.exist_path(path_base_azure) is False:
                return None, RequestResult.ofError(err_msg= f"File {azure_file_path} does not exist. Check full path.")

            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)

            dir_path = self.__root

            if path_base_azure != "":
                dir_path = join(self.__root, path_base_azure)

            directory_client = file_system_client.get_directory_client(dir_path)

            local_file_full_path = os.path.join(local_save_path, azure_file_name)
            local_file = open(local_file_full_path, 'wb')

            file_client = directory_client.get_file_client(basename(azure_file_path))

            download = file_client.download_file()

            downloaded_bytes = download.readall()

            local_file.write(downloaded_bytes)

            local_file.close()

            return local_file_full_path, RequestResult.ofOk("File downloaded")

        except Exception as e:
            print(e)
            return None, RequestResult.ofError(err_msg= f"Download File {azure_file_path} Failed.")

    def read_image(self, azure_file_path: str):
        """
        Reads an uploaded image file

        Parameters:

        azure_file_path: (str)
            full path name to the uploaded image file
        :return: Pillow.Image object
        """
        try:

            path_base_azure = os.path.split(azure_file_path)[0]
            if self.exist_path(path_base_azure) is False:
                return None, RequestResult.ofError(err_msg= f"File {azure_file_path} does not exist. Check full path.")

            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)

            dir_path = self.__root

            if path_base_azure != "":
                dir_path = join(self.__root, path_base_azure)

            directory_client = file_system_client.get_directory_client(dir_path)

            file_client = directory_client.get_file_client(basename(azure_file_path))

            download = file_client.download_file()
            downloaded_bytes = download.readall()

            img = Image.open(io.BytesIO(downloaded_bytes))

            return img, RequestResult.ofOk(f"Image file: {azure_file_path} read")

        except Exception as e:
            print(e)
            return None, RequestResult.ofError(err_msg= f"Could not read image File {azure_file_path}.")

    def read_txt(self, azure_file_path: str):
        """
        Read a text file from azure

        Parameters:
        
        azure_file_path: (str)
            full path name of the uploaded file

        Return:
        
        file_content: (str)
            string containing all lines of the file

        """
        
        try:
            path_base_azure = os.path.split(azure_file_path)[0]
            if self.exist_path(path_base_azure) is False:
                return None, RequestResult.ofError(err_msg= f"File {azure_file_path} does not exist. Check full path.")

            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)

            dir_path = self.__root

            if path_base_azure != "":
                dir_path = join(self.__root, path_base_azure)

            directory_client = file_system_client.get_directory_client(dir_path)

            file_client = directory_client.get_file_client(basename(azure_file_path))

            download = file_client.download_file()
            downloaded_bytes = download.readall()
            file_content = downloaded_bytes.decode("utf-8")

            return file_content, RequestResult.ofOk(f"Image file: {azure_file_path} read")

        except Exception as e:
            print(e)
            return None, RequestResult.ofError(err_msg= f"Could not read image File {azure_file_path}.")

    def mkdir(self, new_dir_name: str) -> None:
        """
        creates a new directory inside specified directory
        :param new_dir_name: name of the new directory
        :return: None
        """
        try:

            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)

            file_system_client.create_directory(join(self.__root, new_dir_name))

        except Exception as e:
            print(e)

    def glob(self, dir_name: str, recursive: bool=True) -> None:
        """
        list all contents in a directory, directories and files, in a generator, can be recursive or not

        Parameters:
        
        dir_name: (str)
            full path name of the directory
        recursive: (bool)
            traverse through directories within the root directory if True. Else, just list the contents of the root

        Return:

        dir_contents: (List)
            list with the contents (recursive or not) of the root directory
        
        """
        try:
            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)

            dir_contents_generator = file_system_client.get_paths(path=dir_name, recursive=recursive)

            dir_contents = [i for i in dir_contents_generator]

            return dir_contents

        except Exception as e:
            print(e)

    def delete_directory(self, dir_name: str) -> None:
        """
        deletes the specified directory and all contents within
        :param dir_name: full path name of the directory
        :return: None
        """
        try:
            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)
            directory_client = file_system_client.get_directory_client(join(self.__root, dir_name))

            directory_client.delete_directory()
        except Exception as e:
            print(e)

    def rename_directory(self, azure_dir_name: str, azure_new_dir_name: str) -> None:
        """
        chances the name of the specified directory
        :param azure_dir_name: current full path name of the directory
        :param azure_new_dir_name: new full name of the directory
        :return:
        """
        try:
            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)
            directory_client = file_system_client.get_directory_client(join(self.__root, azure_dir_name))

            directory_client.rename_directory(new_name=directory_client.file_system_name + '/' + join(self.__root, azure_new_dir_name))

        except Exception as e:
            print(e)

    def move_directory(self, azure_path: str, azure_move_path: str) -> None:
        """
        moves a directory inside to a directory
        :param azure_path: full path name of the directory which wants to be moved
        :param azure_move_path: full path name of the directory which will receive the other directory
        :return: None
        """
        new_dir_path = join(azure_move_path, azure_path)
        self.rename_directory(azure_path, new_dir_path)

    def exist_file(self, azure_file_path: str) -> bool:
        """
        checks the existence of a file
        :param azure_file_path: full path name of the file
        :return: true if file exists else returns false
        """

        try:
            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)
            
            dir_path = self.__root
            path_azure_base = split(azure_file_path)[0]

            if path_azure_base != "":
                dir_path = join(self.__root, path_azure_base)

            directory_client = file_system_client.get_directory_client(dir_path)
            file_client = directory_client.get_file_client(basename(azure_file_path))
            return file_client.exists()
        
        except Exception as e:
            print(e)
            return False
    
    def delete_file(self, azure_file_path: str) -> None:
        """
        deletes a file
        :param azure_file_path: full path name of the file
        :return: None
        """
        try:
            file_system_client = service_client.get_file_system_client(file_system=self.file_system_name)

            dir_path = self.__root
            path_azure_base = split(azure_file_path)[0]

            if path_azure_base != "":
                dir_path = join(self.__root, path_azure_base)

            directory_client = file_system_client.get_directory_client(dir_path)
            file_client = directory_client.get_file_client(basename(azure_file_path))
            file_client.delete_file()

        except Exception as e:
            print(e)
