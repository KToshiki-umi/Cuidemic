#! /usr/bin/python
# --*-- coding:utf-8 --*--

"""
QuarantineSpecialist.py

Copyright (c) 2015 Toshiki Koizumi

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""

#v.1.01

from Player import Player

class QuarantineSpecialist(Player):
    def __init__(self):
        Player.__init__(self)
        self._role = "QuarantineSpecialist"	#役職名英名
        #役職名
        self._name = u"                    検疫官"
