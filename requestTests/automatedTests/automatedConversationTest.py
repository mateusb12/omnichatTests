import re

import pandas as pd
import pytest
from requestTests.automatedTests.testPlanLoader import getDialogflowMessagesPlan
from requestTests.httpCalls import sendTwilioRequest, convertResponseToUtf8


def colorize(text: str, color_code: str):
    return f"\033[{color_code}m{text}\033[0m"


def normalize_string(s: str) -> str:
    """Convert sequences of whitespace to a single space and trim the string."""
    return re.sub(r'\s+', ' ', s).strip()


def less_strict_comparison(str1: str, str2: str) -> bool:
    normalized_str1 = normalize_string(str1)
    normalized_str2 = normalize_string(str2)
    return normalized_str1 == normalized_str2


def test_run_plan():
    plan = getDialogflowMessagesPlan()
    inputMessageList, expectedMessageList = plan["inputMessages"], plan["expectedMessages"]
    combinedMessages = list(zip(inputMessageList, expectedMessageList))
    for actual, expected in combinedMessages:
        print(colorize(f"→               [User]: {actual}", "1;36"))
        rawResponse = sendTwilioRequest(body=actual)
        textResponse = convertResponseToUtf8(rawResponse)
        _actual = textResponse.replace("\n", "")
        _expected = expected.replace("\n", "")
        print(colorize(f"Actual:   {_actual}", "0;33"))
        print(colorize(f"Expected: {_expected}", "0;33"))
        testResult = "Passed" if textResponse == expected else "Failed"
        pytestCheck(textResponse, expected)
        # result_color = "1;31" if testResult == "Failed" else "1;32"
        # print(colorize(f"Test result: {testResult}", result_color))
        print("")
    return


def pytestCheck(actual, expected):
    assert less_strict_comparison(actual, expected), f"Expected: '{expected}', Got: '{actual}'"


def main_test_runner():
    test_run_plan()


def __main():
    main_test_runner()


if __name__ == "__main__":
    pytest.main([__file__])
