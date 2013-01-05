import os
import io
from unittest.mock import Mock, NonCallableMock, NonCallableMagicMock, patch

import django.test.testcases as ut
import django.test.client
from django.core.urlresolvers import reverse

from problem.models import Problem, Solution, Verdict


TEST_FILE_NAME = 'test_solution_file.mock'
TEST_FILE_CONTENT = b'test file content'


def mock_file(name):
    myfile = io.BytesIO(TEST_FILE_CONTENT)
    myfile.name = name
    return myfile


def with_names(*names):
    return set(filter(lambda v: v.name in names,
            Verdict.objects.all()))


def mock_save(mock_file, directory):
    return mock_file.name


class SolutionsTests(ut.TestCase):
    fixtures = ['test_add_solution']

    def setUp(self):
        # Let it be no synchronization - we'll mock all disk IO.
        self.client = django.test.client.Client()
        self.problem = Problem.objects.get(id=1)
        self.expected_verdicts = with_names('OK')
        self.possible_verdicts = with_names('WA', 'TL', 'OK')
        self.solution_file = mock_file(TEST_FILE_NAME)

    @patch('problem.views.solutions.file_save', side_effect=mock_save)
    def test_add_block(self, savemock):
        solution_path = os.path.join(os.path.join(
            self.problem.path, 'solutions'), self.solution_file.name)
        old_solutions = set(self.problem.solution_set.all())
        response = self.client.post(reverse('problem.views.problem.solution',
            args=(self.problem.id,)), data={
                        'solution_file': self.solution_file,
                        'possible_verdicts': [
                            verdict.name for verdict in self.possible_verdicts],
                        'expected_verdicts': [
                            verdict.name for verdict in self.expected_verdicts]
                        }, content_type=django.test.client.MULTIPART_CONTENT)
        self.assertEqual(response.status_code, 200)
        new_solutions = set(
            self.problem.solution_set.all()).difference(old_solutions)
        self.assertEqual(len(new_solutions), 1)
        solution = tuple(new_solutions)[0]
        self.assertSetEqual(set(solution.possible_verdicts.all()),
                self.possible_verdicts)
        self.assertSetEqual(set(solution.expected_verdicts.all()),
                self.expected_verdicts)
        # We have a Django-generated InMemoryUploadedFile as the first argument
        # here so usual mock call assertions won't go.
        self.assertEqual(len(savemock.mock_calls), 1)
        # We've saved exactly one file...
        self.assertEqual(savemock.call_args[0][0].name, TEST_FILE_NAME)
        self.assertEqual(savemock.call_args[0][0].size, len(TEST_FILE_CONTENT))
        # ...named and sized just as our test one...
        self.assertEqual(savemock.call_args[0][1],
                os.path.join(str(self.problem.path), 'solutions'))
        # ...and to the correct directory.

    @patch('problem.views.solutions.file_save', Mock(side_effect=mock_save))
    def test_add(self):
        self.assertEqual(django.test.client.Client().get(reverse('problem.views.problem.solution',
            args=(self.problem.id,))).status_code, 200)
        self.assertTemplateUsed(template_name='add_solution.html')
