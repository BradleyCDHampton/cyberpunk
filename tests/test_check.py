import pytest
from cyberpunk.check import Check


class TestCheck:

    def always_passes(self):
        assert True

    def always_fails(self):
        assert False

