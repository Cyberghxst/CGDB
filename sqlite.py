import sqlite3
from typing import AnyStr

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
        Starts the Database class and creates the given tables.

        Parameters
        ----------
        dir: str
            The database file path.
        tables: list[str]
            The table names.

        Returns
        ----------
        None
        """
        self.__conection = sqlite3.connect(dir)
        self.__cursor = self.__conection.cursor()
        self.dir = dir
        self.body = {}
        self.tables = tables or ["main"]

        # Creates the tables if doesn't exists.
        for table in tables:
            try:
                self.__conection.execute(f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    key TEXT PRIMARY KEY,
                    value TEXT
                )
                """)
            except Exception as error:
                print(error)
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
        try:
            self.__cursor.execute(f"INSERT INTO {table} VALUES (?, ?)", (key, value))
            self.__conection.commit()
        except:
            self.__cursor.execute(f"UPDATE {table} SET value=? WHERE key=?", (value, key))
            self.__conection.commit()
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
        try:
            self.__cursor.execute(f"SELECT * FROM {table} WHERE key=?", (key,))
            result = lambda self: [{ "key": x[0], "value": x[1] } for x in self.__cursor.fetchall()]
            return result(self) or []
        except Exception as error:
            print(f"CGDB :: {error}")

    def delete(self, key: str, table: str) -> bool:
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
        try:
            self.__cursor.execute("DELETE FROM ? WHERE key=?", (table, key))
            self.__conection.commit()
            return True
        except:
            return False
        
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
        try:
            self.__cursor.execute("SELECT * FROM ? WHERE key=?", (table, key))
            if len(self.__cursor.fetchall()) > 0:
                return True
            else:
                return False
        except:
            return False
        
    def all(self, table: str) -> list:
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
        all = []
        try:
            self.__cursor.execute("SELECT * FROM ?", (table,))
            data = self.__cursor.fetchall()
            for tupla in data:
                all.append({ "key": tupla[0], "value": tupla[1] })
            return all
        except:
            return all
    
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
        if not table in self.tables:
            return False
        else:
            return True