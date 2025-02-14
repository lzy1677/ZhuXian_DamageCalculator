from skill import *
from buff import *
from player import Player, LingXi
from enemy import Enemy
import time
from datetime import timedelta


# 游戏时钟
class GameClock:
    def __init__(self):
        self.current_time = 0

    def tick(self, seconds):
        self.current_time += seconds

    def get_time(self):
        return self.current_time
    
    def get_format_time(self):
        minutes = int(self.current_time // 60)
        seconds = int(self.current_time % 60)
        mseconds = int(self.current_time * 1000 % 1000)
        return f"{minutes:02d}分{seconds:02d}秒{mseconds:03d}"


# 游戏循环
class GameLoop:
    def __init__(self, fps, stop_time=600):
        self.fps = fps
        self.clock = GameClock()
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

        # 计算技能伤害
        for skill in player.skills:
            if skill.use(self.clock.get_time()):
                damage = player.calculate_damage(skill, enemy, self.clock.get_time())
                # 打印日志
                print(f"[{self.clock.get_format_time()}] {player.name}使用[{skill.name}]对[{enemy.name}]造成{damage:.1f}点伤害。")

# 示例使用
if __name__ == "__main__":
    # 初始化游戏循环
    game_loop = GameLoop(fps=60, stop_time=20)

    # 创建玩家和敌人
    player = LingXi(level=10, crit_rate=0.2, crit_damage=1.5, attack_power=100, hit_rate=0.9)
    enemy = Enemy(name='噩梦木桩', defense=50, level=10)

    # 创建技能
    fireball = DirectDamageSkill(name="甘霖", cast_time=1.5, cooldown=5, base_damage=70)
    fireball1 = DirectDamageSkill(name="激湍", cast_time=1.5, cooldown=10, base_damage=50)
    fireball2 = DirectDamageSkill(name="流水", cast_time=1.5, cooldown=0.8, base_damage=20)
    player.add_skill(fireball)
    player.add_skill(fireball1)
    player.add_skill(fireball2)

    # 创建Buff
    attack_buff = AttackPowerBuff(name="Attack Boost", duration=3, attack_power_increase=20)
    player.add_buff(attack_buff, game_loop.clock.get_time())

    # 启动游戏循环
    game_loop.run(player, enemy)
