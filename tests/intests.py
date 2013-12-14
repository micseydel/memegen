import sys
from time import strftime
from traceback import print_tb, format_tb

EXPLANATION_FORMAT = "  {0}\n  error: {1}\n"
EQ_FORMAT = "{0} was not equal to {1}"

class AssertionFailure(Exception):
    pass

class Test:
    tests = []
    def __init__(self, f):
        self.tests.append(f)

def assert_equal(*args):
    'assert that all arguments are equal'
    objects = iter(args)
    prev = next(objects)
    for obj in objects:
        if obj != prev:
            raise AssertionFailure(EQ_FORMAT.format(obj, prev))
        prev = obj

def assert_response_ok(status_code, reason=None):
    if status_code < 200 or status_code >= 300:
        error = "Response: {0}, Reason: {1}".format(status_code, reason)

def assert_untested(msg=None):
    'simple function to force AssertionFailure'
    raise AssertionFailure("There is no test yet." if msg is None else msg)

def get_timestamp():
    return strftime('%d/%b/%Y %H:%M:%S')

def run_all():
    for arg in sys.argv:
        if arg.startswith('-o'):
            test_names = set(arg.lstrip('-o').split(','))
            tests = [t for t in Test.tests if t.func_name in test_names]
            break
    else:
        tests = Test.tests

    failures = []

    for test in tests:
        try:
            test()
        except Exception as e:
            desc = '{0} -- {1}: {2}'.format(
                get_timestamp(), test.func_name, test.__doc__.strip())
            failures.append((desc, e))

    passed = len(tests) - len(failures)
    print 'Passed {0}/{1} ({2:.2f}%)'.format(
        passed, len(tests), 100.0 * passed / len(tests)
        )

    if failures:
        print 'Failures:'

    for doc, error in failures:
        print EXPLANATION_FORMAT.format(doc, error)
