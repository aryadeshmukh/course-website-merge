import json
import os

SAVE_FILE = './db.txt'

class Database:
    '''
    Implements a databse structure by storing each record as json data in a separate file.

    ...

    Attributes
    ----------
    primary_keys : list
        maps primary key index to file containing record data
    next_record_index : int
        file index value assigned to next new record

    Methods
    -------
    save_state():
        Marshals database state and stores it into SAVE_FILE.
    add_record(new_record):
        Stores new_record in database and assigns it a unique primary key.
    get_record(index):
        Retrieves record assigned to index from database.
    delete_record(index):
        Deletes record assigned to index from database.
    list_records():
        Returns a list of all records in the database.
    load_state(info_dict):
        Loads a database with state saved in info_dict.
    
    '''
    def __init__(self, primary_keys: list[object] = [], next_record_index: int = 0) -> None:
        '''
        Creates or loads a new database.
        
        Keyword arguments:
        primary_keys -- existing database to be loaded, empty list by default
        '''
        self.primary_keys = primary_keys
        self.next_record_index = next_record_index
        self.save_state()
    
    def save_state(self) -> None:
        '''Marshals database state and stores it into SAVE_FILE.'''
        info_dict = {
            'primary-keys' : self.primary_keys,
            'next-record-index' : self.next_record_index
        }
        with open(SAVE_FILE, 'w') as file:
            file.write(json.dumps(info_dict))

    def add_record(self, new_record: object) -> None:
        '''
        Stores new_record in database and assigns it a unique primary key.
        
        Keyword arguments:
        new_record -- new record to be added to the database
        '''
        try:
            # Create new file in database directory to store record data
            new_file_name = f'record_{self.next_record_index}'
            self.next_record_index += 1
            os.path.join('./records/', new_file_name)

            self.primary_keys.append(new_file_name)

            # Store record data into new file
            with open(f'./records/{new_file_name}', 'w') as file:
                file.write(json.dumps(new_record))

            self.save_state()
        except:
            pass
    
    def get_record(self, index: int) -> object:
        '''
        Retrieves record assigned to index from database.

        Returns None if no record is assigned to index or is failure occurs during retrieval or record.

        Keyword arguments:
        index -- index assigned to record to be retrieved
        '''
        try:
            if index < 0 or index >= len(self.primary_keys):
                raise IndexError()

            record = None
            with open(f'./records/{self.primary_keys[index]}', 'r') as file:
                record = json.loads(file.read())
            return record
        except Exception:
            return None
    
    def delete_record(self, index: int) -> None:
        '''
        Deletes record assigned to index from database.

        If no record is assigned to index, the state of the database remains unchanged.

        Keyword arguments:
        index -- index assigned to record to be deleted
        '''
        try:
            if index < 0 or index >= len(self.primary_keys):
                raise IndexError()
            
            os.remove(f'./records/{self.primary_keys[index]}')
            self.primary_keys.pop(index)

            self.save_state()
        except Exception:
            pass
    
    def list_records(self) -> list[object]:
        '''Returns a list of all records in the database.'''
        records = []
        for i in range(len(self.primary_keys)):
            records.append(self.get_record(i))
        return records
    
    def contains(self, item: object) -> bool:
        '''
        Returns whether an object is currently stored in the database.

        Keyword arguments:
        item -- object to be searched for in database
        '''
        return item in self.list_records()
    
    def clear(self) -> None:
        '''Deletes all records from database.'''
        num_records = len(self.list_records())
        self.next_record_index = 0
        for i in range(num_records):
            self.delete_record(num_records - i - 1)
    
    @staticmethod
    def load_state() -> 'Database':
        '''
        Loads a database with state saved in info_dict.

        Returns a new database if any error occurs.
        '''
        try:
            with open(SAVE_FILE, 'r') as file:
                info_dict = json.loads(file.read())
                return Database(info_dict['primary-keys'], info_dict['next-record-index'])
        except Exception:
            db = Database()
            db.save_state()
            return db