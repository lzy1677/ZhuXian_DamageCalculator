# 玩家类
class Player:
    def __init__(self, level, crit_rate, crit_damage, attack_power, hit_rate):
        self.level = level
        self.crit_rate = crit_rate
        self.crit_damage = crit_damage
        self.attack_power = attack_power
        self.hit_rate = hit_rate
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
    

class LingXi(Player):
    def __init__(self, level, crit_rate, crit_damage, attack_power, hit_rate):
        super().__init__(level, crit_rate, crit_damage, attack_power, hit_rate)
        self.name = "灵灵汐"
        self.lingyin = 0
        self.lingyu = 0
        self.last_lingyin_time = -float('inf')
        self.last_lingyu_time = -float('inf')
        
    def update(self, current_time):
        super().update(current_time)
        if current_time - self.last_lingyin_time >= 1 and self.lingyin <= 3:
            self.lingyin += 1
        if current_time - self.last_lingyu_time >= 1 and self.lingyu <= 4:
            self.lingyu += 1
