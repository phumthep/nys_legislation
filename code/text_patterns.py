""" Define re patterns
"""

import re


def p_bill_no():
    return re.compile(r"""BILL\sNUMBER:\s(?P<id2>.+)\nSPONSOR""", re.DOTALL)


def p_sponsor():
    return re.compile(r"""SPONSOR:\s(?P<sponsor>.+)\nTITLE\sOF\sBILL""", re.DOTALL)


def p_title01():
    return re.compile(r"""TITLE\sOF\sBILL\s:\n(?P<title>.+)\nPURPOSE""", re.DOTALL)


def p_title02():
    return re.compile(r"""TITLE\sOF\sBILL\s:\n(?P<title>.+)\nSUMMARY""", re.DOTALL)


def p_title03():
    return re.compile(r"""TITLE\sOF\sBILL\s:\n(?P<title>.+)\Z""", re.DOTALL)


def p_purpose01():
    return re.compile(r"""PURPOSE(?P<purpose>.+)\nJUSTIFICATION""", re.DOTALL)


def p_purpose02():
    return re.compile(
        r"""PURPOSE\sOR\sGENERAL\sIDEA\sOF\sBILL(?P<purpose>.+).*\nJUSTIFICATION""",
        re.DOTALL,
    )


def p_purpose03():
    return re.compile(
        r"""PURPOSE(?P<purpose>.+)\nSUMMARY""",
        re.DOTALL,
    )


def p_justification01():
    return re.compile(
        r"""JUSTIFICATION(?P<justification>.+)\nLEGISLATIVE""",
        re.DOTALL,
    )


def p_justification02():
    return re.compile(
        r"""JUSTIFICATION(?P<justification>.+)\nPRIOR""",
        re.DOTALL,
    )


def p_justification03():
    return re.compile(
        r"""JUSTIFICATION(?P<justification>.+)\nFISCAL""",
        re.DOTALL,
    )


def p_justification04():
    """Nothing after JUSTIFICATION."""
    return re.compile(
        r"""JUSTIFICATION(?P<justification>.+)\Z""",
        re.DOTALL,
    )


def p_history01():
    return re.compile(
        r"""HISTORY(?P<history>.+)\nFISCAL""",
        re.DOTALL,
    )


def p_history02():
    return re.compile(
        r"""HISTORY(?P<history>.+)\nEFFECTIVE\sDATE""",
        re.DOTALL,
    )


def p_history03():
    return re.compile(
        r"""HISTORY(?P<history>.+)\Z""",
        re.DOTALL,
    )


def p_fiscal01():
    return re.compile(
        r"""FISCAL\sIMPLICATIONS(?P<fiscal>.+)\nEFFECTIVE""",
        re.DOTALL,
    )


def p_fiscal02():
    return re.compile(
        r"""FISCAL\sIMPLICATIONS\sFOR\sSTATE\sAND\sLOCAL\sGOVERNMENTS(?P<fiscal>.+)\nEFFECTIVE\sDATE\s:\n""",
        re.DOTALL,
    )


def p_fiscal03():
    return re.compile(
        r"""FISCAL\sIMPACT(?P<fiscal>.+)\n\b([A-Z]+)\b""",
        re.DOTALL,
    )


def p_fiscal04():
    return re.compile(
        r"""FISCAL\sIMPLICATIONS(?P<fiscal>.+)\Z""",
        re.DOTALL,
    )


def p_fiscal05():
    return re.compile(
        r"""FISCAL-IMPLICATIONS(?P<fiscal>.+)\Z""",
        re.DOTALL,
    )


def p_edate():
    return re.compile(r"""EFFECTIVE(?P<edate>.+)\Z""", re.DOTALL)
