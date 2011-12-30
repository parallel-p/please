#!/usr/bin/env python3

class EjudgeFormatter:
    def __init__(self):
        pass
    def put_all():
        raise NotImplementedError
    def remove_all():
        raise NotImplementedError
    def make_backup():
        raise NotImplementedError
    def use_backup():
        raise NotImplementedError
        
class NewEjudgeFormatter(EjudgeFormatter):
    def __init__(self, path_to_archive, destination):
        self.__path_to_archive = path_to_archive
        self.__destination = destination

    def put_all(self):
        pass
    def remove_all(self):
        pass
    def make_backup(self):
        pass
    def use_backup(self):
        pass

