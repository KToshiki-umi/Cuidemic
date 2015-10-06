"""
Scientist.py

Copyright (c) 2015 Toshiki Koizumi

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""

#v.1.00

#! /usr/bin/python
# --*-- coding:utf-8 --*--

from Player import Player

class Scientist(Player):
    def __init__(self):
        Player.__init__(self)
        self._role = "Scientist"	#役職名英名
        #役職名
        self._name = u"                    科学者"

    def discoverCure(self, game_data):
        print u"■治療薬の発見"
        color_index = -1
        hand_color = [[], [], [], []]
        
        for card in self._hand:
            hand_color[game_data.getColorIndexFromCity(card)].append(card)
        
        for i in range(4):
            if len(hand_color[i]) >= 4:
                color_index = i
                break
        
        consumption_card = []
        if len(hand_color[color_index]) == 4:
            consumption_card = hand_color[color_index]
        
        else:
            while(1):
                available_cards = ""
                
                for card in hand_color[color_index]:
                    available_cards += " %02d" % card
                
                print u"\n 作成に使用するカードを4枚選択してください"
                print u" 例) > 04/01/05/11"
                print u" 選択可能カード：%s" % available_cards
                selected_card = raw_input(" > ")
                
                if selected_card == "":
                    game_data._message = u"■ 処理はキャンセルされました"
                    return 0
                elif self.checkCards(selected_card, hand_color[color_index]) == 0:
                    consumption_card_str = selected_card.split("/")
                    for card in consumption_card_str:
                        consumption_card.append(int(card))
                    break
        
        for discard in consumption_card:
            self.handPop(discard)
            game_data._player_discard.append(discard)
        
        game_data._cure_marker[color_index] = 1
        game_data._message = u"■ %sの治療薬を作成しました" % game_data._disease_name[color_index]
        
        return 1
    
    def checkCards(self, selected_card, check_list):
        selected_list = selected_card.split("/")
        
        if len(selected_list) == 4:
            for card in selected_list:
                if card.isdigit():
                    pass
                else:
                    print u" 数値を入力してください"
                    return 1
            
            #重複チェック
            for selected in selected_list:
                if selected_list.count(selected) > 1:
                    print u" 重複した値が入力されています"
                    return 1
            
            for selected in selected_list:
                if check_list.count(int(selected)) == 0:
                    print u" %02d は選択できません" % int(selected)
                    return 1
        else:
            print u" 形式が間違っています"
            return 1
        
        return 0
    
    def isDiscoverCure(self, game_data):
        hand_color = [[], [], [], []]
        
        for card in self._hand:
            hand_color[game_data.getColorIndexFromCity(card)].append(card)
        
        for i in range(4):
            if len(hand_color[i]) >= 4:
                return 1
        return 0
