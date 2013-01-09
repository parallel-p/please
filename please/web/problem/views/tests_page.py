import os

from django.shortcuts import render_to_response

import please.globalconfig
from please.utils.exceptions import PleaseException
from please.package import package_config
from please.solution_runner.solution_runner import SolutionInfo, run_solution

from problem.models import TestResult, Solution
from problem.views.file_utils import ChangeDir


def generate_single_output(source_path, test, output_filename, execution_limits=please.globalconfig.default_limits):
    config = package_config.PackageConfig.get_config()
    args = (config['args'] if 'args' in config else [])
    solution_config = {'input': config['input'], 'output': config['output']}
    run_solution((SolutionInfo(source_path, args, execution_limits, solution_config, test, output_filename)))


def single_test_block(problem, solution_name, test_id):
    source_path = os.path.join(please.globalconfig.solutions_dir, solution_name).replace(os.sep, '/')
    solution = Solution.objects.get(problem=problem,
                                    path=source_path)
    results = TestResult.objects.get(solution=solution,
                                     test_number=test_id)
    with ChangeDir(problem.path):
        test_path = os.path.join(please.globalconfig.temp_tests_dir, test_id)
        out_path = os.path.join('.please', solution_name + '_' + str(test_id) + '.output')
        try:
            generate_single_output(source_path, test_path, out_path)
        except PleaseException as exc:
            full_output = repr(exc)
        else:
            with open(out_path) as file:
                full_output = file.read()
            os.remove(out_path)

    return {'solution_name': solution_name,
            'full_output': full_output,
            'results': results}
