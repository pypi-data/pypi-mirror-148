from os.path import exists as path_exists
import csv
import functools
import collections
from datetime import datetime
import logging

logger = logging.getLogger('csv')

def property_accessor(path):

    def rgetattr(obj, *args):
        def _getattr(o, a):
            result = None
            try:
                if o is None:
                    result = None
                elif isinstance(o, collections.abc.Mapping):
                    result = o.get(a)
                else:
                    result = getattr(o, a, *args)
                if (result and callable(result)):
                    result = result()
            except RuntimeError as err:
                logger.warning(f'failed to get attribute {a} from {o.__dict__}: {err}')
            return result

        if '.' in path:
            return functools.reduce(_getattr, [obj] + path.split('.'))
        return _getattr(obj, path, *args)

    return rgetattr

def _generate_filename(name):
    date = datetime.now().strftime("%Y-%m-%d-%H%M")
    return "{}-{}.csv".format(name, date)

def _generate_headers(mapping):
    return list(map(lambda m: m[0], mapping))
    
def _generate_mapping_functions(mapping):
    return list(map(lambda m: (m[0], property_accessor(m[1])), mapping))

def _generate_index_function(headers):
    def func(row):
        s = ""
        for header in headers:
            val = row.get(header)
            if (val):
                s += val
        return hash(s)
    return func    

    
class CsvExport(object):
    
    def __init__(self, name, mapping, filename=None, export_dir = "export/"):
        self.name = name
        self.filename = filename or _generate_filename(name)
        self.filepath = export_dir + self.filename
        self.mapping = _generate_mapping_functions(mapping)
        self.headers = _generate_headers(mapping)
        self.header_written = path_exists(self.filepath)
        self._indexers = []
        self._index = set()

    def index(self, *headers):
        indexer = _generate_index_function(headers)
        self._index_file(indexer)
        self._indexers.append(indexer)
        
    def write_record(self, value):
        with open(self.filepath, 'a', newline='') as csvfile:
            logger.info(f'writing CSV {self.filepath}')
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            
            # write header if not written
            if (not self.header_written):
                logger.info(f'writing headers {self.headers}')
                writer.writeheader()
                self.header_written = True
            
            # write the record
            row = self._value_to_row(value)
            logger.info(f'writing row {row}')
            writer.writerow(row)
            self._index_row(row)
    
    def exists(self, value):
        row = self._value_to_row(value)
        for indexer in self._indexers:
            hash = indexer(row)
            if hash in self._index:
                return True
        return False        

    def _value_to_row(self, value):
        row = {}
        for mapping in self.mapping:
            func = mapping[1]
            row[mapping[0]] = func(value)
        return row

    def _index_file(self, indexer):
        count = 0
        if (path_exists(self.filepath)):
            with open(self.filepath, 'r', newline='') as csvfile:
                reader = csv.DictReader(csvfile, fieldnames=self.headers)
                for row in reader:
                    self._index.add(indexer(row))
                    count += 1
        logger.info(f'indexed {count} records')
    
    def _index_row(self, row):
        for indexer in self._indexers:
            self._index.add(indexer(row))    
        