from nose.tools import assert_equals, assert_raises
from nose.tools import istest

from trashcli.trash2 import parse_deletion_date
from trashcli.trash2 import parse_path

def test_how_to_parse_date_from_trashinfo():
    from datetime import datetime
    assert_equals(datetime(2000,12,31,23,59,58), parse_deletion_date('DeletionDate=2000-12-31T23:59:58'))
    assert_equals(datetime(2000,12,31,23,59,58), parse_deletion_date('DeletionDate=2000-12-31T23:59:58\n'))
    assert_equals(datetime(2000,12,31,23,59,58), parse_deletion_date('[TrashInfo]\nDeletionDate=2000-12-31T23:59:58'))

from trashcli.trash2 import maybe_parse_deletion_date
UNKNOWN_DATE='????-??-?? ??:??:??'
@istest
class describe_maybe_parse_deletion_date:
    @istest
    def on_trashinfo_without_date_parse_to_unknown_date(self):
        assert_equals(UNKNOWN_DATE, 
                      maybe_parse_deletion_date(a_trashinfo_without_deletion_date()))
    @istest
    def on_trashinfo_with_date_parse_to_date(self):
        from datetime import datetime
        example_date_as_string='2001-01-01T00:00:00'
        same_date_as_datetime=datetime(2001,1,1)
        assert_equals(same_date_as_datetime, 
                      maybe_parse_deletion_date(make_trashinfo(example_date_as_string)))
    @istest
    def on_trashinfo_with_invalid_date_parse_to_unknown_date(self):
        invalid_date='A long time ago'
        assert_equals(UNKNOWN_DATE,
                      maybe_parse_deletion_date(make_trashinfo(invalid_date)))

def test_parsing_invalid_dates():
    with assert_raises(ValueError):
        parse_deletion_date('DeletionDate=Wrong Date')

def test_how_to_parse_original_path():
    assert_equals('foo.txt',             parse_path('Path=foo.txt'))
    assert_equals('/path/to/be/escaped', parse_path('Path=%2Fpath%2Fto%2Fbe%2Fescaped'))


from trashcli.trash2 import LazyTrashInfoParser, ParseError

class TestParsing:
    def test_1(self):
        parser = LazyTrashInfoParser(lambda:("[TrashInfo]\n"
                                             "Path=/foo.txt\n"), volume_path = '/')
        assert_equals('/foo.txt', parser.original_location())

class TestLazyTrashInfoParser_with_empty_trashinfo:
    def setUp(self):
        self.parser = LazyTrashInfoParser(contents=an_empty_trashinfo, volume_path='/')

    def test_it_raises_error_on_parsing_original_location(self):
        with assert_raises(ParseError):
            self.parser.original_location()

    #def test_it_raises_error_on_parsing_deletion_date(self):
    #    with assert_raises(ParseError):
    #        self.parser.deletion_date()

def a_trashinfo_without_deletion_date():
    return ("[TrashInfo]\n"
            "Path=foo.txt\n")

def make_trashinfo(date):
    return ("[TrashInfo]\n"
            "Path=foo.txt\n"
            "DeletionDate=%s" % date)
def an_empty_trashinfo():
    return ''



