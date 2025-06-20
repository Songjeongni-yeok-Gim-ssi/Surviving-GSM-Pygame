import random
from statAndStatPoint import Stat
from events_data import get_events_data
import pygame

class EventManager:
    def __init__(self):
        self.events = get_events_data()
        
        # 이미 발생한 이벤트를 추적
        self.triggered_events = set()
        
        # 마지막 이벤트 발생 날짜 추적 (이벤트별로)
        self.last_event_days = {}
        
        # 오늘 발생한 이벤트 추적
        self.today_triggered = False
        
        # 고정 이벤트 큐
        self.fixed_event_queue = []
        
        # 취업 조건 체크를 위한 임계값
        self.employment_thresholds = {
            'frontend': 80,  # 프론트엔드 스킬 레벨
            'backend': 80,   # 백엔드 스킬 레벨
            'public': 80,    # 공기업 준비 레벨
            'competition': 90  # 기능 대회 레벨
        }
        
        self._random_event_triggered_today = False
    
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
            elif stat_name == 'job_type':  # 취업 유형인 경우
                self.check_employment_result(value)  # 취업 결과 확인
            elif stat_name == 'func_type':
                self.func_com_result()
    
    def func_com_result(self):
        from study import Study
        from study import Subject
        
        employmentPercentages = 0
        
        for i in range(5):
            if Study.studyList[Subject.FC.value][i]:
                employmentPercentages += 20
        
        import random
        
        Stat.success = random.random() * 100 <= employmentPercentages
    
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
                    'image': event['image'],
                    'choices': event['choices'].get(Stat.major, [])
                }
            # 공통 선택지인 경우
            return event
        return None
    
    def get_random_event(self, event_name):
        """
        랜덤 이벤트 가져오기
        """
        event = self.events['random_events'].get(event_name)
        if event:
            # 전공별 선택지가 있는 경우
            if isinstance(event['choices'], dict):
                return {
                    'title': event['title'],
                    'text': event['text'],
                    'image': event['image'],
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
    
    def check_time_trigger(self, trigger, current_time):
        """
        이벤트의 시간 조건을 검사하는 통합 함수
        """
        current_week = current_time['week']
        current_day = current_time['day']
        current_hour = current_time['hour']
        current_grade = current_time.get('grade', 1)
        
        # 학년 범위 체크
        grade_range = trigger.get('grade_range', [1, 3])
        if not (grade_range[0] <= current_grade <= grade_range[1]):
            return False
        
        # 주차 조건 체크
        if 'week' in trigger:
            week_range = trigger['week']
            if isinstance(week_range, list):
                if not (week_range[0] <= current_week <= week_range[1]):
                    return False
            else:
                if week_range != current_week:
                    return False
        
        # 요일 조건 체크
        if 'day' in trigger:
            day_range = trigger['day']
            if isinstance(day_range, list):
                if not (day_range[0] <= current_day <= day_range[1]):
                    return False
            else:
                if day_range != current_day:
                    return False
        
        # 시간 조건 체크
        if 'hour' in trigger:
            hour_range = trigger['hour']
            if isinstance(hour_range, list):
                # 자정을 걸치는 경우 (예: [22, 6])
                if hour_range[0] > hour_range[1]:
                    if not (current_hour >= hour_range[0] or current_hour <= hour_range[1]):
                        return False
                else:
                    if not (hour_range[0] <= current_hour <= hour_range[1]):
                        return False
            else:
                if hour_range != current_hour:
                    return False
            
        return True

    def check_time_triggered_events(self, time_info):
        """
        시간에 따른 이벤트를 검사 후 트리거된 이벤트들을 반환하는 메서드
        """
        triggered_events = []   
        current_day = time_info['day']
        current_week = time_info['week']
        current_hour = time_info['hour']
        current_grade = time_info.get('grade', 1)  # 현재 학년 정보 가져오기
        
        # 날짜가 바뀌면 today_triggered 초기화
        if not hasattr(self, '_last_checked_day') or self._last_checked_day != current_day:
            self.today_triggered = False
            self._last_checked_day = current_day
            self._random_event_triggered_today = False  # 랜덤 이벤트 발생 여부 초기화
        
        # 고정 이벤트 처리
        # 1. 큐에 있는 고정 이벤트 처리
        if self.fixed_event_queue:
            event_name = self.fixed_event_queue[0]
            event = self.events['fixed_events'][event_name]
            if self.check_requirements(event):
                # 학년 범위 체크
                if 'time_trigger' in event and 'grade_range' in event['time_trigger']:
                    grade_range = event['time_trigger']['grade_range']
                    if not (grade_range[0] <= current_grade <= grade_range[1]):
                        self.fixed_event_queue.pop(0)  # 학년 범위를 벗어나면 큐에서 제거
                        return triggered_events
                
                print(f"\n[큐에서 고정 이벤트 발생] {event['title']} - {time_info['week']}주차 {time_info['day']}일 {time_info['hour']}시")
                triggered_events.append(event_name)
                if not event.get('repeatable', False):
                    self.triggered_events.add(event_name)
                self.today_triggered = True
                self.fixed_event_queue.pop(0)  # 처리된 이벤트 제거
                return triggered_events
        
        # 2. 현재 시간에 발생해야 하는 고정 이벤트 체크
        for event_name, event in self.events['fixed_events'].items():
            # 반복 가능한 이벤트는 triggered_events 체크를 건너뜀
            if event_name in self.triggered_events and not event.get('repeatable', False):
                continue
                
            if 'time_trigger' in event:
                trigger = event['time_trigger']
                
                # 학년 범위 체크
                if 'grade_range' in trigger:
                    if not (trigger['grade_range'][0] <= current_grade <= trigger['grade_range'][1]):
                        continue
                
                # 현재 주차와 요일이 일치하는지 확인
                if (trigger.get('week') == current_week and 
                    trigger.get('day') == current_day):
                    
                    
                    if (not isinstance(trigger.get('hour'), list)):
                        # 정확한 시간에 발생하는 경우
                        if trigger.get('hour') == current_hour:
                            if self.check_requirements(event):
                                print(f"\n[고정 이벤트 발생] {event['title']} - {time_info['week']}주차 {time_info['day']}일 {time_info['hour']}시")
                                triggered_events.append(event_name)
                                if not event.get('repeatable', False):
                                    self.triggered_events.add(event_name)
                                self.today_triggered = True
                                return triggered_events
                        # 시간이 지났고 아직 큐에 없는 경우
                        elif trigger.get('hour') < current_hour and event_name not in self.fixed_event_queue:
                            print(f"\n[고정 이벤트 큐 추가] {event['title']} - {time_info['week']}주차 {time_info['day']}일 {time_info['hour']}시")
                            self.fixed_event_queue.append(event_name)
                            return triggered_events  # 큐에 추가했으면 즉시 반환
                    else:
                        temp = trigger.get('hour')
                        if temp[0] <= current_hour <= temp[1]:
                            print(f"\n[고정 이벤트 큐 추가] {event['title']} - {time_info['week']}주차 {time_info['day']}일 {time_info['hour']}시")
                            self.fixed_event_queue.append(event_name)
                            print(self.fixed_event_queue)
                            return triggered_events  # 큐에 추가했으면 즉시 반환
        
        # 고정 이벤트가 발생하지 않고, 오늘 랜덤 이벤트가 아직 발생하지 않은 경우에만 랜덤 이벤트 체크
        if not triggered_events and not self.today_triggered and not getattr(self, '_random_event_triggered_today', False):
            # 랜덤 이벤트 체크 (20% 확률로만 체크)
            if random.random() < 0.2:  # 80% 확률로 체크 건너뛰기
                possible_random_events = []
                for event_name, event in self.events['random_events'].items():
                    # 이벤트 쿨다운 체크 (5일)
                    last_day = self.last_event_days.get(event_name, 0)
                    days_since_last = ((current_grade - 1) * 30) * 5 + (current_week - 1) * 5 + current_day - last_day
                    if days_since_last < 5 and event_name in self.last_event_days:
                        continue

                    # 요구사항 검사
                    if not self.check_requirements(event):
                        continue
                        
                    if 'time_trigger' in event:
                        # 학년 범위 체크
                        if 'grade_range' in event['time_trigger']:
                            grade_range = event['time_trigger']['grade_range']
                            if not (grade_range[0] <= current_grade <= grade_range[1]):
                                continue
                        
                        if self.check_time_trigger(event['time_trigger'], time_info):
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
                                print(f"\n[랜덤 이벤트 발생] {event['title']} - {time_info['week']}주차 {time_info['day']}일 {time_info['hour']}시")
                                triggered_events.append(event_name)
                                # 이벤트 발생 날짜 기록
                                self.last_event_days[event_name] = ((current_grade - 1) * 30) * 5 + (current_week - 1) * 5 + current_day
                                # 반복 불가능한 이벤트는 triggered_events에 추가
                                if not event.get('repeatable', False):
                                    self.triggered_events.add(event_name)
                                self.today_triggered = True
                                self._random_event_triggered_today = True  # 오늘 랜덤 이벤트 발생 표시
                                break
        
        return triggered_events
    
    def _handle_employment_success(self):
        """
        취업 성공 처리 -> check_employment_result
        """
        print("축하합니다! 취업에 성공했습니다!")
        from game import Game
        game = Game()
        game.endingText.set_text("취업에 성공했습니다!!!")
        if Stat.gender == "man":
            game.endingImage.set_image(pygame.image.load("assets/imgs/ending2.png"))
        elif Stat.gender == "woman":
            game.endingImage.set_image(pygame.image.load("assets/imgs/ending.png"))
        game.hide_all_ui()
        game.endingPanel.show()
        game.time_manager.pause_time()
    
    def _handle_employment_failure(self):
        """
        취업 실패 처리 -> check_employment_result
        """
        print("아쉽게도 취업에 실패했습니다...")
        from game import Game
        game = Game()
        game.endingText.set_text("취업에 실패했습니다...")
        if Stat.gender == "man":
            game.endingImage.set_image(pygame.image.load("assets/imgs/ending4.png"))
        elif Stat.gender == "woman":
            game.endingImage.set_image(pygame.image.load("assets/imgs/ending3.png"))
        game.hide_all_ui()
        game.endingPanel.show()
        game.time_manager.pause_time()
    
    def check_employment_result(self, job_type):
        """
        취업 결과 결정
        """
        from study import Study
        from study import Subject
        
        employmentPercentages = [ 0, 0, 0, 0 ]
        
        for i in range(4):
            for j in range(5):
                if Study.studyList[i][j]:
                    employmentPercentages[i] += 20
        
        import random
        
        if job_type == 'big_company':
            if random.random() * 100 <= (employmentPercentages[Subject.FE.value] + employmentPercentages[Subject.BE.value] + Stat.responsibility) / 3:
                self._handle_employment_success()
            else:
                self._handle_employment_failure()
        elif job_type == 'startup':
            if random.random() * 50 <= (employmentPercentages[Subject.FE.value] + employmentPercentages[Subject.BE.value] + Stat.responsibility) / 3:
                self._handle_employment_success()
            else:
                self._handle_employment_failure()
        elif job_type == 'big_company_functional':
            if random.random() * 100 <= (employmentPercentages[Subject.FC.value] + Stat.responsibility) / 2:
                self._handle_employment_success()
            else:
                self._handle_employment_failure()
        elif job_type == 'medium_company':
            if random.random() * 50 <= (employmentPercentages[Subject.FC.value] + Stat.responsibility) / 2:
                self._handle_employment_success()
            else:
                self._handle_employment_failure()
        elif job_type == 'public_company':
            if random.random() * 50 <= (employmentPercentages[Subject.PC.value] + Stat.responsibility) / 2:
                self._handle_employment_success()
            else:
                self._handle_employment_failure()
        elif job_type == 'bank':
            if random.random() * 100 <= (employmentPercentages[Subject.PC.value] + Stat.responsibility) / 2:
                self._handle_employment_success()
            else:
                self._handle_employment_failure()

    def reset(self):
        """이벤트 매니저의 상태를 초기화하는 메서드"""
        self.fixed_event_queue = []
        self._random_event_triggered_today = False
        self.triggered_events = set()
        self.last_event_days = {}