import django.test
from unittest.mock import Mock, patch


class TodoTests(django.test.TestCase):
    fixtures = ['test']

    def setUp(self):
        self.patcher_import = patch('problem.synchronization.import_to_database', Mock())
        self.patcher_export = patch('problem.synchronization.export_from_database', Mock())
        self.patcher_import.start()
        self.patcher_export.start()

    def tearDown(self):
        self.patcher_import.stop()
        self.patcher_export.stop()

    @patch('problem.views.todo.TodoGenerator')
    def test_todo(TodoGenerator, self):
        TESTS_COUNT = 5
        SAMPLES_COUNT = 2
        STATUS_DESCRIPTION = {'validator': 'ok', 'checker': 'default'}

        TodoGenerator = Mock()
        TodoGenerator.get_status_description.return_value = STATUS_DESCRIPTION
        TodoGenerator.generated_tests_count.return_value = TESTS_COUNT
        TodoGenerator.sample_tests_count.return_value = SAMPLES_COUNT
        
        response = self.client.get('/problem/1/todo/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['status_description'], STATUS_DESCRIPTION)
        self.assertEqual(response.context['tests_count'], TESTS_COUNT)
        self.assertEqual(response.context['samples_count'], SAMPLES_COUNT)
        self.assertTemplateUsed(response, 'todo.html')
