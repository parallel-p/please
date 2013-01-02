import unittest
from functools import partial
from unittest.mock import Mock, MagicMock
from please.todo.todo_generator import TodoGenerator
from please.utils import utests
from please.test_config_parser import parser


class TodoGeneratorTest(unittest.TestCase):
    def setUp(self):
        TodoGenerator._TodoGenerator__read_md5_values = Mock()

    def test_empty_solution(self):
        ITEMS = ('statement', 'checker', 'description', 'analysis', 'validator', 'main_solution', 'tags', 'name', 'tests_description')
        TRANSITION = dict(map(lambda item: (item, 'warning'), ITEMS))

        TodoGenerator._TodoGenerator__get_file_item_status = lambda config, md5_values, item, path=None: TRANSITION[item]
        TodoGenerator._TodoGenerator__get_simple_item_status = lambda config, item: TRANSITION[item]

        self.assertDictEqual(dict(TodoGenerator.get_status_description()), {
            'statement': 'default',
            'checker': 'default',
            'description': 'default',
            'analysis': 'default',
            'validator': 'default',
            'main_solution': 'default',
            'tags': 'empty',
            'name': 'empty',
            'tests description': 'default',
        })

    def test_generated_tests_count(self):
        utests.get_tests = lambda root_path: [1, 2, 3]
        self.assertEqual(TodoGenerator.generated_tests_count(), 3)


if __name__ == '__main__':
    unittest.main()
