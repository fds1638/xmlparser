import os

# reader for xml files
class Reader:
    def __init__(self, subdir="data/xml"):
        self.directory = os.getcwd() + "/" + subdir

    def get_xml_file(self,filename):
        f = open(self.directory+ "/" + filename,"r")
        return f
