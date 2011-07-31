import os
import time


def create_time_file(root_path):
	"""
	Description:
	This function creates in root folder new system folder (.please),
	that contains a file(time.config), that contains it's creation time 
	"""
	system_folder_path = os.path.join(root_path, ".please")
	os.mkdir(system_folder_path)
	time_file_path = os.path.join(system_folder_path, "time.config")
	
	time_file = open(time_file_path, "w", encoding = 'UTF8')
	time_sec = str(time.time())
	time_file.write(time_sec)
	time_file.close()