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
import os
from typing import Any
from logging import Logger

OUTPUT_IS_SHY = os.getenv("OUTPUT_IS_SHY", "true").lower() in ("true", "1", "t")


@staticmethod
def _log_message(logger: Logger, log_level: int, message: str, data: Any = None) -> None:
    """
    Logs a message using the provided logger and logging level. Optionally,
    if the global variable `OUTPUT_IS_SHY` is set to False and the `data`
    parameter is provided, the message will be appended with additional data.

    :param logger: The logging instance to be used for recording the message.
    :type logger: logging.Logger
    :param log_level: The severity level of the message being logged.
    :type log_level: int
    :param message: The primary message to log.
    :type message: str
    :param data: Optional additional data to include in the log message. If
        provided and the `OUTPUT_IS_SHY` global variable is False, the data
        will be appended to the message.
    :type data: Any
    :return: This method does not return any value.
    :rtype: None
    """
    if not OUTPUT_IS_SHY and data is not None:
        message += f", with data: {data}"
    message += "."
    logger.log(log_level, message)

