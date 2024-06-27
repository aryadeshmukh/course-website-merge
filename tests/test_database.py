import pytest
import sys
import os

# Add the parent directory of the 'database' package to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Database

@pytest.fixture(scope='module')
def db() -> Database:
    '''Returns a clean database.'''
    db = Database()
    db.clear()
    return db

def test_add_record(db):
    '''Tests add_record.'''
    db.add_record('test1')
    assert db.list_records() == ['test1']

def test_delete_record(db):
    '''Tests delete_record.'''
    db.delete_record(0)
    assert db.list_records() == []

def test_add_and_delete(db):
    '''Tests adding and deleting records.'''
    db.add_record(['test1', 'pass1'])
    db.add_record('test2')
    db.add_record('test3')
    db.delete_record(1)
    assert db.list_records() == [['test1', 'pass1'], 'test3']

@pytest.mark.parametrize('test_index, expected', [(0, ['test1', 'pass1']), (1, 'test3'), (2, None), (-1, None)])
def test_get_record(db, test_index, expected):
    '''Tests get record.'''
    assert db.get_record(test_index) == expected

@pytest.mark.parametrize('test_index', [2, -1])
def test_delete_fail(db, test_index):
    '''Tests delete failure.'''
    db.delete_record(test_index)
    assert db.list_records() == [['test1', 'pass1'], 'test3']

def test_add_after_delete(db):
    '''Tests adding a record after deletion.'''
    db.add_record('test4')
    assert db.list_records() == [['test1', 'pass1'], 'test3', 'test4']

@pytest.mark.parametrize('test_value, expected', [
    (['test1', 'pass1'], True),
    ('test2', False),
    ('test3', True),
    ('test4', True)])
def test_contains(db, test_value, expected):
    '''Tests contains method.'''
    assert db.contains(test_value) == expected

def test_persistence(db):
    '''Tests persistence of database.'''
    original_records = db.list_records()
    loaded_db = Database.load_state()
    assert loaded_db.list_records() == original_records

def test_clear(db):
    '''Tests clearing of database.'''
    db.clear()
    assert db.list_records() == []