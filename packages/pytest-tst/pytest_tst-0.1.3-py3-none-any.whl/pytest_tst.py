import pytest
from pytest import ExitCode


def pytest_addoption(parser):
    opts = parser.getgroup('tst')

    opts.addoption('--tst',
        action='store_true',
        default=False,
        help='Customize output to run from tst'
    )

    opts.addoption('--clean',
        action='store_true',
        default=False,
        help='Clean output in tst mode'
    )


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(args):
    # find --tst option in args
    try:
        tst_option_index = args.index("--tst")
    except ValueError:
        return

    # get __filename of the module under test
    try:
        from undertst import __filename
    except ImportError as e:
        raise Exception("failed importing undertst")
    except Exception as e:
        raise pytest.UsageError(e)

    # get context from command line and file system
    try:
        if args[tst_option_index + 1] == __filename:
            __target = __filename
    except IndexError:
        __target = None

    import os
    listdir = os.listdir()
    __cmd_files = [a for a in args if a in listdir]
    __other_files_in_cmd = __cmd_files != [__target]

    # identify files containing tests
    __test_files = []
    for fn in listdir:
        if not fn.endswith(".py"): continue
        if fn.endswith("_test.py") or fn.startswith("test_") or fn.endswith("_tests.py"):
            __test_files.append(fn)

    # case 1: pytest ... <filename> ... --tst <target> ... <filename>
    if __target and __other_files_in_cmd:
        # make pytest NOT collect tests from __filename (target)
        args.pop(tst_option_index + 1)

    # case 2: pytest --tst (no target, no further filenames in cmd line)
    elif not __cmd_files: # === not __target and not __other_files_in_cmd
        # make pytest collect tests in __filename
        args.append(__filename)
        args.extend(__test_files)

    # case 3: pytest --tst <target> (with no other filename in cmd line)
    elif __target and not __other_files_in_cmd or not __cmd_files:
        # make pytest collect tests in all __test_files
        args.extend(__test_files)

    if '--clean' in args:
        args.append("--quiet")
        args.append("--capture=no")
        args.append("--no-summary")
        args.append("--color=no")
        args.append("-o console_output_style=none")


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    if session.config.getoption('--tst'):
        if exitstatus == ExitCode.TESTS_FAILED: # or exitstatus == ExitCode.NO_TESTS_COLLECTED:
            session.exitstatus = ExitCode.OK
