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
        print("_apply_effects")
        for stat_name, value in effects.items():
            if hasattr(Stat, stat_name):
                current_value = getattr(Stat, stat_name)
                new_value = current_value + value
                setattr(Stat, stat_name, new_value)
                print(f"[스탯 변경] {stat_name}: {current_value} -> {new_value}")
    
    def get_fixed_event(self, event_name):
        """고정 이벤트 가져오기"""
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
        """랜덤 이벤트 가져오기"""
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
                                'choices': event['choices'].get(Stat.major, event['choices'].get('common', []))
                            }
                        # 공통 선택지인 경우
                        return event
        return None
    
    def check_time_triggered_events(self, time_info):
        """
        시간에 따른 이벤트 체크
        """
        triggered_events = []   
        current_week = time_info['week']
        current_day = time_info['day']
        current_hour = time_info['hour']
        current_grade = time_info.get('grade', 1)  # 현재 학년 정보 가져오기
        
        # 고정 이벤트 체크
        for event_name, event in self.events['fixed_events'].items():
            if event_name not in self.triggered_events:
                if 'time_trigger' in event:
                    trigger = event['time_trigger']
                    # 학년 범위 체크
                    grade_range = trigger.get('grade_range', [1, 3])  # 기본값은 1-3학년
                    if not (grade_range[0] <= current_grade <= grade_range[1]):
                        continue
                        
                    if (trigger['week'] == current_week and 
                        trigger['day'] == current_day and 
                        trigger['hour'] == current_hour):
                        print(f"\n[고정 이벤트 발생] {event['title']} - {current_week}주차 {current_day}일 {current_hour}시")
                        triggered_events.append(event_name)
                        self.triggered_events.add(event_name)
        
        # 고정 이벤트가 발생하지 않은 경우에만 랜덤 이벤트 체크
        if not triggered_events and current_day > self.last_random_event_day:
            # 현재 시간에 발생 가능한 랜덤 이벤트들을 수집
            possible_random_events = []
            for event_name, event in self.events['random_events'].items():
                # 이미 발생한 이벤트는 건너뛰기
                if event_name in self.triggered_events and not event.get('repeatable', False):
                    continue

                # time_trigger 조건 체크
                time_trigger = event.get('time_trigger', {})
                
                # 학년 범위 체크
                grade_range = time_trigger.get('grade_range', [1, 3])  # 기본값은 1-3학년
                if not (grade_range[0] <= current_grade <= grade_range[1]):
                    continue
                
                # 주차 조건 체크
                if 'week' in time_trigger:
                    if time_trigger['week'] != current_week:
                        continue
                else:
                    week_start = time_trigger.get('week_start', 1)
                    week_end = time_trigger.get('week_end', 30)  # 30주로 수정
                    if not (week_start <= current_week <= week_end):
                        continue
                
                # 요일 조건 체크 (5일제로 수정)
                day_start = time_trigger.get('day_start', 1)
                day_end = time_trigger.get('day_end', 5)  # 5일로 수정
                if not (day_start <= current_day <= day_end):
                    continue
                
                # 시간 조건 체크
                hour_start = time_trigger.get('hour_start', 0)
                hour_end = time_trigger.get('hour_end', 23)
                
                if hour_start <= hour_end:
                    if not (hour_start <= current_hour <= hour_end):
                        continue
                else:  # 자정을 걸치는 경우
                    if not (current_hour >= hour_start or current_hour <= hour_end):
                        continue

                # 모든 조건을 만족하는 경우에만 이벤트 추가
                print(f"[이벤트 추가] {event_name} 이벤트가 모든 조건을 만족")
                possible_random_events.append((event_name, event))
            
            # 가능한 랜덤 이벤트가 있다면 하나만 선택
            if possible_random_events:
                # 확률에 따라 이벤트 선택
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
        """취업 성공 처리"""
        print("축하합니다! 취업에 성공했습니다!")
        # 여기에 취업 성공 관련 추가 로직 구현
    
    def _handle_employment_failure(self):
        """취업 실패 처리"""
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