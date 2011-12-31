#!/usr/bin/env python3
import os, shutil, time
def make_backup():
    # this function makes backup of hull contest.
    # it makes folder .backup in the root of this contest
    # and puts there an archive with all files (except .backup).
    root = '..'
    backup_folder = os.join(root, '.backup')
    if not os.isdir(backup_folder):
        os.makedir(backup_folder)
    path_to_current_backup_folder = os.path.join(backup_folder, 'tmp')
    os.copytree('..', path_to_current_backup_folder)
    shutil.rmtree(os.path.join(path_to_current_backup_folder, '.backup'))
    current_time = time.localtime()
    archive_name = ("%04d-%02-%02; %02d:%02d:%02d" % (current_time.tm_year(), current_time.tm_mon(), 
                   current_time.tm_mday(), current_time.tm_hour(), current_time.tm_min(), current_time.tm_sec()))
        
    shutil.rmtree(path_to_current_backup_folder)
    
    