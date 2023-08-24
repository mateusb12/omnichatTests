from pathlib import Path

import pandas as pd

from references.path_reference import getTestPlanCsvFolderPath


def getTestPlan(filename: str):
    planPath = Path(getTestPlanCsvFolderPath(), filename)
    df = pd.read_csv(planPath, sep=";")
    df.replace(to_replace=r"\\n", value="\n", regex=True, inplace=True)
    return df


def getDialogflowMessagesPlan():
    dialogflowPlan = getTestPlan("dialogflowPlan.csv")
    return {"inputMessages": dialogflowPlan["Input"].tolist(),
            "expectedMessages": dialogflowPlan["ExpectedOutput"].tolist()}


def getSignupPlan():
    signupPlan = getTestPlan("signupPlan.csv")
    return {"inputMessages": signupPlan["Input"].tolist(),
            "expectedMessages": signupPlan["ExpectedOutput"].tolist()}


def __main():
    plan = getDialogflowMessagesPlan()
    inputMessages, expectedMessages = plan["inputMessages"], plan["expectedMessages"]
    return


if __name__ == "__main__":
    __main()
