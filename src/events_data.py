from statAndStatPoint import Stat

def get_events_data():
    return {
        # 고정 이벤트
        'fixed_events': {
            'major_selection': {
                'title': 'GSM 입학 / 전공 선택',
                'text': '앞으로의 3년간 학습할 전공을 고르게 됩니다. 신중하게 선택하세요!',
                'image': 'assets/imgs/events/major_selection.png',
                'time_trigger': {
                    'week': 1,
                    'day': 1,
                    'hour': 9,
                    'grade_range': [1, 1]  # 1학년에만 발생
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
            'gender_selection': {
                'title': '성별 선택',
                'text': '당신의 성별을 선택해주세요.',
                'image': 'assets/imgs/events/gender_selection.png',
                'time_trigger': {
                    'week': 1,
                    'day': 1,
                    'hour': 10,
                    'grade_range': [1, 1]  # 1학년에만 발생
                },
                'choices': [
                    {
                        'text': '남성',
                        'effect': lambda: setattr(Stat, 'gender', 'man')
                    },
                    {
                        'text': '여성',
                        'effect': lambda: setattr(Stat, 'gender', 'woman')
                    }
                ]
            },
            'idea_festival': {
                'title': '아이디어 페스티벌',
                'text': '아이디어 페스티벌 기간이 다가왔다. 어떤 역할을 맡을까?',
                'image': 'assets/imgs/events/idea_festival.png',
                'time_trigger': {   
                    'week': 10,
                    'day': 1,
                    'hour': 10,
                    'grade_range': [1, 2]  # 1-2학년에 발생
                },
                'repeatable': True,
                'choices': {
                    'developer': [
                        {
                            'text': '누가 봐도 아름다운 디자인의 웹사이트를 만들자.',
                            'effect': lambda: {'intuitivePoint': 30, 'majorSubjectPoint': 10, 'fatigue': 10}
                        },
                        {
                            'text': '알고 보면 다양한 기능이 들어있는 유용한 앱을 만들자.',
                            'effect': lambda: {'interpretPoint': 30, 'majorSubjectPoint': 10, 'fatigue': 10}
                        },
                        {
                            'text': '기획/발표 같은 보조 업무만 담당한다.',
                            'effect': lambda: {'responsibility': -5, 'fame': -5, 'fatigue': 5}
                        }
                    ],
                    'functional': [
                        {
                            'text': '일반 전공은 할 줄 모르니 기획/발표 같은 잡일에만 참여한다.',
                            'effect': lambda: {'functionalCompetition': 20, 'responsibility': -3}
                        },
                        {
                            'text': '이번 기회에 일반 전공도 같이 배워서 해보자.',
                            'effect': lambda: {'intuitivePoint': 20, 'interpretPoint': 20, 'majorSubjectPoint': 20, 'responsibility' : 10, 'fatigue': 15}
                        }
                    ],
                    'public': [
                        {
                            'text': '발표와 기획에 집중한다.',
                            'effect': lambda: {'responsibility': 8, 'normalSubjectPoint': 15, 'fatigue': 10}
                        },
                        {
                            'text': '개발도 배워보면서 참여한다.',
                            'effect': lambda: {'majorSubjectPoint': 15, 'normalSubjectPoint': 13, 'fatigue': 15}
                        }
                    ]
                }
            },
            'singapore_training': {
                'title': '싱가포르 연수',
                'text': '아기다리고 고기다리던 싱가포르 연수 기회가 왔다!',
                'image': 'assets/imgs/events/singapore_training.png',
                'time_trigger': {
                    'week': 5,
                    'day': 1,
                    'hour': 9,
                    'grade_range': [1, 1]  # 1학년에만 발생
                },
                'choices': [
                    {
                        'text': '선생님 말씀에 따라 일정 잘 지키며 안전하게 다녀오자!',
                        'effect': lambda: {'good': 5, 'fatigue': 10, 'responsibility': 15}
                    },
                    {
                        'text': '난 친구들과 노는게 중요해!',
                        'effect': lambda: {'evil': 5, 'fame': -15, 'fatigue' : -20}
                    }
                ]
            },
            'final_job_selection': {
                'title': '최종 취업 선택',
                'text': '최종 취업을 선택할 시간입니다.',
                'image': 'assets/imgs/events/final_job_selection.jpeg',
                'time_trigger': {
                    'week': 1,
                    'day': 1,
                    'hour': 9,
                    'grade_range': [3, 3]  # 3학년에만 발생
                },
                'choices': {
                    'developer': [
                        {
                            'text': '대기업 개발자로 지원한다.',
                            'effect': lambda: {'job_type': 'big_company'}
                        },
                        {
                            'text': '스타트업에 도전한다.',
                            'effect': lambda: {'job_type': 'startup'}
                        }
                    ],
                    'functional': [
                        {
                            'text': '기능 대회 실력으로 대기업에 도전한다.',
                            'effect': lambda: {'job_type': 'big_company_functional'}
                        },
                        {
                            'text': '중견기업에 안정적으로 취업한다.',
                            'effect': lambda: {'job_type': 'medium_company'}
                        }
                    ],
                    'public': [
                        {
                            'text': '공기업에 지원한다.',
                            'effect': lambda: {'job_type': 'public_company'}
                        },
                        {
                            'text': '은행권에 도전한다.',
                            'effect': lambda: {'job_type': 'bank'}
                        }
                    ]
                }
            },
            'functional_competition': {
                'title': '기능 대회',
                'text': '기능 대회가 시작됩니다. 과연 결과는?!?!?!?!?!?!',
                'image': 'assets/imgs/events/functional_competition.png',
                'time_trigger': {
                    'week': 2,
                    'day': 3,
                    'hour': 12,
                    'grade_range': [2, 3]
                },
                'requirements': {'major': 'functional'},
                'repeatable': True,
                'choices': [
                    {
                        'text': '과연 결과는?!?!?!?!?!?!',
                        'effect': lambda: {'func_type' : 0}
                    }
                ]
            },
            'functional_competition_success': {
                'title': '결과',
                'text': '우승!',
                'image': 'assets/imgs/events/functional_competition.png',
                'time_trigger': {
                    'week': 2,
                    'day': 3,
                    'hour': 13,
                    'grade_range': [2, 3]
                },
                'requirements': {'major': 'functional', 'success' : True},
                'repeatable': True,
                'choices': [
                    {
                        'text': '와!!!!!!',
                        'effect': lambda: {'functionalCompetition' : 300, 'fatigue' : -100}
                    }
                ]
            },
            'functional_competition_fail': {
                'title': '결과',
                'text': '실패...',
                'image': 'assets/imgs/events/functional_competition.png',
                'time_trigger': {
                    'week': 2,
                    'day': 3,
                    'hour': 13,
                    'grade_range': [2, 3]
                },
                'requirements': {'major': 'functional', 'success' : False},
                'repeatable': True,
                'choices': [
                    {
                        'text': '와....',
                        'effect': lambda: {'functionalCompetition' : 100}
                    }
                ]
            },
            'functional_competition_prep': {
                'title': '기능 대회 대비 출결',
                'text': '기능 대회를 위한 준비 시간입니다. 어떻게 공부할까요?',
                'time_trigger': {
                    'week': 15,
                    'day': 1,
                    'hour': 8,
                    'grade_range': [1, 3]
                },
                'requirements': {'major': 'functional'},
                'repeatable': True,
                'choices': [
                    {
                        'text': '기능 대회 문제를 풀며 공부한다.',
                        'effect': lambda: {'functionalCompetition': 100, 'fatigue': 50}
                    },
                    {
                        'text': '개인 공부를 이어간다.',
                        'effect': lambda: {'functionalCompetition': 30, 'fatigue': 10}
                    },
                    {
                        'text': '빠르게 문제를 푸는 방법을 집중적으로 공부한다.',
                        'effect': lambda: {'functionalCompetition': 70, 'fatigue': 35}
                    }
                ]
            },
            'vacation_stay': {
                'title': '방학 중 기숙사 잔류',
                'text': '방학 중 기숙사에 남아서 공부할 수 있습니다.',
                'image': 'assets/imgs/events/vacation_stay.png',
                'time_trigger': {
                    'week': 20,
                    'day': 5,
                    'hour': 16,
                    'grade_range': [1, 2]
                },
                'requirements': {'major': 'functional'},
                'repeatable': True,
                'choices': [
                    {
                        'text': '한다',
                        'effect': lambda: {'functionalCompetition': 150, 'fatigue': 50}
                    },
                    {
                        'text': '안 한다',
                        'effect': lambda: {'fame': -25, 'fatigue': -100}  # 피로도 완전 회복
                    }
                ]
            },
            'hackathon': {
                'title': '해커톤',
                'text': '해커톤이 시작됩니다.',
                'image': 'assets/imgs/events/hackathon.png',
                'time_trigger': {
                    'week': 8,
                    'day': 1,
                    'hour': 9,
                    'grade_range': [2, 3]
                },
                'requirements': {'major': 'developer'},
                'repeatable': True,
                'choices': [
                    {
                        'text': '참여한다.',
                        'effect': lambda: {'majorSubjectPoint': 85, 'fatigue': 10}
                    },
                    {
                        'text': '참여하지 않는다.',
                        'effect': lambda: None
                    }
                ]
            },
            'korean_history_exam': {
                'title': '한국사 시험',
                'text': '한국사 시험이 시작됩니다.',
                'image': 'assets/imgs/events/korean_history_exam.png',
                'time_trigger': {
                    'week': 7,
                    'day': 1,
                    'hour': 9,
                    'grade_range': [1, 2]
                },
                'requirements': {'major': 'public'},
                'repeatable': True,
                'choices': [
                    {
                        'text': '응시한다.',
                        'effect': lambda: {'normalSubjectPoint': 50, 'fatigue': 10}
                    },
                    {
                        'text': '응시하지 않는다.',
                        'effect': lambda: {'fatigue': -10}
                    }
                ]
            },
            'ncs_lecture': {
                'title': 'NCS 강의',
                'text': 'NCS 강의가 시작됩니다.',
                'image': 'assets/imgs/events/ncs_lecture.png',
                'time_trigger': {
                    'week': 15,
                    'day': 1,
                    'hour': 13,
                    'grade_range': [2, 2]
                },
                'requirements': {'major': 'public'},
                'repeatable': True,
                'choices': [
                    {
                        'text': '신청한다.',
                        'effect': lambda: {'normalSubjectPoint': 60, 'fatigue': 10}
                    },
                    {
                        'text': '신청하지 않는다.',
                        'effect': lambda: {'fatigue': -10}
                    }
                ]
            },
            'public_company_lecture': {
                'title': '공기업 특강',
                'text': '디스코드 1학년 게시판에 1학년을 대상으로 하는 공기업 특강이 떴다! 한번 신청해 볼까?',
                'image': 'assets/imgs/events/public_company_lecture.png',
                'time_trigger': {
                    'week': 7,
                    'day': 1,
                    'hour': 13,
                    'grade_range': [1, 1]
                },
                'requirements': {'major': 'public'},
                'repeatable': True,
                'choices': [
                    {
                        'text': '신청한다.',
                        'effect': lambda: {'normalSubjectPoint': 100, 'fatigue': 10}
                    },
                    {
                        'text': '신청하지 않는다.',
                        'effect': lambda: {'fatigue': -10}
                    }
                ]
            },
            'self_directed_learning': {
                'title': '자기주도 체험학습!',
                'text': '친구들과 함께 떠나는 자기주도 체험학습시간이다! 무슨 역할을 맡을까?',
                'image': 'assets/imgs/events/self_directed_learning.png',
                'time_trigger': {
                    'week': 21,
                    'day': 1,
                    'hour': 9,
                    'grade_range': [2, 2]
                },
                'repeatable': True,
                'choices': [
                    {
                        'text': '팀장으로서 친구들을 이끌어주자',
                        'effect': lambda: {'responsibility': 10, 'fatigue': 10}
                    },
                    {
                        'text': '총무로서 팀의 기둥이 되어주자',
                        'effect': lambda: {'responsibility': 5}
                    },
                    {
                        'text': '팀원을 하자',
                        'effect': lambda: {'fatigue': -10}
                    }
                ]
            },
            'major_camp': {
                'title': '전공 캠프',
                'text': '전공 캠프에 참여하게 되었다. 어떤 활동을 할까?',
                'image': 'assets/imgs/events/major_camp.png',
                'time_trigger': {
                    'week': 29,
                    'day': 1,
                    'hour': 9
                },
                'repeatable': True,
                'choices': [
                    {
                        'text': '내가 하고 싶은 주제가 있다! 열심히 해볼까?',
                        'effect': lambda: {'majorSubjectPoint': 70, 'fame': 15, 'fatigue' : 10}
                    },
                    {
                        'text': '적당히 시간만 때워보자…',
                        'effect': lambda: {'fatigue' : -30}
                    }
                ]
            }
        },
        
        # 랜덤 이벤트
        'random_events': {
            'project_experience': {
                'title': '프로젝트 경험',
                'text': '이제 곧 취업을 해야하는데 어떤 프로젝트를 하는게 좋을까?',
                'image': 'assets/imgs/events/project_experience.png',
                'probability': 0.4,
                'repeatable': True,
                'requirements': {'major': 'developer'},
                'time_trigger': {
                    'week': [20, 30],
                    'day': [1, 5],
                    'hour': [9, 21],
                    'grade_range': [2, 2]  # 2학년에만 발생
                },
                'choices': [
                    {
                        'text': '개인 프로젝트에 집중한다.',
                        'effect': lambda: {'majorSubjectPoint': 20, 'responsibility': 8, 'fatigue': 10}
                    },
                    {
                        'text': '팀 프로젝트를 진행한다.',
                        'effect': lambda: {'majorSubjectPoint': 15, 'responsibility': 5, 'fame': 5, 'fatigue': 15}
                    },
                    {
                        'text': '외부 공모전에 참여한다.',
                        'effect': lambda: {'majorSubjectPoint': 20, 'responsibility': 10, 'fame': 8, 'fatigue': 20}
                    }
                ]
            },
            'stay_after_school': {
                'title': '학교 - 잔류',
                'text': '금요일 오후 4시 20분, 학교에 남아서 공부할까요?',
                'image': 'assets/imgs/events/stay_after_school.png',
                'probability': 0.8,
                'repeatable': True,
                'requirements': {'major': 'functional'},
                'time_trigger': {
                    'day': 5,           # 금요일
                    'hour': [16, 16]    # 오후 4시
                },
                'choices': [
                    {
                        'text': '한다',
                        'effect': lambda: {'functionalCompetition': 40, 'fatigue': 10}
                    },
                    {
                        'text': '안 한다',
                        'effect': lambda: {'fatigue': -10}
                    }
                ]
            },
            'principal_recommendation': {
                'title': '학교장 추천서',
                'text': '"00아 너 성적이 좋더라, ~~기업 추천서 넣어줄테니까 한번 해볼래?" 선생님께서 나에게 ~~기업 추천서를 써주시겠다고 여쭤보셨다..! ~~기업은 복지가 좋기로 유명하다 한번 해볼까?',
                'probability': 0.3,
                'repeatable': False,
                'requirements': {'fame': 70},
                'time_trigger': {
                    'week': [20, 30],
                    'grade_range': [3, 3]
                },
                'choices': [
                    {
                        'text': '추천서를 받는다.',
                        'effect': lambda: {'fame': 20, 'responsibility': 10, 'fatigue': 5}
                    },
                    {
                        'text': '신청하지 않는다.',
                        'effect': lambda: {'fatigue': -10}
                    }
                ]
            },
            'idea_festival_team': {
                'title': '아이디어 페스티벌 - 팀원 관리',
                'text': '아이디어 페스티벌 기간, 팀원이 할 일을 미룬다. 어떻게 할까?',
                'image': 'assets/imgs/events/idea_festival_team.png',
                'probability': 0.4,
                'repeatable': True,
                'time_trigger': {
                    'week': [10, 28],
                    'day': [1, 5],
                    'hour': [9, 21]
                },
                'choices': [
                    {
                        'text': '내 일이 아니니 신경을 끈다.',
                        'effect': lambda: {'evil': 10}
                    },
                    {
                        'text': '옆에서 하라고 독촉한다.',
                        'effect': lambda: {'good': 10, 'responsibility' : 5, 'fatigue' : 5}
                    },
                    {
                        'text': '하 어쩔수 없지.. 그냥 내가 한다.',
                        'effect': lambda: {'majorSubjectPoint': 30, 'evil': 10, 'fatigue': 10, 'responsibility': 8}
                    }
                ]
            },
            'certification_exam': {
                'title': '자격증 시험',
                'text': '자격증 시험을 볼 기회가 생겼습니다.',
                'image': 'assets/imgs/events/certification_exam.png',
                'probability': 0.02,
                'repeatable': True,
                'time_trigger': {
                    'week': [1, 30],
                    'day': [1, 5],
                    'hour': [9, 18]
                },
                'choices': [
                    {
                        'text': '시험 보기',
                        'effect': lambda: {'majorSubjectPoint': 20, 'fatigue': 10}
                    },
                    {
                        'text': '시험 안 보기',
                        'effect': lambda: {'fatigue' : -20}
                    },
                    {
                        'text': '더 준비하기',
                        'effect': lambda: {'majorSubjectPoint': 30, 'fatigue': 20}
                    }
                ]
            },
            'study_time': {
                'title': '학교 - 자습',
                'text': '2학년이 되면서 자습 시간이 늘어났다. 무엇을 하면 좋을까?',
                'probability': 0.6,
                'repeatable': True,
                'time_trigger': {
                    'week': [5, 25],
                    'day': [1, 5],
                    'hour': [16, 21]
                },
                'choices': {
                    'developer': [
                        {
                            'text': '프론트엔드 공부를 한다.',
                            'effect': lambda: {'intuitivePoint': 50, 'majorSubjectPoint': 5, 'fatigue': 10}
                        },
                        {
                            'text': '백엔드 공부를 한다.',
                            'effect': lambda: {'interpretPoint': 50, 'majorSubjectPoint': 5, 'fatigue': 10}
                        },
                        {
                            'text': '개인 프로젝트를 한다.',
                            'effect': lambda: {'majorSubjectPoint': 40, 'responsibility': 20, 'fatigue': 15}
                        }
                    ],
                    'functional': [
                        {
                            'text': '기능 대회 준비를 한다.',
                            'effect': lambda: {'functionalCompetition': 50, 'fatigue': 15}
                        },
                        {
                            'text': '일반 전공도 공부한다.',
                            'effect': lambda: {'majorSubjectPoint': 30, 'fatigue': 10}
                        }
                    ],
                    'public': [
                        {
                            'text': '공기업 시험 공부를 한다.',
                            'effect': lambda: {'normalSubjectPoint': 50, 'fatigue': 10}
                        },
                        {
                            'text': '개발 공부도 병행한다.',
                            'effect': lambda: {'normalSubjectPoint': 30, 'majorSubjectPoint': 20, 'fatigue': 15}
                        }
                    ]
                }
            },
            'devfestival_conference': {
                'title': 'DevFestival 컨퍼런스 참여',
                'text': 'DevFestival 컨퍼런스 발표자를 모집한다. 참여해볼까?',
                'image': 'assets/imgs/events/devfestival_conference.png',
                'probability': 0.3,
                'repeatable': True,
                'time_trigger': {
                    'week': 8,
                    'day': [1, 5],
                    'hour': [9, 21],
                    'grade_range': [2, 3]
                },
                'choices': [
                    {
                        'text': '도전해본다',
                        'effect': lambda: {'fame': 10, 'responsibility': 10, 'fatigue': 15}
                    },
                    {
                        'text': '좀 부담스럽다',
                        'effect': lambda: None
                    }
                ]
            },
            'lecture_attendance': {
                'title': '강의',
                'text': '학교에서 강의 공지가 올라왔다! 참여해볼까?',
                'image': 'assets/imgs/events/lecture_attendance.png',
                'probability': 0.4,
                'repeatable': True,
                'time_trigger': {
                    'week': [5, 30],
                    'day': [1, 5],
                    'hour': [9, 21]
                },
                'choices': {
                    'developer': [
                        {
                            'text': '전공 공부 특강이 재밌어 보인다!',
                            'effect': lambda: {'majorSubjectPoint': 20}
                        }
                    ],
                    'functional': [
                        {
                            'text': '기능 대회 준비 특강이 재밌어 보인다!',
                            'effect': lambda: {'functionalCompetition': 20}
                        }
                    ],
                    'public': [
                        {
                            'text': '공기업 특강이 재밌어 보인다!',
                            'effect': lambda: {'normalSubjectPoint': 20}
                        }
                    ]
                }
            },
            'dormitory_ramen': {
                'title': '기숙사 - 라면',
                'text': '기숙사에서 친구가 같이 기숙사 금지 항목인 라면을 먹자고 꼬신다! 어떻게 대처해야 할까?',
                'image': 'assets/imgs/events/dormitory_ramen.png',
                'probability': 0.3,
                'repeatable': True,
                'time_trigger': {
                    'week': [1, 30],
                    'day': [1, 5],
                    'hour': [21, 1]  # 자정을 걸치는 경우
                },
                'choices': [
                    {
                        'text': '같이 먹는다.',
                        'effect': lambda: {'evil': 5, 'fame': -10, 'fatigue' : -100}
                    },
                    {
                        'text': '못 본 척 해준다.',
                        'effect': lambda: {'fame': 10}
                    },
                    {
                        'text': '기자위한테 알린다.',
                        'effect': lambda: {'fame': -5, 'responsibility' : 10}
                    }
                ]
            },
            'dormitory_study_room': {
                'title': '기숙사 - 자습실',
                'text': '기숙사에 도착했다! 피곤하긴 하지만 자습실을 사용할까 고민이 된다.',
                'image': 'assets/imgs/events/dormitory_study_room.png',
                'probability': 0.5,
                'repeatable': True,
                'time_trigger': {
                    'hour': [21, 23]
                },
                'choices': {
                    'developer' : [
                        {
                            'text': '자습실을 사용한다.',
                            'effect': lambda: {'majorSubjectPoint': 30, 'fatigue': 10, 'fame': 5}
                        },
                        {
                            'text': '자습실을 사용하지 않는다.',
                            'effect': lambda: None
                        },
                        {
                            'text': '호실에서 공부한다.',
                            'effect': lambda: {'majorSubjectPoint': 20}
                        }
                    ],
                    'functional' : [
                        {
                            'text': '자습실을 사용한다.',
                            'effect': lambda: {'functionalCompetition': 30, 'fatigue': 10, 'fame': 5}
                        },
                        {
                            'text': '자습실을 사용하지 않는다.',
                            'effect': lambda: None
                        },
                        {
                            'text': '호실에서 공부한다.',
                            'effect': lambda: {'functionalCompetition': 20}
                        }
                    ],
                    'public' : [
                        {
                            'text': '자습실을 사용한다.',
                            'effect': lambda: {'normalSubjectPoint': 30, 'fatigue': 10, 'fame': 5}
                        },
                        {
                            'text': '자습실을 사용하지 않는다.',
                            'effect': lambda: None
                        },
                        {
                            'text': '호실에서 공부한다.',
                            'effect': lambda: {'normalSubjectPoint': 20}
                        }
                    ]
                }
            }
        }
    } 