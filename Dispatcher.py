#! /usr/bin/python
# --*-- coding:utf-8 --*--

"""
OperationExpert.py

Copyright (c) 2015 Toshiki Koizumi

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""

#v.1.01

from Player import Player

class Dispatcher(Player):
    def __init__(self):
        Player.__init__(self)
        self._role = "Dispatcher"	#役職名英名
        self._action_table = [u"", u"車/フェリー                ", u"直行便                     ", u"チャーター便               ", u"シャトル便                 ", u"調査基地の設置             ", u"感染者の治療               ", u"知識の共有(受け取る)       ", u"知識の共有(渡す)           ", u"治療薬の発見               ", u"他プレイヤーの移動         ", u"イベントカードの使用       "]
        self._special_action_table = [u"", u"車/フェリー", u"直行便", u"チャーター便", u"シャトル便", u"他プレイヤーコマへの移動"]
        #役職名
        self._name = u"                通信司令員"
    
    def isSpecialAction(self, game_data):
        return 1
    
    def specialAction(self, game_data):
        selectable_player_list = []
        selectable_action_list = []
        str2 = u" 指定可能プレイヤー：1～%d" % game_data._player_num
        selected_player = 0
        selected_action = 0
        
        # プレイヤーの選択
        while(1):
            selected_player = game_data.getNumFromKey(u" 移動するプレイヤーを指定してください", str2)
            
            if selected_player == -1:
                game_data._message = u"■処理はキャンセルされました"
                return 0;
            elif 1 <= selected_player and selected_player <= game_data._player_num:
                selected_player = game_data._player[selected_player - 1]
                break;
        
        # アクションの選択
        selectable_action_list = self.getSelectableAction(game_data, selected_player)
        str2 = u" 指定可能アクション:"
        
        for selectable_action in selectable_action_list:
            str2 += u" %d:%s" % (selectable_action, self._special_action_table[selectable_action])
        
        while(1):
            selected_action = game_data.getNumFromKey(u" 実行するアクションを指定してください", str2)
            
            if selected_action == -1:
                game_data._message = u"■処理はキャンセルされました"
                return 0;
            elif selectable_action_list.count(selected_action) == 1:
                if selected_action == 1:
                    return self.specialDrive(game_data, selected_player)
                elif selected_action == 2:
                    return self.specialDirectFlight(game_data, selected_player)
                elif selected_action == 3:
                    return self.specialCharterFlight(game_data, selected_player)
                elif selected_action == 4:
                    return self.specialShuttleFlight(game_data, selected_player)
                elif selected_action == 5:
                    return self.specialMoveToPlayer(game_data, selected_player)
        return 0
    
    def getSelectableAction(self, game_data, selected_player):
        selectable_action_list = []
        
        # 車/フェリー
        selectable_action_list.append(1)
        
        # 直行便
        if(self.isDirectFlight(game_data)):
            selectable_action_list.append(2)
        
        # チャーター便
        if(self.isSpecialCharterFlight(selected_player)):
            selectable_action_list.append(3)
        
        # シャトル便
        if(selected_player.isShuttleFlight(game_data)):
            selectable_action_list.append(4)
        
        # 他プレイヤーコマへの移動
        selectable_action_list.append(5)
    
        return selectable_action_list
    
    def isSpecialCharterFlight(self, selected_player):
        for city in self._hand:
            if city == selected_player._location:
                return 1
        
        return 0
    
    def specialDrive(self, game_data, selected_player):
        selected_player.drive(game_data)
        return 1
    
    def specialDirectFlight(self, game_data, selected_player):
        print u"■直行便"
        dest_list = []
        
        for city in self._hand:
            if 1 <= city and city <= 48:
                dest_list.append(city)
        
        dest = selected_player.move(game_data, dest_list, u" どこに飛びますか？")
        
        if dest == 0:
            return 0
        else:
            self._hand.remove(dest)
            game_data._player_discard.append(dest)
            return 1
    
    def specialCharterFlight(self, game_data, selected_player):
        print u"■チャーター便"
        here = selected_player._location
        dest_list = []
        
        dest = self.move(game_data, dest_list, u" どこに飛びますか？")
        
        if dest == 0:
            return 0
        else:
            self._hand.remove(here)
            game_data._player_discard.append(here)
            return 1
    
    def specialShuttleFlight(self, game_data, selected_player):
        print u"■シャトル便"
        dest_list = []
        
        for city_no in range(1,49):
            if game_data._research_station_flag[city_no] == 1:
                dest_list.append(city_no)
        
        dest = self.move(game_data, dest_list, u" どこに飛びますか？")
        
        if dest == 0:
            return 0
        else:
            return 1
    
    def specialMoveToPlayer(self, game_data, selected_player):
        selectable_player_list = []
        str2 = u" 指定可能プレイヤー：1～%d" % game_data._player_num
        
        # プレイヤーの選択
        while(1):
            selected_dest_player = game_data.getNumFromKey(u" 移動先のプレイヤーを指定してください", str2)
            
            if selected_dest_player == -1:
                game_data._message = u"■処理はキャンセルされました"
                return 0;
            elif 1 <= selected_dest_player and selected_dest_player <= game_data._player_num:
                selected_dest_player -= 1
                selected_player._location = game_data._player[selected_dest_player]._location
                game_data._message = u"■%02d:%s に移動しました" % (selected_player._location, game_data._card_info[selected_player._location])
                return 1
