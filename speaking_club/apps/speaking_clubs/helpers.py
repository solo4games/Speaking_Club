import logging
import decimal
import hashlib
from urllib import parse
from speaking_club.settings import ALLOWED_HOSTS, ROBOKASSA_PASSWORD1
from django import forms
from robokassa.forms import SuccessRedirectForm
import urllib.parse

MAX_SCORE = {
    "nav-Writing": 16,
    "nav-Listening": 15,
    "nav-Vocabulary": 20,
    "nav-Grammar": 34,
    "nav-Reading": 16
}


def define_levels(
    grammar: int,
    listening: int,
    writing: int,
    reading: int,
    vocabulary: int
):
    if 0 <= grammar <= 13:
        grammar = 'A1'
    elif 14 <= grammar <= 21:
        grammar = 'A2'
    elif 22 <= grammar:
        grammar = 'B1'

    if 0 <= listening <= 4:
        listening = 'A1'
    elif 5 <= listening <= 7:
        listening = 'A2'
    elif 8 <= listening:
        listening = 'B1'

    if 0 <= writing <= 16:
        writing = 'A1'
    elif 17 <= writing <= 28:
        writing = 'A2'
    elif 29 <= writing:
        writing = 'B1'

    if 0 <= reading <= 5:
        reading = 'A1'
    elif 6 <= reading <= 9:
        reading = 'A2'
    elif 10 <= reading:
        reading = 'B1'

    if 0 <= vocabulary <= 14:
        vocabulary = 'A1'
    elif 15 <= vocabulary <= 25:
        vocabulary = 'A2'
    elif 26 <= vocabulary:
        vocabulary = 'B1'

    return {
        "grammar": grammar if grammar else "-",
        "listening": listening if listening else "-",
        "writing": writing if writing else "-",
        "reading": reading if reading else "-",
        "vocabulary": vocabulary if vocabulary else "-",
    }


def define_total_level(grammar: str, listening: str, writing: str, reading: str, vocabulary: str):
    if any([el == -1 or el == '-' for el in (grammar, listening, writing, reading, vocabulary)]):
        return {
            "total": "-"
        }

    if (grammar == "A1") and (vocabulary == "A1"):
        return {
            "total": "A1"
        }

    if (grammar == "A1") and (vocabulary == "A2" or vocabulary == "B1") and writing == "A1":
        return {
            "total": "A1"
        }

    if (grammar == "A1") and (vocabulary == "A2" or vocabulary == "B1") and (writing == "A2" or writing == "B1"):
        return {
            "total": "A2"
        }

    if (grammar == "A2") and (vocabulary == "A2" or vocabulary == "B1"):
        return {
            "total": "A2"
        }

    if (grammar == "A2") and (vocabulary == "A1") and writing == "A1":
        return {
            "total": "A1"
        }

    if (grammar == "A2") and (vocabulary == "A1") and (writing == "A2" or writing == "B1"):
        return {
            "total": "A2"
        }

    if (grammar == "B1") and (vocabulary == "A2" or vocabulary == "B1"):
        return {
            "total": "B1"
        }

    if (grammar == "B1") and (vocabulary == "A1"):
        return {
            "total": "A2"
        }


def generate_success_form(
    cost: decimal,  # Cost of goods, RU
    number: int,  # Invoice number
    host_url=ALLOWED_HOSTS[0],
    signature=None,
) -> str:
    """URL for redirection of the customer to the service.
    """
    if signature is None:
        signature = calculate_signature(
            cost,
            number,
            ROBOKASSA_PASSWORD1,
        )

    data = {
        'OutSum': cost,
        'InvId': number,
        'SignatureValue': signature,
        "Culture": "ru"
    }

    return SuccessRedirectForm(data).as_table()


def generate_success_url(
    cost: decimal,  # Cost of goods, RU
    number: int,  # Invoice number
    host_url=ALLOWED_HOSTS[0],
    signature=None,
) -> str:
    """URL for redirection of the customer to the service.
    """
    if signature is None:
        signature = calculate_signature(
            cost,
            number,
            ROBOKASSA_PASSWORD1,
        )

    data = {
        'OutSum': cost,
        'InvId': number,
        'SignatureValue': signature,
        "Culture": "ru"
    }

    return f"https://{host_url}/my_order?{urllib.parse.urlencode(data)}"


def calculate_signature(*args) -> str:
    """Create signature MD5.
    """
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


def calculate_levels(_test) -> tuple[dict[str, int], str]:

    grammar = _test.get("nav-Grammar")
    writing = _test.get("nav-Writing")
    listening = _test.get("nav-Listening")
    vocabulary = _test.get("nav-Vocabulary")
    reading = _test.get("nav-Reading")

    levels = define_levels(
        grammar=grammar,
        writing=writing,
        listening=listening,
        vocabulary=vocabulary,
        reading=reading
    )

    grammar = levels.get("grammar")
    writing = levels.get("writing")
    listening = levels.get("listening")
    vocabulary = levels.get("vocabulary")
    reading = levels.get("reading")

    total_level = define_total_level(
        grammar=grammar,
        writing=writing,
        listening=listening,
        vocabulary=vocabulary,
        reading=reading
    )

    return levels, total_level
