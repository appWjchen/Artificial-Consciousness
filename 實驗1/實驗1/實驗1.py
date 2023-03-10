import random
import os
from time import sleep
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.panel import Panel

# 定義除錯
DEBUG_WORLD = True
SLEEP_TIME = 1

# 定義世界的格子數為 N_WORLD * N_WORLD
N_WORLD = 20
count_world_pass = 0


class 生態環境物品類別:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.形狀 = " "

    def 位置(self):
        return self.x, self.y

    def 設定位置(self, x, y):
        self.x = x
        self.y = y


class 營養類別(生態環境物品類別):
    生成植物機率 = 50  # 生成植物的機率預設為 10%

    def __init__(self):
        super().__init__()
        self.x = random.randint(0, N_WORLD - 1)  # 隨機生成 (x,y) 位置
        self.y = random.randint(0, N_WORLD - 1)
        self.形狀 = "."

    def 生成植物(self):
        亂數 = random.randint(1, 100)
        if 亂數 <= 營養類別.生成植物機率:
            return True
        else:
            return False


class 植物類別(生態環境物品類別):
    最大生命期 = 20  # 植物的存活時間, 幾個輪迴

    def __init__(self):
        super().__init__()
        self.目前生命 = 0
        self.形狀 = "$"


class 地圖類別:
    count_map = 0

    def __init__(self):
        self.格子 = []
        self.產生空白地圖()
        self.console = Console(width=N_WORLD + 4, height=N_WORLD + 2)

    def 產生空白地圖(self):
        for x in range(N_WORLD):
            一排格子 = []
            for y in range(N_WORLD):
                一排格子.append(" ")
            self.格子.append(一排格子)

    def 清除地圖(self):
        for x in range(N_WORLD):
            for y in range(N_WORLD):
                self.格子[x][y] = " "

    def 設定(self, x, y, 形狀):
        self.格子[x][y] = 形狀

    def 顯示(self):
        顯示地圖字串 = ""
        for x in range(N_WORLD):
            一行字串 = ""
            for y in range(N_WORLD):
                一行字串 = 一行字串 + self.格子[x][y]
            顯示地圖字串 = 顯示地圖字串 + 一行字串 + "\n"

        os.system("cls")
        print("迴圈 = ", count_world_pass)
        print("營養數量 = ", len(世界.營養列表))
        print("植物數量 = ", len(世界.植物列表))
        print("植物覆蓋率 = ", round(世界.植物涵蓋率, 2), " %")
        print("營養生成機率 = ", 世界.營養生成機率, " %")
        print(顯示地圖字串)
        sleep(SLEEP_TIME)
        """
        # 以下程式是用 rich console 顯示出地圖(各個格子的形狀字元)
        with self.console.screen() as screen:
            self.console.clear()
            self.console.print("迴圈 = ", 地圖類別.count_map)
            self.console.print("營養數量 = ", len(世界.營養列表))
            self.console.print("植物數量 = ", len(世界.植物列表))
            self.console.print("植物覆蓋率 = ", round(世界.植物涵蓋率, 2), " %")
            self.console.print("營養生成機率 = ", 世界.營養生成機率, " %")
            text = Align.center(
                Text.from_markup(顯示地圖字串, justify="center"),
                vertical="middle",
            )
            screen.update(Panel(text))
            地圖類別.count_map += 1
            sleep(SLEEP_TIME)
         """


class 世界類別:
    最大營養生成機率 = 2
    最小營養生成機率 = 0
    預設植物涵蓋率 = 5

    def __init__(self):
        self.產生空世界()
        self.地圖 = 地圖類別()
        self.營養生成機率 = 2  # 初始生成機率為 1% , 以植物含蓋率 5% 動態調整此機率
        self.營養列表 = []
        self.生成全新營養列表()
        self.植物列表 = []
        self.植物涵蓋率 = 0

    def 產生空世界(self):
        self.格子 = []
        for x in range(N_WORLD):
            一排格子 = []
            for y in range(N_WORLD):
                一排格子.append(-1)
            self.格子.append(一排格子)

    def 在格子生成營養(self, x, y):
        亂數 = random.randint(1, 100)
        if 亂數 <= self.營養生成機率:
            新的營養 = 營養類別()
            self.格子[x][y] = 新的營養
            新的營養.設定位置(x, y)
            self.營養列表.append(新的營養)

    def 生成全新營養列表(self):
        for x in range(N_WORLD):
            for y in range(N_WORLD):
                self.在格子生成營養(x, y)
                """
                亂數 = random.randint(1, 100)
                if 亂數 <= self.營養生成機率:
                    新的營養 = 營養類別()
                    self.格子[x][y] = 新的營養
                    新的營養.設定位置(x, y)
                    self.營養列表.append(新的營養)
                    """

    def 更新地圖顯示(self):
        self.地圖.清除地圖()
        for 營養 in self.營養列表:
            x, y = 營養.位置()
            self.地圖.設定(x, y, 營養.形狀)
        for 植物 in self.植物列表:
            x, y = 植物.位置()
            self.地圖.設定(x, y, 植物.形狀)
        self.地圖.顯示()

    def 空地生成營養(self):
        for x in range(N_WORLD):
            for y in range(N_WORLD):
                if self.格子[x][y] == -1:  # 是否為空地
                    self.在格子生成營養(x, y)

    def 營養生成植物(self):
        刪除營養列表 = []
        for 營養 in self.營養列表:
            生成植物 = 營養.生成植物()  # 下一輪改變, 營養生成植物?
            if 生成植物:
                刪除營養列表.append(營養)
                新植物 = 植物類別()
                x, y = 營養.位置()
                新植物.設定位置(x, y)
                self.格子[x][y] = 新植物
                self.植物列表.append(新植物)
        for 營養 in 刪除營養列表:
            self.營養列表.remove(營養)

    def 更新植物涵蓋率(self):
        self.植物涵蓋率 = len(世界.植物列表) / N_WORLD / N_WORLD * 100
        if self.植物涵蓋率 >= 世界類別.預設植物涵蓋率:
            self.營養生成機率 -= 1
            if self.營養生成機率 < 世界類別.最小營養生成機率:
                self.營養生成機率 = 世界類別.最小營養生成機率
        else:
            self.營養生成機率 += 1
            if self.營養生成機率 > 世界類別.最大營養生成機率:
                self.營養生成機率 = 世界類別.最大營養生成機率

    def 處理植物死亡(self):
        刪除植物列表 = []
        for 植物 in self.植物列表:
            植物.目前生命 += 1  # 更新植物目前生命
            if 植物.目前生命 > 植物類別.最大生命期:
                刪除植物列表.append(植物)
                x, y = 植物.位置()
                self.格子[x][y] = -1
        for 植物 in 刪除植物列表:
            self.植物列表.remove(植物)

    def 更新世界(self):
        self.更新地圖顯示()
        # 下一輪改變
        self.營養生成植物()
        self.更新植物涵蓋率()
        self.空地生成營養()
        self.處理植物死亡()


世界 = 世界類別()
while count_world_pass < 10000:
    世界.更新世界()
    count_world_pass += 1