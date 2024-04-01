from pathlib import Path

import pandas as pd

from references.path_reference import getTestPlanCsvFolderPath


def getTestPlan(filename: str):
    planPath = Path(getTestPlanCsvFolderPath(), filename)
    df = pd.read_csv(planPath, sep=";")
    df.replace(to_replace=r"\\n", value="\n", regex=True, inplace=True)
    return df


def formatTestPlanToDict(df: pd.DataFrame) -> dict:
    """
    Format a given DataFrame into the desired dictionary format.
    """
    return {
        "inputMessages": df["Input"].tolist(),
        "expectedMessages": df["ExpectedOutput"].tolist()
    }


def getDialogflowMessagesPlan():
    return formatTestPlanToDict(getTestPlan("dialogflowPlan.csv"))


def getSignupPlan():
    return formatTestPlanToDict(getTestPlan("signupPlan.csv"))


def getFullPathPlan():
    return formatTestPlanToDict(getTestPlan("fullPathPlan.csv"))


def __main():
    plan = getDialogflowMessagesPlan()
    inputMessages, expectedMessages = plan["inputMessages"], plan["expectedMessages"]
    return


if __name__ == "__main__":
    __main()
