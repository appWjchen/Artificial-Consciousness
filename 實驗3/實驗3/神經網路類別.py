import random
from 可儲存物件類別 import 可儲存物件類別


class 嗅覺感測器類別(可儲存物件類別):
    def __init__(self):
        pass

    def 設定大小(self, 大小):
        self.大小 = 大小


class 神經元類別(可儲存物件類別):
    # 權重都是 8 位元整數, 0 ~ 255
    def __init__(self, 輸入數量):
        self.輸入數量 = 輸入數量
        self.輸入 = [0 for _ in range(輸入數量)]
        self.權重 = [0 for _ in range(輸入數量)]
        self.輸出 = 0

    def 隨機初始化(self):
        for i in range(self.輸入數量):
            self.權重[i] = random.randint(0, 255)


class 神經網路類別(可儲存物件類別):
    def __init__(self, 層數, 輸入數值個數):
        self.層數 = 層數
        self.輸入數值個數 = 輸入數值個數
        self.輸入層 = [0 for _ in range(輸入數值個數)]
        self.神經元層級 = [[] for _ in range(層數)]
        self.信息傳播中 = False

    def 設定輸入層數值(self, 輸入數值列表):
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
        self.信息傳播中 = True

    def 設定單層神經元數量(self, 層, 神經元數量, 隨機初始化):
        if 層 < 0 or 層 > self.層數 - 1:  # 超過層數範圍, 不予設定
            return
        if 層 == 0:  # 第0層的輸入是神經網路的輸入層(self.輸入層)
            self.神經元層級[層] = [神經元類別(self.輸入數值個數) for _ in range(神經元數量)]
        else:
            if self.神經元層級[層 - 1] == []:  # 前一層是空列表(未設定), 則神經元的輸入數量未知, 先設為 0
                self.神經元層級[層] = [神經元類別(0) for _ in range(神經元數量)]
            else:  # 前一層不是空列表(已設定), 則此層的輸入數量為前一層神經元數目
                self.神經元層級[層] = [神經元類別(len(self.神經元層級[層 - 1])) for _ in range(神經元數量)]
        if 隨機初始化:
            for 神經元 in self.神經元層級[層]:
                神經元.隨機初始化()