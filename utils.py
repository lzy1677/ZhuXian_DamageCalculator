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
clock = GameClock()