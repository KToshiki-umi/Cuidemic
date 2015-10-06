"""
BasePlayer.py

Copyright (c) 2015 Toshiki Koizumi

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""

#v.1.00

#! /usr/bin/python
# --*-- coding:utf-8 --*--

class Player:
    def __init__(self):
        self._hand = []				#手札
        self._location = 5			#アトランタ
        self._role = "BasePlayer"	#役職名英名
        #役職名
        self._name = u"            基本プレイヤー"
        self._action_table = [u"", u"車/フェリー                ", u"直行便                     ", u"チャーター便               ", u"シャトル便                 ", u"調査基地の設置             ", u"感染者の治療               ", u"知識の共有(受け取る)       ", u"知識の共有(渡す)           ", u"治療薬の発見               ", u"                           ", u"イベントカードの使用       "]
        self._max_actions = 11
    
    def checkHandNum(self, game_data):
        if len(self._hand) > 7:
            print u" %sの手札が7枚を超えています" % self._role
            for i in range(len(self._hand) - 7):
                discard = self.selectDiscard(u" 捨て札を選択してください\nイベントカードを使用する場合は、そのカード番号を入力してください")
                if 49 <= discard and discard <= 53:
                    game_data._player_discard.append(discard)
                    game_data.useEventCard(discard)
                else:
                    game_data._player_discard.append(discard)
                    game_data._message = u"■%02d:%s を捨てました" % (discard, game_data._card_info[discard])
    
    def handPush(self, card):
        self._hand.append(card)
    
    def handPop(self, card):
        if len(self._hand) != 0:
            if self._hand.count(card) > 0:
                self._hand.remove(card)
            else:
                print u" 入力されたカードは手札にはありません"
                return 1
        else:
            print u" 手札がありません"
            return 1
        
        return 0
    
    def selectDiscard(self, message):
        discard = ""
        
        while(1):
            hands = u""
            for card in self._hand:
                hands += str(card) + u" "
            print u"手札 : " + hands
            
            print message
            discard = raw_input(" > ")
            
            if discard.isdigit():
                if self.handPop(int(discard)) == 0:
                    return int(discard)
            else:
                print u" 数値を入力してください"
    
    def getAvailableAction(self, game_data):
        act_flag = [0]
        
        act_flag.append(self.isDrive(game_data))
        act_flag.append(self.isDirectFlight(game_data))
        act_flag.append(self.isCharterFlight(game_data))
        act_flag.append(self.isShuttleFlight(game_data))
        act_flag.append(self.isBuildResearchStation(game_data))
        act_flag.append(self.isTreatDisease(game_data))
        act_flag.append(self.isTakeKnowledge(game_data))
        act_flag.append(self.isGiveKnowledge(game_data))
        act_flag.append(self.isDiscoverCure(game_data))
        act_flag.append(self.isSpecialAction(game_data))
        act_flag.append(self.isUseEventCard(game_data))
            
        return act_flag

    def selectAction(self, game_data):
        action_flags = self.getAvailableAction(game_data)
        
        while(1):
            print u" アクションを選択してください:"
            act_code = raw_input(" > ")
            
            if act_code.isdigit():
                act_code = int(act_code)
                if 1 <= act_code and act_code <= self._max_actions:
                    if action_flags[act_code] == 0:
                        print u" そのアクションは実行できません"
                    else:
                        if act_code == 1:
                            return self.drive(game_data)
                            
                        elif act_code == 2:
                            return self.directFlight(game_data)
                            
                        elif act_code == 3:
                            return self.charterFlight(game_data)
                            
                        elif act_code == 4:
                            return self.shuttleFlight(game_data)
                            
                        elif act_code == 5:
                            return self.buildResearchStation(game_data)
                            
                        elif act_code == 6:
                            return self.treatDisease(game_data)
                            
                        elif act_code == 7:
                            return self.takeKnowledge(game_data)
                            
                        elif act_code == 8:
                            return self.giveKnowledge(game_data)
                            
                        elif act_code == 9:
                            return self.discoverCure(game_data)
                            
                        elif act_code == 10:
                            return self.specialAction(game_data)
                            
                        elif act_code == 11:
                            return self.useEventCard(game_data)
                            
                else:
                    print u" 範囲外の数値です"
                        
            elif act_code == "/":
                print u" 特殊メニュー"
                game_data.specialMenu()
                return 0
            
            else:
                print u" 数値を入力してください"
    
    def move(self,game_data, dest_list, message):
        information = u""
        cities = u""
        
        if len(dest_list) == 0:
            information = u" 移動可能先 : 全ての都市"
            dest_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48]
        else:
            for city in dest_list:
                cities += u" %02d" % city
        
            information = u" 移動可能先 :%s" % cities
        
        while(1):
            print message
            print information
            destination = raw_input(" > ")
            
            if destination.isdigit():
                if dest_list.count(int(destination)) != 0:
                    self._location = int(destination)
                    game_data._message = u"■%02d:%s に移動しました" % (int(destination), game_data._card_info[int(destination)])
                    return int(destination)
                    
            elif destination == "":
                game_data._message = u"■処理はキャンセルされました"
                return 0
    
    def drive(self, game_data):
        print u"■車/フェリー"
        dest = self.move(game_data, game_data._city_connection_info[self._location], u" どこに移動しますか？")
        
        if dest == 0:
            return 0
        else:
            return 1
    
    def directFlight(self, game_data):
        print u"■直行便"
        dest_list = []
        
        for city in self._hand:
            if 1 <= city and city <= 48:
                dest_list.append(city)
        
        dest = self.move(game_data, dest_list, u" どこに飛びますか？")
        
        if dest == 0:
            return 0
        else:
            self._hand.remove(dest)
            game_data._player_discard.append(dest)
            return 1
    
    def charterFlight(self, game_data):
        print u"■チャーター便"
        here = self._location
        dest_list = []
        
        dest = self.move(game_data, dest_list, u" どこに飛びますか？")
        
        if dest == 0:
            return 0
        else:
            self._hand.remove(here)
            game_data._player_discard.append(here)
            return 1
        
    def shuttleFlight(self, game_data):
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
        
    def buildResearchStation(self, game_data):
        print u"■調査基地の設置"
        game_data._research_station_flag[self._location] = 1
        player._hand.remove(self._location)
        game_data._player_discard.append(self._location)
        game_data._message = u"■ %02d:%s に調査基地を建設しました" % (self._location, game_data._card_info[self._location])
        return 1
        
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
                    game_data._message = u"■処理はキャンセルされました"
                    return 0
                else:
                    print u" 数値を入力してください"
        
        game_data.cureDisease(self._location, 1, color_index)
        game_data._message = u"■%02d:%s で%sの治療を行いました" % (self._location, game_data._card_info[self._location], game_data._disease_name[color_index])
        return 1
        
    def takeKnowledge(self, game_data):
        print u"■知識の共有(受け取る)"
        
        take_list = []
        for i in range(game_data._player_num):
            if game_data._player[i]._location == self._location:
                if game_data._player[i]._role == "Researcher":
                    take_list.append(i)
                else:
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
                    take_card = 0
                    
                    if game_data._player[player]._role == "Researcher":
                        take_card_str = u" 受け取り可能カード："
                        
                        for tc in game_data._player[player]._hand:
                            take_card_str += u" %02d" % tc
                        
                        print u" 研究者から受け取るカードを選択してください"
                        print take_card_str
                        selected_card = raw_input(" > ")
                        
                        while(1):
                            if selected_card.isdigit():
                                if game_data._player[player]._hand.count(int(selected_card)) > 0:
                                    take_card = int(selected_card)
                                else:
                                    print u" 入力された値は範囲外です"
                                    
                            elif selected_card == "":
                                game_data._message = u"■処理はキャンセルされました"
                                return 0
                            else:
                                print u" 数値を入力してください"
                    
                    else:
                        take_card = self._location
                        
                    
                    if take_card > 0:
                        game_data._player[player].handPop(take_card)
                        self.handPush(take_card)
                        self.checkHandNum(game_data)
                        game_data._message = u"■プレーヤー:%d から %02d:%s を受け取りました" % (player+1, take_card, game_data._card_info[take_card])
                        
                        return 1
                
                else:
                    print u" 入力された値は範囲外です"
            elif player == "":
                game_data._message = u"■処理はキャンセルされました"
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
            print u"\n %02d:%s を渡すプレーヤーを選択してください" % (self._location, game_data._card_info[self._location])
            give_str = u" 選択可能プレイヤー："
            for pl in give_list:
                give_str += u"%2d" % (pl + 1)
            
            player = raw_input(" > ")
            
            if player.isdigit():
                player = int(player) - 1
                if give_list.count(player) > 0:
                    self.handPop(self._location)
                    game_data._player[player].handPush(self._location)
                    game_data._player[player].checkHandNum(game_data)
                    
                    game_data._message = u"■ プレーヤー%2d に %02d:%s を渡しました" % (player + 1, self._location, game_data._card_info[self._location])
                    return 1
                else:
                    print u" 入力された値は範囲外です"
            elif player == "":
                game_data._message = u"■処理はキャンセルされました"
                return 0
            else:
                print u" 数値を入力してください"
        
        return 1
        
    def discoverCure(self, game_data):
        print u"■治療薬の発見"
        color_index = -1
        hand_color = [[], [], [], []]
        
        for card in self._hand:
            hand_color[game_data.getColorIndexFromCity(card)].append(card)
        
        for i in range(4):
            if len(hand_color[i]) >= 5:
                color_index = i
                break
        
        consumption_card = []
        if len(hand_color[color_index]) == 5:
            consumption_card = hand_color[color_index]
        
        else:
            while(1):
                available_cards = ""
                
                for card in hand_color[color_index]:
                    available_cards += " %02d" % card
                
                print u"\n 作成に使用するカードを5枚選択してください"
                print u" 例) > 04/01/05/11/10"
                print u" 選択可能カード：%s" % available_cards
                selected_card = raw_input(" > ")
                
                if selected_card == "":
                    game_data._message = u"■処理はキャンセルされました"
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
        game_data._message = u"■%sの治療薬を作成しました" % game_data._disease_name[color_index]
        
        return 1
        
    def specialAction(self, game_data):
        return 0
        
    def useEventCard(self, game_data):
        print u"■イベントカードの使用"
        game_data.selectEventCard(game_data.getUsableEventCard())
        
        return 0
    
    def checkCards(self, selected_card, check_list):
        selected_list = selected_card.split("/")
        
        if len(selected_list) == 5:
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
    
    #0:不可、1:受け取り可能、2:受け渡し可能、3:両方可
    def checkShareableKnowledge(self, game_data):
        player_list = []
        
        for i in range(game_data._player_num):
            if self._location == game_data._player[i]._location:
                player_list.append(i)
        
        if len(player_list) < 2:
            return 0
        
        take_flag = 0
        give_flag = 0
        
        for player in game_data._player:
            if player._hand.count(self._location) > 0:
                #対象都市に2人以上おり、かつその内の誰かが対象都市のカードを持っている状態
                if self._hand.count(self._location) > 0:
                    #自分が対象都市カードを持っている
                    give_flag = 1
                else:
                    #他のプレイヤーが持っている
                    take_flag = 1
                
                break
        
        #研究員が同じ都市にいるか？
        for player in game_data._player:
            if player._role == "Researcher":
                take_flag = 1
                break
        
        if give_flag == 1 and take_flag == 1:
            return 3
        elif give_flag == 1 and take_flag == 0:
            return 2
        elif give_flag == 0 and take_flag == 1:
            return 1
        
        return 0
    
    def isDrive(self, game_data):
        return 1
    
    def isDirectFlight(self, game_data):
        for city in self._hand:
            if 1 <= city and city <= 48:
                return 1
        
        return 0
    
    def isCharterFlight(self, game_data):
        for city in self._hand:
            if city == self._location:
                return 1
        
        return 0
    
    def isShuttleFlight(self, game_data):
        if game_data._research_station_flag[self._location] == 1:
            return 1
        
        return 0
    
    def isBuildResearchStation(self, game_data):
        if game_data._research_station_flag[self._location] == 0:
            for city in self._hand:
                if city == self._location:
                    return 1
        
        return 0
    
    def isTreatDisease(self, game_data):
        for disease in game_data._infection_status[self._location]:
            if disease != 0:
                return 1
        
        return 0
    
    def isTakeKnowledge(self, game_data):
        ret = self.checkShareableKnowledge(game_data)
        
        if ret == 1 or ret == 3:
            return 1
        
        return 0
    
    def isGiveKnowledge(self, game_data):
        ret = self.checkShareableKnowledge(game_data)
        
        if ret == 2 or ret == 3:
            return 1
        
        return 0
    
    def isDiscoverCure(self, game_data):
        hand_color = [[], [], [], []]
        
        for card in self._hand:
            hand_color[game_data.getColorIndexFromCity(card)].append(card)
        
        for i in range(4):
            if len(hand_color[i]) >= 5:
                return 1
        return 0
    
    def isSpecialAction(self, game_data):
        return 0
    
    def isUseEventCard(self, game_data):
        if len(game_data.getUsableEventCard()) > 0:
            return 1
        
        return 0
    
    