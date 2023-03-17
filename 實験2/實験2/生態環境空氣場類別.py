class 氣味類別:
    最大容許濃度 = 3
    草地 = 1
    植物 = 2
    腐化物 = 3
    腐化物分解者 = 4
    草地預設濃度 = 1
    植物預設濃度 = 2
    腐化物預設濃度 = 3
    腐化物分解者預設濃度 = 1

    # 來源: p32 ~ p34
    #       1 - 草地
    #       2 - 植物
    #       3 - 腐化物
    #       4 - 腐化物分解者
    # 方向: 依 p34 (2) 濃度方向擴散的說明來處理下一回合的濃度
    #       0 - 原地無方向, 或稱下一回合將向四面八方擴散
    #       1 - 右下 ↘
    #       2 - 下   ↓
    #       3 - 左下 ↙
    #       4 - 左   ←
    #       5 - 左上 ↖
    #       6 - 上   ↑
    #       7 - 右上 ↗
    #       8 - 右   →
    # 大小:
    #       0 - 濃度 0
    #       1 - 濃度 1
    #       2 - 濃度 2
    #       3 - 濃度 3

    def __init__(self, x, y, 來源, 大小, 方向):
        self.x = x
        self.y = y
        self.來源 = 來源
        self.大小 = 大小
        self.方向 = 方向


class 氣味場類別:
    def __init__(self, 世界, 地圖寬度, 地圖高度):
        self.世界 = 世界
        self.地圖寬度 = 地圖寬度
        self.地圖高度 = 地圖高度
        self.氣味格子 = []
        self.產生空的氣味場()

    def 產生空的氣味場(self):
        for x in range(self.地圖高度):
            一排氣味格子 = []
            for y in range(self.地圖寬度):
                一排氣味格子.append([])
            self.氣味格子.append(一排氣味格子)

    def 產生氣味(self, x, y, 來源, 大小):
        if 大小 > 氣味類別.最大容許濃度:
            大小 = 氣味類別.最大容許濃度
        if 大小 < 0:
            大小 = 0
        氣味 = 氣味類別(x, y, 來源, 大小, 0)
        self.氣味格子[x][y].append(氣味)

    def 取得格子的氣味形狀(self, x, y):
        氣味列表 = self.氣味格子[x][y]
        if 氣味列表 == []:
            return " "
        else:
            大小的最大值 = 0
            氣味來源 = 0
            for 氣味 in 氣味列表:
                if 氣味.大小 > 大小的最大值:
                    氣味來源=氣味.來源
                    大小的最大值 = 氣味.大小
            if 大小的最大值 == 1:
                if 氣味來源==氣味類別.腐化物:
                    return "\033[31m◦\033[0m"
                else:
                    return "◦"
            elif 大小的最大值 == 2:
                if 氣味來源==氣味類別.腐化物:
                    return "\033[31m◌\033[0m"
                else:
                    return "◌"
            elif 大小的最大值 == 3:
                if 氣味來源==氣味類別.腐化物:
                    return "\033[31m◯\033[0m"
                else:
                    return "◯"
        return " "

    def 更新氣味傳播(self):
        新氣味場格子 = [[[] for _ in range(self.地圖高度)] for _ in range(self.地圖寬度)]
        for x in range(self.地圖高度):
            for y in range(self.地圖寬度):
                氣味列表 = self.氣味格子[x][y]
                for 氣味 in 氣味列表:
                    if 氣味.方向 == 0:  # 更新氣味大小
                        氣味.大小 -= 1  # 每過一回合氣味大小減1
                        新氣味場格子[x][y].append(氣味)
        for x in range(self.地圖高度):
            for y in range(self.地圖寬度):
                氣味列表 = 新氣味場格子[x][y]
                for 氣味 in 氣味列表:
                    if 氣味.大小 <= 0:
                        新氣味場格子[x][y].remove(氣味)
        self.氣味格子 = 新氣味場格子
