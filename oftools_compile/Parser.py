from configparser import ConfigParser
import sys
'''
The parser class will be responsible for parsing both the COBOL file
as well as the PROFILE.
We can create a child class called ProfileParser which will inherit properties
from the Parser class, but be more specific towards parsing the PROFILE.
'''


class Parser:

    def __init__(self, list_object):
        self.config = ConfigParser()
        self.config.read(list_object.profile)
        self.get_sections()
        # Default Options
        self.openframe_home = '$OPENFRAME_HOME'
        self.default_volume = 'volume_default'
        self.db_sid = 'TVSAM'
        self.db_type = 'tibero'
        self.db_port = 8629
        self.db_user = 'tibero'
        self.db_pass = 'tmax'
        self.fix_periods = True

    def get_sections(self):
        for section in self.config.sections():
            self.section_switcher(section)

    '''
    This function will act as a switch case to search for specific sections
    If the section is not found, that means the script cannot handle that section
    And it needs to ignore the section
    '''

    def section_switcher(self, section):
        if section == 'directory':
            options = self.config.options(section)
            for opt in options:
                self.directory_switcher(opt)
        elif section == 'database':
            # print(self.config.options(section))
            options = self.config.options(section)
            for opt in options:
                self.database_switcher(opt)
        elif section == 'ofcbpp':
            options = self.config.options(section)
            for opt in options:
                self.ofcbpp_switcher(opt)
        else:
            print('Unrecognized Section: ' + section)
            sys.exit(2)

    def directory_switcher(self, option):
        if option == 'openframe_home':
            self.openframe_home = self.config.get('directory',
                                                  'openframe_home')
        elif option == 'default_volume':
            self.default_volume = self.config.get('directory',
                                                  'default_volume')
        else:
            print('Unrecognized Option: ' + option)
            sys.exit(2)

    def database_switcher(self, option):
        if option == 'db_sid':
            self.db_sid = self.config.get('database', 'db_sid')
        elif option == 'db_type':
            self.db_type = self.config.get('database', 'db_type')
        elif option == 'db_port':
            self.db_port = self.config.getint('database', 'db_port')
        elif option == 'db_user':
            self.db_user = self.config.get('database', 'db_user')
        elif option == 'db_pass':
            self.db_pass = self.config.get('database', 'db_pass')
        else:
            print('Unrecognized Option: ' + option)
            sys.exit(2)

    def ofcbpp_switcher(self, option):
        if option == 'fix_periods':
            self.fix_periods = self.config.getboolean('ofcbpp', 'fix_periods')
        else:
            print('Unrecognized Option: ' + option)
            sys.exit(2)
