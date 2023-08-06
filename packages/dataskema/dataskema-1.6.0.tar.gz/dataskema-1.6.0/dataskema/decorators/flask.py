# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring, C0301
import json
import functools
from dataskema.data_schema import DataSchema, SchemaValidationResult
from flask import request, make_response, Response


class JSON(DataSchema):
    def __init__(self):
        super(JSON, self).__init__(request.get_json())


class Query(DataSchema):
    def __init__(self):
        super(Query, self).__init__(request.args)


def flask_json(**kwargs):
    def inner_function(function):
        @functools.wraps(function)
        def wrapper(**data):
            json_validator = JSON()
            outdata = json_validator.validate(kwargs)
            outdata.update(data)
            return function(**outdata)
        return wrapper
    return inner_function


def flask_query(**kwargs):
    def inner_function(function):
        @functools.wraps(function)
        def wrapper(**data):
            query_validator = Query()
            outdata = query_validator.validate(kwargs)
            outdata.update(data)
            return function(**outdata)
        return wrapper
    return inner_function
	