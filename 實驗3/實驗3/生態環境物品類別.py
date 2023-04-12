import random
from 可儲存物件類別 import 可儲存物件類別
from 神經網路類別 import 嗅覺感測器類別, 神經網路類別
from 生態環境空氣場類別 import *


class 生態環境物品類別(可儲存物件類別):
    草地形狀 = "."
    植物形狀 = "T"
    腐化物形狀 = "A"
    腐化物分解者形狀 = "m"

    def __init__(self, 世界):
        super().__init__()
        self.x = 0
        self.y = 0
        self.形狀 = " "
        self.世界 = 世界

    def 位置(self):
        return self.x, self.y

    def 設定位置(self, x, y):
        self.x = x
        self.y = y

    def 隨機移動傳回新位置(self):
        new_x = self.x
        new_y = self.y
        行為 = random.randint(1, 5)
        if 行為 == 1:  # 向上
            new_x = new_x - 1
            new_y = new_y
        elif 行為 == 2:  # 向下
            new_x = new_x + 1
            new_y = new_y
        elif 行為 == 3:  # 向右
            new_x = new_x
            new_y = new_y + 1
        elif 行為 == 4:  # 向左
            new_x = new_x
            new_y = new_y - 1
        else:  # 不動
            pass
        # 超過上邊回到最下邊, 超過最下邊回到最上邊
        if new_x < 0:
            new_x = self.世界.N_WORLD_HEIGHT - 1
        elif new_x >= self.世界.N_WORLD_HEIGHT:
            new_x = 0
        # 超過右邊回到最左邊, 超過最左邊回到最右邊
        if new_y < 0:
            new_y = self.世界.N_WORLD_WIDTH - 1
        elif new_y >= self.世界.N_WORLD_WIDTH:
            new_y = 0
        return new_x, new_y


class 草地類別(生態環境物品類別):
    最大植物生成機率 = 2
    最小植物生成機率 = 0
    生成植物機率 = 2  # 生成植物的機率預設為 2%

    def __init__(self, 世界):
        super().__init__(世界)
        # self.x = random.randint(0, N_WORLD_HEIGHT - 1)  # 隨機生成 (x,y) 位置
        # self.y = random.randint(0, N_WORLD_WIDTH - 1)
        self.形狀 = 生態環境物品類別.草地形狀

    def 生成植物(self):
        亂數 = random.randint(1, 100)
        if 亂數 <= 草地類別.生成植物機率:
            return True
        else:
            return False


class 植物類別(生態環境物品類別):
    最大生命期 = 20  # 植物的存活時間, 幾個輪迴

    def __init__(self, 世界):
        super().__init__(世界)
        self.目前生命 = 0
        self.形狀 = 生態環境物品類別.植物形狀


class 腐化物類別(生態環境物品類別):
    最大生命期 = 12  # 腐化物的存活時間, 幾個輪迴

    def __init__(self, 世界):
        super().__init__(世界)
        self.目前生命 = 0
        self.形狀 = 生態環境物品類別.腐化物形狀


class 腐化物分解者類別(生態環境物品類別):
    預設進食刻數 = 20
    預設能量 = 200
    預設進食獲取能量 = 100
    預設停止消秏能量 = 1
    預設移動消秏能量 = 10

    def __init__(self, 世界):
        super().__init__(世界)
        self.x = random.randint(0, self.世界.N_WORLD_HEIGHT - 1)  # 隨機生成 (x,y) 位置, 小心重複位置
        self.y = random.randint(0, self.世界.N_WORLD_WIDTH - 1)
        self.形狀 = 生態環境物品類別.腐化物分解者形狀
        self.進食中 = False
        self.進食刻數 = 0
        self.能量 = 腐化物分解者類別.預設能量
        self.生命刻數 = 0
        self.生命代數 = 0
        self.刻數 = 0
        self.產生嗅覺感測器()
        self.產生神經網路()

    def 產生神經網路(self):

        # 未來生態環境物品可能會分生植物類別及動物類別, 目前先不分

        self.神經網路 = 神經網路類別(3, 8)  # 產生一個有 3 層神經元群組的神經網路, 共有 8 個輸入
        self.神經網路.設定單層神經元數量(0, 8, True)  # 第 0 層神經元群組有 8 個神經元
        self.神經網路.設定單層神經元數量(1, 4, True)  # 第 1 層神經元群組有 4 個神經元
        self.神經網路.設定單層神經元數量(2, 3, True)  # 第 2 層神經元群組有 3 個神經元

        # 第 2 層即輸出層, 決定腐化物分解者下一次的「行為」是什麼。
        # 腐化物分解者的行動只有 2 種,
        #   第一種「行為」是「前進(1)」或「原地不動(0)」,以 1 個位元表示。
        #   第二種「行為」是前進的方向，以 2 個位元表示 4 個方向。
        #       00 上
        #       01 右
        #       10 下
        #       11 左

        self.神經網路建構完成 = self.神經網路.檢查神經網路()

        # 有一種建構錯誤是群組建構順序不對, 要按第 0 層 -> 第 n 層依序建構

    def 產生嗅覺感測器(self):
        # 分解者沒有前後之分, 嗅覺感測器四面八方都有, 共八個
        self.嗅覺感測器上 = 嗅覺感測器類別()
        self.嗅覺感測器右上 = 嗅覺感測器類別()
        self.嗅覺感測器右 = 嗅覺感測器類別()
        self.嗅覺感測器右下 = 嗅覺感測器類別()
        self.嗅覺感測器下 = 嗅覺感測器類別()
        self.嗅覺感測器左下 = 嗅覺感測器類別()
        self.嗅覺感測器左 = 嗅覺感測器類別()
        self.嗅覺感測器左上 = 嗅覺感測器類別()

    def 感測嗅覺信息(self):
        self.嗅覺感測器上.設定大小(self.世界.氣味場.傳回格子氣味(self.x - 1, self.y, 氣味類別.腐化物))
        self.嗅覺感測器右上.設定大小(self.世界.氣味場.傳回格子氣味(self.x - 1, self.y + 1, 氣味類別.腐化物))
        self.嗅覺感測器右.設定大小(self.世界.氣味場.傳回格子氣味(self.x, self.y + 1, 氣味類別.腐化物))
        self.嗅覺感測器右下.設定大小(self.世界.氣味場.傳回格子氣味(self.x + 1, self.y + 1, 氣味類別.腐化物))
        self.嗅覺感測器下.設定大小(self.世界.氣味場.傳回格子氣味(self.x + 1, self.y, 氣味類別.腐化物))
        self.嗅覺感測器左下.設定大小(self.世界.氣味場.傳回格子氣味(self.x + 1, self.y - 1, 氣味類別.腐化物))
        self.嗅覺感測器左.設定大小(self.世界.氣味場.傳回格子氣味(self.x, self.y - 1, 氣味類別.腐化物))
        self.嗅覺感測器左上.設定大小(self.世界.氣味場.傳回格子氣味(self.x - 1, self.y - 1, 氣味類別.腐化物))

    def 處理死亡(self):
        if self.能量 <= 0:  # 能量用完就算死了, 記錄移動總數, 重設能量
            self.世界.腐化物分解者死亡數 += 1
            self.世界.腐化物分解者死亡時總生命刻數 += self.生命刻數
            self.能量 = 腐化物分解者類別.預設能量
            self.生命刻數 = 0
            self.刻數 = 0
            self.生命代數 += 1

    def 移動(self):
        # 分解者移動有一大問題, 若二個微生物移動到同一格子, 先出生的分解者有移動優先權, 目前暫時先如此行, 以後再處理碰撞問題
        if not self.神經網路建構完成:
            return
        self.刻數 += 1
        self.生命刻數 += 1
        # 每刻會呼叫一次移動, 進食改為 20 刻(即2回合)
        global 腐化物分解者進行分解數
        if self.進食中:
            self.進食刻數 -= 1
            new_x, new_y = self.x, self.y  # 進食中不能移動
            if self.進食刻數 == 0:
                self.能量 += 腐化物分解者類別.預設進食獲取能量
                self.能量 -= 腐化物分解者類別.預設停止消秏能量 / 10
                self.進食中 = False
                self.處理死亡()
            return
        # 回合數小於 200 時, 分解者處於隨機移動的狀態, 用以計算出平均生命回合數
        if self.世界.回合數>200:
            if not self.神經網路.信息傳播中:
                if self.神經網路.輸出確定:
                    # 神經網路的輸出結果已經確定, 腐化物分解者根據結果做出行動, 行動須要花費一定時間(刻數)
                    if self.刻數 % 10 == 0:
                        self.神經網路.輸出確定 = False
                else:
                    # 神經網路中的信息傳遞須要時間, 從感測信息到輸出結果的時間和神經網路的層數有關,
                    # 每一刻數, 信息在神經網路中傳遞一層, 信息從進入到出來共須要「層數」的刻數。
                    self.感測嗅覺信息()
                    self.神經網路.設定輸入層數值(
                        [
                            self.嗅覺感測器上.大小,
                            self.嗅覺感測器右上.大小,
                            self.嗅覺感測器右.大小,
                            self.嗅覺感測器右下.大小,
                            self.嗅覺感測器下.大小,
                            self.嗅覺感測器左下.大小,
                            self.嗅覺感測器左.大小,
                            self.嗅覺感測器左上.大小,
                        ]
                    )
            else:
                self.神經網路.在神經網路中傳播信息()
        else:
            if self.刻數 % 10 == 0:
                new_x, new_y = self.隨機移動傳回新位置()
                if new_x == self.x and new_y == self.y:  # 不移動
                    self.能量 -= 腐化物分解者類別.預設停止消秏能量
                    self.處理死亡()
                    return
                # 判斷移動到的地面格子是否為空地或腐化物
                if (
                    self.世界.地面格子[new_x][new_y] == -1
                    or self.世界.地面格子[new_x][new_y].形狀 == 生態環境物品類別.草地形狀
                ):  # 前往的格子是空地 或者 草地, 注意 or 順序不能相反, 因為self.世界.地面格子[new_x][new_y].形狀有可能不存在
                    if self.世界.地上格子[new_x][new_y] == -1:
                        self.世界.地上格子[new_x][new_y] = self
                        self.世界.地上格子[self.x][self.y] = -1
                        self.x = new_x
                        self.y = new_y
                        self.能量 -= 腐化物分解者類別.預設移動消秏能量
                elif (
                    self.世界.地面格子[new_x][new_y].形狀 == 生態環境物品類別.腐化物形狀
                    and self.世界.地上格子[new_x][new_y] == -1
                ):  # 前往的格子是腐化物 且 上面沒有其它生物, 注意 if 和 elif 順序不能交換, 要先確定格子不是空地, 否則會出錯(空地沒有形狀)
                    腐化物 = self.世界.地面格子[new_x][new_y]
                    self.世界.地面格子[new_x][new_y] = -1
                    self.世界.地上格子[new_x][new_y] = self
                    self.世界.地上格子[self.x][self.y] = -1
                    self.世界.腐化物列表.remove(腐化物)
                    self.x = new_x
                    self.y = new_y
                    self.能量 -= 腐化物分解者類別.預設移動消秏能量
                    self.世界.腐化物分解者進行分解數 += 1
                    self.進食刻數 = 腐化物分解者類別.預設進食刻數
                    self.進食中 = True
                else:  # 不能移到要前往的格子, 算不移動
                    self.能量 -= 腐化物分解者類別.預設停止消秏能量
                self.處理死亡()
