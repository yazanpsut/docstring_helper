# coding=utf-8
import os
import re
from os import listdir
from os.path import isfile
from os.path import join

__author__ = 'yazan'

STRING_TO_THE_START_OF_FILE = "\"\"\"Example Google style docstrings.\n" \
                              "    This module demonstrates documentation as specified by the `Google Python\n" \
                              "    Style Guide`_. Docstrings may extend over multiple lines. Sections are created\n" \
                              "    with a section header and a colon followed by a block of indented text.\n" \
                              "    Example:\n" \
                              "        Examples can be given using either the ``Example`` or ``Examples``\n" \
                              "        sections. Sections support any reStructuredText formatting, including\n" \
                              "        literal blocks::\n" \
                              "            $ python example_google.py\n" \
                              "    Section breaks are created by resuming unindented text. Section breaks\n" \
                              "    are also implicitly created anytime a new section starts.\n" \
                              "    Attributes:\n" \
                              "        module_level_variable1 (int): Module level variables may be documented in\n" \
                              "            either the ``Attributes`` section of the module docstring, or in an\n" \
                              "            inline docstring immediately following the variable.\n" \
                              "            Either form is acceptable, but the two should not be mixed. Choose\n" \
                              "            one convention to document module level variables and be consistent\n" \
                              "            with it.\n" \
                              "\"\"\"\n"
STRING_TO_BE_ADDED = "qqq\"\"\"\n" \
                     "qqqSmall description about the function\n" \
                     "qqqArgs:\n" \
                     "qqq    param1 (int): The first parameter.\n" \
                     "qqq    param2 (Optional[str]): The second parameter. Defaults to None.\n" \
                     "qqq        Second line of description should be indented.\n" \
                     "qqq    *args: Variable length argument list.\n" \
                     "qqq    **kwargs: Arbitrary keyword arguments.\n" \
                     "qqqReturns:\n" \
                     "qqq    bool: True if successful, False otherwise.\n" \
                     "qqq        The return type is optional and may be specified at the beginning of\n" \
                     "qqq        the ``Returns`` section followed by a colon.\n" \
                     "qqq        The ``Returns`` section may span multiple lines and paragraphs.\n" \
                     "qqq        Following lines should be indented to match the first line.\n" \
                     "qqq        The ``Returns`` section supports any reStructuredText formatting,\n" \
                     "qqq        including literal blocks::\n" \
                     "qqq            {\n" \
                     "qqq                'param1': param1,\n" \
                     "qqq                'param2': param2\n" \
                     "qqq            }\n" \
                     "qqqRaises:\n" \
                     "qqq    AttributeError: The ``Raises`` section is a list of all exceptions\n" \
                     "qqq        that are relevant to the interface.\n" \
                     "qqq   ValueError: If `param2` is equal to `param1`.\n" \
                     "qqq\"\"\"\n"

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__).decode('utf-8')).replace('\\', '/')


def process_file(f, new_path):
    if isfile(join(new_path, f)) and re.match('(views.py|models.py)', f):
        index = 0
        print f
        my_file = open(new_path + '/' + f, "r")
        searchlines = my_file.readlines()
        my_file.close()
        for i, line in enumerate(searchlines):
            if "def " in line or "class" in line:
                line_copy = line
                indented_lines = STRING_TO_BE_ADDED
                index_of_line_for_end_of_function = i
                end_of_function_line_number = -1
                while end_of_function_line_number == -1:
                    end_of_function_line_number = searchlines[index_of_line_for_end_of_function].find(':')
                    index_of_line_for_end_of_function += 1

                if "\"\"\"" not in searchlines[index_of_line_for_end_of_function]:
                    space_counter = 0
                    if "def" in line:
                        space_counter = line.index('d')
                    else:
                        space_counter = line.index('c')
                    for space in range(0, line.count(' ', 0, space_counter)):
                        indented_lines = indented_lines.replace('qqq', ' qqq')
                    indented_lines = indented_lines.replace('qqq', '    ')
                    searchlines.insert(index_of_line_for_end_of_function, indented_lines)

        my_file = open(new_path + '/' + f, "w")
        if searchlines[0].startswith("#"):
            searchlines.insert(1, STRING_TO_THE_START_OF_FILE)
        else:
            searchlines.insert(0, "# coding=utf-8\n")
            searchlines.insert(1, STRING_TO_THE_START_OF_FILE)

        my_file.writelines(searchlines)
        my_file.close()


for dirname in os.listdir(CURRENT_PATH):
    # print path to all subdirectories first.
    process_file(dirname, CURRENT_PATH)
    if not (dirname.__contains__('.') or dirname.__contains__('-')):
        os.chdir(os.path.join(CURRENT_PATH, dirname))
        new_path = os.path.join(CURRENT_PATH, dirname)
        for f in listdir(new_path):
            process_file(f, new_path)
        os.chdir(os.path.join(CURRENT_PATH, ".."))
