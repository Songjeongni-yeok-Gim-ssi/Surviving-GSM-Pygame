class Stat:
    good = 0
    ''' 선 수치 (좋은 회사 취업 가능성에 영향) '''
    evil = 0
    ''' 악 수치 (나쁜 회사 취업 가능성에 영향) '''
    responsibility = 0
    ''' 책임감 (면접 성공률에 영향) '''
    intuitivePoint = 0    
    ''' 직관성 포인트 (프론트엔드 개발 능력) '''    
    interpretPoint = 0
    ''' 해석력 포인트 (백엔드 개발 능력) '''    
    majorSubjectPoint = 0
    ''' 전공 과목 포인트 (개발/기능반 취업, 면접에 영향) '''
    normalSubjectPoint = 0
    ''' 기타 과목 포인트 (공기업 취업에 영향) '''
    functionalCompetition = 0
    ''' 기능 대회 포인트 (기능반 취업의 핵심 요소) '''
    fame = 0
    ''' 평판 (팀 프로젝트 성공 확률에 영향) '''
    fatigue = 0
    ''' 피로도 (100이 되면 사망) '''
    major = None
    ''' 선택한 전공 '''
    gender = None
    ''' 성별 '''
    game_completed = False
    ''' 게임 종료 여부 '''
    employment_success = False
    ''' 취업 성공 여부 '''
    stat_points = 0
    ''' 스탯 포인트 (게임 재시작 시 사용) '''

    @classmethod
    def reset_stats(cls):
        """스탯 초기화"""
        cls.good = 0
        cls.evil = 0
        cls.responsibility = 0
        cls.intuitivePoint = 0
        cls.interpretPoint = 0
        cls.majorSubjectPoint = 0
        cls.normalSubjectPoint = 0
        cls.functionalCompetition = 0
        cls.fame = 0
        cls.fatigue = 0
        cls.major = None
        cls.gender = None
        cls.game_completed = False
        cls.employment_success = False
        cls.stat_points = 0

    @classmethod
    def show_stats(cls):
        """현재 스탯 상태를 보여주는 함수"""
        print("\n=== 현재 스탯 상태 ===")
        print(f"전공: {cls.major if cls.major else '미선택'}")
        print(f"성별: {cls.gender if cls.gender else '미선택'}")
        print("\n[기본 스탯]")
        print(f"선함: {cls.good}")
        print(f"악함: {cls.evil}")
        print(f"책임감: {cls.responsibility}")
        print(f"평판: {cls.fame}")
        print(f"피로도: {cls.fatigue}")
        
        print("\n[전공 관련 스탯]")
        print(f"직관성 (프론트엔드): {cls.intuitivePoint}")
        print(f"해석력 (백엔드): {cls.interpretPoint}")
        print(f"전공 과목: {cls.majorSubjectPoint}")
        print(f"일반 과목: {cls.normalSubjectPoint}")
        print(f"기능 대회: {cls.functionalCompetition}")
        
        print("\n[게임 상태]")
        print(f"스탯 포인트: {cls.stat_points}")
        print(f"게임 종료: {'예' if cls.game_completed else '아니오'}")
        print(f"취업 성공: {'예' if cls.employment_success else '아니오'}")
        print("==================\n")
    
    