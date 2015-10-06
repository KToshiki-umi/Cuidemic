"""
Cuidemic.py

Copyright (c) 2015 Toshiki Koizumi

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""

#v.1.00

#! /usr/bin/python
# --*-- coding:utf-8 --*--

# TODO
# 通信司令官の実装 ※あとはこれだけ！
# 作戦エキスパートの特殊能力実装していない気がする(調査基地じゃない方)
# 引いたカードがエピ+エピ、エピ+イベントカードの時正しく動作する？はず
# 空輸で衛生兵を移動させたときに、治療薬作成済みであれば治療 ←確認必要

import random
import os

from Player import Player
from Scientist import Scientist
from ContingencyPlanner import ContingencyPlanner
from Dispatcher import Dispatcher
from Medic import Medic
from OperationExpert import OperationExpert
from QuarantineSpecialist import QuarantineSpecialist
from Researcher import Researcher

class Cuidemic:
    _map = []							#マップ
    _player = []						#プレイヤー
    _player_num = 0						#プレイヤー数
    _turn_counter = 0					#ターンカウンタ
    _difficulty = 0						#難易度
    _infection_deck = []				#感染カード：山札
    _infection_discard = []				#感染カード：捨て札
    _player_deck = []					#都市カード：山札
    _player_discard = []				#都市カード：捨て札
    _outbreak_marker = 0				#アウトブレイクマーカー
    _infection_rate_marker = 1			#感染率マーカー
    _disease_cube = [24,24,24,24]		#感染駒残数[青,黄,黒,赤]
    _cure_marker = [0,0,0,0]			#治療薬マーカー[青,黄,黒,赤], 0:未完成、1:完成、2:根絶
    _research_station_num = 5			#調査基地残数
    
    #都市汚染状況[青,黒,黄,赤]
    _infection_status = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    #感染ゲージ
    _infection_gauge = [0,2,2,2,3,3,4,4]
    #カード情報
    _card_info = {1 : u"サンフランシスコ",2 : u"シカゴ",3 : u"トロント",4 : u"ニューヨーク",5 : u"アトランタ",6 : u"ワシントン",7 : u"ロンドン",8 : u"エッセン",9 : u"サンクトペテルブルグ",10 : u"パリ",11 : u"ミラノ",12 : u"マドリード",13 : u"ロサンゼルス",14 : u"マイアミ",15 : u"メキシコシティ",16 : u"ボゴダ",17 : u"リマ",18 : u"サンパウロ",19 : u"サンチアゴ",20 : u"ブエノスアイレス",21 : u"ラゴス",22 : u"ハルツーム",23 : u"キンシャサ",24 : u"ヨハネスブルク",25 : u"モスクワ",26 : u"テヘラン",27 : u"デリー",28 : u"イスタンブール",29 : u"アルジェ",30 : u"カイロ",31 : u"バグダッド",32 : u"カラチ",33 : u"カルカッタ",34 : u"ムンバイ",35 : u"リヤド",36 : u"チェンナイ",37 : u"北京",38 : u"ソウル",39 : u"東京",40 : u"上海",41 : u"大阪",42 : u"香港",43 : u"台北",44 : u"バンコク",45 : u"ホーチミン",46 : u"マニラ",47 : u"ジャカルタ",48 : u"シドニー",49 : u"予測",50 : u"空輸",51 : u"政府の援助",52 : u"人口回復",53 : u"静かな夜"}
    #病原体名
    _disease_name = [u"炭疽菌(青)", u"腸チフス(黄)", u"エボラ出血熱(黒)", u"天然痘(赤)"]

    _one_quiet_night = 0	#静かな夜フラグ
    #アウトブレイクフラグ[青,黒,黄,赤]
    _outbreak_flag = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    #隣接都市情報 {地域:[隣接都市番号,...]}
    _city_connection_info = [[], [2,13,46,39],[3,5,15,13,1],[4,6,5,2],[7,12,6,3],[3,6,14,2],[4,14,5,3],[8,10,12,4],[9,11,10,7],[25,28,8],[8,11,29,12,7],[28,10,8],[10,29,18,4,7],[2,15,48,1],[6,16,15,5],[14,16,17,13,2],[18,20,17,15,14],[16,19,15],[12,21,20,16],[17],[18,16],[22,23,18],[24,23,21,30],[22,24,21],[23,22],[26,28,9],[27,32,25],[33,36,34,32,26],[25,31,30,29,11,9],[28,30,12,10],[28,31,35,22,29],[32,35,30,28],[27,34,35,31,26],[42,44,36,27],[27,36,32],[32,30,31],[33,44,47,34,27],[38,40],[39,40,37],[1,41,38],[38,43,42,37],[39,43],[40,43,46,45,44,33],[41,46,42,40],[42,45,47,36,33],[46,47,44,42],[1,48,45,42,43],[45,48,36,44],[13,47,46]]
    #調査基地フラグ
    _research_station_flag = [0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    #役職一覧
    _role_list = [u"作戦エキスパート", u"衛生兵", u"通信司令員", u"研究者", u"科学者", u"検疫官", u"危機管理官"]
    _role_list_en = ["OperationExpert", "Medic", "Dispatcher", "Researcher", "Scientist", "QuarantineSpecialist", "ContingencyPlanner"]
    
    #メッセージ
    _message = ""
    
    def __init__(self):
        print u"■プレイ人数と難易度の設定"
        while(1):
            print u" プレイ人数(2-4)と難易度(1-3)を選択してください"
            print u" 例)2人プレイで難易度を1に設定する場合'2-1'と入力"
            data = raw_input(" > ")
                       
            game_setting = data.split("-")
            
            if len(game_setting) != 2:
                print u" 形式が違います\n"
            else:
                if game_setting[0].isdigit() and game_setting[1].isdigit():
                    if 2 <= int(game_setting[0]) and int(game_setting[0]) <= 4:
                         if 1 <= int(game_setting[1]) and int(game_setting[1]) <= 3:
                             self._player_num = int(game_setting[0])
                             self._difficulty = int(game_setting[1])
                             break
                         else:
                             print u" 難易度の値が範囲外です\n"
                    else:
                        print u" プレイ人数が範囲外です\n"
                else:
                    print u" 数値を入力してください\n"
    
    def putDiseaseCube(self, city_no, num, color):
        self._infection_status[city_no][color] += num
        
        diff = 0
        
        if self._infection_status[city_no][color] > 3:
            diff = self._infection_status[city_no][color] - 3
            self._infection_status[city_no][color] = 3
            
            if self._outbreak_flag[city_no][color] == 0:
                self._outbreak_flag[city_no][color] = 1
            
        elif self._infection_status[city_no][color] < 0:
            diff = self._infection_status[city_no][color]
            self._infection_status[city_no][color] = 0
        
        self._disease_cube[color] -= (num - diff)
    
    def getColorIndexFromCity(self, city_no):
        color_index = -1
        if 1 <= city_no and city_no <= 12:
            color_index = 0
        elif 13 <= city_no and city_no <= 24:
            color_index = 1
        elif 25 <= city_no and city_no <= 36:
            color_index = 2
        elif 37 <= city_no and city_no <= 48:
            color_index = 3
        
        return color_index
    
    def getColorNameFromColorIndex(self, color_index):
        color_name = ""
        
        if color_index == 0:
            color_name = u"青"
        elif color_index == 1:
            color_name = u"黄"
        elif color_index == 2:
            color_name = u"黒"
        elif color_index == 3:
            color_name = u"赤"
        
        return color_name
    
    def getColorIndex(self, city_no, color):
        color_index = -1
        
        if color == -1:
            color_index = self.getColorIndexFromCity(city_no)
        else:
            color_index = color
        
        return color_index
    
    # 色指定をしない場合は、その都市の色で治療する
    def cureDisease(self, city_no, num, color=-1):
        color_index = self.getColorIndex(city_no, color)
        
        self.putDiseaseCube(city_no, -1*num, color_index)
        
    # 色指定をしない場合は、その都市の色で感染する
    def infection(self, city_no, num, color=-1):
        color_index = self.getColorIndex(city_no, color)
        
        if self._cure_marker[color_index] == 2 or self.isQuarantineSpecialist(city_no):
            #根絶、もしくは検疫官の影響下
            return 0
            
        elif self._cure_marker[color_index] == 1:
            #治療薬ありの場合
            self.putDiseaseCube(city_no, num, color_index)
            
            if self._disease_cube[color_index] < 0:
                return 1
            
            if self.isMedic(city_no):
                self.putDiseaseCube(city_no, -1 * num, color_index)
                return 0
            
        else:
            self.putDiseaseCube(city_no, num, color_index)
        
        if self.outbreak(city_no, color_index) == 1:
            return 1
        
        if self._disease_cube[color_index] < 0:
            print u" %sの病原体コマがなくなりました" % self.getColorNameFromColorIndex(color_index)
            return 1
        
        return 0
    
    def isQuarantineSpecialist(self, city_no):
        effective_area = []
        
        for player in self._player:
            if player._role == "QuarantineSpecialist":
                effective_area.append(player._location)
        
        if len(effective_area) == 0:
            return False
        
        for area in self._city_connection_info[effective_area[0]]:
            effective_area.append(area)
        
        if effective_area.count(city_no) > 0:
            return True
        
        return False
    
    def isMedic(self, city_no):
        for player in self._player:
            if player._role == "Medic":
                if player._location == city_no:
                    return True
                else:
                    return False
        
    def selectRole(self):
        for i in range(self._player_num):
            os.system("cls")
            print u"■プレイヤーの選択"
            
            while(1):
                print u" \n第%dプレ－ヤーを選択してください。" % (i+1)
                selectable_list = self.printSelectableRoleList()
                role_index = raw_input(" > ")
                
                if role_index.isdigit():
                    role_index = int(role_index) - 1
                    if selectable_list.count(role_index) > 0:
                        self._player.append(self.getRoleFromIndex(role_index))
                        break
                    else:
                        print u" 入力された値は範囲外です"
                else:
                    print u" 数値を入力してください"
    
    def printSelectableRoleList(self):
        selectable_str = u"選択可能役職：\n"
        selectable_list = []
        
        for i in range(len(self._role_list_en)):
            selected_flag = 0
            
            for pl in self._player:
                if pl._role == self._role_list_en[i]:
                    selected_flag = 1
                    break
            
            if selected_flag == 0:
                selectable_str += u"  %d:%s\n" % (i+1, self._role_list[i])
                selectable_list.append(i)
        
        print selectable_str
        return selectable_list
    
    def getRoleFromIndex(self, role_index):
        player_inst = None
        
        if role_index == 0:
            player_inst = OperationExpert()
            
        elif role_index == 1:
            player_inst = Medic()
            
        elif role_index == 2:
            player_inst = Dispatcher()
            
        elif role_index == 3:
            player_inst = Researcher()
            
        elif role_index == 4:
            player_inst = Scientist()
            
        elif role_index == 5:
            player_inst = QuarantineSpecialist()
            
        elif role_index == 6:
            player_inst = ContingencyPlanner()
        
        return player_inst
    
    def makeHand(self, player_card):
        first_hand = 0	#開始時の手札の数
        if self._player_num == 2:
            first_hand = 4
        elif self._player_num == 3:
            first_hand = 3
        elif self._player_num == 4:
            first_hand = 2
        
        for i in range(first_hand):
            for j in range(self._player_num):
                self._player[j].handPush(player_card.pop(random.randrange(len(player_card))))
    
    def preparePlayerDeck(self, player_card):
        epidemic_card_num = self._difficulty + 3
        
        random.seed()
        temp_deck = []
        
        #デッキの番兵
        self._player_deck.append(-2)
        
        for i in range(epidemic_card_num):
            temp_deck.append([])
        
        for i in range(len(player_card)):
            temp_deck[i % epidemic_card_num].append(player_card.pop(random.randrange(len(player_card))))
        
        for t_deck in temp_deck:
            t_deck.insert(random.randrange(len(t_deck)), -1)
        
        for i in range(epidemic_card_num):
            for card in temp_deck[epidemic_card_num - 1 - i]:
                self._player_deck.append(card)
    
    def prepareInfectionDeck(self):
        #カードシャッフル用
        infection_card = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48]
        
        for i in range(len(infection_card)):
            self._infection_deck.append(infection_card.pop(random.randrange(len(infection_card))))
    
    def infectionNineCity(self):
        for i in range(9):
            card = self.infectionDeckPop()
            self.infection(card, (8-i+3)/3)
        
    def infectionDeckPop(self, index=-1):
        discard = -1
        
        if index == -1:
            discard = self._infection_deck.pop()
        else:
            discard = self._infection_deck.pop(index)
        
        self._infection_discard.append(discard)
        
        return discard
    
    def run(self):
        #カードシャッフル用
        player_card = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53]
        
        random.seed()
        self.prepareInfectionDeck()
        self.infectionNineCity()
        self.selectRole()
        self.makeHand(player_card)
        self.preparePlayerDeck(player_card)
        self._turn_counter = 0
        
        while(1):
            result = self.phase(self._turn_counter % self._player_num)
            if result != 0:
                if result == 1:
                    print u" 人類は救われました\nあなたたちの勝利です"
                elif result == -1:
                    print u" 人類は絶滅しました\nあなたたちの敗北です"
                    
                buf = raw_input("press Enter")
                break
            else:
                self._turn_counter = self._turn_counter + 1
    
    def phase(self, num):
        gameover = -1
        win = 1
        player = self._player[num]
        
        max = 4
        counter = 0
        #プレイヤーアクション
        while(counter < max):
            #画面を切り替え
            self.printMap(num, counter)
            
            result =  player.selectAction(self)
            
            counter += result
        
        #勝利条件達成チェック
        if self.checkWin() == 1:
            return win
        
        #根絶状況チェック
        self.checkEradication()
        
        #画面を切り替え
        self.printMap()
        
        buf = raw_input("press Enter")
        
        #プレイヤーカードを引く
        if self.drawPlayerCard(player) == 1:
            return gameover
        
        #画面を切り替え
        self.printMap()
        
        #イベントカード使用の有無
        self.confEventCard()
        
        #画面を切り替え
        self.printMap()
        
        #感染の処理
        if self._one_quiet_night == 0:
            if self.drawInfectionCard() != 0:
                return gameover
        else:
            self._one_quiet_night = 0
            self._message = u"■静かな夜により感染の処理はスキップされました"
        
        return 0
    
    def drawPlayerCard(self, player):
        self._message += u"■プレイヤーカードを2枚引く\n"
        epidemic_count = 0
        
        for i in range(2):
            draw_card = self._player_deck.pop()
            
            if draw_card == -1:
                self._message += u" エピデミックカードを引きました\n"
                epidemic_count += 1
                
            elif draw_card == -2:
                #引けるカードがなくなった場合
                print u" プレイヤーカードがなくなりました"
                return 1
            else:
                player.handPush(draw_card)
                self._message += u" %02d:%s を引きました\n" % (draw_card, self._card_info[draw_card])
        
        #手札の更新
        self.printMap()
        
        if epidemic_count != 0:
            for i in range(epidemic_count):
                if self.epidemic() == 1:
                    return 1
        
        player.checkHandNum(self)
        
        buf = raw_input("press Enter")
        
        return 0
    
    def drawInfectionCard(self):
        for i in range(self._infection_gauge[self._infection_rate_marker]):
            print u"■感染の処理"
            draw_card = self.infectionDeckPop()
            print u" %02d:%s を引きました" % (draw_card, self._card_info[draw_card])
            
            if self.infection(draw_card, 1) == 1:
                return 1
            #アウトブレイクフラグの初期化
            self.clearOutbreakFlag()
            
            buf = raw_input("press Enter")
            self.printMap()
        
        return 0
    
    def clearOutbreakFlag(self):
        for i in range(49):
            self._outbreak_flag[i] = [0,0,0,0]
    
    def outbreak(self, city_no, color_index):
        if self._outbreak_flag[city_no][color_index] == 1:
            print u"■%02d:%s でアウトブレイク" % (city_no, self._card_info[city_no])
            
            self._outbreak_flag[city_no][color_index] = 2
            self._outbreak_marker += 1
            
            if self._outbreak_marker > 7:
                print u" 8回目のアウトブレイクです"
                return 1
            
            for connected_city in self._city_connection_info[city_no]:
                if self.infection(connected_city, 1, color_index) == 1:
                    return 1
                
        return 0
    
    def epidemic(self):
        print u"■エピデミックの発生"
        
        #感染率の上昇
        self._infection_rate_marker += 1
        
        #感染
        draw_card = self.infectionDeckPop(0)
        print u" %02d:%s を引きました" % (draw_card, self._card_info[draw_card])
        
        if self.infection(draw_card, 3) == 1:
            return 1
        
        #アウトブレイクフラグの初期化
        self.clearOutbreakFlag()
        
        #度合いの増加
        for i in range(len(self._infection_discard)):
            self._infection_deck.append(self._infection_discard.pop(random.randrange(len(self._infection_discard))))
        
        return 0
    
    def confEventCard(self):
        usable_ev_cards = self.getUsableEventCard()
        
        if len(usable_ev_cards) != 0:
            print u" イベントカードを使用しますか？"
            self.selectEventCard(usable_ev_cards)
        
    
    def getUsableEventCard(self, a=1, b=1, c=1, d=1, e=1):
        usable_list = []
        target = []
        
        if a == 1:
            target.append(49)
        if b == 1:
            target.append(50)
        if c == 1:
            target.append(51)
        if d == 1:
            target.append(52)
        if e == 1:
            target.append(53)
        
        for player in self._player:
            for hand in player._hand:
                for ev_card in target:
                    if ev_card == hand:
                        usable_list.append(hand)
            
            if player._role == "ContingencyPlanner":
                if player._reuse_ev_card != 0:
                    usable_list.append(player._reuse_ev_card)
        
        return usable_list
    
    def selectEventCard(self, usable_list):
        while(1):
            print u" 使用するイベントカードを指定してください"
            
            card_list_str = ""
            for card_no in usable_list:
                card_list_str += u" %02d" % card_no
            
            print u" 使用可能なイベントカード：" + card_list_str
            
            ev_card = raw_input(" > ")
            
            if ev_card.isdigit():
                ev_card = int(ev_card)
                if 49 <= ev_card and ev_card <= 53:
                    if usable_list.count(ev_card) == 1:
                        result = self.useEventCard(ev_card)
                        
                        if result == 1:
                            self.discardEventCard(ev_card)
                            break
                        
                    else:
                        print u" そのイベントカードは使用できません"
                else:
                    print u" イベントカードの番号を入力してください"
            elif ev_card == "":
                break
                
            else:
                print u" 数値を入力してください"
        
    def useEventCard(self, ev_card):
        result = 0
        if ev_card == 49:
            # 予測
            result = self.useForecast()
        elif ev_card == 50:
            # 空輸
            result = self.useAirlift()
        elif ev_card == 51:
            # 政府の援助
            result = self.useGovernmentGrant()
        elif ev_card == 52:
            # 人口回復
            result = self.useResilientPopulation()
        elif ev_card == 53:
            # 静かな夜
            result = self.useOneQuietNight()
        
        return result
    
    def discardEventCard(self, ev_card):
        # 手札にあるのか危機管理官が確保したものなのかをチェック
        for player in self._player:
            for hand in player._hand:
                if ev_card == hand:
                    # 手札にあれば捨て札に追加
                    player._hand.remove(hand)
                    self._player_discard.append(hand)
                    break
            
            if player._role == "ContingencyPlanner":
                if player._reuse_ev_card == ev_card:
                    # 危機管理官が確保したものであればゲームから除外
                    player._reuse_ev_card = 0
                    break
    
    def useForecast(self):
        print u"■予測"
        
        str2 = u" 指定可能カード："
        forecast_str = u"山札から引いたカード："
        forecast_list_str = u""
        forecast_list = []
        
        # 感染カード山札から上6枚を表示
        for i in range(6):
            infection_card = self.infectionDeckPop()
            forecast_list.append(infection_card)
            forecast_list_str += u" %02d" % infection_card
        
        print forecast_str + forecast_list_str
        
        while(1):
            selected_card = self.getNumFromKey(u" 山札に戻すカードを指定してください", str2 + forecast_list_str)
            
            if forecast_list.count(selected_card) == 1:
                self._infection_deck.append(selected_card)
                forecast_list.remove(selected_card)
                
                print u" %02d:%s を戻しました" % (selected_card, self._card_info[selected_card])
                
                if len(forecast_list) == 1:
                    self._infection_deck.append(forecast_list[0])
                    self._message = u"■予測により感染の順序が入れ替わりました"
                    break
                
                forecast_list_str = u""
                for forecast_card in forecast_list:
                    forecast_list_str += u" %02d" % forecast_card
            
            else:
                print u" 範囲外の値です"
        
        return 1
    
    def useAirlift(self):
        print u"■空輸"
        
        selected_player = 0
        selected_city = 0
        
        while(1):
            str2 = u" 指定可能プレイヤー：1～%d" % self._player_num
            selected_player = self.getNumFromKey(u" 空輸するプレイヤーを指定してください", str2)
            
            if 1 <= selected_player and selected_player <= self._player_num:
                break
            elif selected_player < 0:
                 self._message = u"■処理はキャンセルされました"
                 return 0
            else:
                print u" 範囲外の値です"
        
        while(1):
            selected_city = self.getNumFromKey(u" プレイヤー%dの移動先を選択してください" % selected_player)
            
            if 1 <= selected_city and selected_city <= 48:
                break
            elif selected_city < 0:
                 self._message = u"■処理はキャンセルされました"
                 return 0
            else:
                print u" 範囲外の値です"
        
        self._player[selected_player - 1]._location = selected_city
        self._message = u"プレイヤー%dは %02d:%s に移動しました" % (selected_player, selected_city, self._card_info[selected_city])
        return 1
    
    def useGovernmentGrant(self):
        print u"■政府の援助"
        
        selected_location = u""
        
        while(1):
            print u" 設置をする都市を指定してください"
            selected_location = raw_input(" > ")
            
            if selected_location.isdigit():
                selected_location = int(selected_location)
                
                if 1 <= selected_location and selected_location <= 48:
                    if self._research_station_flag[selected_location] == 1:
                        print u" その都市には既に設置しています"
                    else:
                        break;
                else:
                    print u" 範囲外の数値です"
            
            elif selected_location == "":
                game_data._message = u"■処理はキャンセルされました"
                return 0
            else:
                print u" 数値を入力してください"
        
        self._research_station_flag[selected_location] = 1
        self._message = u"■%02d:%s に調査基地を建設しました" % (selected_location, self._card_info[selected_location])
        return 1
    
    def useResilientPopulation(self):
        print u"■人口回復"
        
        str2 = u" 指定可能カード："
        for infection_card in self._infection_discard:
            str2 += u" %02d" % infection_card
        
        while(1):
            selected_card = self.getNumFromKey(u" 除外する感染カードを指定してください", str2)
            
            if self._infection_discard.count(selected_card) == 1:
                self._infection_discard.remove(selected_card)
                self._message = u"■%02d:%s をゲームから除外しました" % (selected_card, self._card_info[selected_card])
                break;
            
            else:
                print u" 範囲外の値です"
        
        return 1
    
    def useOneQuietNight(self):
        self._one_quiet_night = 1
        self._message = u"■静かな夜を使用しました"
        return 1
    
    # 成功は0以上の数値を返す、キャンセルはマイナス値
    def getNumFromKey(self, str1, str2 = ""):
        while(1):
            print str1
            
            if str2 != "":
                print str2
            
            num = raw_input(" > ")
            
            if num.isdigit():
                if 0 <= int(num):
                    return int(num)
                
            elif num == "":
                return -1
            else:
                print u" 数値を入力してください"
    
    def checkWin(self):
        win_flag = 1
        
        for cm in self._cure_marker:
            win_flag *= cm
        
        if win_flag != 0:
            return 1
        
        return 0
    
    def checkEradication(self):
        for color_index in range(4):
            if self._cure_marker[color_index] == 1 and self._disease_cube[color_index] == 24:
                self._cure_marker[color_index] = 2
    
    def specialMenu(self):
        while(1):
            os.system("cls")
            print u"マップ"
            print self._map
            print u"------------------------------------------------------------"
            print u"プレイヤー"
            print self._player
            print u"------------------------------------------------------------"
            print u"プレイヤー数"
            print self._player_num
            print u"------------------------------------------------------------"
            print u"ターンカウンタ"
            print self._turn_counter
            print u"------------------------------------------------------------"
            print u"難易度"
            print self._difficulty
            print u"------------------------------------------------------------"
            print u"静かな夜フラグ"
            print self._one_quiet_night
            print u"------------------------------------------------------------"
            print u"調査基地残数"
            print self._research_station_num
            print u"------------------------------------------------------------"
            print u"アウトブレイクマーカー"
            print self._outbreak_marker
            print u"------------------------------------------------------------"
            print u"感染ゲージ"
            print self._infection_gauge
            print u"------------------------------------------------------------"
            print u"感染率マーカー"
            print self._infection_rate_marker
            print u"------------------------------------------------------------"
            print u"調査基地フラグ"
            print self._research_station_flag
            print u"------------------------------------------------------------"
            print u"感染駒残数[青,黄,黒,赤]"
            print self._disease_cube
            print u"------------------------------------------------------------"
            print u"都市汚染状況[青,黒,黄,赤]"
            print self._infection_status
            print u"------------------------------------------------------------"
            print u"治療薬マーカー[青,黄,黒,赤], 0:未完成、1:完成、2:根絶"
            print self._cure_marker
            print u"------------------------------------------------------------"
            print u"感染カード：山札"
            print self._infection_deck
            print u"------------------------------------------------------------"
            print u"感染カード：捨て札"
            print self._infection_discard
            print u"------------------------------------------------------------"
            print u"都市カード：山札"
            print self._player_deck
            print u"------------------------------------------------------------"
            print u"都市カード：捨て札"
            print self._player_discard
            print u"------------------------------------------------------------"
            #print u"隣接都市情報 {地域:[隣接都市番号,...]}"
            #print self._city_connection_info
            #print u"------------------------------------------------------------"
            print u"都市名"
            str = u""
            for i in range(1,48):
                str += u" %02d:%s" % (i, self._card_info[i])
            print str
            print u"------------------------------------------------------------"
            print u"病原体名"
            str = u""
            for i in range(4):
                str += u" %d:%s" % (i, self._disease_name[i])
            print str
            print u"------------------------------------------------------------"
            print u"メッセージ"
            print self._message
            print u"------------------------------------------------------------"
        
            com = raw_input(" > ")
            
            if com == "":
                break
            
            self.executeDebugCommand(com)
        
        self.printMap()
    
    def executeDebugCommand(self, com):
        args = com.split(" ")
        
        if args[0] == "pdiscard":
            self.debugPlayerDiscardChange(args)
        elif args[0] == "pdeck":
            self.debugPlayerDeckChange(args)
        if args[0] == "idiscard":
            self.debugInfectionDiscardChange(args)
        elif args[0] == "ideck":
            self.debugInfectionDeckChange(args)
        elif args[0] == "curemkr":
            self.debugCureMarkerChange(args)
        elif args[0] == "dcube":
            self.debugDiseaseCubeChange(args)
        elif args[0] == "istatus":
            self.debugInfectionStatusChange(args)
    
    # pdiscard <add:追加 remove:削除> <カード番号...>
    def debugPlayerDiscardChange(self, args):
        if len(args) < 2:
            return 0
        
        if args[1] == "add":
            if len(args) > 2:
                for i in range(2, len(args)):
                    if args[i].isdigit():
                        self._player_discard.append(int(args[i]))
        elif args[1] == "remove":
            if len(args) > 2:
                for i in range(2, len(args)):
                    if args[i].isdigit():
                        if self._player_discard.count(int(args[i])) != 0:
                            self._player_discard.remove(int(args[i]))
         
    # pdeck <add:追加 remove:削除> <カード番号...>
    def debugPlayerDeckChange(self, args):
        if len(args) < 2:
            return 0
        
        if args[1] == "add":
            if len(args) > 2:
                for i in range(2, len(args)):
                    if args[i].isdigit():
                        self._player_deck.append(int(args[i]))
        elif args[1] == "remove":
            if len(args) > 2:
                for i in range(2, len(args)):
                    if args[i].isdigit():
                        if self._player_deck.count(int(args[i])) != 0:
                            self._player_deck.remove(int(args[i]))
    
    # idiscard <add:追加 remove:削除> <カード番号...>
    def debugInfectionDiscardChange(self, args):
        pass
    
    # ideck <add:追加 remove:削除> <カード番号...>
    def debugInfectionDeckChange(self, args):
        pass
    
    # curemkr <治療薬の色> <治療薬の状態 0:未開発 1:開発 2:根絶>
    def debugCureMarkerChange(self, args):
        if len(args) < 2:
            return 0
        
        if args[1].isdigit() and args[2].isdigit():
            cure_marker_color = int(args[1])
            cure_marker_value = int(args[2])
            
            if 0 <= cure_marker_color and cure_marker_color <= 3:
                self._cure_marker[cure_marker_color] = cure_marker_value
    
    # dcube <病原体の色> <病原体コマの残数>
    def debugDiseaseCubeChange(self, args):
        if len(args) < 2:
            return 0
        
        if args[1].isdigit() and args[2].isdigit():
            disease_cube_color = int(args[1])
            disease_cube_num = int(args[2])
            
            if 0 <= disease_cube_color and disease_cube_color <= 3:
                self._disease_cube[disease_cube_color] = disease_cube_num
    
    # istatus <都市番号> <病原体の色> <病原体の個数>
    def debugInfectionStatusChange(self, args):
        if len(args) < 3:
            return 0
        
        if args[1].isdigit() and args[2].isdigit() and args[3].isdigit():
            city_no = int(args[1])
            disease_cube_color = int(args[2])
            disease_cube_num = int(args[3])
            
            if 1 <= city_no and city_no <= 48:
                if 0 <= disease_cube_color and disease_cube_color <= 3:
                    self._infection_status[city_no][disease_cube_color] = disease_cube_num
    
    def printMap(self, player_no = -1, act_time = -1):
        # 衛生兵の治療
        for player in self._player:
            if player._role == "Medic":
                for color_index in range(4):
                    if self._cure_marker[color_index] == 1:
                        #治療薬ありの場合
                        self.cureDisease(player._location, 3, color_index)
        
        #手札とプレイヤー位置の作成
        hand = [u"",u"",u"",u""]
        location = []
        player_name = []
        
        for i in range(self._player_num):
            hand_counter = 0
            
            for card in self._player[i]._hand:
                hand[i] = hand[i] + u" " + str(card).zfill(2)
                hand_counter += 1
            
            for j in range(9-hand_counter):
                hand[i] = hand[i] + u"   "
            
            location.append(str(self._player[i]._location).zfill(2))
            # 危機管理官の場合は確保したイベントカードを表示
            if self._player[i]._role == "ContingencyPlanner":
                if self._player[i]._reuse_ev_card != 0:
                    player_name.append(self._player[i]._name % str(self._player[i]._reuse_ev_card).zfill(2))
                else:
                    player_name.append(self._player[i]._name % "")
            
            else:
                player_name.append(self._player[i]._name)
        
        for i in range(self._player_num, 4):
            hand[i] = u" xxxxxxxxxxxxxxxxxxxxxxxxxx"
            location.append("xx")
            player_name.append(u"%26s" % "")
        
        #アクション一覧の作成
        action_table = []
        
        if player_no == -1 and act_time == -1:
            # リストの最後のプレイヤーを指定しているが、最大アクション数は変わらないので特に意味なし
            for i in range(self._player[player_no]._max_actions+1):
                action_table.append(u"                           ")
        else:
            action_flags = self._player[player_no].getAvailableAction(self)
            
            for i in range(1,self._player[player_no]._max_actions+1):
                if action_flags[i] == 1:
                    action_table.append(self._player[player_no]._action_table[i])
                else:
                    action_table.append(u"                           ")
        
        #治療マーカーの作成
        cure_marker = []
        
        for cm in self._cure_marker:
            if cm == 0:
                cure_marker.append(u"未開発    ")
            elif cm == 1:
                cure_marker.append(u"開発      ")
            elif cm == 2:
                cure_marker.append(u"根絶      ")
        
        #病原体コマ情報の作成
        disease_cube = [u""]
        
        for i in range(1,49):
            infection_status = []
            
            for status in self._infection_status[i]:
                if status == 0:
                    infection_status.append(u" ")
                else:
                    infection_status.append(str(status))
            
            parser = u" "
            disease_cube.append(infection_status[0] + parser + infection_status[1] + parser + infection_status[2] + parser + infection_status[3])
        
        #調査基地情報の作成
        research_station = [""]
        
        for i in range(1,49):
            if self._research_station_flag[i] == 1:
                research_station.append(u"+")
            else:
                research_station.append(u" ")
            
        os.system("cls")
        print u"  |------------------------------------------------------------------------------------------------------------------|-------------------------------------|"
        print u"  |                                                       マップ                                                     |              プレイヤー             |"
        print u"  |------------------------------------------------------------------------------------------------------------------|-------------------------------------|"
        print u"  |                                                                                                                  | 1 | %s | %s |" % (location[0], player_name[0])
        print u"  |                                                            ／09                                                  |   |    |%s |" %  hand[0]
        print u"  |                                                  ／--08--／   |＼                            37-----＼           |---|---------------------------------|"
        print u"  |                                            07--／   / ＼      |  25＼                         ＼     38--＼      | 2 | %s | %s |" % (location[1], player_name[1])
        print u"  |                                          ／|＼     /   |      |  /   ＼                        |    ／     39    |   |    |%s |" %  hand[1]
        print u"  |                                        ／  |  ＼  /    |      | /      26-------27            40--／     ／  ＼  |---|---------------------------------|" 
        print u"  |          02-----03----04--------------<    |    10----11------28        ＼     / |＼           |      41       ＼| 3 | %s | %s |" % (location[2], player_name[2])
        print u"  |＼      ／ |＼ ／ ＼  ／                ＼  |   ／＼         ／/ ＼        ＼ ／  |  ＼        /＼  ／            |   |    |%s |" % hand[2]
        print u"  |  ＼  ／   |  05-----06                   ＼| ／   |       ／ /    31-------32   /＼   33-----42--43              |---|---------------------------------|" 
        print u"  |    01     |    ＼   /                      12-----29-----<  /   ／ ＼      / ＼34 |  / ＼    /＼  ＼             | 4 | %s | %s |" % (location[3], player_name[3])
        print u"  |  ／  ＼ ／ ＼    ＼/                      /               30---<     ＼   /     ＼| /    ＼ /  |＼  |            |   |    |%s |" % hand[3]
        print u"  |／      13    |    |                      /                 ＼   ＼-----35/        36------44---45 ＼|            |-------------------------------------|"
        print u"  |        |＼  /    14                     /                   |                      ＼      |   / ＼ |          ／| プレイヤーカード枚数 : %2d/%d        |" % (len(self._player_deck) - 1, 53 + (self._difficulty + 3))
        print u"  |      ／   15---／ |                    /         21--------22                        ＼    |  /    46--------／  | 感染カード枚数       : %2d/48        |" % len(self._infection_deck)
        print u"  |      |    | ＼    |                   /        ／  ＼      /|                          ＼  | |      ＼           | 感染率               : %s          |" % (str(self._infection_rate_marker) + u"-" + str(self._infection_gauge[self._infection_rate_marker]))
        print u"  |    ／     |   ＼  |                  /       ／     |     / |                            ＼| /        ＼         | アウトブレイク       : %d回          |" % self._outbreak_marker
        print u"  |  ／       |     ＼16                /      ／       ＼   /  |                              47          |         | 治療マーカー(青)     : %s   |" % cure_marker[0]
        print u"  |／         ＼      | ＼             /     ／            23   |                                ＼        |         | 治療マーカー(黄)     : %s   |" % cure_marker[1]
        print u"  |             ＼    |   ＼          /    ／              |    |                                  ＼      |       ／| 治療マーカー(黒)     : %s   |" % cure_marker[2]
        print u"  |               ＼  /＼   ＼       /   ／                |    |                                    ＼    |     ／  | 治療マーカー(赤)     : %s   |" % cure_marker[3]
        print u"  |                 17   ＼  |      /  ／                  |    |                                      ＼  |   ／    | 調査基地残数         : %d/6          |" % self._research_station_num
        print u"  |                  |    |  ＼    / ／                     ＼  |                                        ＼| ／      |                                     |"
        print u"  |                  |    |    ＼ |／                         ＼|                                          48        |-------------------------------------|"
        print u"  |                  |    ＼     18                             24                                                   |           イベントカード            |"
        print u"  |                  |      |    /                                                                                   |-------------------------------------|"
        print u"  |                  |      ＼  /                                                                                    | 49:予測                             |"
        print u"  |                 19        20                                                                                     | 50:空輸                             |"
        print u"  |                                                                                                                  | 51:政府の援助                       |"
        print u"  |------------------------------------------------------------------------------------------------------------------| 52:人口回復                         |"
        print u"  | 炭疽菌(青)            青黄黒赤 | 腸チフス(黄)       青黄黒赤 | エボラ出血熱(黒) 青黄黒赤 | 天然痘(赤)   青黄黒赤 | 53:静かな夜                         |"
        print u"  |--------------------------------|-----------------------------|---------------------------|-----------------------|-------------------------------------|"
        
        if player_no == -1 and act_time == -1:
            print u"  |01%sサンフランシスコ     %s | 13%sロサンゼルス     %s | 25%sモスクワ       %s | 37%s北京       %s |          アクション                 |" % (research_station[1],disease_cube[1],research_station[13],disease_cube[13],research_station[25],disease_cube[25],research_station[37],disease_cube[37])
        else:
            print u"  |01%sサンフランシスコ     %s | 13%sロサンゼルス     %s | 25%sモスクワ       %s | 37%s北京       %s |          アクション:%d - %d/4         |" % (research_station[1],disease_cube[1],research_station[13],disease_cube[13],research_station[25],disease_cube[25],research_station[37],disease_cube[37], player_no + 1, act_time + 1)
        
        print u"  |02%sシカゴ               %s | 14%sマイアミ         %s | 26%sテヘラン       %s | 38%sソウル     %s |-------------------------------------|" % (research_station[2],disease_cube[2],research_station[14],disease_cube[14],research_station[26],disease_cube[26],research_station[38],disease_cube[38])
        print u"  |03%sトロント             %s | 15%sメキシコシティ   %s | 27%sデリー         %s | 39%s東京       %s | 1:%s       |" % (research_station[3],disease_cube[3],research_station[15],disease_cube[15],research_station[27],disease_cube[27],research_station[39],disease_cube[39], action_table[0])
        print u"  |04%sニューヨーク         %s | 16%sボゴダ           %s | 28%sイスタンブール %s | 40%s上海       %s | 2:%s       |" % (research_station[4],disease_cube[4],research_station[16],disease_cube[16],research_station[28],disease_cube[28],research_station[40],disease_cube[40], action_table[1])
        print u"  |05%sアトランタ           %s | 17%sリマ             %s | 29%sアルジェ       %s | 41%s大阪       %s | 3:%s       |" % (research_station[5],disease_cube[5],research_station[17],disease_cube[17],research_station[29],disease_cube[29],research_station[41],disease_cube[41], action_table[2])
        print u"  |06%sワシントン           %s | 18%sサンパウロ       %s | 30%sカイロ         %s | 42%s香港       %s | 4:%s       |" % (research_station[6],disease_cube[6],research_station[18],disease_cube[18],research_station[30],disease_cube[30],research_station[42],disease_cube[42], action_table[3])
        print u"  |07%sロンドン             %s | 19%sサンチアゴ       %s | 31%sバグダッド     %s | 43%s台北       %s | 5:%s       |" % (research_station[7],disease_cube[7],research_station[19],disease_cube[19],research_station[31],disease_cube[31],research_station[43],disease_cube[43], action_table[4])
        print u"  |08%sエッセン             %s | 20%sブエノスアイレス %s | 32%sカラチ         %s | 44%sバンコク   %s | 6:%s       |" % (research_station[8],disease_cube[8],research_station[20],disease_cube[20],research_station[32],disease_cube[32],research_station[44],disease_cube[44], action_table[5])
        print u"  |09%sサンクトペテルブルグ %s | 21%sラゴス           %s | 33%sカルカッタ     %s | 45%sホーチミン %s | 7:%s       |" % (research_station[9],disease_cube[9],research_station[21],disease_cube[21],research_station[33],disease_cube[33],research_station[45],disease_cube[45], action_table[6])
        print u"  |10%sパリ                 %s | 22%sハルツーム       %s | 34%sムンバイ       %s | 46%sマニラ     %s | 8:%s       |" % (research_station[10],disease_cube[10],research_station[22],disease_cube[22],research_station[34],disease_cube[34],research_station[46],disease_cube[46], action_table[7])
        print u"  |11%sミラノ               %s | 23%sキンシャサ       %s | 35%sリヤド         %s | 47%sジャカルタ %s | 9:%s       |" % (research_station[11],disease_cube[11],research_station[23],disease_cube[23],research_station[35],disease_cube[35],research_station[47],disease_cube[47], action_table[8])
        print u"  |12%sマドリード           %s | 24%sヨハネスブルク   %s | 36%sチェンナイ     %s | 48%sシドニー   %s |10:%s       |" % (research_station[12],disease_cube[12],research_station[24],disease_cube[24],research_station[36],disease_cube[36],research_station[48],disease_cube[48], action_table[9])
        print u"  |--------------------------------|-----------------------------|---------------------------|-----------------------|11:%s       |" % action_table[10]
        print u"  | 病原体コマ(青)           %2d/24 |病原体コマ(黄)         %2d/24 | 病原体コマ(黒)      %2d/24 |病原体コマ(赤)   %2d/24 |                                     |" % (self._disease_cube[0], self._disease_cube[1], self._disease_cube[2], self._disease_cube[3])
        print u"  |--------------------------------|-----------------------------|---------------------------|-----------------------|-------------------------------------|"
        
        print self._message
        
        self._message = ""
