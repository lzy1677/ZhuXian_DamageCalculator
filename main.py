from skill import *
from buff import *
from player import Player
from enemy import Enemy
import time

# 游戏时钟
class GameClock:
    def __init__(self):
        self.current_time = 0

    def tick(self, seconds):
        self.current_time += seconds

    def get_time(self):
        return self.current_time


# 游戏循环
class GameLoop:
    def __init__(self, fps):
        self.fps = fps
        self.clock = GameClock()
        self.last_tick_time = time.time()
        self.frame_duration = 1.0 / fps

    def run(self, player, enemy):
        while True:
            current_time = time.time()
            if current_time - self.last_tick_time >= self.frame_duration:
                self.update(player, enemy)
                self.last_tick_time = current_time

    def update(self, player, enemy):
        # 每秒结束时推进游戏时间
        if int(self.clock.get_time()) < int(self.clock.get_time() + self.frame_duration):
            self.clock.tick(self.frame_duration)

        # 更新状态
        player.update(self.clock.get_time())
        enemy.update(self.clock.get_time())

        # 计算技能伤害
        for skill in player.skills:
            if skill.use(self.clock.get_time()):
                damage = player.calculate_damage(skill, enemy, self.clock.get_time())
                print(f"{skill.name} used at {self.clock.get_time()}s, damage: {damage}")

# 示例使用
if __name__ == "__main__":
    # 初始化游戏循环
    game_loop = GameLoop(fps=60)

    # 创建玩家和敌人
    player = Player(level=10, crit_rate=0.2, crit_damage=1.5, attack_power=100, hit_rate=0.9, special_resource=5)
    enemy = Enemy(defense=50, level=10)

    # 创建技能
    fireball = DirectDamageSkill(name="Fireball", cast_time=1.5, cooldown=5, base_damage=50)
    player.add_skill(fireball)

    # 创建Buff
    attack_buff = AttackPowerBuff(name="Attack Boost", duration=3, attack_power_increase=20)
    player.add_buff(attack_buff, game_loop.clock.get_time())

    # 启动游戏循环
    game_loop.run(player, enemy)
