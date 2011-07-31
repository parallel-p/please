import glob
import os
import shutil
import sys
import logging
from distutils.core import setup
from please.utils import platform_detector
     
def make_dir(dirr):
     if not(os.path.exists(dirr)):
          os.mkdir(dirr)
          logger.info("Make dir: "+dirr)

def copy_file(src,dst):
     logger.info("Copy file "+src+" in "+dst)
     shutil.copyfile(src, dst)

def delete_garbage():
     logger.info("Deleting dir: build")
     shutil.rmtree("build")


logger = logging.getLogger("Installer")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


if len(sys.argv) == 3 :
     path = sys.argv[2]
else:
     system = platform_detector.get_platform()
     print(system)
     if   system[0] == "Windows":
          path = os.path.join("C://Program Files","Please")
          make_dir(path)
          copy_file("please.py",os.path.join(path, "please.py"))
     elif system[0] == 'Linux':
          path = os.path.join("","usr","bin","please")
          make_dir(path)
          copy_file("please.py",os.path.join(path, "please"))
     elif system[0] == 'Darwin':
          path = os.path.join("/Application","Please")
          make_dir(path)
          copy_file("please.py",os.path.join(path, "please.py"))
     else:
          print("Your platform is unsupported")
          exit()
     
logger.info("Copying finished!")
logger.info("Setup library Please in Python")

setup(name        = 'Please',
      version     = '0.1',
      description = '***',
      py_modules = ['please'], 
      packages    = glob.glob("please/*/")
      )

delete_garbage()
logger.info("Installation finished!")