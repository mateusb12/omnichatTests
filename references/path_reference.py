import os
from pathlib import Path


def getMainFolderPath() -> Path:
    return Path(os.path.dirname(os.path.realpath(__file__))).parent


def getTestPlanCsvFolderPath() -> Path:
    return getMainFolderPath() / 'test_plans'


def __main():
    testPlan = getTestPlanCsvFolderPath()
    print(testPlan)
    return


if __name__ == '__main__':
    __main()
