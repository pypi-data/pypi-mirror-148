"""Module containing the logic for describe-get-system to parse
user describing request"""

import re

from dgspoc.utils import DotObject


class CheckStatement:

    @classmethod
    def is_execute_cmdline(cls, data):
        pattern = r'(?i) *[{]?([a-z0-9]\S*)(, ?([a-z0-9]\S*))*[}]? +exec(utes?)? +'
        match = re.match(pattern, data)
        return bool(match)

    @classmethod
    def is_performer_statement(cls, data):
        pattern = (r'(?i) *[{]?([a-z0-9]\S*)(, ?([a-z0-9]\S*))*[}]? +'
                   r'(exec(utes?)?|conf(ig(ures?)?)?|reloads?) +')
        match = re.match(pattern, data)
        return bool(match)

    @classmethod
    def is_verification_statement(cls, data):
        pattern = r'(?i) +must +be +\S+( +[0-9]+)? *$'
        chk = bool(re.search(pattern, data))
        chk &= cls.is_execute_cmdline(data)
        return chk

    @classmethod
    def is_regular_iterative_statement(cls, data):
        pattern = r'(?i) *loop +[0-9]+ +times? *$'
        match = re.match(pattern, data)
        return bool(match)

    @classmethod
    def is_until_iterative_statement(cls, data):
        pattern = r'(?i) *loop +[0-9]+ +times? +until *$'
        match = re.match(pattern, data)
        return bool(match)

    @classmethod
    def is_to_last_iterative_statement(cls, data):
        pattern = r'(?i) *loop +[0-9]+ +times? +to +last *$'
        match = re.match(pattern, data)
        return bool(match)

    @classmethod
    def is_iterative_statement(cls, data):
        chk = cls.is_regular_iterative_statement(data)
        chk |= cls.is_until_iterative_statement(data)
        chk |= cls.is_to_last_iterative_statement(data)
        return chk

    @classmethod
    def is_pausing_statement(cls, data):
        match = re.match(r'(?i) *(sleeps?|(wait +for)) +', data)
        return bool(match)

    @classmethod
    def is_connect_device_statement(cls, data):
        match = re.match(r'(?i) *connects? +device +', data)
        return bool(match)

    @classmethod
    def is_disconnect_device_statement(cls, data):
        match = re.match(r'(?i) *disconnects?( +device)? +', data)
        return bool(match)

    @classmethod
    def is_release_device_statement(cls, data):
        match = re.match(r'(?i) *releases? +device +', data)
        return bool(match)

    @classmethod
    def is_dummy_statement(cls, data):
        match = re.match(r'(?i) *dummy[_. -]*(pass|fail)', data)
        return bool(match)

    @classmethod
    def is_child_execute_cmdline(cls, data):
        chk = cls.is_execute_cmdline(data) and data.startswith(' ')
        return chk

    @classmethod
    def is_child_performer_statement(cls, data):
        chk = cls.is_performer_statement(data) and data.startswith(' ')
        return chk

    @classmethod
    def is_child_verification_statement(cls, data):
        chk = cls.is_verification_statement(data) and data.startswith(' ')
        return chk

    @classmethod
    def is_child_iterative_statement(cls, data):
        chk = cls.is_iterative_statement(data) and data.startswith(' ')
        return chk

    @classmethod
    def is_child_pausing_statement(cls, data):
        chk = cls.is_pausing_statement(data) and data.startswith(' ')
        return chk

    @classmethod
    def is_child_connect_device_statement(cls, data):
        chk = cls.is_connect_device_statement(data) and data.startswith(' ')
        return chk

    @classmethod
    def is_child_disconnect_device_statement(cls, data):
        chk = cls.is_disconnect_device_statement(data) and data.startswith(' ')
        return chk

    @classmethod
    def is_child_release_device_statement(cls, data):
        chk = cls.is_release_device_statement(data) and data.startswith(' ')
        return chk

    @classmethod
    def is_child_dummy_statement(cls, data):
        chk = cls.is_dummy_statement(data) and data.startswith(' ')
        return chk


class ParsedOperation:
    def __init__(self, data):
        self.name = ''
        self.devices_names = []
        self.operation_type = ''
        self.data = data
        self.operation_ref = ''
        self.convertor = ''
        self.convertor_arg = ''
        self._has_select_statement = False
        self.select_statement = ''
        self.condition = ''
        self.expected_condition = -1

        self.error = ''

        self.parse()

    @property
    def is_parsed(self):
        return self.error == ''

    @property
    def is_execution(self):
        return self.operation_type == 'execution'

    @property
    def is_configuration(self):
        return self.operation_type == 'configuration'

    @property
    def is_verification(self):
        chk = self.is_execution
        chk &= self.convertor != ''
        chk &= self.select_statement != ''
        chk &= self.condition != ''
        return chk

    @property
    def is_reload(self):
        return self.operation_type == 'reload'

    @property
    def is_valid_operation(self):
        result = self.is_execution
        result |= self.is_configuration
        result |= self.is_reload
        return result

    @property
    def has_select_statement(self):
        return self._has_select_statement

    @property
    def is_json(self):
        return self.convertor == 'json'

    @property
    def is_csv(self):
        return self.convertor == 'csv'

    @property
    def is_template(self):
        return self.convertor == 'template'

    def parse(self):
        pattern = (r'(?i) *(?P<devices_names>[{]?([a-z0-9]\S*)(, ?([a-z0-9]\S*))*[}]?) +'
                   r'(?P<operation_type>exec(utes?)?|conf(ig(ures?)?)?|reloads?) +'
                   r'(?P<operation>.+) *$')
        match = re.match(pattern, self.data)
        if not match:
            return

        node = DotObject(match.groupdict())

        self.parse_devices_names(node.devices_names)
        self.is_parsed and self.parse_operation_type(node.operation_type)   # noqa

        if self.is_parsed and self.is_valid_operation:
            if self.is_execution:
                result = ExecuteOperation(node.operation)
                self.name = result.name
                self.operation_ref = result.operation_ref
                self.convertor = result.convertor
                self.convertor_arg = result.convertor_arg
                self.select_statement = result.select_statement
                self.condition = result.condition
                self.expected_condition = result.expected_condition
                self._has_select_statement = result.has_select_statement
                self.error = result.error
            elif self.is_configuration:
                result = ConfigOperation(node.operation)
                self.name = result.name
                self.operation_ref = result.operation_ref
            elif self.is_reload:
                result = ReloadOperation(node.operation)
                self.name = result.name
                self.operation_ref = result.operation_ref

    def parse_devices_names(self, data):
        other_data = data.strip().lstrip('{').rstrip('}')
        pattern = r'([a-z0-9]\S*)(, ?([a-z0-9]\S*))*$'
        match = re.match(pattern, other_data, re.I)
        if match:
            names = re.split(r' *, *', other_data)
            if names:
                self.devices_names = names
                return
        self.error = 'Invalid devices names format ("%s")' % data

    def parse_operation_type(self, data):
        tbl = dict(e='execution', c='configuration', r='reload')
        key = data.strip().lower()[:1]
        self.operation_type = tbl.get(key, '')
        if not self.operation_type:
            fmt = 'Invalid operation ("%s").  It MUST BE execute, configure, or reload.'
            self.error = fmt % data


class ExecuteOperation:
    def __init__(self, data):
        self.name = 'execution'
        self._remaining_data = ''
        self.data = data
        self.operation_ref = ''
        self.convertor = ''
        self.convertor_arg = ''
        self.select_statement = ''
        self.condition = ''
        self.expected_condition = -1

        self.error = ''

        self.parse()

    @property
    def is_parsed(self):
        return self.error == ''

    @property
    def has_select_statement(self):
        return self.select_statement != ''

    @property
    def is_need_verification(self):
        return self.condition != '' and self.expected_condition >= 0

    def parse(self):
        self._remaining_data = self.data
        self.parse_condition()
        self.parse_select_statement()
        self.parse_convertor()
        self.operation_ref = self._remaining_data

    def parse_condition(self):

        data = self._remaining_data

        pattern = r'(?i) +must +be +\S+( +\S+)? *$'
        if not re.search(pattern, data):
            return

        pattern = (r'(?i) +must +be +((?P<val1>true|false)|'
                   r'((?P<op>\S+) +(?P<val2>[0-9]+)))$')
        match = re.search(pattern, self._remaining_data)

        if not match:
            self.error = 'Invalid command line verification format'
            return

        self._remaining_data = re.sub(pattern, '', data)

        node = DotObject(match.groupdict())
        if node.val1:
            self.condition = '=='
            self.expected_condition = 1 if node.val1.lower() == 'true' else 0
        else:
            tbl = dict(
                EQ='==', EQUAL_TO='==',
                NE='!=', NOT_EQUAL='!=', NOT_EQUAL_TO='!=',
                GT='>', GREATER_THAN='>',
                GE='>=', GREATER_THAN_OR_EQUAL_TO='>=', EQUAL_TO_OR_GREATER_THAN='>=',
                LT='<', LESS_THAN='<',
                LE='<=', LESS_THAN_OR_EQUAL_TO='<=', EQUAL_TO_OR_LESS_THAN='<='
            )

            op = node.op.upper()
            found = [True for k, v in tbl.items() if k == op or v == op]
            if any(found):
                self.condition = tbl[op] if op in tbl else op
                self.expected_condition = int(node.val2)
            else:
                fmt = 'Invalid comparison operator (%r).  It must be %s'
                self.error = fmt % (node.op, list(tbl))

    def parse_select_statement(self):

        data = self._remaining_data.strip()

        pattern = r'(?i) +(?P<sel_stmt>select +([*]|_+all_+|[a-z].+) where +.+)'
        match = re.search(pattern, data)
        if not match:
            return

        self.select_statement = match.group('sel_stmt').strip()
        self._remaining_data = re.sub(pattern, '', data)

    def parse_convertor(self):

        data = self._remaining_data.strip()

        pattern = r'(?i) using_(?P<type>csv|json|template)( +(?P<arg>\S+))? *$'
        match = re.search(pattern, data)
        if not match:
            if self.has_select_statement:
                self.error = 'Invalid command line verification without convertor'
            return
        self.convertor = match.group('type').lower()
        self.convertor_arg = match.group('arg')
        self._remaining_data = re.sub(pattern, '', data)


class ConfigOperation:
    def __init__(self, data):
        self.name = 'configuration'
        self.operation_ref = ''
        self.data = data

        self.error = ''

        self.parse()

    @property
    def is_parsed(self):
        return self.error == ''

    def parse(self):
        self.operation_ref = self.data


class ReloadOperation:
    def __init__(self, data):
        self.name = 'reload'
        self.operation_ref = ''
        self.data = data

        self.error = ''

        self.parse()

    @property
    def is_parsed(self):
        return self.error == ''

    def parse(self):
        self.operation_ref = self.data
