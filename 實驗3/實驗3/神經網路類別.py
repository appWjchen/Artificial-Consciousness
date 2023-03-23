from 可儲存物件類別 import 可儲存物件類別


class 嗅覺感測器類別(可儲存物件類別):
    def __init__(self):
        pass

    def 設定大小(self, 大小):
        self.大小 = 大小


class 神經元類別(可儲存物件類別):
    def __init__(self, 輸入數量):
        self.輸入數量 = 輸入數量
        self.輸入 = [[] for _ in range(輸入數量)]
        self.權重 = [[] for _ in range(輸入數量)]
        self.輸出 = 0
