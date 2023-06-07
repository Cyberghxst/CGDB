import json, pydash as _
from typing import AnyStr
from os import path, makedirs

class CGDB:
    """
    A class to start a table-based database with a key-value interface.
    ...

    Attributes
    ----------
    path: str
        The database files path.
    tables: list[str]
        The database tables.

    Methods
    ----------
    set(key: str, value: str, table: str)
        Sets the provided data in the given table.
    get(key: str, table: str)
        Gets the given key from the provided table.
    has(key: str, table: str)
        Checks if the given key exists in the provided table.
    delete(key: str, table: str)
        Deletes the provided data from the given table.
    all(table: str)
        Return every value stored in the given database table inside a list.
    """
    def __init__(self, dir: str, tables: list[str]) -> None:
        """
        Starts the Database class and creates table files.

        Parameters
        ----------
        path: str
            The database files path.
        tables: list[str]
            The table names.

        Returns
        ----------
        None
        """
        self.dir = dir
        self.body = {}
        self.tables = tables or ["main"]

        # Creates the tables if doesn't exists.
        for table in tables:
            if not path.exists(self.dir):
                makedirs(self.dir)
            if not path.isfile(f"{self.dir}/{table}.json"):
                try:
                    file = open(f"{self.dir}/{table}.json", "w")
                    file.write(json.dumps(self.body))
                    file.close()
                except Exception as error:
                    print(error)

    def __append(self, table: str, data: dict) -> None:
        """
        Appends data to the given table.

        Parameters
        ----------
        table: str
            The database table.
        data: dict
            The given data to append into the table.

        Returns
        ----------
        None
        """
        if not self.__check_table(table):
            raise Exception(f"CGDB :: Invalid table \"{table}\" provided!")
        with open(f"{self.dir}/{table}.json", "w") as file:
            file.write(json.dumps(data))
            file.close()
        return
    
    def __check_table(self, table: str) -> bool:
        """
        Checks whether a table is valid or not.

        Parameters
        ----------
        table: str
            The database table.

        Returns
        ----------
        Boolean
        """
        if not path.isfile(f"{self.dir}/{table}.json"):
            return False
        else:
            return True
        
    def __get_table(self, table: str) -> dict | None:
        """
        Gets an table data.

        Parameters
        ----------
        table: str
            The database table.

        Returns
        ----------
        dict | None
        """
        if not self.__check_table(table):
            raise Exception(f"CGDB :: Invalid table \"{table}\" provided!")
        try:
            with open(f"{self.dir}/{table}.json", "r") as file:
                if not file:
                    return None
                else:
                    return json.loads(file.read())
        except:
            return None
        
    def set(self, key: str, value: str, table: str) -> None:
        """
        Sets the provided data in the given table.

        Parameters
        ----------
        key: str
            The variable key.
        value: str
            The variable value.
        table: str
            The database table.

        Returns
        ----------
        None
        """
        if not self.__check_table(table):
            raise Exception(f"CGDB :: Invalid table \"{table}\" provided!")
        content = self.__get_table(table) or self.body
        _.set_(content, key, value)
        self.__append(table, content)
        return None
    
    def get(self, key: str, table: str) -> AnyStr:
        """
        Gets the provided data from the given table.

        Parameters
        ----------
        key: str
            The variable key.
        table: str
            The database table.

        Returns
        ----------
        AnyStr
        """
        if not self.__check_table(table):
            raise Exception(f"CGDB :: Invalid table \"{table}\" provided!")
        content = self.__get_table(table) or self.body
        return _.get(content, key)
    
    def delete(self, key: str, table: str) -> None:
        """
        Deletes the provided data from the given table.

        Parameters
        ----------
        key: str
            The variable key.
        table: str
            The database table.

        Returns
        ----------
        None
        """
        if not self.__check_table(table):
            raise Exception(f"CGDB :: Invalid table \"{table}\" provided!")
        content = self.__get_table(table)
        if not content:
            return None
        if not self.has(key, table):
            return None
        _.unset(content, key)
        self.__append(table, content)
        return None
    
    def has(self, key: str, table: str) -> bool:
        """
        Checks if the given key exists in the provided table.

        Parameters
        ----------
        key: str
            The variable key.
        table: str
            The database table.

        Returns
        ----------
        Boolean
        """
        if not self.__check_table(table):
            raise Exception(f"CGDB :: Invalid table \"{table}\" provided!")
        content = self.__get_table(table)
        return key in content

    def all(self, table: str) -> dict:
        """
        Returns all saved data from the given table inside a list.

        Parameters
        ----------
        table: str
            The database table.

        Returns
        ----------
        list
        """
        if not self.__check_table(table):
            raise Exception(f"CGDB :: Invalid table \"{table}\" provided!")
        content = self.__get_table(table) or self.body
        final = []
        if len(content) > 0:
            temp = {}
            for i in range(0, len(content)):
                temp["key"] = list(content.keys())[i]
                temp["value"] = list(content.values())[i]
                final.append(temp)
                temp = {}
        return final