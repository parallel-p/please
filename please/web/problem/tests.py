import django.test
from .models import Problem, ProblemTag


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
