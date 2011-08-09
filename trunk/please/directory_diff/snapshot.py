import os


class Snapshot:    
    
    """
    Description:
    This class represents a snapshot of a directory and all child directories and files.
    
    snapshot = Snapshot("path/to/dir")
    
    Snapshot.get_changes(old_snapshot, new_snapshot)
    output: [ "new_file.txt", "/new_dir/new_file.txt" ]
    (it returns list of full paths from root to appeared files and directories )
    """
    
    def __init__(self, dir=None, dirs_to_ignore=None, recursive=True):
        
        """
        dirs_to_ignore - an optional parameter that allows to configure the directories that are ignored by
        the Snapshot
        
        recursive - an optional parameter that  defines whether Snapshot needs to be looking for files recursively.       
        """
        
        if(dir == None):
            dir = os.getcwd()
        
        # This will probably be removed on 21.12.2012
        if dirs_to_ignore is None:
            dirs_to_ignore = [".svn"]
        else:
            dirs_to_ignore.append(".svn")
        
        self.items_list = []        
        
        if not recursive:             
            # Not recursive, just get the list of files and dirs         
            self.items_list = os.listdir(dir)     
            self.__ignore_dir(dirs_to_ignore, self.items_list)        
            # Append file's directory to the file path
            self.items_list = [os.path.join(dir, item) for item in self.items_list]            
        else:      
            # Recursive, loop through all files via os.walk type: generator with tuples   
            # Convert os.walk(dir) result (generator with tuples (root, sub_folders, files)) to a list of dirs and a list of files         
            lst = [(root, sub_folders, files) for root, sub_folders, files in os.walk(dir)]
            for root, sub_folders, files in lst:
                self.__ignore_dir(dirs_to_ignore, sub_folders)   
                # Append the directory         
                self.items_list.append(root)
                
                for file in files:
                    # Get the actual file path by joining the dir path and the file name: ("root/dir", [], "a.txt") => "root/dir/a.txt"
                    file_path = os.path.join(root, file)
                    # Append the file
                    self.items_list.append(file_path)
        
     
    def __ignore_dir(self, dirs_to_ignore, sub_folders): 
        """ Removes all files and folders that are inside all of the directories to ignore."""
        for dir_to_ignore in dirs_to_ignore:
            if dir_to_ignore in sub_folders:
                sub_folders.remove(dir_to_ignore)

    def __str__(self):
        return str('\n'.join(self.items_list))

def get_changes(old_snapshot, new_snapshot):
    
    """
    This static method returns all the changes within files/directories that occurred in new snapshot
    compared to old snapshot.
    """
    
    # Get a set of all matching files
    matches = set(old_snapshot.items_list) & set(new_snapshot.items_list)
    
    # Now find the files that changed
    changes = []
    
    # Get files that have been added
    for element in new_snapshot.items_list:
        if element not in matches:
            changes.append(element)    

    # Get files that have been removed            
    #for element in old_snapshot.items_list:
    #    if element not in matches:
    #        changes.append(element) 
    
    return changes

