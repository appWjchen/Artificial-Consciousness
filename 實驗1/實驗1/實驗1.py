import random
from time import sleep
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.panel import Panel

# 定義除錯
DEBUG_WORLD = True

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


class 營養類別(生態環境物品類別):
    生成植物機率 = 10  # 生成植物的機率預設為 10%

    def __init__(self):
        super().__init__()
        self.x = random.randint(0, N_WORLD - 1)  # 隨機生成 (x,y) 位置
        self.y = random.randint(0, N_WORLD - 1)
        self.形狀 = "."


class 地圖類別:
    def __init__(self):
        self.格子 = []
        self.產生空白地圖()
        self.console = Console(width=N_WORLD + 2, height=N_WORLD + 2)

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
                一行字串 = 一行字串 + "[green]"+self.格子[x][y]+"[/]"
            顯示地圖字串 = 顯示地圖字串 + 一行字串 + "\n"

        # 以下程式是用 rich console 顯示出地圖(各個格子的形狀字元)
        with self.console.screen("white on green") as screen:
            self.console.clear()
            text = Align.center(
                Text.from_markup(
                    顯示地圖字串, justify="center"
                ),
                vertical="middle",
            )
            screen.update(Panel(text))
            sleep(0.2)


class 世界類別:
    def __init__(self):
        self.產生空世界()
        self.地圖 = 地圖類別()
        self.營養生成機率 = 25  # 初始生成機率為 25% , 以植物含蓋率 30% 動態調整此機率
        self.營養列表 = []
        self.生成營養列表()

    def 產生空世界(self):
        self.格子 = []
        for x in range(N_WORLD):
            一排格子 = []
            for y in range(N_WORLD):
                一排格子.append(-1)
            self.格子.append(一排格子)

    def 生成營養列表(self):
        for x in range(N_WORLD):
            for y in range(N_WORLD):
                亂數 = random.randint(1, 100)
                if 亂數 <= self.營養生成機率:
                    新的營養 = 營養類別()
                    self.格子[x][y] = 新的營養
                    新的營養.x = x
                    新的營養.y = y
                    self.營養列表.append(新的營養)

    def 更新世界(self):
        self.地圖.清除地圖()
        for 營養 in self.營養列表:
            x, y = 營養.位置()
            self.地圖.設定(x, y, 營養.形狀)
        self.地圖.顯示()


世界 = 世界類別()
while count_world_pass < 1000:
    世界.更新世界()
    count_world_pass += 1