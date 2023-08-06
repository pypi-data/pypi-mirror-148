import time
from behave import step


@step(u"I wait for {timeout:d} seconds")
def wait_for_timeout(context, timeout):
    time.sleep(timeout)

