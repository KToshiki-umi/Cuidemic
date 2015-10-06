#! /usr/bin/python
# --*-- coding:utf-8 --*--

"""
Resercher.py

Copyright (c) 2015 Toshiki Koizumi

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""

#v.1.01

from Player import Player

class Researcher(Player):
    def __init__(self):
        Player.__init__(self)
        self._role = "Researcher"	#役職名英名
        #役職名
        self._name = u"                    研究者"

    def takeKnowledge(self, game_data):
        print u"■知識の共有(受け取る)"
        
        take_list = []
        for i in range(game_data._player_num):
            if game_data._player[i]._location == self._location:
                for card in game_data._player[i]._hand:
                    if card == self._location:
                        take_list.append(i)
        
        while(1):
            take_str = u" 選択可能可能プレイヤー："
            
            for pl in take_list:
                take_str += u"%2d" % (pl+1)
            
            print u"\n カードをどのプレーヤーから受け取るか選択してください"
            print take_str
            player = raw_input(" > ")
            
            if player.isdigit():
                player = int(player) - 1
                if take_list.count(player) > 0:
                    take_card = self._location
                    
                    game_data._player[player].handPop(take_card)
                    self.handPush(take_card)
                    self.checkHandNum(game_data)
                    game_data._message = u"■ プレーヤー:%d から %02d:%s を受け取りました" % (player+1, take_card, game_data._card_info[take_card])
                    
                    return 1
                
                else:
                    print u" 入力された値は範囲外です"
            elif player == "":
                game_data._message = u"■ 処理はキャンセルされました"
                return 0
            else:
                print u" 数値を入力してください"
        
        return 1
        
    def giveKnowledge(self, game_data):
        print u"■知識の共有(渡す)"
        
        give_list = []
        for i in range(game_data._player_num):
            if game_data._player[i]._location == self._location:
                give_list.append(i)
        give_list.remove(game_data._turn_counter % game_data._player_num)
        
        while(1):
            print u"\n カードを渡すプレーヤーを選択してください"
            give_str = u" 選択可能プレイヤー："
            for pl in give_list:
                give_str += u"%2d" % (pl + 1)
            
            player = raw_input(" > ")
            
            if player.isdigit():
                player = int(player) - 1
                if give_list.count(player):
                    while(1):
                        give_card_str = u" 受け渡し可能カード："
                        
                        for hand in self._hand:
                            give_card_str += u" %02d" % hand
                        
                        print u" 渡すカードを選択してください"
                        print give_card_str
                        give_card = raw_input(" > ")
                        
                        if give_card.isdigit():
                            give_card = int(give_card)
                            if self._hand.count(give_card) > 0:
                                self.handPop(give_card)
                                game_data._player[player].handPush(give_card)
                                game_data._player[player].checkHandNum(game_data)
                                
                                game_data._message = u"■ プレーヤー%2d に %02d:%s を渡しました" % (player + 1, self._location, game_data._card_info[self._location])
                                return 1
                            else:
                                print u" 入力された値は範囲外です"
                            
                        elif give_card == "":
                            game_data._message = u"■ 処理はキャンセルされました"
                            return 0
                        else:
                            print u" 数値を入力してください"
                    
                else:
                    print u" 入力された値は範囲外です"
            elif player == "":
                game_data._message = u"■ 処理はキャンセルされました"
                return 0
            else:
                print u" 数値を入力してください"
        
        return 1
    
    #0:不可、1:受け取り可能、2:受け渡し可能、3:両方可
    def checkShareableKnowledge(self, game_data):
        player_list = []
        
        for i in range(game_data._player_num):
            if self._location == game_data._player[i]._location:
                player_list.append(i)
        
        if len(player_list) < 2:
            return 0
        
        take_flag = 0
        give_flag = 1
        
        for player in game_data._player:
            if player._hand.count(self._location) > 0:
                #対象都市に2人以上おり、かつその内の誰かが対象都市のカードを持っている状態
                if self._hand.count(self._location) != 0:
                    #対象都市カードを他のプレイヤーが持っている
                    take_flag = 1
                break
        
        if give_flag == 1 and take_flag == 1:
            return 3
        elif give_flag == 1 and take_flag == 0:
            return 2
        elif give_flag == 0 and take_flag == 1:
            return 1
        
        return 0