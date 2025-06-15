import pygame
import pygame_gui
from pygame.locals import *
from settings import *
from gameTimeManager import GameTimeManager
from selectPaper import SelectPaper
from events import EventManager
from statAndStatPoint import Stat
import math
from techTree import TechTree

class Game:
    '''
        Game 실행을 위한 Game 객체 입니다.
    '''
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):         
            cls._instance = super().__new__(cls) 
        return cls._instance       
    
    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            
            # 테마 파일과 함께 UI 매니저 생성
            self.manager = pygame_gui.UIManager(
                (SCREEN_WIDTH, SCREEN_HEIGHT),
                theme_path='theme.json'  # 테마 파일 경로
            )

            self.running = True
            self.clock = pygame.time.Clock()
            self.state = GameState.MAIN_MENU 
            self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
            self.all_sprites = pygame.sprite.Group()
            
            # 시간 매니저 초기화
            self.time_manager = GameTimeManager()
            
            # 이벤트 매니저 초기화
            self.event_manager = EventManager()
            
            # exit 이미지 로드
            self.exit_image = pygame.image.load('assets/imgs/exit.png')
            original_width, original_height = self.exit_image.get_size()
            scale_factor = 50 / original_height
            new_width = int(original_width * scale_factor)
            self.exit_image = pygame.transform.scale(self.exit_image, (new_width, 50))
            
            # UI 요소들 초기화
            self.init_ui_elements()
            cls._init = True

    def init_ui_elements(self):
        '''
            각 화면별 UI 요소들을 초기화하는 메서드
        '''
        # 메인 메뉴 제목 라벨 (특별한 ID로 스타일링)
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(SCREEN_WIDTH//2 - 200, 150, 400, 80),
            text='GSM에서 살아남기',
            manager=self.manager,
            object_id='#main_menu_title'  # 테마에서 정의한 ID
        )
        
        # 시작 버튼 (특별한 ID로 스타일링)
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(SCREEN_WIDTH//2 - 100, 300, 200, 60),
            text='시작',
            manager=self.manager,
            object_id='#start_button'  # 테마에서 정의한 ID
        )
        
        # 도움말 버튼 (특별한 ID로 스타일링)
        self.help_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(SCREEN_WIDTH//2 - 100, 380, 200, 60),
            text='도움말',
            manager=self.manager,
            object_id='#help_button'  # 테마에서 정의한 ID
        )
        
        # 게임 종료 버튼
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(SCREEN_WIDTH//2 - 100, 460, 200, 60),
            text='게임 종료',
            manager=self.manager
        )
        
        # 게임 화면용 UI 패널 (상단 중앙)
        self.game_ui_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(SCREEN_WIDTH//2 - 200, 20, 400, 100),
            manager=self.manager,
            object_id='#game_ui_panel'
        )
        
        # 시간 표시 라벨 (상단 중앙)
        self.time_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 380, 30),
            text='AM 09:00',
            manager=self.manager,
            container=self.game_ui_panel,
            object_id='#time_label'
        )
        
        # 날짜 표시 라벨 (시간 라벨 아래)
        self.date_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 45, 380, 30),
            text='1학년 1주차 월요일',
            manager=self.manager,
            container=self.game_ui_panel,
            object_id='#date_label'
        )
        
        # 좌상단 게임 컨트롤 패널
        self.control_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(20, 20, 300, 150),
            manager=self.manager,
            object_id='#control_panel'
        )
        
        # 게임 속도 조절 섹션
        self.speed_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 280, 25),
            text='게임 속도',
            manager=self.manager,
            container=self.control_panel
        )
        
        # 속도 조절 버튼들
        self.speed_1x_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 35, 60, 25),
            text='1x',
            manager=self.manager,
            container=self.control_panel
        )
        
        self.speed_2x_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(80, 35, 60, 25),
            text='2x',
            manager=self.manager,
            container=self.control_panel
        )
        
        self.speed_5x_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(150, 35, 60, 25),
            text='5x',
            manager=self.manager,
            container=self.control_panel
        )
        
        self.speed_50x_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(220, 35, 60, 25),
            text='50x',
            manager=self.manager,
            container=self.control_panel
        )
        
        # 개발자 도구 섹션
        self.dev_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 70, 280, 25),
            text='개발자 도구',
            manager=self.manager,
            container=self.control_panel
        )
        
        self.skip_year_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, 95, 135, 25),
            text='학년 스킵',
            manager=self.manager,
            container=self.control_panel
        )
        
        self.reset_time_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(155, 95, 135, 25),
            text='시간 리셋',
            manager=self.manager,
            container=self.control_panel
        )
        
        # 졸업 상태 라벨
        self.graduation_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 200, 380, 30),
            text='',
            manager=self.manager,
            container=self.game_ui_panel
        )
        self.graduation_label.hide()  # 처음에는 숨김
        
        # 메인 메뉴로 돌아가기 버튼
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, SCREEN_HEIGHT - 60, 100, 50),
            text='',
            manager=self.manager,
            object_id='#exit_button'  # 테마에서 정의한 ID
        )
        
        # 도움말 패널 추가 (마지막에 생성하여 최상위에 표시)
        self.help_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2 - 200, 600, 400),
            manager=self.manager,
            object_id='#help_panel'
        )
        
        # 도움말 텍스트
        help_text = "당신은 현재 광주 소프트웨어 마이스터 고등학교에 입학한 학생 중 한 명입니다. 당신의 일과는 7:00 A.M ~ 09:20 P.M까지 학교에서 공부하며 남은 시간은 기숙사에서 공부나 휴식을 하는 것입니다. 당신의 목표는 취업. 어떤 전공을 선택하든 자유입니다! 그럼 행운을 빕니다!"
        self.help_text_label = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(20, 20, 560, 300),
            html_text=help_text,
            manager=self.manager,
            container=self.help_panel,
            object_id='#help_text_box'  # 테마에서 정의한 ID
        )
        
        # 도움말 닫기 버튼
        self.help_close_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(250, 340, 100, 40),
            text='닫기',
            manager=self.manager,
            container=self.help_panel
        )
        
        # 스탯 패널 추가 (오른쪽)
        self.stat_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(SCREEN_WIDTH - 320, 20, 300, 500),
            manager=self.manager,
            object_id='#stat_panel'
        )
        
        # 스탯 제목
        self.stat_title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 280, 30),
            text='현재 스탯',
            manager=self.manager,
            container=self.stat_panel,
            object_id='#stat_title'
        )
        
        # 기본 스탯 라벨들
        self.major_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 50, 280, 25),
            text='전공: 미선택',
            manager=self.manager,
            container=self.stat_panel
        )
        
        self.gender_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 75, 280, 25),
            text='성별: 미선택',
            manager=self.manager,
            container=self.stat_panel
        )
        
        # 기본 스탯 섹션
        self.basic_stats_title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 110, 280, 25),
            text='[기본 스탯]',
            manager=self.manager,
            container=self.stat_panel
        )
        
        self.good_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 135, 280, 25),
            text='선함: 0',
            manager=self.manager,
            container=self.stat_panel
        )
        
        self.evil_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 160, 280, 25),
            text='악함: 0',
            manager=self.manager,
            container=self.stat_panel
        )
        
        self.responsibility_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 185, 280, 25),
            text='책임감: 0',
            manager=self.manager,
            container=self.stat_panel
        )
        
        self.fame_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 210, 280, 25),
            text='평판: 0',
            manager=self.manager,
            container=self.stat_panel
        )
        
        self.fatigue_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 235, 280, 25),
            text='피로도: 0',
            manager=self.manager,
            container=self.stat_panel
        )
        
        # 전공 관련 스탯 섹션
        self.major_stats_title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 270, 280, 25),
            text='[전공 관련 스탯]',
            manager=self.manager,
            container=self.stat_panel
        )
        
        self.intuitive_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 295, 280, 25),
            text='직관성 (프론트엔드): 0',
            manager=self.manager,
            container=self.stat_panel
        )
        
        self.interpret_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 320, 280, 25),
            text='해석력 (백엔드): 0',
            manager=self.manager,
            container=self.stat_panel
        )
        
        self.major_subject_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 345, 280, 25),
            text='전공 과목: 0',
            manager=self.manager,
            container=self.stat_panel
        )
        
        self.normal_subject_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 370, 280, 25),
            text='일반 과목: 0',
            manager=self.manager,
            container=self.stat_panel
        )
        
        self.functional_competition_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 395, 280, 25),
            text='기능 대회: 0',
            manager=self.manager,
            container=self.stat_panel
        )
        
        # 게임 상태 섹션
        self.game_status_title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 430, 280, 25),
            text='[게임 상태]',
            manager=self.manager,
            container=self.stat_panel
        )
        
        self.stat_points_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 455, 280, 25),
            text='스탯 포인트: 0',
            manager=self.manager,
            container=self.stat_panel
        )
        
        self.techTree = TechTree(self.manager)
        
        self.studyButton = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 600), (100, 100)),
            text="공부",
            manager=self.manager
        )
        
        # 처음에는 메인 메뉴만 보이게
        self.show_main_menu_ui()
        self.help_panel.hide()  # 도움말 패널은 처음에 숨김

    def hide_all_ui(self):
        '''
            모든 UI 요소를 숨기는 메서드
        '''
        # 메인 메뉴 UI 숨기기
        self.title_label.hide()
        self.start_button.hide()
        self.help_button.hide()
        self.exit_button.hide()
        
        # 도움말 패널 숨기기
        self.help_panel.hide()
        
        # 게임 UI 숨기기
        self.game_ui_panel.hide()
        self.back_button.hide()
        self.control_panel.hide()  # 컨트롤 패널도 숨기기
        self.stat_panel.hide()  # 스탯 패널도 숨기기
        
        self.studyButton.hide()

    def show_main_menu_ui(self):
        '''
            메인 메뉴 UI를 보여주는 메서드
        '''
        self.hide_all_ui()
        self.title_label.show()
        self.start_button.show()
        self.help_button.show()
        self.exit_button.show()
        self.control_panel.hide()  # 메인 메뉴에서는 컨트롤 패널 숨기기

    def show_game_ui(self):
        '''
            게임 UI를 보여주는 메서드
        '''
        self.hide_all_ui()
        self.game_ui_panel.show()
        self.back_button.show()
        self.control_panel.show()  # 게임 진행 중에만 컨트롤 패널 보이기
        self.stat_panel.show()  # 스탯 패널도 보이기
        self.studyButton.show()

    def process_events(self):
        '''
            사용자의 Input을 토대로 이벤트를 발생시키는 메서드
        '''
        time_delta = self.clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            
            # pygame-gui 버튼 이벤트 처리
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    print("게임 시작!")
                    self.state = GameState.PLAYING
                    self.time_manager.reset()  # 게임 시작 시 시간 초기화
                    self.show_game_ui()
                    
                elif event.ui_element == self.help_button:
                    print("도움말 열기!")
                    self.help_panel.show()
                    # 도움말이 열렸을 때 다른 버튼들 숨기기
                    self.start_button.hide()
                    self.help_button.hide()
                    self.exit_button.hide()
                    
                elif event.ui_element == self.help_close_button:
                    print("도움말 닫기!")
                    self.help_panel.hide()
                    # 도움말이 닫혔을 때 다른 버튼들 다시 보이기
                    if self.state == GameState.MAIN_MENU:
                        self.start_button.show()
                        self.help_button.show()
                        self.exit_button.show()
                    
                elif event.ui_element == self.exit_button:
                    print("게임 종료!")
                    self.running = False
                
                # SelectPaper 버튼 이벤트 처리
                elif hasattr(self, 'current_select_paper') and event.ui_element in self.current_select_paper.buttons:
                    button_index = self.current_select_paper.buttons.index(event.ui_element)
                    
                    # 전공 선택 처리
                    if hasattr(self, '_is_major_selection'):
                        self._handle_event_choice('major_selection', button_index)
                        delattr(self, '_is_major_selection')
                    
                    # 이벤트 선택 처리
                    elif hasattr(self, '_current_event'):
                        self._handle_event_choice(self._current_event, button_index)
                        delattr(self, '_current_event')
                    
                    # 선택지 닫기
                    self.current_select_paper.close()
                    delattr(self, 'current_select_paper')
                    self.time_manager.resume_time()  # 시간 다시 흐르게
                
                elif event.ui_element == self.back_button:
                    print("메인 메뉴로 돌아가기!")
                    self.state = GameState.MAIN_MENU
                    self.time_manager.reset()  # 메인 메뉴로 돌아갈 때 시간 초기화
                    self.show_main_menu_ui()
                
                # 시간 속도 조절 버튼들
                elif event.ui_element == self.speed_1x_button:
                    self.time_manager.set_time_speed(1.0)
                    print("시간 속도: 1배속")
                    
                elif event.ui_element == self.speed_2x_button:
                    self.time_manager.set_time_speed(2.0)
                    print("시간 속도: 2배속")
                    
                elif event.ui_element == self.speed_5x_button:
                    self.time_manager.set_time_speed(5.0)
                    print("시간 속도: 5배속")
                elif event.ui_element == self.speed_50x_button:
                    self.time_manager.set_time_speed(50.0)
                    print("시간 속도: 50배속")
                
                # 개발자 도구 버튼들
                elif event.ui_element == self.skip_year_button:
                    if self.time_manager.skip_to_next_year():
                        print(f"학년 스킵 완료! 현재: {self.time_manager.current_year}학년")
                    else:
                        print("더 이상 스킵할 수 없습니다.")
                
                elif event.ui_element == self.reset_time_button:
                    print("시간 리셋!")
                    self.time_manager.reset()
                
                elif event.ui_element == self.studyButton:
                    print("테크 트리 창 열기!")
                    self.techTree.show()
                    
                elif event.ui_element == self.techTree.exitButton:
                    print("테크 트리 창 닫기")
                    self.techTree.hide()
            
            # UI 매니저에 이벤트 전달 (중요!)
            self.manager.process_events(event)
        
        # UI 매니저 업데이트 (중요!)
        self.manager.update(time_delta)
        
        return time_delta

    def update(self):
        '''
            동적 객체를 표현하기 위한 메서드
        '''
        # 시간 델타 계산
        time_delta = self.clock.get_time() / 1000.0  # 밀리초를 초로 변환
        
        if self.state == GameState.PLAYING:
            # PLAYING 상태일 때만 게임 시간 업데이트
            self.time_manager.update(time_delta)
            
            # UI 업데이트
            self.update_game_ui()
            
            # 게임 오브젝트 업데이트
            self.all_sprites.update()
            
            # 시간에 따른 게임 로직
            self.handle_time_events()

    def handle_time_events(self):
        """
        시간 관련 이벤트 처리
        """
        # 이미 이벤트가 진행 중이면 새로운 이벤트를 체크하지 않음
        if hasattr(self, 'current_select_paper'):
            return
        
        # 시간 업데이트
        delta_time = self.clock.get_time() / 1000.0
        self.time_manager.update(delta_time)
        
        # 시간 정보 가져오기
        time_info = self.time_manager.get_current_time_info()
        
        # 이벤트 체크
        triggered_events = self.event_manager.check_time_triggered_events(time_info)
        
        # 고정 이벤트 우선 처리
        fixed_events = [event for event in triggered_events if event in self.event_manager.events['fixed_events']]
        if fixed_events:
            self._trigger_event(fixed_events[0], 'fixed')
            return
        
        # 고정 이벤트가 없는 경우에만 랜덤 이벤트 처리
        random_events = [event for event in triggered_events if event in self.event_manager.events['random_events']]
        if random_events:
            self._trigger_event(random_events[0], 'random')
            return

    def update_game_ui(self):
        """게임 UI 업데이트"""
        # 시간 정보 가져오기
        time_info = self.time_manager.get_current_time_info()
        
        # 시간 표시 업데이트
        current_hour = time_info['hour']
        am_pm = "오전" if current_hour < 12 else "오후"
        hour = current_hour if current_hour <= 12 else current_hour - 12
        if hour == 0:  # 0시는 12시로 표시
            hour = 12
        time_str = f"{am_pm} {hour:02d}:{time_info['minute']:02d}"
        self.time_label.set_text(time_str)
        
        # 날짜 라벨 업데이트 (학년 주차 요일)
        date_str = f"{time_info['year']}학년 {time_info['week']}주차 {time_info['day']}일"
        self.date_label.set_text(date_str)
        
        # 졸업 상태 업데이트
        if time_info['is_graduated']:
            self.graduation_label.set_text("축하합니다! 졸업하셨습니다!")
            self.graduation_label.show()
        else:
            self.graduation_label.hide()
            
        # 스탯 업데이트
        self.major_label.set_text(f'전공: {Stat.major if Stat.major else "미선택"}')
        self.gender_label.set_text(f'성별: {Stat.gender if Stat.gender else "미선택"}')
        
        # 기본 스탯 업데이트
        self.good_label.set_text(f'선함: {Stat.good}')
        self.evil_label.set_text(f'악함: {Stat.evil}')
        self.responsibility_label.set_text(f'책임감: {Stat.responsibility}')
        self.fame_label.set_text(f'평판: {Stat.fame}')
        self.fatigue_label.set_text(f'피로도: {Stat.fatigue}')
        
        # 전공 관련 스탯 업데이트
        self.intuitive_label.set_text(f'직관성 (프론트엔드): {Stat.intuitivePoint}')
        self.interpret_label.set_text(f'해석력 (백엔드): {Stat.interpretPoint}')
        self.major_subject_label.set_text(f'전공 과목: {Stat.majorSubjectPoint}')
        self.normal_subject_label.set_text(f'일반 과목: {Stat.normalSubjectPoint}')
        self.functional_competition_label.set_text(f'기능 대회: {Stat.functionalCompetition}')
        
        # 게임 상태 업데이트
        self.stat_points_label.set_text(f'스탯 포인트: {Stat.stat_points}')

    def draw(self):
        '''
            정적인 화면을 출력하는 메서드
        '''
        if self.state == GameState.MAIN_MENU or self.state == GameState.PLAYING:
            bg = pygame.image.load('assets/imgs/gsm_meister_highschool_cover.jpeg')
            bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(bg, (0, 0))
            
            # 게임 스프라이트들 그리기
            self.all_sprites.draw(self.screen)
            
            # exit 이미지 그리기
            self.screen.blit(self.exit_image, (10, SCREEN_HEIGHT - 60))
            
            # 졸업 축하 효과
            if self.time_manager.graduation_completed:
                # 간단한 축하 효과 (점점 깜빡이는 텍스트)
                alpha = int(127 + 127 * math.sin(pygame.time.get_ticks() * 0.01))
                congrat_surface = pygame.Surface((SCREEN_WIDTH, 100))
                congrat_surface.set_alpha(alpha)
                congrat_surface.fill((255, 255, 255))
                
                font = pygame.font.Font(FONT_NAME, 48)
                text = font.render("🎓 CONGRATULATIONS! 🎓", True, (255, 215, 0))
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 50))
                congrat_surface.blit(text, text_rect)
                self.screen.blit(congrat_surface, (0, SCREEN_HEIGHT//2 - 50))
        
        # UI 요소들 그리기 (중요!)
        self.manager.draw_ui(self.screen)
        pygame.display.flip()

    def _trigger_event(self, event_name, event_type):
        """
        고정/랜덤 이벤트로 SelectPaper 생성하는 메서드
        """
        print(f"\n[{event_type} 이벤트 트리거] {event_name} 이벤트를 트리거합니다.")
        
        # 이미 이벤트가 진행 중이면 새로운 이벤트를 발생시키지 않음
        if hasattr(self, 'current_select_paper'):
            print(f"[이벤트 중복] 이미 진행 중인 {event_name} 이벤트가 있습니다.")
            return
        
        # 이벤트 가져오기
        if event_type == 'fixed':
            event = self.event_manager.get_fixed_event(event_name)
        elif event_type == 'random':
            event = self.event_manager.get_random_event(event_name)
        
        if event:
            print(f"[{event_type} 선택지] {event_name} 이벤트의 선택지를 생성합니다.")
            self.time_manager.pause_time() # 이벤트 선택지 선택 전까지 시간 정지
            self._current_event = event_name
            
            # 선택지 텍스트 추출
            if isinstance(event['choices'], dict):
                # 전공에 따른 선택지 처리
                major_type = Stat.major
                choices = event['choices'].get(major_type, event['choices'])
                choice_texts = [choice['text'] for choice in choices]
            else:
                choices = event['choices']
                choice_texts = [choice['text'] for choice in choices]
            
            print(f"[선택지] {choice_texts}")
            
            try:
                # SelectPaper 생성
                self.current_select_paper = SelectPaper(
                    'assets/imgs/exit.png', # 이벤트에 이미지 추가 예정
                    event['title'],
                    event['text'],
                    self.manager,
                    *choice_texts
                )
                print("[SelectPaper] 생성 완료")
                print(f"{event}")
            except Exception as e:
                print(f"[에러] SelectPaper 생성 실패: {str(e)}")
            
            # 전공 선택 이벤트인 경우 플래그 설정
            if event_name == 'major_selection':
                self._is_major_selection = True

    def _handle_event_choice(self, event_name, choice_index):
        """
        이벤트 선택지 처리 -> 이벤트에서 선택한 선택지를 반영합니다.
        """
        print(f"\n[이벤트 선택] {event_name} 이벤트의 {choice_index}번 선택지를 처리합니다.")
        
        event = self.event_manager.get_fixed_event(event_name)
        if not event:
            event = self.event_manager.events['random_events'].get(event_name)
        
        if event and 'choices' in event:
            if isinstance(event['choices'], dict):
                major_type = Stat.major
                choices = event['choices'].get(major_type, event['choices'])
            else:
                choices = event['choices']
            
            if 0 <= choice_index < len(choices):
                choice = choices[choice_index]
                
                # 선택지 요구사항 체크
                if not self.event_manager.check_requirements(event, choice):
                    print("요구사항을 충족하지 못했습니다.")
                    return
                
                print(f"[선택지 효과] {choice['text']} 선택지의 효과를 적용합니다.")
                effect_result = choice['effect']()
                print(f"[선택지 효과 결과] {effect_result}")
                if effect_result is not None:
                    self.event_manager._apply_effects(effect_result)

    def run(self):
        '''
            게임 루프 메서드
        '''
        while self.running:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)