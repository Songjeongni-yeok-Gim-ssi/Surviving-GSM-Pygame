import random
from statAndStatPoint import Stat
from events_data import get_events_data

class EventManager:
    def __init__(self):
        self.events = get_events_data()
        
        # 이미 발생한 이벤트를 추적
        self.triggered_events = set()
        
        # 마지막 랜덤 이벤트 발생 날짜 추적
        self.last_random_event_day = 0
        
        # 취업 조건 체크를 위한 임계값
        self.employment_thresholds = {
            'frontend': 80,  # 프론트엔드 스킬 레벨
            'backend': 80,   # 백엔드 스킬 레벨
            'public': 80,    # 공기업 준비 레벨
            'competition': 90  # 기능 대회 레벨
        }
    
    def _apply_effects(self, effects):
        '''
            이벤트에 명시된 스탯 수치 적용
        '''
        print("[스탯 변경] 선택지에 따른 효과를 적용합니다.")
        for stat_name, value in effects.items():
            if hasattr(Stat, stat_name):
                current_value = getattr(Stat, stat_name)
                new_value = current_value + value
                setattr(Stat, stat_name, new_value)
                print(f"[스탯 변경] {stat_name}: {current_value} -> {new_value}")
    
    def get_fixed_event(self, event_name):
        """
        고정 이벤트 가져오기(고정 이벤트 딕셔너리를 반환합니다.)
        """
        event = self.events['fixed_events'].get(event_name)
        if event:
            # 전공별 선택지가 있는 경우
            if isinstance(event['choices'], dict):
                return {
                    'title': event['title'],
                    'text': event['text'],
                    'choices': event['choices'].get(Stat.major, [])
                }
            # 공통 선택지인 경우
            return event
        return None
    
    def get_random_event(self, current_hour):
        """
        랜덤 이벤트 가져오기
        """
        possible_events = []
        for event_name, event in self.events['random_events'].items():
            # repeatable이 True이거나 아직 발생하지 않은 이벤트만 추가
            if event.get('repeatable', False) or event_name not in self.triggered_events:
                # 시간 체크
                time_trigger = event.get('time_trigger', {})
                hour_start = time_trigger.get('hour_start', 0)
                hour_end = time_trigger.get('hour_end', 23)
                
                # 시간이 범위 내에 있는지 체크 (자정을 걸치는 경우 처리)
                if hour_start <= hour_end:
                    if hour_start <= current_hour <= hour_end:
                        possible_events.append((event_name, event))
                else:  # 자정을 걸치는 경우 (예: 22시 ~ 6시)
                    if current_hour >= hour_start or current_hour <= hour_end:
                        possible_events.append((event_name, event))
        
        if possible_events:
            # 확률에 따라 이벤트 선택
            total_probability = sum(event['probability'] for _, event in possible_events)
            if total_probability > 0:
                random_value = random.random() * total_probability
                current_sum = 0
                for event_name, event in possible_events:
                    current_sum += event['probability']
                    if random_value <= current_sum:
                        # 전공별 선택지가 있는 경우
                        if isinstance(event['choices'], dict):
                            return {
                                'title': event['title'],
                                'text': event['text'],
                                'choices': event['choices'].get(Stat.major, event['choices'])
                            }
                        # 공통 선택지인 경우
                        return event
        return None
    
    def check_requirements(self, event, choice=None):
        """
        이벤트와 선택지의 요구사항을 검사하는 메서드(검사 후 불리언 반환)
        """
        
        # 이벤트 요구사항 검사
        if 'requirements' in event:
            requirements = event['requirements']
            
            # 전공 요구사항 검사
            if 'major' in requirements:
                if Stat.major != requirements['major']:
                    return False
            
            # 스탯 요구사항 검사
            for stat_name, required_value in requirements.items():
                if stat_name != 'major' and hasattr(Stat, stat_name):
                    current_value = getattr(Stat, stat_name)
                    if current_value < required_value:
                        return False
        
        # 선택지별 요구사항 검사
        if choice and 'requirements' in choice:
            for stat_name, required_value in choice['requirements'].items():
                if hasattr(Stat, stat_name):
                    current_value = getattr(Stat, stat_name)
                    if current_value < required_value:
                        return False
        
        return True
    
    def check_time_triggered_events(self, time_info):
        """
        시간에 따른 이벤트를 검사 후 트리거된 이벤트들을 반환하는 메서드 -> handle_time_events
        """
        triggered_events = []   
        current_week = time_info['week']
        current_day = time_info['day']
        current_hour = time_info['hour']
        current_grade = time_info.get('grade', 1)
        
        # 고정 이벤트 체크
        for event_name, event in self.events['fixed_events'].items():
            if event_name not in self.triggered_events:
                if 'time_trigger' in event:
                    trigger = event['time_trigger']
                    # 학년 범위 체크
                    grade_range = trigger.get('grade_range', [1, 3])
                    if not (grade_range[0] <= current_grade <= grade_range[1]):
                        continue
                    
                    # 요구사항 체크
                    if not self.check_requirements(event):
                        continue
                    
                    if (trigger['week'] == current_week and 
                        trigger['day'] == current_day and 
                        trigger['hour'] == current_hour):
                        print(f"\n[고정 이벤트 발생] {event['title']} - {current_week}주차 {current_day}일 {current_hour}시")
                        triggered_events.append(event_name)
                        self.triggered_events.add(event_name)
                        return triggered_events
        
        # 랜덤 이벤트 체크 (고정 이벤트가 없는 경우에만)
        if current_day > self.last_random_event_day:
            possible_random_events = []
            for event_name, event in self.events['random_events'].items():
                # 이미 발생한 이벤트 중 반복이 불가능한 이벤트 건너뛰기
                if event_name in self.triggered_events and not event.get('repeatable', False):
                    continue

                # 요구사항 검사
                if not self.check_requirements(event):
                    continue

                time_trigger = event.get('time_trigger', {})
                
                # 학년 범위 검사
                if 'grade_range' in time_trigger:
                    grade_range = time_trigger['grade_range']
                    if not (grade_range[0] <= current_grade <= grade_range[1]):
                        continue
                
                # 주차 조건 검사
                if 'week' in time_trigger:
                    if time_trigger['week'] != current_week:
                        continue
                elif 'week_start' in time_trigger or 'week_end' in time_trigger:
                    week_start = time_trigger.get('week_start', 1)
                    week_end = time_trigger.get('week_end', 30)
                    if not (week_start <= current_week <= week_end):
                        continue
                
                # 요일 조건 체크
                if 'day' in time_trigger:
                    if time_trigger['day'] != current_day:
                        continue
                elif 'day_start' in time_trigger or 'day_end' in time_trigger:
                    day_start = time_trigger.get('day_start', 1)
                    day_end = time_trigger.get('day_end', 5)
                    if not (day_start <= current_day <= day_end):
                        continue
                
                # 시간 조건 체크
                if 'hour' in time_trigger:
                    if time_trigger['hour'] != current_hour:
                        continue
                elif 'hour_start' in time_trigger or 'hour_end' in time_trigger:
                    hour_start = time_trigger.get('hour_start', 0)
                    hour_end = time_trigger.get('hour_end', 23)
                    
                    # 자정을 걸치는 경우 (예: 22시 ~ 6시)
                    if hour_start > hour_end:
                        if not (current_hour >= hour_start or current_hour <= hour_end):
                            continue
                    else:
                        if not (hour_start <= current_hour <= hour_end):
                            continue

                print(f"[이벤트 추가] {event_name} 이벤트가 모든 조건을 만족")
                possible_random_events.append((event_name, event))
            
            # 랜덤 이벤트 선택
            if possible_random_events:
                total_probability = sum(event['probability'] for _, event in possible_random_events)
                if total_probability > 0:
                    random_value = random.random() * total_probability
                    current_sum = 0
                    for event_name, event in possible_random_events:
                        current_sum += event['probability']
                        if random_value <= current_sum:
                            print(f"\n[랜덤 이벤트 발생] {event['title']} - {current_week}주차 {current_day}일 {current_hour}시")
                            triggered_events.append(event_name)
                            self.triggered_events.add(event_name)
                            self.last_random_event_day = current_day
                            break
                
        return triggered_events
    
    def _handle_employment_success(self):
        """
        취업 성공 처리 -> check_employment_result
        """
        print("축하합니다! 취업에 성공했습니다!")
        # 여기에 취업 성공 관련 추가 로직 구현
    
    def _handle_employment_failure(self):
        """
        취업 실패 처리 -> check_employment_result
        """
        print("아쉽게도 취업에 실패했습니다...")
        # 여기에 취업 실패 관련 추가 로직 구현
    
    def check_employment_result(self, job_type):
        """
        취업 결과 결정
        """
        if job_type == 'big_company':
            if Stat.majorSubjectPoint >= 30 and Stat.responsibility >= 60:
                self._handle_employment_success()
            else:
                self._handle_employment_failure()
        elif job_type == 'startup':
            if Stat.majorSubjectPoint >= 20 and Stat.intuitivePoint >= 15:
                self._handle_employment_success()
            else:
                self._handle_employment_failure()
        elif job_type == 'big_company_functional':
            if Stat.functionalCompetition >= 50 and Stat.responsibility >= 50:
                self._handle_employment_success()
            else:
                self._handle_employment_failure()
        elif job_type == 'medium_company':
            if Stat.functionalCompetition >= 25:
                self._handle_employment_success()
            else:
                self._handle_employment_failure()
        elif job_type == 'public_company':
            if Stat.normalSubjectPoint >= 40 and Stat.responsibility >= 70:
                self._handle_employment_success()
            else:
                self._handle_employment_failure()
        elif job_type == 'bank':
            if Stat.normalSubjectPoint >= 50 and Stat.responsibility >= 80:
                self._handle_employment_success()
            else:
                self._handle_employment_failure()