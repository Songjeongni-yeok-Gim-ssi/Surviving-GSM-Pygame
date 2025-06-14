from statAndStatPoint import Stat

def get_events_data():
    return {
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
                            'effect': lambda: {'intuitivePoint': 10, 'majorSubjectPoint': 5, 'fatigue': 20}
                        },
                        {
                            'text': '알고 보면 다양한 기능이 들어있는 유용한 앱을 만들자.',
                            'effect': lambda: {'interpretPoint': 10, 'majorSubjectPoint': 5, 'fatigue': 20}
                        },
                        {
                            'text': '기획/발표 같은 보조 업무만 담당한다.',
                            'effect': lambda: {'responsibility': -5, 'fame': -3, 'fatigue': 10}
                        }
                    ],
                    'functional': [
                        {
                            'text': '일반 전공은 할 줄 모르니 기획/발표 같은 잡일에만 참여한다.',
                            'effect': lambda: {'functionalCompetition': 5, 'responsibility': -3}
                        },
                        {
                            'text': '이번 기회에 일반 전공도 같이 배워서 해보자.',
                            'effect': lambda: {'intuitivePoint': 5, 'interpretPoint': 5, 'majorSubjectPoint': 3, 'fatigue': 25}
                        }
                    ],
                    'public': [
                        {
                            'text': '발표와 기획에 집중한다.',
                            'effect': lambda: {'responsibility': 8, 'normalSubjectPoint': 5, 'fatigue': 15}
                        },
                        {
                            'text': '개발도 배워보면서 참여한다.',
                            'effect': lambda: {'majorSubjectPoint': 3, 'normalSubjectPoint': 3, 'fatigue': 20}
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
                        'effect': lambda: {'responsibility': 10, 'fame': 5, 'fatigue': 20}
                    },
                    {
                        'text': '팀원으로 성실히 참여한다.',
                        'effect': lambda: {'responsibility': 5, 'fame': 3, 'fatigue': 15}
                    },
                    {
                        'text': '적당히 참여한다.',
                        'effect': lambda: {'responsibility': -3, 'fame': -2, 'fatigue': 5}
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
                        'effect': lambda: {'good': 10, 'responsibility': 8, 'fame': 8, 'majorSubjectPoint': 5, 'fatigue': 15}
                    },
                    {
                        'text': '관광을 즐기며 적당히 참여한다.',
                        'effect': lambda: {'evil': 3, 'fatigue': -10}
                    },
                    {
                        'text': '학습에만 집중한다.',
                        'effect': lambda: {'majorSubjectPoint': 10, 'responsibility': 5, 'fatigue': 20}
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
                            'effect': lambda: 'big_company'
                        },
                        {
                            'text': '스타트업에 도전한다.',
                            'requirements': {'majorSubjectPoint': 20, 'intuitivePoint': 15},
                            'effect': lambda: 'startup'
                        }
                    ],
                    'functional': [
                        {
                            'text': '기능 대회 실력으로 대기업에 도전한다.',
                            'requirements': {'functionalCompetition': 50, 'responsibility': 50},
                            'effect': lambda: 'big_company_functional'
                        },
                        {
                            'text': '중견기업에 안정적으로 취업한다.',
                            'requirements': {'functionalCompetition': 25},
                            'effect': lambda: 'medium_company'
                        }
                    ],
                    'public': [
                        {
                            'text': '공기업에 지원한다.',
                            'requirements': {'normalSubjectPoint': 40, 'responsibility': 70},
                            'effect': lambda: 'public_company'
                        },
                        {
                            'text': '은행권에 도전한다.',
                            'requirements': {'normalSubjectPoint': 50, 'responsibility': 80},
                            'effect': lambda: 'bank'
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
                'repeatable': True,
                'time_trigger': {
                    'hour_start': 22,  # 오후 10시
                    'hour_end': 6      # 오전 6시
                },
                'choices': [
                    {
                        'text': '같이 먹는다.',
                        'effect': lambda: {'evil': 5, 'fame': -3, 'fatigue': -15}
                    },
                    {
                        'text': '안 먹고 못 본 채 한다.',
                        'effect': lambda: None
                    },
                    {
                        'text': '기자위한테 알린다.',
                        'effect': lambda: {'good': 5, 'responsibility': 3, 'fame': -8, 'fatigue': 10}
                    }
                ]
            },
            'study_time_choice': {
                'title': '학교 자습 시간',
                'text': '2학년이 되면서 자습 시간이 늘어났다. 무엇을 하면 좋을까?',
                'probability': 0.6,
                'time_range': {'week_start': 20, 'week_end': 80},
                'repeatable': True,
                'time_trigger': {
                    'hour_start': 9,   # 오전 9시
                    'hour_end': 20     # 오후 8시 20분
                },
                'choices': {
                    'developer': [
                        {
                            'text': '프론트엔드 공부를 한다.',
                            'effect': lambda: {'intuitivePoint': 8, 'majorSubjectPoint': 5, 'fatigue': 15}
                        },
                        {
                            'text': '백엔드 공부를 한다.',
                            'effect': lambda: {'interpretPoint': 8, 'majorSubjectPoint': 5, 'fatigue': 15}
                        },
                        {
                            'text': '개인 프로젝트를 한다.',
                            'effect': lambda: {'majorSubjectPoint': 10, 'responsibility': 5, 'fatigue': 20}
                        }
                    ],
                    'functional': [
                        {
                            'text': '기능 대회 준비를 한다.',
                            'effect': lambda: {'functionalCompetition': 10, 'fatigue': 20}
                        },
                        {
                            'text': '일반 전공도 공부한다.',
                            'effect': lambda: {'majorSubjectPoint': 8, 'fatigue': 18}
                        }
                    ],
                    'public': [
                        {
                            'text': '공기업 시험 공부를 한다.',
                            'effect': lambda: {'normalSubjectPoint': 10, 'fatigue': 15}
                        },
                        {
                            'text': '개발 공부도 병행한다.',
                            'effect': lambda: {'normalSubjectPoint': 5, 'majorSubjectPoint': 5, 'fatigue': 20}
                        }
                    ],
                    'common': [
                        {
                            'text': '그냥 놀면서 쉰다.',
                            'effect': lambda: {'evil': 2, 'fatigue': -10}
                        }
                    ]
                }
            },
            'project_experience': {
                'title': '프로젝트 경험',
                'text': '이제 곧 취업을 해야하는데 어떤 프로젝트를 하는게 좋을까?',
                'probability': 0.5,
                'time_range': {'week_start': 60, 'week_end': 90},
                'repeatable': False,
                'time_trigger': {
                    'hour_start': 9,   # 오전 9시
                    'hour_end': 20     # 오후 8시 20분
                },
                'choices': [
                    {
                        'text': '개인 프로젝트에 집중한다.',
                        'effect': lambda: {'majorSubjectPoint': 12, 'responsibility': 8, 'fatigue': 30}
                    },
                    {
                        'text': '팀 프로젝트를 진행한다.',
                        'effect': lambda: {'majorSubjectPoint': 8, 'responsibility': 5, 'fame': 5, 'fatigue': 25}
                    },
                    {
                        'text': '외부 공모전에 참여한다.',
                        'effect': lambda: {'majorSubjectPoint': 10, 'responsibility': 10, 'fame': 8, 'fatigue': 35}
                    }
                ]
            },
            'lecture_attendance': {
                'title': '특별 강의',
                'text': '학교에서 특별 강의 공지가 올라왔다! 참여해볼까?',
                'probability': 0.4,
                'repeatable': True,
                'time_trigger': {
                    'hour_start': 9,   # 오전 9시
                    'hour_end': 20     # 오후 8시 20분
                },
                'choices': [
                    {
                        'text': '적극적으로 참여한다.',
                        'effect': lambda: {'majorSubjectPoint': 5, 'normalSubjectPoint': 3, 'fatigue': 15}
                    },
                    {
                        'text': '다른 공부를 한다.',
                        'effect': lambda: {'majorSubjectPoint': 3, 'fatigue': 10}
                    }
                ]
            }
        }
    } 