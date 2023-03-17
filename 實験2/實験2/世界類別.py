import random
import os
from pynput import keyboard
from time import sleep
from 生態環境物品類別 import 生態環境物品類別, 草地類別, 植物類別, 腐化物類別, 腐化物分解者類別
from 生態環境空氣場類別 import *
from pyconio import *


class 地圖類別:
    視窗高度 = 20
    視窗寬度 = 40
    視窗左上角的世界X = 0
    視窗左上角的世界Y = 0
    先前顯示模式 = 1
    顯示模式 = 0  # 顯示模式 = 0 為一般地圖, 顯示模式 = 1 為氣味場地圖

    def __init__(self, 世界):
        self.世界 = 世界
        self.地圖格子 = []
        self.產生空白地圖()
        # 設定非同步按鍵讀取函式
        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        self.listener.start()

    def on_press(self, key):
        try:
            # 要取一次 key 製造 except AttributeError
            p = key.char
            if p == "0":
                地圖類別.顯示模式 = 0
            elif p == "1":
                地圖類別.顯示模式 = 1

        except AttributeError:
            if key == keyboard.Key.left:
                地圖類別.視窗左上角的世界Y -= 1
                if 地圖類別.視窗左上角的世界Y < 0:
                    地圖類別.視窗左上角的世界Y = 0
            elif key == keyboard.Key.right:
                地圖類別.視窗左上角的世界Y += 1
                if 地圖類別.視窗左上角的世界Y > (self.世界.N_WORLD_WIDTH - 地圖類別.視窗寬度):
                    地圖類別.視窗左上角的世界Y = self.世界.N_WORLD_WIDTH - 地圖類別.視窗寬度
            elif key == keyboard.Key.up:
                地圖類別.視窗左上角的世界X -= 1
                if 地圖類別.視窗左上角的世界X < 0:
                    地圖類別.視窗左上角的世界X = 0
            elif key == keyboard.Key.down:
                地圖類別.視窗左上角的世界X += 1
                if 地圖類別.視窗左上角的世界X > (self.世界.N_WORLD_HEIGHT - 地圖類別.視窗高度):
                    地圖類別.視窗左上角的世界X = self.世界.N_WORLD_HEIGHT - 地圖類別.視窗高度
            else:
                pass

    def on_release(self, key):
        pass

    def 產生空白地圖(self):
        for x in range(self.世界.N_WORLD_HEIGHT):
            一排格子 = []
            for y in range(self.世界.N_WORLD_WIDTH):
                一排格子.append(" ")
            self.地圖格子.append(一排格子)

    def 清除地圖(self):
        for x in range(self.世界.N_WORLD_HEIGHT):
            for y in range(self.世界.N_WORLD_WIDTH):
                self.地圖格子[x][y] = " "

    def 設定(self, x, y, 形狀):
        self.地圖格子[x][y] = 形狀

    def 顯示(self):
        顯示地圖字串 = ""
        最小顯示高度 = min(地圖類別.視窗高度, self.世界.N_WORLD_HEIGHT - 地圖類別.視窗左上角的世界X)
        if 地圖類別.顯示模式 == 0:
            if 地圖類別.先前顯示模式 != 地圖類別.顯示模式:
                os.system("cls")
                地圖類別.先前顯示模式 = 地圖類別.顯示模式
            for x in range(最小顯示高度):
                一行字串 = ""
                最小顯示寬度 = min(地圖類別.視窗寬度, self.世界.N_WORLD_WIDTH - 地圖類別.視窗左上角的世界Y)
                for y in range(最小顯示寬度):
                    一行字串 = 一行字串 + self.地圖格子[地圖類別.視窗左上角的世界X + x][地圖類別.視窗左上角的世界Y + y]
                顯示地圖字串 = 顯示地圖字串 + 一行字串 + "\n"
        elif 地圖類別.顯示模式 == 1:
            if 地圖類別.先前顯示模式 != 地圖類別.顯示模式:
                os.system("cls")
                地圖類別.先前顯示模式 = 地圖類別.顯示模式
            for x in range(最小顯示高度):
                一行字串 = ""
                最小顯示寬度 = min(地圖類別.視窗寬度, self.世界.N_WORLD_WIDTH - 地圖類別.視窗左上角的世界Y)
                for y in range(最小顯示寬度):
                    一行字串 = 一行字串 + self.世界.氣味場.取得格子的氣味形狀(
                        地圖類別.視窗左上角的世界X + x, 地圖類別.視窗左上角的世界Y + y
                    )
                顯示地圖字串 = 顯示地圖字串 + 一行字串 + "\n"

        # os.system("cls")
        gotoxy(0, 0)
        print(
            "草地",
            生態環境物品類別.草地形狀,
            "植物",
            生態環境物品類別.植物形狀,
            "腐化物",
            生態環境物品類別.腐化物形狀,
            "腐化物分解者",
            生態環境物品類別.腐化物分解者形狀,
        )
        print("迴圈 = ", self.世界.迴圈數, " " * 10)
        print("草地數量 = ", len(self.世界.草地列表), ", 植物數量 = ", len(self.世界.植物列表), " " * 10)
        print(
            "植物覆蓋率 = ",
            round(self.世界.植物涵蓋率, 2),
            " %",
            ", 草地涵蓋率 = ",
            round(self.世界.草地涵蓋率, 2),
            " %",
            "腐化物覆蓋率 = ",
            round(self.世界.腐化物涵蓋率, 2),
            " %",
            " " * 10,
        )
        print("腐化物分解者進行分解數 = ", self.世界.腐化物分解者進行分解數, " " * 10)
        腐化物分解者死亡時平均生命回合數 = "?"
        if self.世界.腐化物分解者死亡數 != 0:
            腐化物分解者死亡時平均生命回合數 = self.世界.腐化物分解者死亡時總生命回合數 / self.世界.腐化物分解者死亡數
        print("腐化物分解者死亡時平均生命回合數 = ", 腐化物分解者死亡時平均生命回合數, " " * 20)
        print(顯示地圖字串)
        print(
            "視窗左上角的世界 ( X , Y ) = (", 地圖類別.視窗左上角的世界X, ",", 地圖類別.視窗左上角的世界Y, ")", " " * 10
        )
        print("按鍵 0 - 顯示一般地圖, 按鍵 1 - 顯示氣味場")
        sleep(self.世界.SLEEP_TIME)


class 世界類別:
    最大草地生成機率 = 1
    最小草地生成機率 = 0
    草地生成機率 = 最大草地生成機率  # 初始生成機率為 1% , 以植物含蓋率 5% 動態調整此機率
    預設草地涵蓋率 = 20
    預設植物涵蓋率 = 5

    def __init__(self):
        os.system("cls")
        # 定義除錯
        self.DEBUG_MODE = True
        self.SLEEP_TIME = 0.1

        # 定義世界的格子數為 N_WORLD_HEIGHT(x) * N_WORLD_WIDTH(y)
        self.N_WORLD_WIDTH = 100
        self.N_WORLD_HEIGHT = 100
        self.腐化物分解者進行分解數 = 0
        self.產生空世界()
        self.地圖 = 地圖類別(self)
        self.氣味場 = 氣味場類別(self, self.N_WORLD_WIDTH, self.N_WORLD_HEIGHT)
        self.草地列表 = []
        self.草地涵蓋率 = 0
        self.生成全新草地列表()
        self.植物列表 = []
        self.植物涵蓋率 = 0
        self.腐化物列表 = []
        self.腐化物涵蓋率 = 0
        self.腐化物分解者列表 = []  # 保持個數 = N_WORLD_HEIGHT
        self.迴圈數 = 0
        self.腐化物分解者死亡數 = 0
        self.腐化物分解者死亡時總生命回合數 = 0
        self.氣味場 = 氣味場類別(self, self.N_WORLD_WIDTH, self.N_WORLD_HEIGHT)

    def 產生空世界(self):
        self.地面格子 = []
        self.地上格子 = []
        for x in range(self.N_WORLD_HEIGHT):
            一排地面格子 = []
            一排地上格子 = []
            for y in range(self.N_WORLD_WIDTH):
                一排地面格子.append(-1)
                一排地上格子.append(-1)
            self.地面格子.append(一排地面格子)
            self.地上格子.append(一排地上格子)

    def 在地面格子生成草地(self, x, y):
        亂數 = random.randint(1, 100)
        if 亂數 <= 世界類別.草地生成機率:
            新的草地 = 草地類別(self)
            self.地面格子[x][y] = 新的草地
            新的草地.設定位置(x, y)
            self.草地列表.append(新的草地)

    def 生成全新草地列表(self):
        for x in range(self.N_WORLD_HEIGHT):
            for y in range(self.N_WORLD_WIDTH):
                self.在地面格子生成草地(x, y)

    def 更新地圖顯示(self):
        self.地圖.清除地圖()
        for 草地 in self.草地列表:
            x, y = 草地.位置()
            self.地圖.設定(x, y, 草地.形狀)
        for 植物 in self.植物列表:
            x, y = 植物.位置()
            self.地圖.設定(x, y, 植物.形狀)
        for 腐化物 in self.腐化物列表:
            x, y = 腐化物.位置()
            self.地圖.設定(x, y, 腐化物.形狀)
        for 腐化物分解者 in self.腐化物分解者列表:
            x, y = 腐化物分解者.位置()
            self.地圖.設定(x, y, 腐化物分解者.形狀)
        self.地圖.顯示()

    def 空地生成草地(self):
        for x in range(self.N_WORLD_HEIGHT):
            for y in range(self.N_WORLD_WIDTH):
                if self.地面格子[x][y] == -1:  # 是否為空地
                    self.在地面格子生成草地(x, y)

    def 草地生成植物(self):
        刪除草地列表 = []
        for 草地 in self.草地列表:
            生成植物 = 草地.生成植物()  # 下一輪改變, 草地生成植物?
            if 生成植物:
                刪除草地列表.append(草地)
                新植物 = 植物類別(self)
                x, y = 草地.位置()
                新植物.設定位置(x, y)
                self.地面格子[x][y] = 新植物
                self.植物列表.append(新植物)
        for 草地 in 刪除草地列表:
            self.草地列表.remove(草地)

    def 更新涵蓋率(self):
        self.植物涵蓋率 = len(self.植物列表) / self.N_WORLD_HEIGHT / self.N_WORLD_WIDTH * 100
        self.草地涵蓋率 = len(self.草地列表) / self.N_WORLD_HEIGHT / self.N_WORLD_WIDTH * 100
        self.腐化物涵蓋率 = len(self.腐化物列表) / self.N_WORLD_HEIGHT / self.N_WORLD_WIDTH * 100
        if self.植物涵蓋率 >= 世界類別.預設植物涵蓋率:
            草地類別.生成植物機率 -= 1
            if 草地類別.生成植物機率 < 草地類別.最小植物生成機率:
                草地類別.生成植物機率 = 草地類別.最小植物生成機率
        else:
            草地類別.生成植物機率 += 1
            if 草地類別.生成植物機率 > 草地類別.最大植物生成機率:
                草地類別.生成植物機率 = 草地類別.最大植物生成機率

        if self.草地涵蓋率 >= 世界類別.預設草地涵蓋率:
            世界類別.草地生成機率 -= 1
            if 世界類別.草地生成機率 < 世界類別.最小草地生成機率:
                世界類別.草地生成機率 = 世界類別.最小草地生成機率
        else:
            世界類別.草地生成機率 += 1
            if 世界類別.草地生成機率 > 世界類別.最大草地生成機率:
                世界類別.草地生成機率 = 世界類別.最大草地生成機率

    def 處理植物死亡(self):
        刪除植物列表 = []
        for 植物 in self.植物列表:
            植物.目前生命 += 1  # 更新植物目前生命
            if 植物.目前生命 > 植物類別.最大生命期:
                刪除植物列表.append(植物)
                x, y = 植物.位置()
                腐化物 = 腐化物類別(self)
                腐化物.設定位置(x, y)
                self.地面格子[x][y] = 腐化物
                self.腐化物列表.append(腐化物)
        for 植物 in 刪除植物列表:
            self.植物列表.remove(植物)

    def 處理腐化物死亡(self):
        刪除腐化物列表 = []
        for 腐化物 in self.腐化物列表:
            腐化物.目前生命 += 1  # 更新腐化物目前生命
            if 腐化物.目前生命 > 腐化物類別.最大生命期:
                刪除腐化物列表.append(腐化物)
                x, y = 腐化物.位置()
                self.地面格子[x][y] = -1
        for 腐化物 in 刪除腐化物列表:
            self.腐化物列表.remove(腐化物)

    def 隨機生成腐化物分解者(self):
        不超過100迴圈計數 = 0
        # 若一直沒有空間生成 N_WORLD_WIDTH 個腐化物分解者, 迴圈將不停止
        while len(self.腐化物分解者列表) < self.N_WORLD_WIDTH:
            腐化物分解者 = 腐化物分解者類別(self)
            x, y = 腐化物分解者.位置()
            if self.地面格子[x][y] == -1:
                self.地上格子[x][y] = 腐化物分解者
                self.腐化物分解者列表.append(腐化物分解者)
            不超過100迴圈計數 += 1
            if 不超過100迴圈計數 > 100:
                break

    def 腐化物分解者移動(self):
        for 腐化物分解者 in self.腐化物分解者列表:
            腐化物分解者.移動()

    def 產生草地氣味場(self):
        for 草地 in self.草地列表:
            x, y = 草地.位置()
            self.氣味場.產生氣味(x, y, 氣味類別.草地, 氣味類別.草地預設濃度)

    def 產生植物氣味場(self):
        for 植物 in self.植物列表:
            x, y = 植物.位置()
            self.氣味場.產生氣味(x, y, 氣味類別.植物, 氣味類別.植物預設濃度)

    def 產生腐化物氣味場(self):
        for 腐化物 in self.腐化物列表:
            x, y = 腐化物.位置()
            self.氣味場.產生氣味(x, y, 氣味類別.腐化物, 氣味類別.腐化物預設濃度)

    def 產生氣味場(self):
        self.產生草地氣味場()
        self.產生植物氣味場()
        self.產生腐化物氣味場()

    def 更新世界(self):
        self.更新涵蓋率()
        self.更新地圖顯示()
        # 下一輪改變
        if self.迴圈數>20:
            self.隨機生成腐化物分解者()
        self.氣味場.更新氣味傳播()
        self.產生氣味場()
        self.草地生成植物()
        self.空地生成草地()
        self.腐化物分解者移動()
        self.處理植物死亡()
        self.處理腐化物死亡()
