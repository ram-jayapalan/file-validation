"""
Unit test for helper module
"""

__Author__ = "Ram J"
__PyVersion__ = 3


from validatefile import helper
import pytest


class TestHelper(object):
    """Test class for Helper modules"""

    def test_empty(self):
        """
        Method to test empty function
        """
        assert helper.isempty('') is True
        assert helper.isempty(' ') is True
        assert helper.isempty('hello') is False

    def test_isnumeric(selfs):
        """
        Method to test numeric function
        """
        assert helper.isnumeric(3.0) is False
        assert helper.isnumeric('-3.00') is True
        assert helper.isnumeric('3') is True
        assert helper.isnumeric(3) is False
        assert helper.isnumeric('hello') is False
        assert helper.isnumeric('34h') is False

    def test_isinteger(self):
        """
        Method to test interger function
        """
        assert helper.isinteger('3') is True
        assert helper.isinteger(3) is False
        assert helper.isinteger('3.0') is False
        assert helper.isinteger(-3.00) is False
        assert helper.isinteger('hello') is False
        assert helper.isnumeric('34h') is False

    def test_isdecimal(self):
        """
        Method to test interger function
        """
        assert helper.isdecimal('3.0') is True
        assert helper.isdecimal(3.00) is False
        assert helper.isdecimal('3') is False
        assert helper.isdecimal(-3) is False
        assert helper.isdecimal('hello') is False
        assert helper.isdecimal('34h') is False

    def test_isexpectedformat(self):
        """
        Method to test expected format function
        """
        assert helper.isexpectedformat(string='hello', pattern='\\d+') is False
        assert helper.isexpectedformat(string='hello', pattern='\\w+') is True
        assert helper.isexpectedformat(string='hello', pattern='hello') is True
        assert helper.isexpectedformat(string='t@e.com',
                                       pattern='[^@]+@[^@]+\\.[^@]+') is True
        assert helper.isexpectedformat(string='t@e.com',
                                       pattern='[^@]+@[^@]+\\.[^@]+',
                                       count=1) is True
        assert helper.isexpectedformat(string='t@e.com',
                                       pattern='[^@]+@[^@]+\\.[^@]+',
                                       count=2) is False
        pytest.raises(ValueError, helper.isexpectedformat, string='t@e.com',
                      pattern='[^@]+@[^@]+\\.[^@]+', count=0)
        assert helper.isexpectedformat(string='hello',
                                       pattern='Hello') is False
        assert helper.isexpectedformat(string='hello', pattern='Hello',
                                       ignorecase=True) is True

    def test_isexpectedlength(self):
        """
        Method to test expected length function
        """
        assert helper.isexpectedlength(value='hello', maxvalue=5) is True
        assert helper.isexpectedlength(value='hello', maxvalue=3) is False
        assert helper.isexpectedlength(value='hello', maxvalue=5,
                                       minvalue=1) is True
