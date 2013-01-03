import os
import hashlib
from ..package import package_config
from ..todo import painter
from .. import globalconfig
from ..template import info_generator
from ..utils import utests
from ..test_config_parser import parser

#TODO: make it nonstatic class
class TodoGenerator:

    @staticmethod
    def __read_md5_values(root_path = '.'):
        md5path = os.path.join(root_path, '.please', 'md5.config')
        if not os.path.exists(md5path):
            info_generator.create_md5_file(root_path)
            
        md5values = {}
        with open(md5path) as md5file:
            for s in md5file:
                resource, md5 = s.strip().split(':')
                md5values[resource] = md5
        return md5values                    

    @staticmethod
    def is_item_modified(item, config):
        md5values = TodoGenerator.__read_md5_values()
        status = TodoGenerator.__get_file_item_status(config, md5values, item)
        return status == "ok"

    @staticmethod
    def get_todo(root_path='.'):
        for item, (internal_status, external_status) in TodoGenerator.__get_internal_status_description(root_path):
            print(painter.__dict__[internal_status]('{} is {}'.format(item, external_status)))
        TodoGenerator.__counter_print(TodoGenerator.generated_tests_count(root_path), ' tests generated')
        TodoGenerator.__counter_print(TodoGenerator.sample_tests_count(root_path),
                      ' samples in tests.config', False)

    @staticmethod
    def generated_tests_count(root_path='.'):
        return len(list(utests.get_tests(os.path.join(root_path, globalconfig.temp_tests_dir))))

    @staticmethod
    def sample_tests_count(root_path='.'):
        return parser.FileTestConfigParser(path=os.path.join(root_path, globalconfig.default_tests_config)).count_by_tag('sample')

    @staticmethod
    def get_status_description(root_path='.'):
        return [(item, external) for item, (internal, external) in TodoGenerator.__get_internal_status_description(root_path)]

    @staticmethod
    def __get_internal_status_description(root_path='.'):
        FILE_ITEMS = ('statement', 'checker', 'description', 'analysis', 'validator', 'main_solution')
        SIMPLE_ITEMS = ('tags', 'name')
        FILE_ITEM_TRANSITION = {
            'ok': 'ok',
            'warning': 'default',
            'error': 'does not exist',
        }
        SIMPLE_ITEM_TRANSITION = {
            'ok': 'ok',
            'warning': 'empty',
            'error': 'does not exist',
        }
        md5values = TodoGenerator.__read_md5_values(root_path)
        config = package_config.PackageConfig.get_config(root_path)
        result = []
        for item in FILE_ITEMS:
            status = TodoGenerator.__get_file_item_status(config, md5values, item, root_path=root_path)
            result.append((item, (status, FILE_ITEM_TRANSITION[status])))
        for item in SIMPLE_ITEMS:
            status = TodoGenerator.__get_simple_item_status(config, item)
            result.append((item, (status, SIMPLE_ITEM_TRANSITION[status])))
        tests_description_path = globalconfig.default_tests_config
        tests_description_status = TodoGenerator.__get_file_item_status(config, md5values, 'tests_description', tests_description_path, root_path=root_path)
        result.append(('tests description', (tests_description_status, FILE_ITEM_TRANSITION[tests_description_status])))
        return result
        
    @staticmethod
    def __counter_print(amount, text, error_when_0=True):
        msg = str(amount) + text
        if amount > 0: print(painter.ok(msg))
        else:
            if error_when_0: print(painter.error(msg))
            else: print(painter.warning(msg))
            
    @staticmethod
    def __get_simple_item_status(config, item):
        if item in config:
            if config[item].strip() != "":
                return "ok"
            else:
                return "warning"
        else:
            return "error" 
    
    @staticmethod   
    def __simple_print(status, text, warn_msg=" is default", err_msg = " does not exist"):
        """ prints message to please console. color depends on objective's status"""
        if (status == "ok"):
            print(painter.ok(text + " ok"))
        elif (status == "warning"):
            print(painter.warning(text + warn_msg))
        else:
            print(painter.error(text + err_msg))
            
    @staticmethod
    def __get_file_item_status(config, md5values, item=None, path=None, root_path='.'):
        """
        Description:
        this function returns one of three item statuses (types):
        1) error - the file does not exist, or it's path is not written in config
        2) warning - the file exists, it's path is written in config file, or it's path is default,
        but the file is default(it's content is same as in creation of problem)
        3) ok - the file exists, it's path is written in config file, or it's path is default,
        and this file is not default(it's content was modified after creation problem)
        """
        if (path != None):
            item_path = os.path.join(root_path, path)
        else:
            if (item in config):
                item_path = os.path.join(root_path, config.get(item, ''))
            else:
                return "error"
        if (os.path.exists(item_path)):
            hashobj = hashlib.md5()
            with open(item_path,"rb") as item_file:
                hashobj.update(item_file.read())
            if (hashobj.hexdigest() != md5values[item]):
                return "ok" 
            else:
                return "warning"
        else:
            return "error"

