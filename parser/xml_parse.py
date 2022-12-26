from readers import reader
from writers import database

def getOpeningTag(s, i):
    """ Get the text from an xml opening tag: <text>."""
    tag = ""
    while s[i]=='<':
        i += 1
    while s[i]!='>':
        tag = tag + s[i]
        i += 1
    return tag, i+1

def getClosingTag(s, i):
    """ Get the text from an xml closing tag: </text>."""
    tag = ""
    while s[i]=='<':
        i += 1
    while s[i]!='>':
        tag = tag + s[i]
        i += 1
    return tag, i+1

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

def get_rows_from_xml(s):
    """ Given a valid xml string s, return the list of columns in the table to be created
    and the values rows to be inserted in the table.
    """
    current_tag = ""
    tag_stack = []
    child_map = {}
    i = 0
    end_output = []
    columns = set()
    c2 = {}
    cur_output = []
    while i <len(s):
        value = ""
        while s[i]!='<':
            value = value + s[i]
            i += 1
        if s[i+1]=='/':
            tag, i = getClosingTag(s,i)
            last_col = tag_stack.pop()
            if len(value)>0:
                cur_output.append({last_col: value})
                columns.add(last_col)
                if last_col not in c2.keys(): c2[last_col]=len(c2)
            if len(tag_stack) == 1: 
                end_output.append(cur_output)
                cur_output = []
        else:
            tag, i = getOpeningTag(s, i)
            if len(tag_stack)==0:
                child_map[tag]=set()
            else:
                if tag_stack[-1] in child_map.keys():
                    child_map[tag_stack[-1]].add(tag)
                if not tag in child_map.keys():
                    child_map[tag]=set()
            tag_stack.append(tag)
            if len(tag_stack)==1:
                db_name = tag
            if len(tag_stack)==2:
                table_name = tag
    
    col_list = get_col_list(c2)
    return db_name, table_name, col_list, end_output

def parse_xml_to_db(filename):
    r = reader.Reader()
    f = r.get_xml_file(filename)
    xml_string = get_xml_from_file(f) 
    db_name, table_name, col_list, values_row_list = get_rows_from_xml(xml_string)
    write_to_database(db_name, table_name, col_list, values_row_list)
    f.close()
 
