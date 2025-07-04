class GameTimeManager:
    """게임 내 시간을 관리하는 클래스 (3년 * 30주 시스템)"""
    def __init__(self):
        self.reset()
        self.time_speed = 1.0  # 시간 흐름 속도 (1.0 = 12초당 1일)
        self.WEEKS_PER_YEAR = 30  # 30주로 수정
        self.TOTAL_YEARS = 3
        self.SECONDS_PER_DAY = 12  # 1일 = 12초 (실시간)
        self.is_paused = False  # 시간 멈춤 상태
        
    def reset(self):
        """시간을 초기화"""
        self.total_seconds = 0  # 게임 내 총 초
        self.current_year = 1  # 현재 학년 (1-3년)
        self.current_week = 1  # 현재 주차 (1-30주)
        self.current_day = 1   # 현재 요일 (1-5일)
        self.current_hour = 9  # 현재 시간 (기본 오전 9시 시작)
        self.current_minute = 0
        self.graduation_completed = False
        self.is_paused = False  # 시간 멈춤 상태 초기화
        
    def update(self, delta_time):
        """시간 업데이트 (delta_time은 실제 초 단위)"""
        if self.graduation_completed or self.is_paused:  # 시간이 멈춰있으면 업데이트하지 않음
            return
            
        # 1배속 기준: 실제 12초 = 게임 1일
        game_seconds_to_add = (delta_time / self.SECONDS_PER_DAY) * 24 * 60 * 60 * self.time_speed
        self.total_seconds += game_seconds_to_add
        
        # 시간 계산
        self._calculate_time_units()
        
        if self.current_year == 3 and self.current_week == 15:
            self.total_seconds += 16 * 5 * 24 * 60 * 60
        
        # 졸업 체크
        if self.current_year > self.TOTAL_YEARS:
            self.graduation_completed = True
            print("축하합니다! 졸업하셨습니다!")
    
    def _calculate_time_units(self):
        """총 초를 기반으로 년/주/일/시/분 계산"""
        total_minutes = int(self.total_seconds // 60)
        total_hours = total_minutes // 60 + 9
        total_days = total_hours // 24
        total_weeks = total_days // 5  # 5일제로 수정
        
        # 학년 계산
        self.current_year = min((total_weeks // self.WEEKS_PER_YEAR) + 1, self.TOTAL_YEARS + 1)
        
        # 현재 학년의 주차 계산
        weeks_in_current_year = total_weeks % self.WEEKS_PER_YEAR
        self.current_week = weeks_in_current_year + 1
        
        # 현재 주의 요일 계산 (5일제)
        days_in_current_week = total_days % 5
        self.current_day = days_in_current_week + 1
        
        # 현재 시간 계산 (9시부터 시작)
        hours_in_current_day = total_hours % 24
        self.current_hour = (hours_in_current_day) % 24
        self.current_minute = total_minutes % 60
    
    def skip_to_next_year(self):
        """다음 학년으로 스킵"""
        if self.graduation_completed:
            return False
            
        if self.current_year <= self.TOTAL_YEARS:
            # 현재 학년의 남은 주를 모두 건너뛰기
            weeks_to_skip = self.WEEKS_PER_YEAR - (self.current_week - 1)
            seconds_to_add = weeks_to_skip * 5 * 24 * 60 * 60  # 주 -> 초 변환 (5일제)
            self.total_seconds += seconds_to_add
            self._calculate_time_units()
            
            print(f"{self.current_year}학년으로 진급했습니다!")
            return True
        return False
    
    def get_time_string(self):
        """시간을 문자열로 반환"""
        if self.graduation_completed:
            return "졸업 완료!"
            
        # 요일 변환 (5일제)
        day_names = ["", "월", "화", "수", "목", "금"]
        day_name = day_names[min(self.current_day, 5)]
        
        # 오전/오후 변환
        if self.current_hour < 12:
            period = "오전"
            hour_12 = self.current_hour if self.current_hour != 0 else 12
        else:
            period = "오후"
            hour_12 = self.current_hour - 12 if self.current_hour != 12 else 12
            
        return f"{self.current_year}학년 {self.current_week}주차 {day_name}요일 {period} {hour_12:02d}:{self.current_minute:02d}"
    
    def set_time_speed(self, speed):
        """시간 흐름 속도 설정"""
        self.time_speed = max(0.1, speed)
        
    def get_current_time_info(self):
        """현재 시간 정보를 딕셔너리로 반환"""
        return {
            'year': self.current_year,  
            'week': self.current_week,
            'day': self.current_day,
            'hour': self.current_hour,
            'minute': self.current_minute,
            'time_string': self.get_time_string(),
            'is_graduated': self.graduation_completed,
            'grade': self.current_year  # 학년 정보 추가
        }
    
    def pause_time(self):
        """시간을 멈춤"""
        self.is_paused = True
        
    def resume_time(self):
        """시간을 다시 흐르게 함"""
        self.is_paused = False