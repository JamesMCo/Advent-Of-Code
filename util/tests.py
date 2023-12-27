from decimal import Decimal
import os
import pyperclip
import time
import types
import typing as t
import unittest
from util.colour import *

exc_info_tuple = tuple[t.Type[BaseException], BaseException, types.TracebackType] | tuple[None, None, None]

class Result(unittest.TextTestResult):
    def getDescription(self: t.Self, test: unittest.TestCase) -> str:
        return test.id().split("ex")[1]

    def startTest(self: t.Self, test: unittest.TestCase) -> None:
        super(unittest.TextTestResult, self).startTest(test)
        self.stream.write(f"{magenta("Testing against")} {cyan(f"Example #{self.getDescription(test):>02}")}: ")
        self.stream.flush()

    def addSuccess(self: t.Self, test: unittest.TestCase) -> None:
        super(unittest.TextTestResult, self).addSuccess(test)
        self.stream.write(green("Correct") + "\n")

    def addError(self: t.Self, test: unittest.TestCase, err: exc_info_tuple) -> None:
        super(unittest.TextTestResult, self).addError(test, err)
        self.stream.write(red("Error") + "\n")

    def addFailure(self: t.Self, test: unittest.TestCase, err: exc_info_tuple) -> None:
        super(unittest.TextTestResult, self).addFailure(test, err)
        self.stream.write(yellow("Fail") + "\n")

    def addSkip(self: t.Self, test: unittest.TestCase, reason: str) -> None:
        super(unittest.TextTestResult, self).addSkip(test, reason)
        self.stream.write(magenta(f"Skipped {reason!r}") + "\n")

    def addExpectedFailure(self: t.Self, test: unittest.TestCase, err: exc_info_tuple) -> None:
        super(unittest.TextTestResult, self).addExpectedFailure(test, err)
        self.stream.write(green("Expected Failure") + "\n")

    def addUnexpectedSuccess(self: t.Self, test: unittest.TestCase) -> None:
        super(unittest.TextTestResult, self).addUnexpectedSuccess(test)
        self.stream.write(red("Unexpected Success") + "\n")

class Runner(unittest.TextTestRunner):
    def __init__(self: t.Self, stream: t.Optional[t.TextIO] = None, descriptions: bool = True, verbosity: int = 1,
                 failfast: bool = False, buffer: bool = False, resultclass=Result, warnings: t.Optional[t.Type[Warning]] = None,
                 *, tb_locals: bool = False) -> None:
        super().__init__(stream, descriptions, verbosity,
                         failfast, buffer, resultclass, warnings, tb_locals=tb_locals)

def sort_tests(x: str, y: str) -> int:
    x_num = int(x[7:])
    y_num = int(y[7:])
    return x_num - y_num

def run(main: t.Callable[[], t.Optional[tuple[str, t.Any]]], *, skip_on_ci: bool = False) -> t.Optional[t.NoReturn]:
    unittest.TestLoader.sortTestMethodsUsing = staticmethod(sort_tests)
    if unittest.main(verbosity=2, exit=False, testRunner=Runner).result.wasSuccessful():
        if skip_on_ci and os.getenv("GITHUB_STEP_SUMMARY"):
            print(cyan("Solution skipped due to running on GitHub Actions. This is often due to very large runtimes."))
            if os.path.isfile("../../times.txt"):
                with open("../../times.txt", "a") as f:
                    f.write("skippedonci\n")
            return

        start = time.perf_counter_ns()
        try:
            result = main()
        except KeyboardInterrupt:
            end = time.perf_counter_ns()
            seconds = Decimal(
                (end - start) / 1_000_000_000  # ns -> s by dividing by 10^9
            ).quantize(Decimal("0.001"))
            print(f"{cyan("Solution halted after")} {red(f"{seconds}s")}{cyan(".")}")
            exit(1)
        end = time.perf_counter_ns()

        if result:
            # Solutions before 2023 were written in such a way that main() printed its own output.
            # Since 2023, run(main) handles printing and copying the result to the clipboard.
            print(result[0].format(green(result[1])))
            try:
                pyperclip.copy(result[1])
            except pyperclip.PyperclipException:
                # When run on a GitHub Actions runner, pyperclip.copy() raises
                # an exception as it cannot find a copy/paste mechanism.
                # This can be safely ignored (and, if not, will print a traceback).
                pass

        seconds = Decimal(
            (end - start) / 1_000_000_000 # ns -> s by dividing by 10^9
        ).quantize(Decimal("0.001"))

        print(f"{cyan("Solution found in")} {green(f"{seconds}s")}{cyan(".")}")

        if os.path.isfile("../../times.txt"):
            with open("../../times.txt", "a") as f:
                f.write(f"{end - start}\n")
    else:
        exit(1)
