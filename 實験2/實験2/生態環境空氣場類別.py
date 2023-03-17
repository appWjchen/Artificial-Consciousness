﻿class 氣味類別:
    最大容許濃度 = 3
    草地 = 1
    植物 = 2
    腐化物 = 3
    腐化物分解者 = 4
    草地預設濃度 = 1
    植物預設濃度 = 2
    腐化物預設濃度 = 3
    腐化物分解者預設濃度 = 2
    方向無 = 0
    方向右下 = 1
    方向下 = 2
    方向左下 = 3
    方向左 = 4
    方向左上 = 5
    方向上 = 6
    方向右上 = 7
    方向右 = 9
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
                    氣味來源 = 氣味.來源
                    大小的最大值 = 氣味.大小
            if 大小的最大值 == 1:
                if 氣味來源 == 氣味類別.腐化物:
                    return "\033[31m◦\033[0m"
                elif 氣味來源 == 氣味類別.腐化物分解者:
                    return "\033[32m◦\033[0m"
                else:
                    return "◦"
            elif 大小的最大值 == 2:
                if 氣味來源 == 氣味類別.腐化物:
                    return "\033[31m◌\033[0m"
                elif 氣味來源 == 氣味類別.腐化物分解者:
                    return "\033[32m◌\033[0m"
                else:
                    return "◌"
            elif 大小的最大值 == 3:
                if 氣味來源 == 氣味類別.腐化物:
                    return "\033[31m◯\033[0m"
                elif 氣味來源 == 氣味類別.腐化物分解者:
                    return "\033[32m◯\033[0m"
                else:
                    return "◯"
        return " "

    def 產生傳播氣味(self, x, y, 方向, 大小, 來源):
        new_x = x
        new_y = y
        if x < 0:
            new_x = self.地圖高度 - 1
        elif x > self.地圖高度 - 1:
            new_x = 0
        if y < 0:
            new_y = self.地圖寬度 - 1
        elif y > self.地圖寬度 - 1:
            new_y = 0
        氣味 = 氣味類別(new_x, new_y, 來源, 大小, 方向)
        return 氣味

    def 更新氣味傳播(self):
        新氣味場格子 = [[[] for _ in range(self.地圖寬度)] for _ in range(self.地圖高度)]
        for x in range(self.地圖高度):
            for y in range(self.地圖寬度):
                氣味列表 = self.氣味格子[x][y]
                for 氣味 in 氣味列表:
                    if 氣味.方向 == 氣味類別.方向無:  # 更新氣味大小
                        氣味.大小 -= 1  # 每過一回合氣味大小減1
                        新氣味場格子[x][y].append(氣味)
                        if 氣味.大小 > 0:
                            # 在八個方向形成新的傳播氣味
                            氣味右上 = self.產生傳播氣味(x - 1, y + 1, 氣味類別.方向右上, 氣味.大小, 氣味.來源)
                            新氣味場格子[氣味右上.x][氣味右上.y].append(氣味)
                            氣味右 = self.產生傳播氣味(x, y + 1, 氣味類別.方向右, 氣味.大小, 氣味.來源)
                            新氣味場格子[氣味右.x][氣味右.y].append(氣味)
                            氣味右下 = self.產生傳播氣味(x + 1, y + 1, 氣味類別.方向右下, 氣味.大小, 氣味.來源)
                            新氣味場格子[氣味右下.x][氣味右下.y].append(氣味)
                            氣味下 = self.產生傳播氣味(x + 1, y, 氣味類別.方向下, 氣味.大小, 氣味.來源)
                            新氣味場格子[氣味下.x][氣味下.y].append(氣味)
                            氣味左下 = self.產生傳播氣味(x + 1, y - 1, 氣味類別.方向左下, 氣味.大小, 氣味.來源)
                            新氣味場格子[氣味左下.x][氣味左下.y].append(氣味)
                            氣味左 = self.產生傳播氣味(x, y - 1, 氣味類別.方向左, 氣味.大小, 氣味.來源)
                            新氣味場格子[氣味左.x][氣味左.y].append(氣味)
                            氣味左上 = self.產生傳播氣味(x - 1, y - 1, 氣味類別.方向左上, 氣味.大小, 氣味.來源)
                            新氣味場格子[氣味左上.x][氣味左上.y].append(氣味)
                            氣味上 = self.產生傳播氣味(x - 1, y, 氣味類別.方向上, 氣味.大小, 氣味.來源)
                            新氣味場格子[氣味上.x][氣味上.y].append(氣味)
                    # elif 氣味.方向==1:
                    # 氣味.大小 -= 1  # 每過一回合氣味大小減1
        for x in range(self.地圖高度):
            for y in range(self.地圖寬度):
                氣味列表 = 新氣味場格子[x][y]
                for 氣味 in 氣味列表:
                    if 氣味.大小 <= 0:
                        新氣味場格子[x][y].remove(氣味)
        self.氣味格子 = 新氣味場格子
