import pytest
from requestTests.automation.testPlanLoader import getDialogflowMessagesPlan, getSignupPlan, getFullPathPlan
from requestTests.automation.testUtils import colorize, less_strict_comparison
from requestTests.calls.sendHttpCalls import sendTwilioRequest, convertResponseToUtf8, sendInstagramRequest, \
    sendFirebaseLessRequest


def getCurrentPlan():
    return getDialogflowMessagesPlan()


def test_run_plan():
    plan = getCurrentPlan()
    inputMessageList, expectedMessageList = plan["inputMessages"], plan["expectedMessages"]
    combinedMessages = list(zip(inputMessageList, expectedMessageList))
    for actual, expected in combinedMessages:
        print(colorize(f"→               [User]: {actual}", "1;36"))
        rawResponse = sendFirebaseLessRequest(body=actual)
        textResponse = str(rawResponse.text)
        # textResponse = convertResponseToUtf8(rawResponse)
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


def __main():
    test_run_plan()


if __name__ == "__main__":
    pytest.main([__file__])
