import random
from statAndStatPoint import Stat

class EventManager:
    def __init__(self):
        self.events = {
            # 고정 이벤트 (타이밍 기반)
            'fixed_events': {
                'major_selection': {
                    'title': 'GSM 입학 / 전공 선택',
                    'text': '앞으로의 3년간 학습할 전공을 고르게 됩니다. 신중하게 선택하세요!',
                    'time_trigger': {
                        'week': 1,
                        'day': 1,
                        'hour': 9
                    },
                    'choices': [
                        {
                            'text': '개발자: 프론트엔드와 백엔드 같은 일반 전공을 공부합니다!',
                            'effect': lambda: setattr(Stat, 'major', 'developer')
                        },
                        {
                            'text': '기능반: 게임 개발과 같은 특수 전공을 공부합니다!',
                            'effect': lambda: setattr(Stat, 'major', 'functional')
                        },
                        {
                            'text': '공기업: 공기업과 금융권 취업을 목적으로 공부합니다!',
                            'effect': lambda: setattr(Stat, 'major', 'public')
                        }
                    ]
                },
                
                'certification_exam': {
                    'title': '자격증 시험',
                    'text': '자격증 시험을 볼 수 있는 기회가 왔다. 도전해볼까?',
                    'time_trigger': {
                        'week': 20,
                        'day': 1,
                        'hour': 9
                    },
                    'choices': [
                        {
                            'text': '도전한다.',
                            'effect': lambda: self._apply_effects({
                                'majorSubjectPoint': 8,
                                'normalSubjectPoint': 5,
                                'fatigue': 25
                            })
                        },
                        {
                            'text': '아직 준비가 안됐다.',
                            'effect': lambda: None
                        }
                    ]
                },
                
                'idea_festival': {
                    'title': '아이디어 페스티벌',
                    'text': '아이디어 페스티벌 기간이 다가왔다. 어떤 역할을 맡을까?',
                    'time_trigger': {
                        'week': 30,
                        'day': 1,
                        'hour': 10
                    },
                    'choices': {
                        'developer': [
                            {
                                'text': '누가 봐도 아름다운 디자인의 웹사이트를 만들자.',
                                'effect': lambda: self._apply_effects({
                                    'intuitivePoint': 10,
                                    'majorSubjectPoint': 5,
                                    'fatigue': 20
                                })
                            },
                            {
                                'text': '알고 보면 다양한 기능이 들어있는 유용한 앱을 만들자.',
                                'effect': lambda: self._apply_effects({
                                    'interpretPoint': 10,
                                    'majorSubjectPoint': 5,
                                    'fatigue': 20
                                })
                            },
                            {
                                'text': '기획/발표 같은 보조 업무만 담당한다.',
                                'effect': lambda: self._apply_effects({
                                    'responsibility': -5,
                                    'fame': -3,
                                    'fatigue': 10
                                })
                            }
                        ],
                        'functional': [
                            {
                                'text': '일반 전공은 할 줄 모르니 기획/발표 같은 잡일에만 참여한다.',
                                'effect': lambda: self._apply_effects({
                                    'functionalCompetition': 5,
                                    'responsibility': -3
                                })
                            },
                            {
                                'text': '이번 기회에 일반 전공도 같이 배워서 해보자.',
                                'effect': lambda: self._apply_effects({
                                    'intuitivePoint': 5,
                                    'interpretPoint': 5,
                                    'majorSubjectPoint': 3,
                                    'fatigue': 25
                                })
                            }
                        ],
                        'public': [
                            {
                                'text': '발표와 기획에 집중한다.',
                                'effect': lambda: self._apply_effects({
                                    'responsibility': 8,
                                    'normalSubjectPoint': 5,
                                    'fatigue': 15
                                })
                            },
                            {
                                'text': '개발도 배워보면서 참여한다.',
                                'effect': lambda: self._apply_effects({
                                    'majorSubjectPoint': 3,
                                    'normalSubjectPoint': 3,
                                    'fatigue': 20
                                })
                            }
                        ]
                    }
                },
                
                'self_directed_learning': {
                    'title': '자기주도 체험학습',
                    'text': '친구들과 함께하는 자기주도 체험학습이다! 나는 어떤 역할을 맡게될까?',
                    'time_trigger': {
                        'week': 40,
                        'day': 3,
                        'hour': 10
                    },
                    'choices': [
                        {
                            'text': '리더 역할을 맡는다.',
                            'effect': lambda: self._apply_effects({
                                'responsibility': 10,
                                'fame': 5,
                                'fatigue': 20
                            })
                        },
                        {
                            'text': '팀원으로 성실히 참여한다.',
                            'effect': lambda: self._apply_effects({
                                'responsibility': 5,
                                'fame': 3,
                                'fatigue': 15
                            })
                        },
                        {
                            'text': '적당히 참여한다.',
                            'effect': lambda: self._apply_effects({
                                'responsibility': -3,
                                'fame': -2,
                                'fatigue': 5
                            })
                        }
                    ]
                },
                
                'singapore_training': {
                    'title': '싱가포르 연수',
                    'text': '아기다리고 고기다리던 싱가포르 연수 기회가 왔다!',
                    'time_trigger': {
                        'week': 50,
                        'day': 1,
                        'hour': 9
                    },
                    'choices': [
                        {
                            'text': '적극적으로 참여하며 네트워킹한다.',
                            'effect': lambda: self._apply_effects({
                                'good': 10,
                                'responsibility': 8,
                                'fame': 8,
                                'majorSubjectPoint': 5,
                                'fatigue': 15
                            })
                        },
                        {
                            'text': '관광을 즐기며 적당히 참여한다.',
                            'effect': lambda: self._apply_effects({
                                'evil': 3,
                                'fatigue': -10
                            })
                        },
                        {
                            'text': '학습에만 집중한다.',
                            'effect': lambda: self._apply_effects({
                                'majorSubjectPoint': 10,
                                'responsibility': 5,
                                'fatigue': 20
                            })
                        }
                    ]
                },
                
                'final_job_selection': {
                    'title': '취업의 선택',
                    'text': '결전의 순간이 왔다. 어떤 길을 선택할 것인가?',
                    'time_trigger': {
                        'week': 100,
                        'day': 1,
                        'hour': 9
                    },
                    'choices': {
                        'developer': [
                            {
                                'text': '대기업 개발자로 지원한다.',
                                'requirements': {'majorSubjectPoint': 30, 'responsibility': 60},
                                'effect': lambda: self._determine_job_outcome('big_company')
                            },
                            {
                                'text': '스타트업에 도전한다.',
                                'requirements': {'majorSubjectPoint': 20, 'intuitivePoint': 15},
                                'effect': lambda: self._determine_job_outcome('startup')
                            }
                        ],
                        'functional': [
                            {
                                'text': '기능 대회 실력으로 대기업에 도전한다.',
                                'requirements': {'functionalCompetition': 50, 'responsibility': 50},
                                'effect': lambda: self._determine_job_outcome('big_company_functional')
                            },
                            {
                                'text': '중견기업에 안정적으로 취업한다.',
                                'requirements': {'functionalCompetition': 25},
                                'effect': lambda: self._determine_job_outcome('medium_company')
                            }
                        ],
                        'public': [
                            {
                                'text': '공기업에 지원한다.',
                                'requirements': {'normalSubjectPoint': 40, 'responsibility': 70},
                                'effect': lambda: self._determine_job_outcome('public_company')
                            },
                            {
                                'text': '은행권에 도전한다.',
                                'requirements': {'normalSubjectPoint': 50, 'responsibility': 80},
                                'effect': lambda: self._determine_job_outcome('bank')
                            }
                        ]
                    }
                }
            },
            
            # 랜덤 이벤트
            'random_events': {
                'dormitory_ramen': {
                    'title': '기숙사 라면 사건',
                    'text': '친구가 같이 기숙사 금지 항목인 라면을 먹자고 꼬신다!',
                    'probability': 0.3,
                    'location': 'dormitory',
                    'repeatable': True,
                    'choices': [
                        {
                            'text': '같이 먹는다.',
                            'effect': lambda: self._apply_effects({
                                'evil': 5,
                                'fame': -3,
                                'fatigue': -15
                            })
                        },
                        {
                            'text': '안 먹고 못 본 채 한다.',
                            'effect': lambda: None
                        },
                        {
                            'text': '기자위한테 알린다.',
                            'effect': lambda: self._apply_effects({
                                'good': 5,
                                'responsibility': 3,
                                'fame': -8,
                                'fatigue': 10
                            })
                        }
                    ]
                },
                
                'team_project_conflict': {
                    'title': '아이디어 페스티벌 - 팀원 관리',
                    'text': '아이디어 페스티벌 기간, 팀원이 할 일을 미룬다. 어떻게 할까?',
                    'probability': 0.4,
                    'time_range': {'week_start': 30, 'week_end': 35},
                    'choices': [
                        {
                            'text': '직접 대화해서 해결한다.',
                            'effect': lambda: self._apply_effects({
                                'responsibility': 8,
                                'fame': 5,
                                'fatigue': 15
                            })
                        },
                        {
                            'text': '교사에게 신고한다.',
                            'effect': lambda: self._apply_effects({
                                'good': 3,
                                'fame': -5,
                                'fatigue': 5
                            })
                        },
                        {
                            'text': '내가 대신 해준다.',
                            'effect': lambda: self._apply_effects({
                                'responsibility': -5,
                                'majorSubjectPoint': 3,
                                'fatigue': 25
                            })
                        },
                        {
                            'text': '그냥 놔둔다.',
                            'effect': lambda: self._apply_effects({
                                'evil': 3,
                                'fame': -3
                            })
                        }
                    ]
                },
                
                'study_time_choice': {
                    'title': '학교 자습 시간',
                    'text': '2학년이 되면서 자습 시간이 늘어났다. 무엇을 하면 좋을까?',
                    'probability': 0.6,
                    'time_range': {'week_start': 20, 'week_end': 80},
                    'repeatable': True,
                    'choices': {
                        'developer': [
                            {
                                'text': '프론트엔드 공부를 한다.',
                                'effect': lambda: self._apply_effects({
                                    'intuitivePoint': 8,
                                    'majorSubjectPoint': 5,
                                    'fatigue': 15
                                })
                            },
                            {
                                'text': '백엔드 공부를 한다.',
                                'effect': lambda: self._apply_effects({
                                    'interpretPoint': 8,
                                    'majorSubjectPoint': 5,
                                    'fatigue': 15
                                })
                            },
                            {
                                'text': '개인 프로젝트를 한다.',
                                'effect': lambda: self._apply_effects({
                                    'majorSubjectPoint': 10,
                                    'responsibility': 5,
                                    'fatigue': 20
                                })
                            }
                        ],
                        'functional': [
                            {
                                'text': '기능 대회 준비를 한다.',
                                'effect': lambda: self._apply_effects({
                                    'functionalCompetition': 10,
                                    'fatigue': 20
                                })
                            },
                            {
                                'text': '일반 전공도 공부한다.',
                                'effect': lambda: self._apply_effects({
                                    'majorSubjectPoint': 8,
                                    'fatigue': 18
                                })
                            }
                        ],
                        'public': [
                            {
                                'text': '공기업 시험 공부를 한다.',
                                'effect': lambda: self._apply_effects({
                                    'normalSubjectPoint': 10,
                                    'fatigue': 15
                                })
                            },
                            {
                                'text': '개발 공부도 병행한다.',
                                'effect': lambda: self._apply_effects({
                                    'normalSubjectPoint': 5,
                                    'majorSubjectPoint': 5,
                                    'fatigue': 20
                                })
                            }
                        ],
                        'common': [
                            {
                                'text': '그냥 놀면서 쉰다.',
                                'effect': lambda: self._apply_effects({
                                    'evil': 2,
                                    'fatigue': -10
                                })
                            }
                        ]
                    }
                },
                
                'devfestival_conference': {
                    'title': 'DevFestival 컨퍼런스 참여',
                    'text': 'DevFestival 컨퍼런스 발표자를 모집한다. 참여해볼까?',
                    'probability': 0.2,
                    'time_range': {'week_start': 25, 'week_end': 35},
                    'choices': [
                        {
                            'text': '발표자로 참여한다.',
                            'effect': lambda: self._apply_effects({
                                'responsibility': 10,
                                'fame': 8,
                                'majorSubjectPoint': 5,
                                'fatigue': 25
                            })
                        },
                        {
                            'text': '청중으로만 참여한다.',
                            'effect': lambda: self._apply_effects({
                                'majorSubjectPoint': 3,
                                'fatigue': 10
                            })
                        },
                        {
                            'text': '참여하지 않는다.',
                            'effect': lambda: None
                        }
                    ]
                },
                
                'project_experience': {
                    'title': '프로젝트 경험',
                    'text': '이제 곧 취업을 해야하는데 어떤 프로젝트를 하는게 좋을까?',
                    'probability': 0.5,
                    'time_range': {'week_start': 60, 'week_end': 90},
                    'repeatable': False,
                    'choices': [
                        {
                            'text': '개인 프로젝트에 집중한다.',
                            'effect': lambda: self._apply_effects({
                                'majorSubjectPoint': 12,
                                'responsibility': 8,
                                'fatigue': 30
                            })
                        },
                        {
                            'text': '팀 프로젝트를 진행한다.',
                            'effect': lambda: self._apply_effects({
                                'majorSubjectPoint': 8,
                                'responsibility': 5,
                                'fame': 5,
                                'fatigue': 25
                            })
                        },
                        {
                            'text': '외부 공모전에 참여한다.',
                            'effect': lambda: self._apply_effects({
                                'majorSubjectPoint': 10,
                                'responsibility': 10,
                                'fame': 8,
                                'fatigue': 35
                            })
                        }
                    ]
                },
                
                'lecture_attendance': {
                    'title': '특별 강의',
                    'text': '학교에서 특별 강의 공지가 올라왔다! 참여해볼까?',
                    'probability': 0.4,
                    'repeatable': True,
                    'choices': [
                        {
                            'text': '적극적으로 참여한다.',
                            'effect': lambda: self._apply_effects({
                                'majorSubjectPoint': 5,
                                'normalSubjectPoint': 3,
                                'fatigue': 15
                            })
                        },
                        {
                            'text': '다른 공부를 한다.',
                            'effect': lambda: self._apply_effects({
                                'majorSubjectPoint': 3,
                                'fatigue': 10
                            })
                        }
                    ]
                }
            },
            
            # 기능반 전용 이벤트
            'functional_events': {
                'skill_competition_prep': {
                    'title': '기능 대회 대비 잔류',
                    'text': '방학 중 기능 대회를 대비해 학교에 잔류할 수 있다.',
                    'probability': 0.8,
                    'major_required': 'functional',
                    'time_range': {'week_start': 15, 'week_end': 18},
                    'choices': [
                        {
                            'text': '잔류하며 집중 훈련한다.',
                            'effect': lambda: self._apply_effects({
                                'functionalCompetition': 15,
                                'fame': 3,
                                'fatigue': 35
                            })
                        },
                        {
                            'text': '집에서 개인적으로 준비한다.',
                            'effect': lambda: self._apply_effects({
                                'functionalCompetition': 8,
                                'fatigue': 20
                            })
                        },
                        {
                            'text': '쉬면서 컨디션을 관리한다.',
                            'effect': lambda: self._apply_effects({
                                'fatigue': -20
                            })
                        }
                    ]
                },
                
                'skill_competition': {
                    'title': '기능 대회',
                    'text': '드디어 기능 대회 당일이다! 최선을 다해보자.',
                    'major_required': 'functional',
                    'time_trigger': {
                        'week': 45,
                        'day': 3,
                        'hour': 9
                    },
                    'choices': [
                        {
                            'text': '평소 실력을 발휘한다.',
                            'effect': lambda: self._skill_competition_result('normal')
                        },
                        {
                            'text': '위험하지만 새로운 기술을 시도한다.',
                            'effect': lambda: self._skill_competition_result('risky')
                        },
                        {
                            'text': '안전하게 완성도에 집중한다.',
                            'effect': lambda: self._skill_competition_result('safe')
                        }
                    ]
                }
            },
            
            # 위치 기반 이벤트
            'location_events': {
                'dormitory': {
                    'study_room': {
                        'title': '기숙사 자습실',
                        'text': '기숙사에 도착했다! 피곤하긴 하지만 자습실을 사용할까 고민이 된다.',
                        'probability': 0.7,
                        'choices': [
                            {
                                'text': '자습실에서 공부한다.',
                                'effect': lambda: self._apply_effects({
                                    'majorSubjectPoint': 5,
                                    'normalSubjectPoint': 3,
                                    'fatigue': 20
                                })
                            },
                            {
                                'text': '방에서 쉰다.',
                                'effect': lambda: self._apply_effects({
                                    'fatigue': -15
                                })
                            }
                        ]
                    }
                }
            }
        }
        
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
        """스탯 효과 적용"""
        for stat_name, value in effects.items():
            if hasattr(Stat, stat_name):
                current_value = getattr(Stat, stat_name)
                new_value = current_value + value
                setattr(Stat, stat_name, new_value)
                print(f"[스탯 변경] {stat_name}: {current_value} -> {new_value}")
    
    def get_fixed_event(self, event_name):
        """고정 이벤트 가져오기"""
        return self.events['fixed_events'].get(event_name)
    
    def get_random_event(self, location):
        """랜덤 이벤트 가져오기"""
        possible_events = []
        for event_name, event in self.events['random_events'].items():
            if event_name not in self.triggered_events:
                if 'location' in event and event['location'] == location:
                    possible_events.append((event_name, event))
        
        if possible_events:
            event_name, event = random.choice(possible_events)
            self.triggered_events.add(event_name)
            return event
        return None
    
    def check_time_triggered_events(self, time_info):
        """시간에 따른 이벤트 체크"""
        triggered_events = []   
        current_week = time_info['week']
        current_day = time_info['day']
        current_hour = time_info['hour']
        
        # 고정 이벤트 체크
        for event_name, event in self.events['fixed_events'].items():
            if event_name not in self.triggered_events:
                if 'time_trigger' in event:
                    trigger = event['time_trigger']
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
                # repeatable이 True이거나 아직 발생하지 않은 이벤트만 추가
                if event.get('repeatable', False) or event_name not in self.triggered_events:
                    if 'time_range' in event:
                        if (event['time_range']['week_start'] <= current_week <= event['time_range']['week_end']):
                            possible_random_events.append((event_name, event))
                    else:
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
    
    def _determine_job_outcome(self, job_type):
        """취업 결과 결정"""
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
    
    def _handle_employment_success(self):
        """취업 성공 처리"""
        print("\n[취업 성공!] 🎉")
        print("\n[최종 스탯]")
        self._print_final_stats()
        Stat.game_completed = True
        Stat.employment_success = True
    
    def _handle_employment_failure(self):
        """취업 실패 처리"""
        print("\n[취업 실패...] 😢")
        print("\n[최종 스탯]")
        self._print_final_stats()
        Stat.game_completed = True
        Stat.employment_success = False
    
    def _print_final_stats(self):
        """최종 스탯 출력"""
        stats = {
            '전공 과목': Stat.majorSubjectPoint,
            '일반 과목': Stat.normalSubjectPoint,
            '기능 대회': Stat.functionalCompetition,
            '직관력': Stat.intuitivePoint,
            '해석력': Stat.interpretPoint,
            '책임감': Stat.responsibility,
            '선함': Stat.good,
            '악함': Stat.evil,
            '명성': Stat.fame,
            '피로도': Stat.fatigue
        }
        
        for stat_name, value in stats.items():
            print(f"- {stat_name}: {value}")
    
    def _skill_competition_result(self, strategy):
        """기능 대회 결과 처리"""
        if strategy == 'normal':
            self._apply_effects({
                'functionalCompetition': 20,
                'fatigue': 30
            })
        elif strategy == 'risky':
            if random.random() < 0.3:  # 30% 확률로 성공
                self._apply_effects({
                    'functionalCompetition': 40,
                    'fame': 10,
                    'fatigue': 40
                })
            else:
                self._apply_effects({
                    'functionalCompetition': -10,
                    'fatigue': 20
                })
        elif strategy == 'safe':
            self._apply_effects({
                'functionalCompetition': 15,
                'fatigue': 20
            })
