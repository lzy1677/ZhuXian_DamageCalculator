# older ===================================================================
class Player:
    def __init__(self, level, crit_rate, crit_damage, attack_power, hit_rate, special_resource):
        self.level = level
        self.crit_rate = crit_rate
        self.crit_damage = crit_damage
        self.attack_power = attack_power
        self.hit_rate = hit_rate
        self.special_resource = special_resource
        self.buffs = []

    def add_buff(self, buff):
        self.buffs.append(buff)

    def remove_buff(self, buff):
        self.buffs.remove(buff)

    def calculate_damage(self, skill, enemy):
        base_damage = skill.calculate_base_damage(self, enemy)
        total_damage = base_damage
        for buff in self.buffs:
            total_damage = buff.apply(self, total_damage)
        return total_damage

class Enemy:
    def __init__(self, defense, level):
        self.defense = defense
        self.level = level

class Skill:
    def __init__(self, name, cast_time, cooldown, damage_type):
        self.name = name
        self.cast_time = cast_time
        self.cooldown = cooldown
        self.damage_type = damage_type

    def calculate_base_damage(self, player, enemy):
        raise NotImplementedError("Subclasses should implement this method")

class DirectDamageSkill(Skill):
    def __init__(self, name, cast_time, cooldown, base_damage):
        super().__init__(name, cast_time, cooldown, "direct")
        self.base_damage = base_damage

    def calculate_base_damage(self, player, enemy):
        return self.base_damage * (player.attack_power / enemy.defense)

class DotSkill(Skill):
    def __init__(self, name, cast_time, cooldown, base_damage, duration):
        super().__init__(name, cast_time, cooldown, "dot")
        self.base_damage = base_damage
        self.duration = duration

    def calculate_base_damage(self, player, enemy):
        return self.base_damage * (player.attack_power / enemy.defense) * self.duration

class MixedSkill(Skill):
    def __init__(self, name, cast_time, cooldown, direct_damage, dot_damage, duration):
        super().__init__(name, cast_time, cooldown, "mixed")
        self.direct_damage = direct_damage
        self.dot_damage = dot_damage
        self.duration = duration

    def calculate_base_damage(self, player, enemy):
        direct = self.direct_damage * (player.attack_power / enemy.defense)
        dot = self.dot_damage * (player.attack_power / enemy.defense) * self.duration
        return direct + dot

class Buff:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def apply(self, player, damage):
        raise NotImplementedError("Subclasses should implement this method")

class AttackPowerBuff(Buff):
    def __init__(self, name, duration, attack_power_increase):
        super().__init__(name, duration)
        self.attack_power_increase = attack_power_increase

    def apply(self, player, damage):
        player.attack_power += self.attack_power_increase
        return damage

class CritRateBuff(Buff):
    def __init__(self, name, duration, crit_rate_increase):
        super().__init__(name, duration)
        self.crit_rate_increase = crit_rate_increase

    def apply(self, player, damage):
        player.crit_rate += self.crit_rate_increase
        return damage

class CritDamageBuff(Buff):
    def __init__(self, name, duration, crit_damage_increase):
        super().__init__(name, duration)
        self.crit_damage_increase = crit_damage_increase

    def apply(self, player, damage):
        player.crit_damage += self.crit_damage_increase
        return damage


# latest ========================================================================================
import time

# 游戏时钟
class GameClock:
    def __init__(self):
        self.current_time = 0

    def tick(self, seconds):
        self.current_time += seconds

    def get_time(self):
        return self.current_time

# Buff类
class Buff:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.start_time = None
        self.end_time = None

    def apply(self, player, damage):
        raise NotImplementedError("Subclasses should implement this method")

    def is_active(self, current_time):
        return self.start_time <= current_time < self.end_time

# 具体Buff实现
class AttackPowerBuff(Buff):
    def __init__(self, name, duration, attack_power_increase):
        super().__init__(name, duration)
        self.attack_power_increase = attack_power_increase

    def apply(self, player, damage):
        player.attack_power += self.attack_power_increase
        return damage

# 玩家类
class Player:
    def __init__(self, level, crit_rate, crit_damage, attack_power, hit_rate, special_resource):
        self.level = level
        self.crit_rate = crit_rate
        self.crit_damage = crit_damage
        self.attack_power = attack_power
        self.hit_rate = hit_rate
        self.special_resource = special_resource
        self.buffs = []
        self.skills = []

    def add_buff(self, buff, current_time):
        buff.start_time = current_time
        buff.end_time = current_time + buff.duration
        self.buffs.append(buff)

    def remove_expired_buffs(self, current_time):
        self.buffs = [buff for buff in self.buffs if buff.is_active(current_time)]

    def add_skill(self, skill):
        self.skills.append(skill)

    def update(self, current_time):
        self.remove_expired_buffs(current_time)
        for skill in self.skills:
            skill.update(current_time)

    def calculate_damage(self, skill, enemy, current_time):
        base_damage = skill.calculate_base_damage(self, enemy)
        total_damage = base_damage
        for buff in self.buffs:
            if buff.is_active(current_time):
                total_damage = buff.apply(self, total_damage)
        return total_damage

# 敌人类
class Enemy:
    def __init__(self, defense, level):
        self.defense = defense
        self.level = level

    def update(self, current_time):
        pass  # 敌人状态更新逻辑

# 技能类
class Skill:
    def __init__(self, name, cast_time, cooldown, damage_type):
        self.name = name
        self.cast_time = cast_time
        self.cooldown = cooldown
        self.damage_type = damage_type
        self.last_used_time = -float('inf')

    def calculate_base_damage(self, player, enemy):
        raise NotImplementedError("Subclasses should implement this method")

    def is_ready(self, current_time):
        return current_time - self.last_used_time >= self.cooldown

    def use(self, current_time):
        if self.is_ready(current_time):
            self.last_used_time = current_time
            return True
        return False

    def update(self, current_time):
        pass  # 技能状态更新逻辑

class DirectDamageSkill(Skill):
    def __init__(self, name, cast_time, cooldown, base_damage):
        super().__init__(name, cast_time, cooldown, "direct")
        self.base_damage = base_damage

    def calculate_base_damage(self, player, enemy):
        return self.base_damage * (player.attack_power / enemy.defense)

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
