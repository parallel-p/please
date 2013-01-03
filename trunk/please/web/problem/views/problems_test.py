import django.test
from unittest.mock import Mock, patch


def names(problems):
    return [x.name for x in problems]


class ProblemsTests(django.test.TestCase):
    fixtures = ['test']

    def setUp(self):
        self.patcher_import = patch('problem.synchronization.import_to_database', Mock())
        self.patcher_export = patch('problem.synchronization.export_from_database', Mock())
        self.patcher_import.start()
        self.patcher_export.start()

    def tearDown(self):
        self.patcher_import.stop()
        self.patcher_export.stop()

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
