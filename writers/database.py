import sqlite3
import os

# write to sqlite3 database
class DbWriter:
    def __init__(self, subdir="data/database"):
        self.directory = os.getcwd() + "/" + subdir

    def get_conn_to_new_db(self,filename):
        try:
            os.remove(self.directory+ "/" + filename + ".db")
        except OSError:
            pass
        con = sqlite3.connect(self.directory+ "/" + filename + ".db")
        cur = con.cursor()
        return con, cur

    def create_table(self, cur, tablename, columns, len_common_prefix):
        """ Create table with cursor cur with the given table name and columns."""
        query = "CREATE TABLE " + tablename + "(" 
        allcols = ""
        for col in columns:
            if allcols == "":
                allcols += col
            else:
                allcols += ", " + col
        query += allcols + ")"
        cur.execute(query)

    def insert_row(self, con, cur, table, value_dict_list, len_common_prefix):
        """ Insert one row of values into a given table.
        Assumes all columns exist in the table.
        Assume value_dict_list is list of key-value pairs,
        where key is column name and value is value to be inserted.
        """
        # Get list of column names and list of values ordered the same.
        cols = ""
        vals = ""
        for i,d in enumerate(value_dict_list):
            if len(d)!=1:
                print("ERROR")
            for col,val in d.items(): # there should be only one item
                if i==0:
                    cols += "'" + col + "'"
                    vals += "'" + val + "'"
                else:
                    cols += ", " + "'" + col + "'" 
                    vals += ", " + "'" + val + "'"
        query  = "INSERT INTO " + table + "("
        query += cols + ") VALUES("
        query += vals + ")"
        cur.execute(query)
        con.commit()



