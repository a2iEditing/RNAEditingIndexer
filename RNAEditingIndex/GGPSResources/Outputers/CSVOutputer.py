__author__ = 'Hillel'
# =====================imports=====================#
from Outputer import Outputer

import os

# =====================constants===================#
EMPTY_VAL = "-"
NOT_AVAILABLE = "NA"

OVERRIDE_APPEND_CONFLICT = "Cannot Init CSVOutputer with both override and append on True!"


# =====================classes=====================#


class CSVOutputer(Outputer):
    """
    This class implements creating csv output (i.e. writing data into a csv file)
    :ivar override: If set will override existing files, else will not write the new ones.
    :ivar delim: The delimiter for the output file.
    :ivar append: If set will append output to existing files, else will not write the new ones.
    :ivar write_headers: If set will write the headers to the file, else won't.
    """

    def __init__(self, override=True, delim=",", append=False, write_headers=True):
        assert override & append is False, OVERRIDE_APPEND_CONFLICT
        self.override = override
        self.delim = delim
        self.append = append
        self.write_headers = write_headers

    def output(self, paths, headers, records):
        """
        This function creates the output.
        :param headers: The headers of the csv
        :type headers: C{list} of C{str}
        :param records: The records to write, header name => value
        :type records: C{dict} of C{str} to C{str}
        :return: None
        """
        if self.append:
            mode = 'ab'
        else:
            mode = 'wb'
        for path in paths:
            exists = False
            if os.path.isfile(path):
                if self.append:
                    exists = True
                    if self.write_headers:
                        with open(path) as temp:
                            headers = [x.strip() for x in temp.readlines()[0].split(self.delim)]
                else:
                    pass

            self.make_dir(path)

            with open(path, mode) as o:
                if exists:
                    if self.append:
                        for record in records:
                            line = ""
                            for header in headers:
                                line += record.get(header, EMPTY_VAL) + self.delim

                            line = line[:-1] + "\n"
                            o.write(line)
                        self.chmod_to_all(path)
                else:
                    if self.write_headers:
                        o.write(self.delim.join(headers) + "\n")
                    for record in records:
                        line = ""
                        for header in headers:
                            line += record.get(header, EMPTY_VAL) + self.delim

                        line = line[:-1] + "\n"
                        o.write(line)
                    self.chmod_to_all(path)
