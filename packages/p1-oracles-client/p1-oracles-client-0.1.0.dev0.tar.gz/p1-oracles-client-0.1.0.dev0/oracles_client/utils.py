import sys


def _assert(condition, msg, exception_class=AssertionError):
    if not condition:
        raise exception_class(msg)


def _abort(msg, exception_class=AssertionError):
    _assert(False, msg, exception_class)


def cli(func):
    def wrapper():
        try:
            return func()

        except AssertionError as e:
            print(f"error: {e}", file=sys.stderr)

        except Exception as e:
            raise e

    return wrapper
