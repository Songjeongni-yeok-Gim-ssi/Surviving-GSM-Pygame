class GameTimeManager:
    """게임 내 시간을 관리하는 클래스"""
    def __init__(self):
        self.reset()
        self.time_speed = 1.0  # 시간 흐름 속도 (1.0 = 실시간, 2.0 = 2배속)
        
    def reset(self):
        """시간을 초기화"""
        self.game_minutes = 0  # 게임 내 총 분
        self.current_hour = 0  # 현재 시간 (0-23)
        self.current_minute = 0  # 현재 분 (0-59)
        
    def update(self, delta_time):
        """시간 업데이트 (delta_time은 초 단위)"""
        # 실제 시간 1초 = 게임 내 1분으로 설정 (조정 가능)
        minutes_to_add = delta_time * self.time_speed
        self.game_minutes += minutes_to_add
        
        # 시간과 분 계산
        total_minutes = int(self.game_minutes)
        self.current_hour = total_minutes // 60
        self.current_minute = total_minutes % 60
        
        # 24시간 주기로 리셋
        if self.current_hour >= 24:
            self.current_hour = 0
            self.game_minutes = self.game_minutes % (24 * 60)
    
    def get_time_string(self):
        """시간을 문자열로 반환"""
        if self.current_hour < 12:
            period = "오전"
            hour_12 = self.current_hour if self.current_hour != 0 else 12
        else:
            period = "오후"
            hour_12 = self.current_hour - 12 if self.current_hour != 12 else 12
            
        return f"시간: {period} {hour_12:02d}:{self.current_minute:02d}"
    
    def set_time_speed(self, speed):
        """시간 흐름 속도 설정"""
        self.time_speed = max(0.1, speed)  # 최소 0.1배속
        
    def get_current_time_info(self):
        """현재 시간 정보를 딕셔너리로 반환"""
        return {
            'hour': self.current_hour,
            'minute': self.current_minute,
            'total_minutes': int(self.game_minutes),
            'is_morning': self.current_hour < 12,
            'time_string': self.get_time_string()
        }