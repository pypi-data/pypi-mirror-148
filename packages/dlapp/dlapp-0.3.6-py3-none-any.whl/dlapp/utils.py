"""Module containing the logic for utilities."""

import re
from collections import OrderedDict
from dlapp.argumenthelper import validate_argument_type


class UtilsError(Exception):
    """Use to capture utility error."""


class RegexConversionError(UtilsError):
    """Use to capture regular expression conversion error."""


class Printer:
    """A printer class.

    Methods
    Printer.get(data, header='', footer='', failure_msg='', width=80) -> str
    Printer.print(data, header='', footer='', failure_msg='', print_func=None) -> None
    """
    @classmethod
    def get(cls, data, header='', footer='', width=80, failure_msg=''):
        """Decorate data by organizing header, data, footer, and failure_msg

        Parameters
        ----------
        data (str, list): a text or a list of text.
        header (str): a header text.  Default is empty.
        footer (str): a footer text.  Default is empty.
        width (int): width of displayed text.  Default is 80.
        failure_msg (str): a failure message.  Default is empty.
        """
        headers = str(header).splitlines()
        footers = str(footer).splitlines()
        data = data if isinstance(data, (list, tuple)) else [data]
        lst = []
        result = []

        left_limit = 20
        left_bound, right_bound = left_limit - 4, width - 4

        if width > left_limit:
            pat = r'(.{%s,%s}\S) +' % (left_bound, right_bound)
        else:
            pat = ''

        for item in data:
            if pat:
                for line in str(item).splitlines():
                    line = line.rstrip()
                    if len(line) > right_bound:
                        line = re.sub(pat, r'\1\n', line)
                        lst.extend(line.splitlines())
                    else:
                        lst.append(line)
            else:
                lst.extend(line.rstrip() for line in str(item).splitlines())
        length = max(len(str(i)) for i in lst + headers + footers)
        if width > left_limit:
            length = right_bound if right_bound > length else length
        result.append('+-{}-+'.format('-' * length))
        if header:
            for item in headers:
                result.append('| {} |'.format(item.ljust(length)))
            result.append('+-{}-+'.format('-' * length))

        for item in lst:
            result.append('| {} |'.format(item.ljust(length)))
        result.append('+-{}-+'.format('-' * length))

        if footer:
            for item in footers:
                result.append('| {} |'.format(item.ljust(length)))
            result.append('+-{}-+'.format('-' * length))

        if failure_msg:
            result.append(failure_msg)

        txt = '\n'.join(result)
        return txt

    @classmethod
    def print(cls, data, header='', footer='', width=80, failure_msg='',
              print_func=None):
        """Decorate data by organizing header, data, footer, and failure_msg

        Parameters
        ----------
        data (str, list): a text or a list of text.
        header (str): a header text.  Default is empty.
        footer (str): a footer text.  Default is empty.
        width (int): width of displayed text.  Default is 80.
        failure_msg (str): a failure message.  Default is empty.
        print_func (function): a print function.  Default is None.
        """

        txt = Printer.get(data, header=header, footer=footer,
                          failure_msg=failure_msg, width=width)

        print_func = print_func if callable(print_func) else print
        print_func(txt)


def convert_wildcard_to_regex(pattern, closed=False):
    """Convert a wildcard pattern to a regex pattern.

    Parameters
    ----------
    pattern (str): a wildcard pattern.
    closed (bool): will prepend ^ symbol and append $ symbol to pattern
            if set to True
    Returns
    -------
    str: a regular express pattern.

    Notes
    -----
    Wildcard support:
        ? (question mark): this can represent any single character.
        * (asterisk): this can represent any number of characters
            (including zero, in other words, zero or more characters).
        [] (square brackets): specifies a range.
        [!] : match any that not specifies in a range.

    """
    validate_argument_type(str, pattern=pattern)
    regex_pattern = ''
    try:
        regex_pattern = pattern.replace('.', r'\.')
        regex_pattern = regex_pattern.replace('+', r'\+')
        regex_pattern = regex_pattern.replace('?', '_replacetodot_')
        regex_pattern = regex_pattern.replace('*', '_replacetodotasterisk_')
        regex_pattern = regex_pattern.replace('_replacetodot_', '.')
        regex_pattern = regex_pattern.replace('_replacetodotasterisk_', '.*')
        regex_pattern = regex_pattern.replace('[!', '[^')
        regex_pattern = '^{}$'.format(regex_pattern) if closed else regex_pattern
        re.compile(regex_pattern)
        return regex_pattern
    except Exception as ex:
        fmt = 'Failed to convert wildcard({!r}) to regex({!r})\n{}'
        raise RegexConversionError(fmt.format(pattern, regex_pattern, ex))


def foreach(data, choice='keys'):
    """"a set-like object providing a view on D's keys/values/items

    Parameters
    ----------
    data (Any): data
    choice (str): keys|values|items.  Default is keys.

    Returns
    -------
    dict_keys or odict_keys if choice is keys
    dict_values or odict_values if choice is values
    dict_items or odict_items if choice is items
    """
    if isinstance(data, dict):
        node = data
    elif isinstance(data, (list, tuple)):
        total = len(data)
        node = OrderedDict(zip(range(total), data))
    else:
        node = dict()

    if choice == 'keys':
        return node.keys()
    elif choice == 'values':
        return node.values()
    else:
        return node.items()
