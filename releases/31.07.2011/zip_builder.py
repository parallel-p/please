import os
import shutil
import zipfile
import logging
import sys

if  len(sys.argv) <= 1:
     zip_name = "Archve.zip"
else:
     zip_name = sys.argv[1]
     
def make_str(line):
     return os.path.join(*line.split("\\"))

def get_file_name (path):
     path = path.split("\\")
     path = path[len(path)-1]
     return path

def make_dir(dirr):
     if not(os.path.exists(dirr)):
          os.mkdir(dirr)
          logger.info("Make dir: "+dirr)

def copy_dir(src,dst):
     logger.info("Copy "+src+" in "+dst)
     shutil.copytree(src, dst, ignore = shutil.ignore_patterns('*.pyc', '.svn', "_test.py", "testdata"))

def rmfile (file):
     logger.info("Deleting file "+ file)
     os.remove(file)

def add (path,files):
     directory = make_str("archive\\tests"+'\\'+get_file_name(path))
     make_dir(directory)
     for file in files:
          file_name = get_file_name(file)
          shutil.copyfile(make_str(path+"\\"+file), make_str(directory+'\\'+file_name))
          logger.info("Make file: "+directory+'\\'+file_name)

def addinzip (name):
     logger.info("Add file: " + name + " in zipfile")
     filezip.write(name,make_str("archive\\"+name))

def copy_please ():
     make_dir("archive")        
     make_dir(make_str("archive\\tests"))

     for root, dirs, files in os.walk('please'):
          flag = False
          tests_names = []
          for file in files:
               if "_test.py" in file:
                    flag = True
                    tests_names.append(file)
          if flag:
               add (root,tests_names)

     copy_dir("please",make_str("archive\\please"))

def create_zip():    
     for root, dirs, files in os.walk('archive'):
          for file in files:
               path = make_str(root+"\\"+file)
               logger.info("Add file: " + path + " in zipfile")
               filezip.write(path)

     addinzip("please.py")
     addinzip("run_tests.py")
     addinzip("setup.py")
     addinzip("README")

def delete_garbage():
     logger.info("Deleting dir: archive")
     shutil.rmtree("archive")

logger = logging.getLogger("zip_creator")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

copy_please()
logger.info("create zipfile")
filezip = zipfile.ZipFile(zip_name, "w")
create_zip()
delete_garbage()
logger.info("Creating ZIP-file finished!")