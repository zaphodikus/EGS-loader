# a line in the file
from egs_read import ALine


def test_emptyline():
    assert str(ALine('#')) == ""

def test_commentline():
    assert str(ALine('# acomment')) == ""
    assert str(ALine('  #')) == "" # spaces line with only a comment on it
    assert str(ALine("\t\t\t#")) == "" # tabs line with only a comment on it


def test_singleLine():
    l = ALine("hello world", 42)
    assert str(l) == "hello world"


def test_single_number():
    l = ALine("hello world", 42)
    assert l.line == 42

