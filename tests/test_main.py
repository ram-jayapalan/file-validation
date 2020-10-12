__Author__ = "Ram J"
__PyVersion__ = 3


from validatefile.main import ValidateFile
import os
import pytest


class TestValidateFile:

    @pytest.fixture
    def init_class(self):
        """
        Validate file class instantiation block
        """
        testdir = os.path.abspath(os.path.dirname(__file__))
        configfile = os.path.join(testdir, 'static', 'fieldchecks.ini')
        sourcefile = None
        return ValidateFile(configfile=configfile, sourcefile=sourcefile)

    def test_filename(self, init_class):
        """
        Method to test filename validation with the given pattern
        """
        filename = 'sample_20200501.csv'
        assert bool(init_class._validatefilename(value=filename)) is False
        filename = 'sample_yyyymmdd.csv'
        assert bool(init_class._validatefilename(value=filename)) is True
        filename = 'sample_20200301'
        assert bool(init_class._validatefilename(value=filename)) is True
        filename = ''
        assert bool(init_class._validatefilename(value=filename)) is True

    def test_validateheader(self, init_class):
        """
        Method to test header validation
        """
        init_class._dictconfig['HCaseSensitive'] = True
        header = ['Id', 'firstname', 'lastname', 'email', 'numericcolumn',
                  'count', 'integercolumn', 'decimalcolumn', 'formatcolumn1',
                  'formatcolumn2', 'lengthcolumn1', 'lengthcolumn2']
        assert bool(init_class._validateheader(value=header)) is False
        header = ['Id', 'firstname', 'lastname', 'email', 'numericcolumn',
                  'count', 'integercolumn', 'decimalcolumn', 'formatcolumn1',
                  'formatcolumn2', 'lengthcolumn1']
        assert bool(init_class._validateheader(value=header)) is True
        init_class._dictconfig['HCaseSensitive'] = False
        header = ['id', 'Firstname', 'lastname', 'Email', 'numericcolumn',
                  'count', 'integercolumn', 'decimalcolumn', 'formatcolumn1',
                  'formatcolumn2', 'lengthcolumn1', 'lengthcolumn2']
        assert bool(init_class._validateheader(value=header)) is False

    def test_validateheadercount(self, init_class):
        """
        Method to test header count validation block
        """
        header = ['Id', 'firstname', 'lastname', 'email', 'numericcolumn',
                  'count', 'integercolumn', 'decimalcolumn', 'formatcolumn1',
                  'formatcolumn2', 'lengthcolumn1', 'lengthcolumn2']
        assert bool(init_class._validateheadercount(value=header)) is False
        header = ['Id', 'firstname', 'lastname', 'email', 'numericcolumn',
                  'count', 'integercolumn', 'decimalcolumn', 'formatcolumn1',
                  'formatcolumn2', 'lengthcolumn1']
        assert bool(init_class._validateheadercount(value=header)) is True

    def test_validaterecord_response(self, init_class):
        """
        Method to test _validaterecord() response
        """
        record = {
            'id': '1',
            'firstname': 'Ram',
            'lastname': 'J',
            'email': 'ram@test.com'
        }
        assert isinstance(init_class._validaterecord(value=record),
                          dict)
        assert bool(init_class._validaterecord(value=record)) is False

    def test_emptycheck(self, init_class):
        """
        Method to test empty check logic
        """
        record = {
            'id': '',
            'firstname': 'Ram',
            'lastname': 'J',
            'email': ''
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 2
        assert init_class._validaterecord(
            value=record)['ErrorCount']['EmptyCheck'] == 2

    def test_numericcheck(self, init_class):
        """
        Method to test numeric check logic
        """
        record = {
            'numericcolumn': 'ten'
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['NumericCheck'] == 1
        record = {
            'numericcolumn': '-10.0'
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'numericcolumn': '+10'
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'numericcolumn': '10'
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'numericcolumn': ''
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'count': ''
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['EmptyCheck'] == 1

    def test_integercheck(self, init_class):
        """
        Method to test integer check logic
        """
        record = {
            'integercolumn': 'ten'
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['IntegerCheck'] == 1
        record = {
            'integercolumn': '-10.0'
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['IntegerCheck'] == 1
        record = {
            'integercolumn': '+10'
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'integercolumn': '-10'
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'integercolumn': '0.0'
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['IntegerCheck'] == 1
        record = {
            'integercolumn': ''
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'count': ''
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['EmptyCheck'] == 1

    def test_decimalcheck(self, init_class):
        """
        Method to test decimal check logic
        """
        record = {
            'decimalcolumn': 'ten'
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['DecimalCheck'] == 1
        record = {
            'decimalcolumn': '+10'
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['DecimalCheck'] == 1
        record = {
            'decimalcolumn': '+0.0'
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'decimalcolumn': '-10.0'
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'decimalcolumn': '0'
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['DecimalCheck'] == 1
        record = {
            'decimalcolumn': ''
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'count': ''
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['EmptyCheck'] == 1

    def test_formatcheck(self, init_class):
        """
        Method to test decimal check logic
        """
        record = {
            'formatcolumn1': 'test@@test.com'
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['FormatCheck'] == 1
        record = {
            'formatcolumn1': 'test.com'
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['FormatCheck'] == 1
        record = {
            'formatcolumn1': 'test@test.com'
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'formatcolumn2': 'Hello'
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'count': ''
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['EmptyCheck'] == 1

    def test_lengthcheck(self, init_class):
        """
        Method to test decimal check logic
        """
        record = {
            'lengthcolumn1': '1'
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['LengthCheck'] == 1
        record = {
            'lengthcolumn1': 'tests_'
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['LengthCheck'] == 1
        record = {
            'lengthcolumn1': 'tests'
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'lengthcolumn1': 'Hello'
        }
        assert bool(init_class._validaterecord(value=record)) is False
        record = {
            'count': ''
        }
        assert bool(init_class._validaterecord(value=record)) is True
        assert len(init_class._validaterecord(
            value=record)['Error']) == 1
        assert init_class._validaterecord(
            value=record)['ErrorCount']['EmptyCheck'] == 1

    def test_getresult(self, tmpdir):
        """
        Method to test getresult() logic
        """
        testdir = os.path.abspath(os.path.dirname(__file__))
        configfile = os.path.join(testdir, 'static', 'fieldchecks.ini')
        tempdir = tmpdir.mkdir('test')
        sourcefile = tempdir.join('sample_20200301.csv')
        sourcefile.write(b'Id,firstname,lastname,email,numericcolumn,count,'
                         b'integercolumn,decimalcolumn,formatcolumn1,'
                         b'formatcolumn2,lengthcolumn1,lengthcolumn2\n'
                         b'1,Ram,Jayapalan,test@gmail.com,-123,141,12,10.20,'
                         b'sample@email.com,Hello,CDE,rj\n')
        assert os.path.exists(sourcefile) is True
        init_class = ValidateFile(sourcefile=sourcefile, configfile=configfile)
        assert isinstance(init_class.getresult(), dict) is True
        assert isinstance(init_class.getresult(outputdir=tempdir), dict) is \
            True
        res = init_class.getresult(outputdir=tempdir)
        assert bool(res) is True
        assert os.path.exists(res['Results']['OutputFile']) is True
        res = init_class.getresult()
        assert bool(res['Results']['OutputFile']) is False
        sourcefile = tempdir.join('sample_20200301.csv')
        sourcefile.write(b'Id,firstname,lastname,email,numericcolumn,count,'
                         b'integercolumn,decimalcolumn,formatcolumn1,'
                         b'formatcolumn2,lengthcolumn1,lengthcolumn2\n'
                         b'1,Ram,Jayapalan,test@gmail.com,-123,141,12,10,'
                         b'sampleemail.com,Hello,CDE,rj\n')
        init_class = ValidateFile(sourcefile=sourcefile, configfile=configfile)
        res = init_class.getresult()
        assert bool(res['Results']['ErrorDetails']) is True
        assert res['Results']['ErrorDetails'][0]['DecimalCheck'] == 1
        assert res['Results']['ErrorDetails'][0]['FormatCheck'] == 1
