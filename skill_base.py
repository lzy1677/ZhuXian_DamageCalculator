from utils import clock


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

    def update(self, current_time):
        pass  # 技能状态更新逻辑
    
    def use(self, player, current_time):
        if self.is_ready(current_time):
            self.last_used_time = current_time
            base_damage = self.calculate_base_damage(player, enemy)
            total_damage = player.calculate_damage(self, enemy, current_time)
            print(f'使用技能[{self.name}]，造成伤害: {total_damage}')
            # 其他逻辑，如施法动画、音效等
        return False


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