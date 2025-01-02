#   Copyright (c) 2024.
#  #
#   Proprietary License
#  #
#   management-tool License Agreement
#  #
#   Permission is hereby granted, to any person contracted with Rapid Dev Group to
#   use this software and associated documentation files (the "Software"), to use
#   the Software for personal and commercial purposes, subject to the following
#   conditions:
#  #
#   1. Redistribution and use in source and binary forms, with or without
#      modification, are not permitted.
#   2. The Software shall be used for Good, not Evil.
#  #
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
#  #
#   Contact: pn@goldeverywhere.com
#
from typing import NoReturn, Optional
# from coolify_api.exceptions import (CoolifyKeyRequiredError, CoolifyKeyValueTypeError,
#                                     CoolifyKeyValueError, CoolifyKeyUnknownError)


@staticmethod
def create_data_with_kwargs(data: Optional[dict] = None, **kwargs) -> dict:
    if data is None:
        data = {}
    for key, value in kwargs.items():
        data[key] = value
    return data






# K_NAME = 0
# K_TYPE = 1
# K_REQUIRED = 2
# K_VALUES = 3
#



# @staticmethod
# def verify_data_keys(expected_keys: tuple, data: dict) -> bool | NoReturn:
#
#     all_keys = []
#     required_keys = []
#     keys_data = {}
#     for key_data in expected_keys:
#         k_name, k_type, k_required, k_values = key_data
#         all_keys.append(k_name)
#         if k_required:
#             required_keys.append(k_name)
#         keys_data[k_name] = {
#             "type": k_type,
#             "required": k_required,
#             "values": k_values
#         }
#
#     for key_name in required_keys:
#         if key_name not in data:
#             raise CoolifyKeyRequiredError(key_name)
#
#     for key_name, key_value in data.items():
#         if key_name not in all_keys:
#             raise CoolifyKeyUnknownError(key_name)
#         if not isinstance(key_value, keys_data[key_name]["type"]):
#             raise CoolifyKeyValueTypeError(key_name, keys_data[key_name]["type"])
#         if keys_data[key_name]["values"] and key_value not in keys_data[key_name]["values"]:
#             raise CoolifyKeyValueError(key_name, keys_data[key_name]["values"])
#
