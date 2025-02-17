from skill_base import *
from utils import clock
from buff import *
from player import Player, LingXi
from enemy import Enemy


# 游戏循环
class GameLoop:
    def __init__(self, fps, stop_time=600):
        self.fps = fps
        self.clock = clock
        self.frame_duration = 1.0 / fps
        self.stop_time = stop_time

    def run(self, player, enemy):
        while True:
            # 每一帧更新状态
            self.update(player, enemy)
            # 每帧结束时推进游戏时间
            self.clock.tick(self.frame_duration)
            # 定时结束，防止死循环
            if self.clock.get_time() >= self.stop_time:
                break

    def update(self, player, enemy):
        # 更新状态
        player.update(self.clock.get_time())
        enemy.update(self.clock.get_time())

        # # 计算技能伤害
        # for skill in player.skills:
        #     if skill.use(self.clock.get_time()):
        #         damage = player.calculate_damage(skill, enemy, self.clock.get_time())
        #         # 打印日志
        #         print(f"[{self.clock.get_format_time()}] {player.name}使用[{skill.name}]对[{enemy.name}]造成{damage:.1f}点伤害。")
        
        

# 示例使用
if __name__ == "__main__":
    # 初始化游戏循环
    game_loop = GameLoop(fps=60, stop_time=20)

    # 创建玩家和敌人
    enemy = Enemy(name='噩梦木桩', defense=50, level=10)
    player = LingXi(level=10, crit_rate=0.2, crit_damage=1.5, attack_power=100, hit_rate=0.9, enemy=enemy)
    
    # 设置技能循环列表
    player.add_skill_queue('自定义循环', ['激湍', '流水', '灵豚咏', '碎雨'])
    
    # 启动游戏循环
    game_loop.run(player, enemy)
