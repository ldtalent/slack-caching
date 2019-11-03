from nose.tools import *
import slack

def setup():
    """Setup tests."""
    pass

def teardown():
    """Tear down tests."""
    pass

def test_get_version():
    assert type(slack.get_version()) == str
