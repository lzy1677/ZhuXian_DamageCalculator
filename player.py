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