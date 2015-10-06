"""
ContingencyPlanner.py

Copyright (c) 2015 Toshiki Koizumi

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""

#v.1.00

#! /usr/bin/python
# --*-- coding:utf-8 --*--

from Player import Player

class ContingencyPlanner(Player):
    def __init__(self):
        Player.__init__(self)
        self._role = "ContingencyPlanner"	#役職名英名
        #役職名
        self._name = u"%2s              危機管理官"
        self._action_table = [u"", u"車/フェリー                ", u"直行便                     ", u"チャーター便               ", u"シャトル便                 ", u"調査基地の設置             ", u"感染者の治療               ", u"知識の共有(受け取る)       ", u"知識の共有(渡す)           ", u"治療薬の発見               ", u"イベントカードの再利用     ", u"イベントカードの使用       "]
        self._reuse_ev_card = 0
        
    def specialAction(self, game_data):
        if self._reuse_ev_card == 0:
            #捨て札からイベントカード取得
            discard_ev_card_list = []
            for discard in game_data._player_discard:
                if 49 <= discard and discard <= 53:
                    discard_ev_card_list.append(discard)
            
            while(1):
                #選択
                print u" 確保するカードを選択してください。"
                #リストを表示
                ev_card_str = u""
                
                for ev_card in discard_ev_card_list:
                    ev_card_str += u" %02d" % ev_card
                
                print ev_card_str
                selected_card = raw_input(" > ")
                
                if selected_card == "":
                    game_data._message = u"■ 処理はキャンセルしました"
                    return 0
                
                if selected_card.isdigit():
                    selected_card = int(selected_card)
                    
                    if discard_ev_card_list.count(selected_card) == 1:
                        self._reuse_ev_card = selected_card
                        game_data._player_discard.remove(selected_card)
                        game_data._message = u"■ %sを確保しました" % game_data._card_info[selected_card]
                        return 1
                    else:
                        print u" そのカードは指定できません"
                            
                else:
                    print u" 数値を入力してください"
        return 0
    
    def isSpecialAction(self, game_data):
        if self._reuse_ev_card != 0:
            return 0
        
        discard_ev_card_list = []
        
        for discard in game_data._player_discard:
            if 49 <= int(discard) and int(discard) <= 53:
                    discard_ev_card_list.append(int(discard))
            
        if len(discard_ev_card_list) == 0:
            return 0
            
        return 1