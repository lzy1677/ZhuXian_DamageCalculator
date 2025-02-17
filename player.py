from skill_base import *
from collections import OrderedDict
from enemy import Enemy


# 玩家类
class Player:
    def __init__(self, level, crit_rate, crit_damage, attack_power, hit_rate, enemy):
        self.name = 'Player'
        self.level = level
        self.crit_rate = crit_rate
        self.crit_damage = crit_damage
        self.attack_power = attack_power
        self.hit_rate = hit_rate
        self.buffs = []
        self.skills = []
        self.skill_queues = OrderedDict()
        self.current_queue_name = None
        self.current_skill_index = 0
        self.last_skill_use_time = -float('inf')
        self.current_skill_start_time = -float('inf')
        if isinstance(enemy, Enemy):
            self.enemys = [enemy]
        elif isinstance(enemy, list):
            self.enemys = enemy
        else:
            print('请传入Enemy实例或Enemy列表.当前使用默认敌人')
            self.enemys = [Enemy('Enemy', 1, 1)]

    # 添加buff
    def add_buff(self, buff, current_time):
        buff.start_time = current_time
        buff.end_time = current_time + buff.duration
        self.buffs.append(buff)

    # 移除过期的buff
    def remove_expired_buffs(self, current_time):
        self.buffs = [buff for buff in self.buffs if buff.is_active(current_time)]

    # 初始化技能
    def _add_skill(self, skill):
        self.skills.append(skill)
        print(f'技能[{skill.name}]已添加.')
        
    # 添加自定义技能队列
    def add_skill_queue(self, name, skill_list):
        for skill in skill_list:
            if not skill in [s.name for s in self.skills]:
                print(f'技能[{skill}]不在已知技能中，请使用完整技能名称，或检查技能名称是否正确.')
                return
        if name in self.skill_queues:
            print(f'技能队列[{name}]已存在，请使用其他名称.')
            return
        self.skill_queues[name] = skill_list
        print(f'技能队列[{name}]已添加.')

    # 更新技能状态，移出过期buff
    def update(self, current_time):
        self.remove_expired_buffs(current_time)
        for skill in self.skills:
            skill.update(current_time)
        self._use_skill_queue(current_time)

    def calculate_damage(self, skill, enemy, current_time):
        base_damage = skill.calculate_base_damage(self, enemy)
        total_damage = base_damage * self.attack_power  # 基础伤害乘以攻击力
        if random.random() < self.crit_rate:
            total_damage *= self.crit_damage  # 暴击伤害
        for buff in self.buffs:
            if buff.is_active(current_time):
                total_damage = buff.apply(self, total_damage)
        return total_damage
    
    def _use_skill_queue(self, current_time):
        if self.current_queue_name is None:
            return
        
        skill_queue = self.skill_queues[self.current_queue_name]
        if self.current_skill_index >= len(skill_queue):
            self.current_skill_index = 0  # 重置技能队列
            return
        
        skill_name = skill_queue[self.current_skill_index]
        skill = next((s for s in self.skills if s.name == skill_name), None)
        if skill is None:
            print(f'技能[{skill_name}]未找到.')
            self.current_skill_index += 1
            return
        
        if current_time - self.current_skill_start_time >= self.last_skill_use_time:
            skill.use(current_time, self)  # 调用技能的use函数 # todo 伤害计算
            self.current_skill_start_time = current_time
            self.current_skill_index += 1
            self.last_skill_use_time = skill.cast_time

class LingXi(Player):
    def __init__(self, level, crit_rate, crit_damage, attack_power, hit_rate):
        super().__init__(level, crit_rate, crit_damage, attack_power, hit_rate)
        self.name = "灵灵汐"
        self.lingyin = 0
        self.lingyu = 0
        self.last_lingyin_time = -float('inf')
        self.last_lingyu_time = -float('inf')
        self.lingyin_interval = 1
        self.lingyu_interval = 1
        
        self._init_skills()
        self._init_skill_queue()
        
    def update(self, current_time):
        super().update(current_time)
        if current_time - self.last_lingyin_time >= self.lingyin_interval and self.lingyin <= 3:
            self.lingyin += 1
        if current_time - self.last_lingyu_time >= self.lingyu_interval and self.lingyu <= 4:
            self.lingyu += 1

    # 初始化灵汐技能            
    def _init_skills(self):
        self._add_skill(DirectDamageSkill(name="甘霖", cast_time=1.5, cooldown=5, base_damage=70))
        self._add_skill(DirectDamageSkill(name="激湍", cast_time=1.5, cooldown=10, base_damage=50))
        self._add_skill(DirectDamageSkill(name="流水", cast_time=1.5, cooldown=0.8, base_damage=20))
        self._add_skill(DirectDamageSkill(name="玄水", cast_time=1, cooldown=0.8, base_damage=20))
        self._add_skill(DirectDamageSkill(name="灵爆", cast_time=2, cooldown=0.8, base_damage=20))

    # 初始化内置技能队列，玄水爆发，无玄水爆发等        
    def _init_skill_queue(self):
        self.add_skill_queue("玄水爆发", ["玄水", "灵爆"])
        self.add_skill_queue("无玄水爆发", ["流水", "灵爆"])
        self.current_queue_name = "玄水爆发"  # 设置默认技能队列