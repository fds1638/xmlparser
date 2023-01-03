from readers import reader
from writers import database
import string

def getOpeningTag(s, i):
    """ Get an xml opening tag: <tag>."""
    tag = ""
    while s[i]=='<':
        i += 1
    while s[i]!='>':
        tag = tag + s[i]
        i += 1
    return tag.strip(), i+1

def getClosingTag(s, i):
    """ Get an xml closing tag: </tag>."""
    tag = ""
    while s[i]=='<' or s[i]=='/':
        i += 1
    while s[i]!='>':
        tag = tag + s[i]
        i += 1
    return tag.strip(), i+1

def getElementText(s, i):
    """ Get the text from an xml element: <tag>text</tag>."""
    val = ""
    while s[i]!='<':
        val = val + s[i]
        i += 1
    return val.strip(), i

def get_col_list(col_dict):
    """ Assume col_dict has keys of column names and values of column order.
    First create a list with the correct number of elements.
    Then go through and populate the list by putting each column name in its place.
    Note: it seems that dictionary iteration order is guaranteed to be consistent
    in Python 3.7+, but it may not be the order we want.
    """
    col_list = ["" for i in range(len(col_dict))]
    for k, v in col_dict.items():
        col_list[v]=k
    return col_list

def write_to_database(filename, tablename, col_list, values_row_list):
    db = database.DbWriter()
    con, cur = db.get_conn_to_new_db(filename)
    db.create_table(cur,tablename,col_list)
    for value_row in values_row_list:
        db.insert_row(con,cur,tablename,value_row)

def get_xml_from_file(f):
    """ Given a file f, return the xml in a string s."""
    lines = f.readlines()
    s = ""
    for line in lines:
        line = line.replace("\n","")
        if s=="": s = line
    return s

def xml_lexer(s):
    """ Input: xml string s. Output: list of tuples (token, token type) where both are strings and
    token type is from the set ("ot", "val", "ct") i.e. opening tag, value, or closing tag.
    """
    tags_and_types = []
    i=0
    while i < len(s):
        value = ""
        while s[i]==string.whitespace:
            i += 1
        if s[i]=='<':
            if s[i+1]=='/':
                tag, i = getClosingTag(s,i)
                tags_and_types.append((tag,"ct"))
            else:
                tag, i = getOpeningTag(s,i)
                tags_and_types.append((tag,"ot"))
        else:
            value, i = getElementText(s, i)
            tags_and_types.append((value,"val"))
    return tags_and_types

def get_rows_from_lexer(tags_and_types):
    """ Given a list of tags_and_types output by the xml_lexer, return:
    db_name: the first tag, the name of the database,
    table_name: the second tag, the name of the table,
    col_list: a list of columns of the table,
    end_output: list of lists of key-value pairs where key is column and value is value,
                and each list is one row.
    """
    tag_stack = []
    end_output = []
    c2 = {}
    cur_output = []
    # Method:
    # If it's an opening tag:
    #     if it's the first tag, it's the db_name
    #     if it's the second tag, it's the table_name
    #     update the prefix for use as a column name
    #     if the next tag is a val, record the column name and its place in the order
    # If it's a val tag:
    #    record the value
    # If it's a closing tag:
    #    remove from prefix
    #    if it matches the table_name, it's the end of a row, so process the row
    #    One: the next tag is a val, in which case put the prefix in the column list
    #    Two: the next tag is not a val, in 
    i=0
    prefix = ""
    row_tag = "person"
    while i < len(tags_and_types):
        tat = tags_and_types[i]
        if tags_and_types[i][1]=="ot":
            if i==0: db_name = tat[0]
            elif i==1: table_name = tat[0]
            elif tags_and_types[i][0]!=db_name and tags_and_types[i][0]!=table_name: 
                prefix = tags_and_types[i][0] if prefix=="" else prefix + "_" + tags_and_types[i][0]
            if tags_and_types[i+1][1]=="val":
                if prefix not in c2.keys():
                    c2[prefix] = len(c2)
        elif tags_and_types[i][1]=="val":
            cur_output.append({prefix:tags_and_types[i][0]})
        else:
            num_chars_to_delete = len(tags_and_types[i][0])+1
            prefix = prefix[:-1*num_chars_to_delete]
            if tags_and_types[i][0]==tags_and_types[1][0]:
                end_output.append(cur_output)
                cur_output=[]
        i += 1
    col_list = get_col_list(c2)
    return db_name, table_name, col_list, end_output
 
def parse_xml_to_db(filename):
    r = reader.Reader()
    f = r.get_xml_file(filename)
    xml_string = get_xml_from_file(f) 
    tags_and_types = xml_lexer(xml_string)
    db_name, table_name, col_list, values_row_list = get_rows_from_lexer(tags_and_types)
    write_to_database(db_name, table_name, col_list, values_row_list)
    f.close()

