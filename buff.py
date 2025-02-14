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


# 玩家攻击力buff
class AttackPowerBuff(Buff):
    def __init__(self, name, duration, attack_power_increase):
        super().__init__(name, duration)
        self.attack_power_increase = attack_power_increase

    def apply(self, player, damage):
        player.attack_power += self.attack_power_increase
        return damage
    

# 玩家暴击率buff
class CritRateBuff(Buff):
    def __init__(self, name, duration, crit_rate_increase):
        super().__init__(name, duration)
        self.crit_rate_increase = crit_rate_increase

    def apply(self, player, damage):
        player.crit_rate += self.crit_rate_increase
        return damage


# 玩家暴击伤害buff
class CritDamageBuff(Buff):
    def __init__(self, name, duration, crit_damage_increase):
        super().__init__(name, duration)
        self.crit_damage_increase = crit_damage_increase

    def apply(self, player, damage):
        player.crit_damage += self.crit_damage_increase
        return damage