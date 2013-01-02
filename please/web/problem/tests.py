import django.test
from unittest.mock import Mock, patch
from .models import Problem, ProblemTag
from . import synchronization


def names(problems):
    return [x.name for x in problems]


def add_problem(problem, tag):
    p = Problem(name=problem)
    t = ProblemTag(name=tag)
    p.save()
    t.save()
    p.tags.add(t)
    p.save()
    t.save()


class ViewTest(django.test.TestCase):
    def setUp(self):
        synchronization.import_to_database = Mock()
        synchronization.export_from_database = Mock()
        add_problem("first", "gcd")
        add_problem("second", "lcm")

    def test_all_problems(self):
        resp = self.client.get("/problems/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(names(resp.context["problems"]),
                ["first", "second"])
        self.assertTemplateUsed(resp, "problems_list.html")

    def test_problems_by_tags(self):
        resp = self.client.get("/problems/", {"tags": "lcm"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(names(resp.context["problems"]),
                ["second"])
        self.assertTemplateUsed(resp, "problems_list.html")

        resp = self.client.get("/problems/", {"tags": "gcd"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(names(resp.context["problems"]),
                ["first"])
        self.assertTemplateUsed(resp, "problems_list.html")

    @patch('problem.views.TodoGenerator')
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

