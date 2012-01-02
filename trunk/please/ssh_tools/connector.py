import psutil
from please.log import logger
from ..invoker.invoker import ExecutionLimits, invoke
from ..utils.platform_detector import get_platform
import os.path

class Connector:
    """
    This class connects to the server using ssh and has two functions:
    1) downloads file from the server.
    2) uploads zip archive to the server and unzips it. 
    also deletes (cleanes) package with the same name as the package in zip archive.
    after all deletes auxiliary files.
    Example:
    
    s = Connector("10.0.0.21", "22", "user", "1")
    s.download_file("/var/lib/ejudge/000001/conf/serve.cfg", "D:\downloaded_file.txt")
    
    s.upload_file("C:\Program Files\file.zip", "/var/lib/ejudge/000001/conf/new_file.zip") 
    # file.zip consists of {new_file\*}. 
    # after this procedure server will contain package "new_file" in the "/var/lib/ejudge/000001/conf/".
    # there will be only those files in "new_file\" that had already been in "file.zip/new_file"
    
    """
    def __init__(self, host, port, login, password): 
        if (port is None):
            port = "22"
        
        self.__platform = get_platform()
        if (get_platform()[0] == 'Windows'):
            self.__connector = WindowsConnector(host, port, login, password)
        else:
            self.__connector = LinuxConnector(host, port, login, password)

    def upload_file(self, source, destination):
        logger.info("Uploading...")
        self.__connector.upload_file(source, destination)
        logger.info("File was uploaded.")
                    
    def download_file(self, source, destination):
        logger.info("Downloading...")
        self.__connector.download_file(source, destination)
        logger.info("File was downloaded.")

    def run_command(self, command):
        logger.info("Connecting to server and running the command")
        self.__connector.run_command(command)
        logger.info("Command executed")
        
class WindowsConnector:
    def __init__(self, host, port, login, password): 
        self.__host = host
        self.__port = port
        self.__login = login
        self.__password = password
       
    def upload_file(self, source, destination, need_to_extract_zip = True):
        limits = ExecutionLimits(real_time=600, memory=128, cpu_time=600) 
        
        handler = psutil.Popen(["pscp", "-P", self.__port, "-pw", self.__password, source, self.__login + "@" + self.__host + ":" + destination])
        result = invoke(handler, limits)
        if need_to_extract_zip:
            splitted = destination.split(".")
            new_dir = os.path.split(destination)[0] + '/' + 'please_tmp/'
            handler = psutil.Popen(["plink", "-P", self.__port, "-pw", self.__password, "-l", self.__login, self.__host, "rm -rf", new_dir, "; unzip", 
                destination,"-d", new_dir, ";rm", destination])
            #result = invoke(handler, limits)

    def download_file(self, source, destination):
        handler = psutil.Popen(["pscp", "-P", self.__port, "-pw", self.__password, self.__login + "@" + self.__host + ":" + source, destination])
        limits = ExecutionLimits(real_time=600, memory=128, cpu_time=600) 
        result = invoke(handler, limits)

    def run_command(self, command):
        handler = psutil.Popen(["plink", "-P", self.__port, "-pw", self.__password, "-l", self.__login, self.__host, command])
        limits = ExecutionLimits(real_time=600, memory=128, cpu_time=600)
        result = invoke(handler, limits)


class LinuxConnector:
    def __init__(self, host, port, login, password):
        self.__host = host
        self.__port = port
        self.__login = login
        self.__password = password
    
    def upload_file(self, source, destination, need_to_extract_zip = True):
        limits = ExecutionLimits(real_time=600, memory=128, cpu_time=600)
        
        handler = psutil.Popen(["scp", "-P", self.__port, source, self.__login + "@" + self.__host + ":" + destination])
        result = invoke(handler, limits)

        if need_to_extract_zip:
            splitted = destination.split(".")
            new_dir = os.path.split(destination)[0] + '/' + 'please_tmp/'
            handler = psutil.Popen(["ssh", "-p", self.__port, "-l", self.__login, self.__host, "rm -rf", new_dir, "; unzip", 
                destination,"-d", new_dir, ";rm", destination])
            result = invoke(handler, limits)
        
    def download_file(self, source, destination):
        handler = psutil.Popen(["scp", "-P", self.__port, self.__login + "@" + self.__host + ":" + source, destination])
        limits = ExecutionLimits(real_time=600, memory=128, cpu_time=600)
        result = invoke(handler, limits)

    def run_command(self, command):
        handler = psutil.Popen(["ssh", "-p", self.__port, "-l", self.__login, self.__host, command])
        limits = ExecutionLimits(real_time=600, memory=128, cpu_time=600)
        result = invoke(handler, limits)
