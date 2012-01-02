import zipfile
import os

class ZIPArchiver:
    '''
    ZIPArchiver is the class witch is support ZIP archivation.
    
    Usage:
    z = ZIPArchiver('filename.zip', 'w')               #open filename.zip in rewrite mode ('a' to append)
    z.add('file1.txt')                                 #add file1.txt
    z.add('file2.txt', 'new_file2_name.txt')           #add file2.txt as new_file2_name.txt
    z.add('file3.txt', 'new_dir1/')                    #add file3.txt in new_dir1 dir
    z.add('file4.txt', 'new_dir2\\')                    #add file4.txt in new_dir2 dir
    z.add('file5.txt', 'new_dir3/new_file5_name.txt')  #add file5.txt in new_dir3 as new_file5_name.txt
    z.add('file6.txt', 'new_dir4\\new_file6_name.txt')  #add file6.txt in new_dir4 as new_file6_name.txt
    z.add('file7.txt', 'new_dir5')                     #add file7.txt as new_dir5
    z.add_folder('dir1')                               #add folder dir1 in root
    z.add_folder('dir2', 'path1')                       #add folder dir2 in path1
    '''
    def add_folder(self, directory, folder = ""):
        for item in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, item)):
                self.sbj.write(os.path.join(directory, item), folder + os.sep + item)
            elif os.path.isdir(os.path.join(directory, item)):
                self.add_folder(os.path.join(directory, item), folder + os.sep + item)
    def __init__(self, path, mod = 'w'):
        self.sbj = zipfile.ZipFile(path, mod)
        self.path = path
    def add(self, src_path, dst_path = './'):
        self.sbj.write(src_path, dst_path + src_path if dst_path[-1] in ['/', '\\'] else dst_path)
    def close(self):
        self.sbj.close()
