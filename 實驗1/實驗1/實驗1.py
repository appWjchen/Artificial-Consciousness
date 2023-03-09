import random

# 定義除錯
DEBUG_WORLD = True

# 定義世界的格子數為 N_WORLD * N_WORLD
N_WORLD = 20


class 生態環境物品類別:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.形狀 = " "

    def 位置(self):
        return {"x": self.x, "y": self.y}


class 營養類別(生態環境物品類別):
    生成植物機率 = 10  # 生成植物的機率預設為 10%

    def __init__(self):
        super().__init__()
        self.x = random.randint(0, N_WORLD)  # 隨機生成 (x,y) 位置
        self.y = random.randint(0, N_WORLD)
        self.形狀 = "."


class 地圖類別:
    def __init__(self):
        self.格子 = []
        self.產生空白地圖()

    def 產生空白地圖(self):
        for x in range(N_WORLD):
            一排格子 = []
            for y in range(N_WORLD):
                一排格子.append(" ")
            self.格子.append(一排格子)


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


世界 = 世界類別()
print(世界.地圖.格子)