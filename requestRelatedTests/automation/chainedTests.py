from typing import List

from requestRelatedTests.calls.sendHttpCalls import sendFirebaseLessRequest, sendEraseRequest


def simple_plan():
    return ["Oii", "Vou querer uma pizza meia calabresa meia margherita e uma pizza de frango", "Sim",
            "Vou querer um guaraná e dois sucos de laranja", "Pix"]


def loop_messages(plan: List[str]):
    for message in plan:
        rawResponse = sendFirebaseLessRequest(body=message)
        textResponse = str(rawResponse.text)
        print(textResponse)
    sendEraseRequest(location="backend")
    return


def __main():
    myPlan = simple_plan()
    loop_messages(myPlan)


if __name__ == "__main__":
    __main()
