from zipfile import ZipFile
from colorama import Fore
import requests
import shutil
import os
import json


class InterfaceInstaller:

    def __init__(self, path = "", project_name = ""):
        self.__url = self.getLastRelease()
        self.__file_path = os.path.join(path, project_name + '.zip')
        self.__global_path = path
        self.__project_name = project_name

    def getLastRelease(self):

        release = requests.get("https://api.github.com/repos/rizki4106/interface/releases").content
        release = json.loads(release.decode("utf-8"))
        url =  "https://github.com/rizki4106/interface/archive/refs/tags/" + release[0]['zipball_url'].split("/")[-1] + ".zip"

        return url

    def downloadSourceZip(self, url = ""):

        print(Fore.GREEN + "downloading souce code....")

        headers = {}
        file = requests.get(self.__url, headers=headers)

        with open(self.__file_path, "wb") as source:
            source.write(file.content)
            source.close()
        
        return file.status_code == 200

    def unzipFile(self):
        
        print(Fore.GREEN + "extracting files...")

        # remove folder if already exists
        if os.path.exists(self.__file_path.replace(".zip", "")):
            shutil.rmtree(self.__file_path.replace(".zip", ""))
        
        with ZipFile(self.__file_path, 'r') as zip:
            zip.extractall()
            zip.close()

        # rename file to what user want
        filename = os.path.join(self.__global_path, 'interface-' + self.__url.split("/")[-1].split(".zip")[0]) 
        if os.path.exists(filename):
            os.rename(filename, self.__file_path.replace(".zip", ""))
        
        return self.__project_name

    def deleteRemoteRepository(self, path):

        print(Fore.RED + "delete origin...")

        git_dir = os.path.join(self.__global_path, path, ".git")
        if os.path.exists(git_dir):
            os.remove(git_dir)
            return True

        return False

    def deleteZip(self):

        print(Fore.RED + "delete zip file")

        project_path = os.path.join(self.__global_path, self.__project_name + ".zip")
        if os.path.exists(project_path):
            os.remove(project_path)
            return True
        return False

    def run(self):

        last_release = self.getLastRelease()
        download = self.downloadSourceZip(last_release)

        if download:    
            self.deleteRemoteRepository(self.unzipFile() + '/.git')
            self.deleteZip()
            print(Fore.GREEN + "done...")
            print(Fore.BLUE + "\n{}\n\ncd {} \npython3 app.py\n".format("-"*10,self.__project_name))
            print(Fore.BLUE + "\n\nor run with docker compose\n\ncd {}\ndocker-compose up\n\n".format(self.__project_name))
        else:
            print(Fore.RED + "download failed, please check your network...")