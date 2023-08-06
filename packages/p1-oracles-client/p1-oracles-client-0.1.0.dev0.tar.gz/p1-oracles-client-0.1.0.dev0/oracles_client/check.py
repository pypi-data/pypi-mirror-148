import os
import sys
from pathlib import Path

import requests

import p1
from . utils import _assert, _abort, cli

HELP_MSG = ("usage: \n"
            "   p1-oracles-check <name> <tests> [--url <url>] [--token <token>]\n"
            "\n"
            "you can use set environment variables:\n"
            "   - P1_ORACLE_SERVER_URL\n"
            "   - P1_ORACLE_SERVER_TOKEN\n")


def pop_url(args):
    try:
        arg_index = args.index("--url")
        args.pop(arg_index)
        return args.pop(arg_index)

    except ValueError:
        # não há --url
        pass

    except IndexError:
        # há --url, mas não há argumento logo após
        _assert(url, "missing --url value")

    return os.environ.get("P1_ORACLE_SERVER_URL") or p1.get_config().get("oracle-url")


def pop_token(args):
    try:
        arg_index = args.index("--token")
        args.pop(arg_index)
        return args.pop(arg_index)

    except ValueError:
        # no --token
        pass

    except ValueError:
        # --token without value
        _assert(token, "no url defined")

    token = os.environ.get("P1_ORACLE_SERVER_URL")
    if not token:
        token_path = Path("~/.p1/oracle-token.jwt").expanduser()
        if token_path.exists():
            token = open(token_path, "r").read()

    return token


def pop_name_and_tests(args):
    test_suite = args.pop()
    oracle_name = args.pop()
    return oracle_name, test_suite


def help():
    return HELP_MSG

@cli
def check():
    args = sys.argv[:]
    if len(args) < 3:
        print(HELP_MSG, file=sys.stderr)
        sys.exit(1)

    _assert(len(args) <= 7, help())
    url = pop_url(args)
    token = pop_token(args)
    _assert(len(args) == 3, help())
    oracle_name, test_suite = pop_name_and_tests(args)

    #print(f"oracle: {oracle_name}")
    #print(f"tests: {test_suite}")
    #print(f"url: {url}")
    #print(f"token: {token}")
    #print("----")
    #sys.exit(1)

    _assert(Path(test_suite).exists(), f"file {test_suite} not found")
    response = requests.post(
        f"{url}/oracle/{oracle_name}/check",
        headers={"Authorization": f"Bearer {token}"},
        files={'tests': open(test_suite, "rb")}
    )

    payload = response.json()
    if response.status_code != 200:
        _abort(payload.get("error", "error reported by server"))

    return payload
