# from requestTests.calls.sendHttpCalls import sendFirebaseLessRequest
import os
import sys

sys.path.append(r'E:\Python\omnichatTests\requestTests')
sys.path.append(r'E:\Python\omnichatTests')


def dummyFunction():
    return list(sys.path)


def __main():
    aux = dummyFunction()
    print(aux)
    return


if __name__ == "__main__":
    print(dummyFunction())
