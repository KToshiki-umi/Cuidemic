"""
OperationExpert.py

Copyright (c) 2015 Toshiki Koizumi

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""

#v.1.00

#! /usr/bin/python
# --*-- coding:utf-8 --*--

from Player import Player

class OperationExpert(Player):
    def __init__(self):
        Player.__init__(self)
        self._role = "OperationExpert"	#役職名英名
        #役職名
        self._name = u"          作戦エキスパート"


    def buildResearchStation(self, game_data):
        game_data._research_station_flag[self._location] = 1
        game_data._message = u"■ %02d:%s に調査基地を建設しました" % (self._location, game_data._card_info[self._location])
        
        return 1
    
    def isBuildResearchStation(self, game_data):
        if game_data._research_station_flag[self._location] == 1:
            return 0
        
        return 1