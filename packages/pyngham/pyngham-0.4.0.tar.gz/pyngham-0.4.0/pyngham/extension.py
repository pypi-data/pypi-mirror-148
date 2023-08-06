#
# extension.py
# 
# Copyright (C) 2022, Gabriel Mariano Marcelino - PU5GMA <gabriel.mm8@gmail.com>
# 
# This file is part of PyNGHam library.
# 
# PyNGHam library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyNGHam library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with PyNGHam library. If not, see <http://www.gnu.org/licenses/>.
# 
#


# Seria Port Protocol packets types
_PYNGHAM_EXT_PKT_TYPE_DATA          = 0
_PYNGHAM_EXT_PKT_TYPE_ID            = 1
_PYNGHAM_EXT_PKT_TYPE_STAT          = 2
_PYNGHAM_EXT_PKT_TYPE_SIMPLEDIGI    = 3
_PYNGHAM_EXT_PKT_TYPE_POS           = 4
_PYNGHAM_EXT_PKT_TYPE_TOH           = 5
_PYNGHAM_EXT_PKT_TYPE_DEST          = 6     # Destination/receiver callsign
_PYNGHAM_EXT_PKT_TYPE_CMD_REQ       = 7     # Command packet
_PYNGHAM_EXT_PKT_TYPE_CMD_REPLY     = 8     # Command packet
_PYNGHAM_EXT_PKT_TYPE_REQUEST       = 9

_PYNGHAM_EXT_PKT_TYPES              = 10
_PYNGHAM_EXT_PKT_SIZE_VARIABLE      = 0xFFFF


class PyNGHamExtension:

    def __init__(self):
        pass

    def numpkts(self, d):
        pass

    def encode_callsign(self, callsign):
        pass

    def decode_callsign(self, enc_callsign):
        pass
