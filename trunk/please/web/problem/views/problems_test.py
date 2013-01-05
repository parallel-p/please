import os.path
import shutil
from unittest.mock import Mock, patch

import django.test
from django.core.urlresolvers import reverse

from problem.models import Problem

POLYGON_IMPORT_TARGET_PATH = os.path.abspath(os.path.curdir)
POLYGON_IMPORTED_CONTEST_ID = 777
POLYGON_IMPORTED_PROBLEM_LETTER = 'X'
POLYGON_IMPORTED_PROBLEM_NAME = 'centroid'
# ~~~Problem name must be same as a name of a
# zip archive in please/import_from_polygon/testdata
# because Polygon names the archive by the problem name~~~

TEST_POLYGON_ARCHIVE_PATH = os.path.abspath(os.path.join(
        # please/web/problem/views/
        os.path.dirname(os.path.abspath(__file__)),
        '..',  # please/web/problem
        '..',  # please/web/
        '..',  # please/
        'import_from_polygon',  # please/import_from_polygon
        'testdata',  # please/import_from_polygon/testdata
        'centroid-70.zip'))
# please/import_from_polygon/testdata/centroid-70_correct.zip


def fake_download(contest_id, problem_letter):
    shutil.copyfile(TEST_POLYGON_ARCHIVE_PATH,
            os.path.join(
                POLYGON_IMPORT_TARGET_PATH,
                POLYGON_IMPORTED_PROBLEM_NAME + '.zip'))
    return POLYGON_IMPORTED_PROBLEM_NAME


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

    def test_import_from_polygon(self):
        response = self.client.get(reverse('polygon-import'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(template_name='import_from_polygon.html')

    @patch('problem.views.problems.download_zip.get_problem',
            side_effect=fake_download)
    def test_import_from_polygon_block(self, download):
        old_problems = set(Problem.objects.all())
        response = self.client.post(
                reverse('polygon-import'),
                data={
                    'target_path': POLYGON_IMPORT_TARGET_PATH,
                    'contest_id': POLYGON_IMPORTED_CONTEST_ID,
                    'problem_letter': POLYGON_IMPORTED_PROBLEM_LETTER
                })
        self.assertEqual(response.status_code, 302)
        download.assertCalledOnceWith(POLYGON_IMPORTED_CONTEST_ID,
                POLYGON_IMPORTED_PROBLEM_LETTER)
        new_problems = set(Problem.objects.all()).difference(old_problems)
        self.assertEqual(len(new_problems), 1)
        problem, *_ = tuple(new_problems)
        self.assertEqual(problem.short_name, POLYGON_IMPORTED_PROBLEM_NAME)
        self.assertEqual(problem.path, os.path.join(
            POLYGON_IMPORT_TARGET_PATH, POLYGON_IMPORTED_PROBLEM_NAME))
