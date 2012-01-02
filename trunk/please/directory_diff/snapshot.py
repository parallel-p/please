import os


class Snapshot:    
    
    """
    Description:
    This class represents a snapshot of a directory and all child directories and files.
    
    snapshot = Snapshot("path/to/dir")
    
    Snapshot.get_changes(old_snapshot, new_snapshot)
    output: [ ["new_dir"], ["new_file.txt", "/new_dir/new_file.txt"] ]
    (it returns list of absolute full paths from root to appeared files and directories )
    """
    
    def __init__(self, dir=os.getcwd(), dirs_to_ignore=[], recursive=True, files_to_ignore=[]):
        
        """
        dirs_to_ignore - an optional parameter that allows to configure the directories that are ignored by
        the Snapshot
        
        recursive - an optional parameter that  defines whether Snapshot needs to be looking for files recursively.       
        """
        
        if not os.path.isabs(dir):
            dir=os.path.join(os.getcwd(), dir)
        
        # This will probably be removed on 21.12.2012
        if ".svn" not in dirs_to_ignore:
            dirs_to_ignore.append(".svn")
        
        self.items_list = [[], []]
        
        if not recursive:
            self.__walk(False, dir, dirs_to_ignore, files_to_ignore)            
        else:      
            self.__walk(True, dir, dirs_to_ignore, files_to_ignore)
                    
    def __str__(self):
        return str('\n'.join(self.items_list))
    
    def __walk(self, topdown, dir, dirs_to_ignore, files_to_ignore):
        for root, dirs, files in os.walk(dir, topdown):
                for dr in dirs: 
                    if dr not in dirs_to_ignore:
                        self.items_list[0].append(os.path.join(root, dr))
                for file in files:
                    if file not in files_to_ignore:
                        self.items_list[1].append(os.path.join(root, file)) 

def get_changes(old_snapshot, new_snapshot):
    
    """
    This static method returns all the changes within files/directories that occurred in new snapshot
    compared to old snapshot.
    """
    
    # Get a set of all matching files
    matches_files = set(old_snapshot.items_list[1]) & set(new_snapshot.items_list[1])
    matches_dirs = set(old_snapshot.items_list[0]) & set(new_snapshot.items_list[0])
    changes = [[], []]
    
    # Get files and dirs that have been added
    
    for element in new_snapshot.items_list[1]:
        if element not in matches_files:
            changes[1].append(element)    
    
    for element in new_snapshot.items_list[0]:
        if element not in matches_dirs:
            changes[0].append(element)
    
    return changes

