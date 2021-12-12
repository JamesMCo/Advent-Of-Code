import unittest, sys
import colorama
import time

Fore = colorama.Fore
colorama.init()


class Result(unittest.TextTestResult):
    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        return str(test).split()[0].split("ex")[1]

    def startTest(self, test):
        super(unittest.TextTestResult, self).startTest(test)
        self.stream.write(Fore.MAGENTA + "Testing against" + \
                          Fore.CYAN    + " Example #")
        self.stream.write(self.getDescription(test).zfill(2))
        self.stream.write(Fore.RESET + ": ")
        self.stream.flush()

    def addSuccess(self, test):
        super(unittest.TextTestResult, self).addSuccess(test)
        self.stream.writeln(Fore.GREEN + "Correct" + Fore.RESET)

    def addError(self, test, err):
        super(unittest.TextTestResult, self).addError(test, err)
        self.stream.writeln(Fore.RED + "Error" + Fore.RESET)

    def addFailure(self, test, err):
        super(unittest.TextTestResult, self).addFailure(test, err)
        self.stream.writeln(Fore.YELLOW + "Fail" + Fore.RESET)

    def addSkip(self, test, reason):
        super(unittest.TextTestResult, self).addSkip(test, reason)
        self.stream.writeln(Fore.MAGENTA + "Skipped {0!r}".format(reason) + Fore.RESET)

    def addExpectedFailure(self, test, err):
        super(unittest.TextTestResult, self).addExpectedFailure(test, err)
        self.stream.writeln(Fore.GREEN + "Expected Failure" + Fore.RESET)

    def addUnexpectedSuccess(self, test):
        super(unittestTextTestResult, self).addUnexpectedSuccess(test)
        self.stream.writeln(Fore.RED + "Unexpected Success" + Fore.RESET)

class Runner(unittest.TextTestRunner):
    def __init__(self, stream=None, descriptions=True, verbosity=1,
                 failfast=False, buffer=False, resultclass=Result, warnings=None,
                 *, tb_locals=False):
        super().__init__(stream, descriptions, verbosity,
                         failfast, buffer, resultclass, warnings, tb_locals=tb_locals)

def run(main):
    if unittest.main(verbosity=2, exit=False, testRunner=Runner).result.wasSuccessful():
        start = time.time()
        main()
        end = time.time()

        duration = str(round(end - start, 3))
        duration += "0" * (3 - len(duration.split(".")[1]))

        print(f"{colorama.Fore.CYAN}Solution found in {colorama.Fore.GREEN}{duration}s{colorama.Fore.CYAN}.{colorama.Fore.RESET}")

        if os.path.isfile("../../times.txt"):
            with open("../../times.txt", "a") as f:
                f.write(f"{end - start}\n")
    else:
        exit(1)