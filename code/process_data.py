"""
This script processes the raw data from webscraper and produce a new csv file with the following columns:
- id
- title
- sponsor
- cosponsor
- Purpose
- status
- vote
- effective date
"""

import os
import re

import pandas as pd

from text_patterns import (
    p_bill_no,
    p_title01,
    p_title02,
    p_title03,
    p_purpose01,
    p_purpose02,
    p_purpose03,
    p_justification01,
    p_justification02,
    p_justification03,
    p_justification04,
    p_history01,
    p_history02,
    p_history03,
    p_fiscal01,
    p_fiscal02,
    p_fiscal03,
    p_fiscal04,
    p_fiscal05,
    p_edate,
)


# User defined inputs
target_spreadsheet = "labor_2023.xlsx"

# Processing the raw data
filename = os.path.join("..", "raw_data", target_spreadsheet)
df = pd.read_excel(filename)
df["memo"] = df["memo"].str.replace("_x000D_", "")
df["summary"] = df["summary"].str.replace("_x000D_", "")


def clean_text(text: str) -> str:
    """
    First, we remove the newline characters and extra spaces at the beginning and end of the text.
    Furthermore, the text might start with a colon and a newline, so we remove these two characters.
    """
    if "DATE" in text:
        text = text.split("DATE")[1]
    if "FOR STATE AND LOCAL GOVERNMENTS" in text:
        text = text.split("FOR STATE AND LOCAL GOVERNMENTS")[1]
    if text.startswith("::"):
        text = text.split("::")[1]
    if ":\n" in text:
        text = text.split(":\n")[1]
    if text.startswith(":"):
        text = text[1:]
    text = text.replace("\n", " ")
    text = text.replace("SUMMARY OF PROVISIONS", "")
    text = text.replace("SUMMARY OF SPECIFIC PROVISIONS", "")
    text = text.replace("SAME AS ", "")
    text = text.strip()
    return text


def extract_text(text: str, patterns: list[re.Pattern], section: str) -> str:
    for pattern in patterns:
        result = pattern.search(text)
        if result:
            output = clean_text(result.group(1))
            if "DATE :" in output:
                raise ValueError("CHECKK")
            return clean_text(result.group(1))
    # If no pattern is found, return None or raise an error
    if not section in text:
        return None
    else:
        raise ValueError(f"{section} not found")


# Will store the processed data in outputs
outputs = pd.DataFrame()
for i in range(len(df)):

    memo = df.loc[i, "memo"]

    bill_no = p_bill_no().search(memo).group(1)

    title = extract_text(memo, [p_title01(), p_title02(), p_title03()], "TITLE")

    purpose = extract_text(
        memo, [p_purpose01(), p_purpose02(), p_purpose03()], "PURPOSE"
    )

    justification = extract_text(
        memo,
        [
            p_justification01(),
            p_justification02(),
            p_justification03(),
            p_justification04(),
        ],
        "JUSTIFICATION",
    )

    history = extract_text(
        memo, [p_history01(), p_history02(), p_history03()], "HISTORY"
    )

    fiscal = extract_text(
        memo,
        [p_fiscal01(), p_fiscal02(), p_fiscal03(), p_fiscal04(), p_fiscal05()],
        "FISCAL",
    )

    edate = extract_text(memo, [p_edate()], "EFFECTIVE")

    subset1 = pd.DataFrame(
        {
            "id2": bill_no,
            "title": title,
            "purpose": purpose,
            "justification": justification,
            "history": history,
            "fiscal": fiscal,
            "edate": edate,
        },
        index=[i],
    )

    summ_pattern = re.compile(
        r"""SAME\sAS(?P<same_as>.+)\nSPONSOR(?P<sponsor>.+)\nCOSPNSR(?P<cosponsor>.*)\nMLTSPNSR(?P<mltsponsor>.*)\n(?P<summary>.*)""",
        re.DOTALL,
    )
    summary = df.loc[i, "summary"]
    re_result2 = summ_pattern.search(summary)
    re_result2 = re_result2.groupdict()
    subset2 = pd.DataFrame(re_result2, index=[i])

    # Append
    subset1["id1"] = df.loc[i, "id"]
    subset1["vote"] = df.loc[i, "vote"]
    subset1["link"] = df.loc[i, "link"]

    subset = pd.concat([subset1, subset2], axis=1)
    outputs = pd.concat([outputs, subset], axis=0)


# Save the processed data
filename = os.path.join("..", "data", f"{target_spreadsheet.split('.')[0]}.csv")

# Reorder columns and save
order = [
    "id1",
    "id2",
    "title",
    "sponsor",
    "cosponsor",
    "purpose",
    "justification",
    "history",
    "vote",
    "fiscal",
    "edate",
    "link",
]
outputs = outputs[order]
outputs.to_csv(filename, index=False)
