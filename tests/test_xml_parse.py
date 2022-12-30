import unittest
import sqlite3
import os
from parser import xml_parse
from writers import database

class TestXmlParse(unittest.TestCase):
    def test_xml_parse(self):
        """Check if queries to table are as expected."""
        # Create answer dictionary.
        answer1 = ('Alice', '123 Main', 'October', '11', 'Consulting', None, None)
        answer2 = ('Bob', '456 North', None, None, 'Marketing', None, None)
        answer3 = ('Carol', '789 South', None, None, 'Advertising', 'Texas', 'Houston')
        answer_dict = {}
        answer_dict['Alice']=answer1
        answer_dict['Bob']  =answer2
        answer_dict['Carol']=answer3
        # Run tests.
        os.getcwd() + "/"
        con = sqlite3.connect(os.getcwd() + "/data/database/friends.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM person")
        row1 = cur.fetchone()
        self.assertEqual(row1, answer_dict[row1[0]])
        row2 = cur.fetchone()
        self.assertEqual(row2, answer_dict[row2[0]])
        row3 = cur.fetchone()
        self.assertEqual(row3, answer_dict[row3[0]])

if __name__ == '__main__':
    unittest.main()



