"""
Medic.py

Copyright (c) 2015 Toshiki Koizumi

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""

#v.1.00

#! /usr/bin/python
# --*-- coding:utf-8 --*--

from Player import Player

class Medic(Player):
    def __init__(self):
        Player.__init__(self)
        self._role = "Medic"	#役職名英名
        #役職名
        self._name = u"                    衛生兵"

    def treatDisease(self, game_data):
        print u"■感染者の治療"
        diseases = u""
        disease_flag = []
        disease_count = 0
        color_index = ""
        
        for temp_color_index in range(4):
            if game_data._infection_status[self._location][temp_color_index] > 0:
                diseases += u"%d : %s  " % (temp_color_index, game_data._disease_name[temp_color_index])
                disease_flag.append(temp_color_index)
                color_index = temp_color_index
                disease_count += 1
        
        while(1):
            if disease_count == 1:
                # 感染が1種類のみの場合、自動的に治療
                break
            else:
                print u"\n 治療したい病原体を選択してください"
                print diseases
                color_index = raw_input(" > ")
                
                if color_index.isdigit():
                    color_index = int(color_index)
                    if disease_flag.count(color_index) > 0:
                        break
                    else:
                        print u" 入力した値は範囲外です"
                    
                elif color_index == "":
                    game_data._message = u"■ 処理はキャンセルされました"
                    return 0
                else:
                    print u" 数値を入力してください"
        
        game_data.cureDisease(self._location, 3, int(color_index))
        game_data._message = u"■ %02d:%s で%sの治療を行いました" % (self._location, game_data._card_info[self._location], game_data._disease_name[int(color_index)])
        return 1
        
