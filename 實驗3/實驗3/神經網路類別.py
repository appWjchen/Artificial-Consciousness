import random
from 可儲存物件類別 import 可儲存物件類別
from pyconio import *
import math


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


class 嗅覺感測器類別(可儲存物件類別):
    def __init__(self):
        pass

    def 設定大小(self, 大小):
        self.大小 = 大小


class 神經元類別(可儲存物件類別):
    # 權重都是 8 位元整數, 0 ~ 255
    def __init__(self, 輸入數量):
        self.輸入數量 = 輸入數量
        # self.輸入 = [0 for _ in range(輸入數量)]    # 用不到, 每一層的輸入是前級的輸出
        self.權重編碼 = [0 for _ in range(輸入數量)]
        self.權重 = [0 for _ in range(輸入數量)]
        self.輸出 = 0

    def 隨機初始化(self):
        for i in range(self.輸入數量):
            self.權重編碼[i] = random.randint(0, 255)
            self.權重[i] = self.權重編碼[i] - 128


class 神經網路類別(可儲存物件類別):
    def __init__(self, 層數, 輸入數值個數):
        self.層數 = 層數
        self.輸入數值個數 = 輸入數值個數
        self.輸入層 = [0 for _ in range(輸入數值個數)]
        self.神經元群組 = [[] for _ in range(層數)]
        self.信息傳播中 = False
        self.信息位置 = 0
        self.輸出確定 = False

    def 設定輸入層數值(self, 輸入數值列表):
        # 輸入層只負責由感測器將信息讀入並儲存, 只是一個緩衝, 不是神經元
        if self.信息傳播中:  # 已設定輸入信息, 要等神經網路把信息傳達到輸出才結束
            return
        拷貝長度 = 0
        if len(輸入數值列表) >= len(self.輸入層):
            拷貝長度 = len(self.輸入層)
        else:
            self.輸入層 = [0 for _ in range(self.輸入數值個數)]
            拷貝長度 = len(輸入數值列表)
        for i in range(拷貝長度):
            self.輸入層[i] = 輸入數值列表[i]
        self.信息位置 = 0
        self.信息傳播中 = True

    def 設定單層神經元數量(self, 層, 神經元數量, 隨機初始化):
        if 層 < 0 or 層 > self.層數 - 1:  # 超過層數範圍, 不予設定
            return
        if 層 == 0:  # 第0層的輸入是神經網路的輸入層(self.輸入層)
            self.神經元群組[層] = [神經元類別(self.輸入數值個數) for _ in range(神經元數量)]
        else:
            if self.神經元群組[層 - 1] == []:  # 前一層是空列表(未設定), 則神經元的輸入數量未知, 先設為 0
                self.神經元群組[層] = [神經元類別(0) for _ in range(神經元數量)]
            else:  # 前一層不是空列表(已設定), 則此層的輸入數量為前一層神經元數目
                self.神經元群組[層] = [神經元類別(len(self.神經元群組[層 - 1])) for _ in range(神經元數量)]
        if 隨機初始化:
            for 神經元 in self.神經元群組[層]:
                神經元.隨機初始化()

    def 檢查神經網路(self):
        checkok = True
        for i in range(len(self.神經元群組)):
            神經元群組 = self.神經元群組[i]
            if len(神經元群組) == 0:  # 若有任一層神經網路群組中的神經元數量是 0 , 腐化物分解者將不能移動
                return False  # 代表神經網路建構有誤
            else:
                for j in range(len(神經元群組)):
                    神經元 = 神經元群組[j]  # 某神經元輸入數量是 0 ,代表沒有任何連結, 有誤
                    if 神經元.輸入數量 == 0:
                        return False
        return checkok

    def 在神經網路中傳播信息(self):
        # 每次信息傳播計算一層群組數據(根據 self.信息位置)
        for 神經元 in self.神經元群組[self.信息位置]:
            神經元.輸出 = 0
            for i in range(神經元.輸入數量):
                if self.信息位置 == 0:  # 第 0 層
                    神經元.輸出 += self.輸入層[i] * 神經元.權重[i]
                else:
                    神經元.輸出 += self.神經元群組[self.信息位置 - 1][i].輸出 * 神經元.權重[i]
                神經元.輸出 = sigmoid(神經元.輸出)

        self.信息位置 += 1
        if self.信息位置 == self.層數:
            if True:
                gotoxy(60, 10)
                if self.神經元群組[self.信息位置 - 1][0].輸出 > 0.5:
                    print("前進", " " * 10)
                else:
                    print("停止", " " * 10)
                gotoxy(60, 11)
                if (
                    self.神經元群組[self.信息位置 - 1][1].輸出 <= 0.5
                    and self.神經元群組[self.信息位置 - 1][2].輸出 <= 0.5
                ):
                    print("上", " " * 10)
                elif (
                    self.神經元群組[self.信息位置 - 1][1].輸出 <= 0.5
                    and self.神經元群組[self.信息位置 - 1][2].輸出 > 0.5
                ):
                    print("右", " " * 10)
                elif (
                    self.神經元群組[self.信息位置 - 1][1].輸出 > 0.5
                    and self.神經元群組[self.信息位置 - 1][2].輸出 <= 0.5
                ):
                    print("下", " " * 10)
                elif (
                    self.神經元群組[self.信息位置 - 1][1].輸出 > 0.5
                    and self.神經元群組[self.信息位置 - 1][2].輸出 > 0.5
                ):
                    print("左", " " * 10)

            self.信息傳播中 = False
            self.輸出確定 = True