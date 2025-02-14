# 敌人类
class Enemy:
    def __init__(self, name, defense, level):
        self.name = name
        self.defense = defense
        self.level = level

    def update(self, current_time):
        pass  # 敌人状态更新逻辑