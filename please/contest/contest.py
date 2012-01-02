#!/usr/bin/env python3
# coding=utf-8

import errno, os
from ..package.config import Config
from ..solution_tester.package_config import PackageConfig

class IdMethod:

    class IdException(Exception):
        def __init__( self, id=None ):
            self.__id = id
        def __str__( self ):
            if self.__id is None:
                return "cannot assign id to new problem"
            else:
                return "problem with id '%s' already in contest" % id

    @classmethod
    def default( ids, short ):
        if short not in ids:
            return short
        raise IdException(short)

    @classmethod
    def alpha( ids, short ):
        ids = set(ids)
        # iterate letters from A to Z
        for x in map(chr, range(ord('A'), ord('Z') + 1)):
            if x not in ids:
                return x
        raise IdException()

    @classmethod
    def numeric( ids, short ):
        ids = set(ids)
        id = 1
        while id in ids:
            ids += 1
        return id
    
    methods = {
        'default': default,
        'alpha': alpha,
        'numeric': numeric
    }


class Contest:
    def __init__( self, config_name, ok_if_not_exists = False ):
        try:
            with open(config_name, 'r') as config_file:
                config_data = config_file.readall()
            self.config = Config(config_data)
        except IOError as e:
            if e.errno == errno.ENOENT and ok_if_not_exists:
                self.config = Config("")
            else:
                raise e

        self.__id_method = IdMethod.methods.get(self.config['id_method'], IdMethod.default)
        if not isinstance(self.config['problem'], list):
            self.config['problem'] = []
        self.__problems = self.config['problem']
        self.__dict = {problem['id'] : i for i, problem in enumerate(self.__problems)}

    def problem_add( self, path, id = False ):
        problem_config = PackageConfig.get_config(path)
        if not id:
            id = self.__id_method(self.__dict, problem_config['shortname'])
        config = Config("")
        config['path'] = path
        config['id'] = id
        self.config.set('problem', config, in_list=True)
        self.__dict[id] = len(self.__problems)
        self.__problems.append(config)

    def problem_find( self, path ):
        for problem in self.__problems:
            if problem['path'] == path:
                return problem['id']
        return None

    def problem_remove( self, id ):
        i = self.__dict[id]
        del self.__dict[id]
        del self.__problems[i]
        self.config.delete('problem', i)

    def __contains__( self, id ):
        return id in self.__dict

