# try wrapping the code below that reads a persons.csv file in a class and make it more general such that it can read in any csv file
import csv
import os
import copy


class ReadCsv:
    def __init__(self, file_name=None):
        self.file_name = file_name
        self.data = []
        self.__location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))

    def read_csv(self):
        with open(os.path.join(self.__location__, self.file_name)) as f:
            rows = csv.DictReader(f)
            for r in rows:
                self.data.append(dict(r))

    def update_csv(self, table):
        file_name = os.path.join(self.__location__, f"{table.table_name}.csv")
        with open(file_name, "w", newline='') as my_file:
            fieldnames = set().union(*(d.keys() for d in table.table))
            writer = csv.DictWriter(my_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(table.table)


# add in code for a Database class
class Database:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None

    def str(self):
        return '\n'.join(map(str, self.database))


# add in code for a Table class
class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table
        self.readcsv = ReadCsv()

    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def __is_float(self, element):
        if element is None:
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            if self.__is_float(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
            else:
                temps.append(item1[aggregation_key])
        return function(temps)

    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def insert(self, data):
        self.table.append(data)
        self.readcsv.update_csv(self)

    def update(self, search_criteria, update_data, extra_argument=None):
        for row in self.table:
            if all(row[key] == value for key, value in search_criteria.items()):
                row.update(update_data)
        self.readcsv.update_csv(self)

    def get_schema(self):
        if len(self.table) > 0:
            return list(self.table[0].keys())
        else:
            return []

    def __str__(self):
        return self.table_name + ':' + str(self.table)

# modify the code in the Table class so that it supports the insert operation where an entry can be added to a list of dictionary

# modify the code in the Table class so that it supports the update operation where an entry's value associated with a key can be updated
