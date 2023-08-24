import pandas as pd

from requestTests.automatedTests.testPlanLoader import getDialogflowMessagesPlan
from requestTests.httpCalls import sendTwilioRequest, convertResponseToUtf8


def colorize(text: str, color_code: str):
    return f"\033[{color_code}m{text}\033[0m"


def runTestPlan(testPlan: pd.DataFrame):
    inputMessageList, expectedMessageList = testPlan["inputMessages"], testPlan["expectedMessages"]
    combinedMessages = list(zip(inputMessageList, expectedMessageList))
    for actual, expected in combinedMessages:
        print(colorize(f"User: {actual}", "1;36"))
        rawResponse = sendTwilioRequest(body=actual)
        textResponse = convertResponseToUtf8(rawResponse)
        print(colorize(f"Bot: {textResponse}", "1;35"))
        testResult = "Passed" if textResponse == expected else "Failed"
        result_color = "1;31" if testResult == "Failed" else "1;32"
        print(colorize(f"Test result: {testResult}", result_color))
    return


def __main():
    plan = getDialogflowMessagesPlan()
    runTestPlan(plan)


if __name__ == "__main__":
    __main()
