import unittest
import sqlite3
import os
from parser import xml_parse
from writers import database

class TestXmlParse(unittest.TestCase):
    def test_xml_parse(self):
        os.getcwd() + "/"
        con = sqlite3.connect(os.getcwd() + "/data/database/friends.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM person")
        row1 = cur.fetchone()
        answer1 = ('Alice', '123 Main', 'October', 'Consulting')
        self.assertEqual(row1, answer1)
        row2 = cur.fetchone()
        answer2 = ('Bob', '456 North', None, 'Marketing')
        self.assertEqual(row2, answer2)

if __name__ == '__main__':
    unittest.main()



