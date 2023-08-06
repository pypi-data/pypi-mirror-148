"""
This file is part of APAV.

APAV is a python package for performing analysis and visualization on
atom probe tomography data sets.

Copyright (C) 2018 Jesse Smith

APAV is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

APAV is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with APAV.  If not, see <http://www.gnu.org/licenses/>.
"""

import logging
from os.path import abspath, join, dirname


_logger_form = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s',
                                  datefmt='%d/%m/%Y %H:%M:%S')

_stream_handler = logging.StreamHandler()
_stream_handler.setFormatter(_logger_form)
_stream_handler.setLevel(logging.WARNING)

_log_path = join(abspath(dirname(__file__)), "..", "apav.log")
_file_handler = logging.FileHandler(_log_path)
_file_handler.setFormatter(_logger_form)
_file_handler.setLevel(logging.DEBUG)


log = logging.getLogger("apav")
log.setLevel(logging.DEBUG)
log.addHandler(_stream_handler)
log.addHandler(_file_handler)
