import random


class 生態環境物品類別:
    def __init__(self, 世界):
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
        self.形狀 = "."

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
        self.形狀 = "$"


class 腐化植物類別(生態環境物品類別):
    最大生命期 = 10  # 腐化植物的存活時間, 幾個輪迴

    def __init__(self, 世界):
        super().__init__(世界)
        self.目前生命 = 0
        self.形狀 = "@"


class 腐化植物分解者類別(生態環境物品類別):
    def __init__(self, 世界):
        super().__init__(世界)
        self.x = random.randint(0, self.世界.N_WORLD_HEIGHT - 1)  # 隨機生成 (x,y) 位置, 小心重複位置
        self.y = random.randint(0, self.世界.N_WORLD_WIDTH - 1)
        self.形狀 = "M"

    def 移動(self):
        global 腐化植物分解者進行分解數
        new_x, new_y = self.隨機移動傳回新位置()
        # 判斷移動到的地面格子是否為空地或腐化植物
        if self.世界.地面格子[new_x][new_y] == -1 or self.世界.地面格子[new_x][new_y].形狀 == ".":
            if self.世界.地上格子[new_x][new_y] == -1:
                self.世界.地上格子[new_x][new_y] = self
                self.世界.地上格子[self.x][self.y] = -1
                self.x = new_x
                self.y = new_y
        elif self.世界.地面格子[new_x][new_y].形狀 == "@" and self.世界.地上格子[new_x][new_y] == -1:
            腐化植物 = self.世界.地面格子[new_x][new_y]
            self.世界.地面格子[new_x][new_y] = -1
            self.世界.地上格子[new_x][new_y] = self
            self.世界.地上格子[self.x][self.y] = -1
            self.世界.腐化植物列表.remove(腐化植物)
            self.x = new_x
            self.y = new_y
            self.世界.腐化植物分解者進行分解數 += 1
