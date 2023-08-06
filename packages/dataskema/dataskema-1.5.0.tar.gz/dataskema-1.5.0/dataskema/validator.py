# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301
import re

from dataskema import util
from dataskema import lang


DEFAULT_SEPARATOR = ','

KEYWORD_IS_VALID = 'valid'

KEYWORD_NAME = 'name'
KEYWORD_LABEL = 'label'
KEYWORD_MESSAGE = 'message'
KEYWORD_DESCRIPTION = 'description'
KEYWORD_SEPARATOR = 'separator'
KEYWORD_MANDATORY = 'mandatory'
KEYWORD_DEFAULT = 'default'
KEYWORD_TYPE = 'type'
KEYWORD_TYPE_LIST = 'list'
KEYWORD_TYPE_DICT = 'dict'

KEYWORD_TYPE_STR = 'str'
KEYWORD_MIN_SIZE = 'min-size'
KEYWORD_MAX_SIZE = 'max-size'
KEYWORD_REGEXP = 'regexp'
KEYWORD_ICASE = 'icase'
KEYWORD_WHITE_LIST = 'white-list'
KEYWORD_MAX_LINES = 'max-lines'

KEYWORD_TYPE_INT = 'int'
KEYWORD_TYPE_FLOAT = 'float'
KEYWORD_MIN_VALUE = 'min-value'
KEYWORD_MAX_VALUE = 'max-value'

KEYWORD_TYPE_BOOL = 'bool'
KEYWORD_BOOL_TRUE = 'true'
KEYWORD_BOOL_FALSE = 'false'

KEYWORD_TYPE_ANY = 'any'
KEYWORD_SCHEMA = 'schema'

KEYWORD_TO = 'to'
KEYWORD_TO_FUNC_LOWER = 'lower'
KEYWORD_TO_FUNC_UPPER = 'upper'
KEYWORD_TO_FUNC_NO_TRIM = 'no-trim'
KEYWORD_TO_FUNC_TRIM = 'trim'

ERROR_INVALID_TYPE = "'{keyword}' has an invalid value '{itype}'"
ERROR_INVALID_DEFAULT_TYPE = "Invalid default value type '{def_itype}'. Expected type '{itype}"
ERROR_UNEXPECTED_TYPE = "Type '{expected_type}' expected. Found '{utype}'"
ERROR_INVALID_FUNCTION_NAME = "'Invalid '{keyword}' function '{func_name}'"


class SchemaFormatError(ValueError):
    def __init__(self, message: dict or str, params: dict):
        super(SchemaFormatError, self).__init__(lang.get_message(message, params))


class SchemaValidationFailure(Exception):

    def __init__(self, message: dict or str, params: dict):
        if isinstance(message, dict):
            self.message = message.get(lang.DEFAULT)
            if self.message is None:
                self.message = message.get(lang.EN)
        else:
            self.message = message
        self.params = params
        super(SchemaValidationFailure, self).__init__(self.get_message())

    def get_message(self, anonymize: bool or None = False) -> str:
        return lang.get_message(self.message, self.params, anonymize)

    def get_name(self) -> str:
        return self.params.get(KEYWORD_NAME)


class SchemaValidator:

    def __init__(self, data_schema: dict):
        """
        """
        self.data_schema = data_schema

    def validate(self, name: str, value: any) -> any:
        # -- obtiene la etiquea del parámetro
        keyword = KEYWORD_LABEL
        label_map = self._get_obj(keyword)
        if isinstance(label_map, dict):
            label = label_map.get(lang.DEFAULT)
            if label is None:
                label = label_map.get(lang.EN)
        elif isinstance(label_map, str):
            label = label_map
        else:
            label = name

        # -- obtiene el valor según su tipo
        keyword = KEYWORD_TYPE
        itype = self._get_str(keyword)
        if itype is None:
            itype = util.typeof(value)
        if itype is not None:
            try:
                if itype == KEYWORD_TYPE_STR:
                    value = _get_type_str(label, value)
                elif itype == KEYWORD_TYPE_INT:
                    value = _get_type_int(label, value)
                elif itype == KEYWORD_TYPE_FLOAT:
                    value = _get_type_float(label, value)
                elif itype == KEYWORD_TYPE_BOOL:
                    value = _get_type_bool(label, value)
                elif itype == KEYWORD_TYPE_LIST:
                    keyword2 = KEYWORD_SEPARATOR
                    separator = self._get_str(keyword2)
                    separator = separator if separator is not None else DEFAULT_SEPARATOR
                    value = _get_type_list(label, value, separator)
                elif itype == KEYWORD_TYPE_DICT:
                    value = _get_type_dict(label, value)
                elif itype != KEYWORD_TYPE_ANY:
                    raise SchemaFormatError(ERROR_INVALID_TYPE, {'keyword': keyword, 'itype': itype})
            # -- comprueba si existe un mensaje customizado para un error de tipo
            except SchemaValidationFailure as fail:
                self._check_error_custom_message(label, fail)

        # -- aplica el valor por defecto en su caso
        keyword = KEYWORD_DEFAULT
        defvalue = self._get_obj(keyword)
        if itype is None and defvalue is not None:
            def_itype = util.typeof(defvalue)
            if itype != def_itype:
                raise SchemaFormatError(ERROR_INVALID_DEFAULT_TYPE, {'def_itype': def_itype, 'itype': itype})
        if value is None and defvalue is not None:
            value = defvalue

        # -- comprueba si es mandatorio (fuera de comprobación de mensaje específico)
        keyword = KEYWORD_MANDATORY
        mandatory = self._get_bool(keyword)
        if mandatory:
            _check_mandatory(label, value)

        # -- comprueba el tipo 'str'
        if isinstance(value, str):

            # -- aplica las funciones de transformación
            keyword = KEYWORD_TO
            tos = self._get_str(keyword)
            if tos is not None:
                tos = tos.split(',')
                for to in tos:
                    to = util.trim(to)
                    if not util.is_empty(to):
                        value = _process_to(keyword, value, to)
            else:
                value = util.trim(value)

            keyword = KEYWORD_MIN_SIZE
            min_size = self._get_int(keyword)
            _check_minsize(label, value, min_size)
            keyword = KEYWORD_MAX_SIZE
            max_size = self._get_int(keyword)
            _check_maxsize(label, value, max_size)
            # -- comprueba la cadena en el caso que sea distinta a ''
            if value != '':
                try:
                    keyword = KEYWORD_REGEXP
                    regexp = self._get_str(keyword)
                    _check_regexp(label, value, regexp)
                # -- comprueba si existe un mensaje customizado para un error de formato
                except SchemaValidationFailure as fail:
                    self._check_error_custom_message(label, fail)

                keyword = KEYWORD_WHITE_LIST
                whitelist = self._get_list(keyword)
                keyword = KEYWORD_ICASE
                icase = self._get_bool(keyword)
                icase = icase if icase is not None else True
                _check_whitelist(label, value, whitelist, icase)
                keyword = KEYWORD_MAX_LINES
                max_lines = self._get_int(keyword)
                _check_max_lines(label, value, max_lines)

        # -- comprueba el tipo 'int' o 'float'
        if isinstance(value, int) or isinstance(value, float):
            keyword = KEYWORD_MIN_VALUE
            min_value = self._get_int(keyword)
            _check_minvalue(label, value, min_value)
            keyword = KEYWORD_MAX_VALUE
            max_value = self._get_int(keyword)
            _check_maxvalue(label, value, max_value)

        # -- comprueba el tipo 'list'
        if isinstance(value, list):
            keyword = KEYWORD_SCHEMA
            item_schema = self._get_dict(keyword)
            _check_item_list_schema(label, value, item_schema)

        return value

    def _get_obj(self, keyword: str):
        return self.data_schema.get(keyword)

    def _get_bool(self, keyword: str) -> bool:
        value = self._get_obj(keyword)
        if value is not None and not isinstance(value, bool):
            _schema_error_unexpected_type(keyword, value, KEYWORD_TYPE_BOOL)
        return value

    def _get_dict(self, keyword: str) -> dict:
        value = self._get_obj(keyword)
        if value is not None and not isinstance(value, dict):
            _schema_error_unexpected_type(keyword, value, KEYWORD_TYPE_DICT)
        return value

    def _get_str(self, keyword: str) -> str:
        value = self._get_obj(keyword)
        if value is not None and not isinstance(value, str):
            _schema_error_unexpected_type(keyword, value, KEYWORD_TYPE_STR)
        return value

    def _get_int(self, keyword: str):
        value = self._get_obj(keyword)
        if value is not None and not isinstance(value, int):
            _schema_error_unexpected_type(keyword, value, KEYWORD_TYPE_INT)
        return value

    def _get_list(self, keyword: str):
        value = self._get_obj(keyword)
        if value is not None and not isinstance(value, list):
            _schema_error_unexpected_type(keyword, value, KEYWORD_TYPE_LIST)
        return value

    def _check_error_custom_message(self, label: str, fail: SchemaValidationFailure):
        keyword = KEYWORD_MESSAGE
        message_map = self._get_obj(keyword)
        if message_map is None:
            raise fail
        if isinstance(message_map, dict):
            message = message_map.get(lang.DEFAULT)
            if message is None:
                message = message_map.get(lang.EN)
            if message is None:
                message = fail.message
        elif isinstance(message_map, str):
            message = message_map
        else:
            raise fail
        raise SchemaValidationFailure(message, {KEYWORD_NAME: label})


def _schema_error_unexpected_type(keyword: str, found_value: any, expected_type: str):
    utype = util.typeof(found_value)
    raise SchemaFormatError(ERROR_UNEXPECTED_TYPE, {'keyword': keyword, 'utype': utype, 'expected_type': expected_type})


def _val_error_unexpected_type(name: str, found_value: any, expected_type: str):
    utype = util.typeof(found_value)
    raise SchemaValidationFailure(lang.VAL_ERROR_PARAM_HAS_INVALID_TYPE, {KEYWORD_NAME: name, 'utype': utype, 'expected_type': expected_type})


def _get_type_str(name: str, value: any) -> str or None:
    if value is None:
        return None
    if isinstance(value, int) or isinstance(value, float) or isinstance(value, bool):
        value = str(value)
    if not isinstance(value, str):
        _val_error_unexpected_type(name, value, KEYWORD_TYPE_STR)
    return value


def _get_type_int(name: str, value: any) -> int or None:
    if value is None:
        return None
    if isinstance(value, str):
        try:
            value = int(util.trim(value))
        except ValueError:
            _val_error_unexpected_type(name, value, KEYWORD_TYPE_INT)
    if isinstance(value, float):
        return int(value)
    if not isinstance(value, int):
        _val_error_unexpected_type(name, value, KEYWORD_TYPE_INT)
    return value


def _get_type_float(name: str, value: any) -> int or None:
    if value is None:
        return None
    if isinstance(value, str):
        try:
            value = float(util.trim(value))
        except ValueError:
            _val_error_unexpected_type(name, value, KEYWORD_TYPE_FLOAT)
    if isinstance(value, int):
        return float(value)
    if not isinstance(value, float):
        _val_error_unexpected_type(name, value, KEYWORD_TYPE_FLOAT)
    return value


def _get_type_bool(name: str, value: any) -> bool or None:
    if value is None:
        return None
    if isinstance(value, str):
        sbool = util.trim(value).lower()
        if sbool != KEYWORD_BOOL_TRUE and sbool != KEYWORD_BOOL_FALSE:
            _val_error_unexpected_type(name, value, KEYWORD_TYPE_BOOL)
        value = sbool == KEYWORD_BOOL_TRUE
    elif isinstance(value, int):
        if value != 0 and value != 1:
            _val_error_unexpected_type(name, value, KEYWORD_TYPE_BOOL)
        value = value == 1
    elif not isinstance(value, bool):
        _val_error_unexpected_type(name, value, KEYWORD_TYPE_BOOL)
    return value


def _get_type_list(name: str, value: any, separator: str) -> list or None:
    if value is None:
        return None
    if isinstance(value, str):
        return value.split(separator)
    elif not isinstance(value, list):
        _val_error_unexpected_type(name, value, KEYWORD_TYPE_LIST)
    return value


def _get_type_dict(name: str, value: any) -> list or None:
    if value is None:
        return None
    if not isinstance(value, dict):
        _val_error_unexpected_type(name, value, KEYWORD_TYPE_DICT)
    return [value]


def _process_to(keyword: str, value: any, func_name: str) -> str:
    if func_name == KEYWORD_TO_FUNC_LOWER:
        return value.lower()
    if func_name == KEYWORD_TO_FUNC_UPPER:
        return value.upper()
    if func_name == KEYWORD_TO_FUNC_NO_TRIM:
        return value
    if func_name == KEYWORD_TO_FUNC_TRIM:
        return util.trim(value)
    raise SchemaFormatError(ERROR_INVALID_FUNCTION_NAME, {'keyword': keyword, 'func_name': func_name})


def _check_mandatory(name: str, value: any):
    if value is None or (isinstance(value, str) and len(util.trim(value)) == 0):
        raise SchemaValidationFailure(lang.VAL_ERROR_PARAM_IS_MANDATORY, {KEYWORD_NAME: name})


def _check_regexp(name: str, value: str, pattern_to_match: str):
    if value is not None and len(value) > 0 and pattern_to_match is not None:
        regex = re.compile(pattern_to_match, re.I)
        match = regex.match(str(value))
        if not bool(match):
            raise SchemaValidationFailure(lang.VAL_ERROR_PARAM_HAS_INVALID_FORMAT, {KEYWORD_NAME: name})


def _check_minsize(name: str, value: str, minsize: int or None):
    slen = len(util.trim(value))
    if value is not None and minsize is not None and slen < minsize:
        raise SchemaValidationFailure(lang.VAL_ERROR_PARAM_IS_TOO_SHORT, {KEYWORD_NAME: name, 'minsize': minsize})


def _check_maxsize(name: str, value: str, maxsize: int or None):
    slen = len(util.trim(value))
    if value is not None and maxsize is not None and slen > maxsize:
        raise SchemaValidationFailure(lang.VAL_ERROR_PARAM_IS_TOO_LONG, {KEYWORD_NAME: name, 'maxsize': maxsize})


def _check_minvalue(name: str, value: any, minvalue: any):
    if value is not None and minvalue is not None and value < minvalue:
        raise SchemaValidationFailure(lang.VAL_ERROR_PARAM_IS_TOO_SMALL, {KEYWORD_NAME: name, 'minvalue': minvalue})


def _check_maxvalue(name: str, value: any, maxvalue: any):
    if value is not None and maxvalue is not None and value > maxvalue:
        raise SchemaValidationFailure(lang.VAL_ERROR_PARAM_IS_TOO_BIG, {KEYWORD_NAME: name, 'maxvalue': maxvalue})


def _check_item_list_schema(name: str, plist: list, item_schema: dict):
    if item_schema is not None:
        schema_validator = SchemaValidator(item_schema)
        for pitem in plist:
            try:
                schema_validator.validate('item list', pitem)
            except SchemaValidationFailure as ex:
                raise SchemaValidationFailure(lang.VAL_ERROR_LIST_ITEM_HAS_INVALID_ELEMENT, {KEYWORD_NAME: name, 'message': ex.get_message()})


def _check_whitelist(name: str, value: any, whitelist: list, icase: bool = True):
    if whitelist is None:
        return
    if icase:
        value = str(value).lower()
        for pitem in whitelist:
            if str(pitem).lower() == value:
                return
    else:
        for pitem in whitelist:
            if pitem == value:
                return
    raise SchemaValidationFailure(lang.VAL_ERROR_PARAM_HAS_INVALID_VALUE, {KEYWORD_NAME: name})


def _check_max_lines(name: str, value: any, max_lines: int):
    if max_lines is not None and max_lines > 0:
        total_nl = util.trim(value).count('\n') + 1
        if total_nl > max_lines:
            raise SchemaValidationFailure(lang.VAL_ERROR_PARAM_HAS_TOO_MUCH_LINES, {KEYWORD_NAME: name, 'maxlines': max_lines})

