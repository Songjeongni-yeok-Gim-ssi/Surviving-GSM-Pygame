import pygame
import pygame_gui
from pygame.locals import *
from settings import *
from gameTimeManager import GameTimeManager
from selectPaper import SelectPaper

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
            
            # 시간 관리자 초기화
            self.time_manager = GameTimeManager()
            
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
        
        # 게임 화면용 UI 패널 (더 큰 크기로 조정)
        self.game_ui_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(50, 50, 400, 280),
            manager=self.manager,
            object_id='#game_ui_panel'
        )
        
        # 게임 상태 라벨들
        self.time_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 380, 30),
            text='1학년 1주차 월요일 오전 09:00',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        self.progress_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 45, 380, 25),
            text='전체 진행도: 0.0% | 학년 진행도: 2.0%',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        self.health_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 75, 280, 30),
            text='체력: 100/100',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        self.money_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 105, 280, 30),
            text='돈: 10,000원',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        # 시간 속도 조절 섹션
        self.time_speed_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 140, 100, 25),
            text='시간 속도:',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        self.speed_1x_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(110, 140, 40, 25),
            text='1x',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        self.speed_2x_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(155, 140, 40, 25),
            text='2x',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        self.speed_5x_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(200, 140, 40, 25),
            text='5x',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        # 개발자 도구 섹션
        self.dev_tools_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 175, 100, 25),
            text='개발자 도구:',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        self.skip_year_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(110, 175, 80, 25),
            text='학년 스킵',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        self.reset_time_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(195, 175, 80, 25),
            text='시간 리셋',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        # 졸업 상태 라벨
        self.graduation_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 210, 380, 30),
            text='',
            manager=self.manager,
            container=self.game_ui_panel
        )
        self.graduation_label.hide()  # 처음에는 숨김
        
        # 선택지 버튼들
        self.choice_button1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(SCREEN_WIDTH//2 - 150, 500, 300, 50),
            text='기숙사 가기',
            manager=self.manager
        )
        
        self.choice_button2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(SCREEN_WIDTH//2 - 150, 560, 300, 50),
            text='공부하기',
            manager=self.manager
        )
        
        # 메인 메뉴로 돌아가기 버튼
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(10, SCREEN_HEIGHT - 60, 100, 50),
            text='나가기',
            manager=self.manager
        )
        
        # 도움말 패널 추가 (마지막에 생성하여 최상위에 표시)
        self.help_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(SCREEN_WIDTH//2 - 300, SCREEN_HEIGHT//2 - 200, 600, 400),
            manager=self.manager,
            object_id='#help_panel'
        )
        
        # 도움말 텍스트
        help_text = "당신은 현재 광주 소프트웨어 마이스터 고등학교에 입학한 학생 중 한 명입니다. 당신의 일과는 7:00 A.M ~ 10:00 P.M까지 학교에서 공부하며 남은 시간은 기숙사에서 공부나 휴식을 하는 것입니다. 당신의 목표는 취업. 어떤 전공을 선택하든 자유입니다! 그럼 행운을 빕니다!"
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
        
        # 예제 SelectPaper용 버튼 생성 (SelectPaper 패널 내부에 생성)
        self.paper_ok_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(0, 0, 150, 50),  # 임시 위치, SelectPaper에서 재조정됨
            text='확인',
            manager=self.manager
        )

        # 예제 SelectPaper 생성 (이미지는 첨부하신 이미지 사용)
        self.example_select_paper = SelectPaper(
            'assets/imgs/exit.png',  # 첨부하신 이미지를 여기에 저장했다고 가정
            'GSM에서 살아남기',
            '안녕하세요! GSM에서 살아남기 게임에 오신 것을 환영합니다.<br><br>이 게임에서는 GSM 학생으로서 3년간의 학교 생활을 경험하게 됩니다. 공부, 취업 준비, 그리고 다양한 선택지들이 여러분을 기다리고 있습니다.<br><br>시작하기 전에 도움말을 확인하시면 게임에 대해 더 자세히 알아볼 수 있습니다.',
            self.manager,
            self.paper_ok_button
        )
        
        # 처음에는 메인 메뉴만 보이게
        self.show_main_menu_ui()
        self.help_panel.hide()  # 도움말 패널은 처음에 숨김
        self.example_select_paper.panel.hide()  # SelectPaper는 처음에 숨김
        self.paper_ok_button.hide()  # 확인 버튼도 처음에 숨김

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
        self.choice_button1.hide()
        self.choice_button2.hide()
        self.back_button.hide()
        
        # SelectPaper 관련 UI 숨기기
        self.example_select_paper.panel.hide()
        self.paper_ok_button.hide()

    def show_main_menu_ui(self):
        '''
            메인 메뉴 UI를 보여주는 메서드
        '''
        self.hide_all_ui()
        self.title_label.show()
        self.start_button.show()
        self.help_button.show()
        self.exit_button.show()

    def show_game_ui(self):
        '''
            게임 UI를 보여주는 메서드
        '''
        self.hide_all_ui()
        self.game_ui_panel.show()
        self.choice_button1.show()
        self.choice_button2.show()
        self.back_button.show()
        self.example_select_paper.panel.show()  # SelectPaper 보이기
        self.paper_ok_button.show()  # 확인 버튼도 보이기

    def process_events(self):
        '''
            사용자의 Input을 토대로 이벤트를 발생시키는 메서드
        '''
        time_delta = self.clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            
            # pygame-gui 이벤트 처리
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    print("게임 시작!")
                    self.state = GameState.PLAYING
                    self.time_manager.reset()
                    self.show_game_ui()
                    self.example_select_paper.panel.show()  # SelectPaper 보이기
                    
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
                    
                elif event.ui_element == self.choice_button1:
                    print("기숙사로 이동!")
                    # 1시간 소모
                    self.time_manager.total_seconds += 60 * 60
                    
                elif event.ui_element == self.choice_button2:
                    print("공부하기 선택!")
                    # 3시간 소모
                    self.time_manager.total_seconds += 3 * 60 * 60
                
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
                
                # 개발자 도구 버튼들
                elif event.ui_element == self.skip_year_button:
                    if self.time_manager.skip_to_next_year():
                        print(f"학년 스킵 완료! 현재: {self.time_manager.current_year}학년")
                    else:
                        print("더 이상 스킵할 수 없습니다.")
                
                elif event.ui_element == self.reset_time_button:
                    print("시간 리셋!")
                    self.time_manager.reset()
                
                elif event.ui_element == self.paper_ok_button:
                    self.example_select_paper.close()
            
            # 기존 키보드 이벤트도 유지 (백업용)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # ESC로 메인 메뉴로 돌아가기
                    if self.state == GameState.PLAYING:
                        self.state = GameState.MAIN_MENU
                        self.time_manager.reset()  # ESC로 나갈 때도 시간 초기화
                        self.show_main_menu_ui()
                
                # 개발자 단축키
                elif event.key == K_F1:  # F1로 학년 스킵
                    if self.state == GameState.PLAYING:
                        self.time_manager.skip_to_next_year()
                        
                elif event.key == K_F2:  # F2로 시간 리셋
                    if self.state == GameState.PLAYING:
                        self.time_manager.reset()
            
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
        '''시간에 따른 게임 이벤트 처리'''
        time_info = self.time_manager.get_current_time_info()
        
        # 학년 변경 이벤트
        if hasattr(self, '_last_year'):
            if self._last_year != time_info['year'] and not time_info['is_graduated']:
                print(f"축하합니다! {time_info['year']}학년이 되었습니다!")
        self._last_year = time_info['year']
        
        # 졸업 이벤트
        if time_info['is_graduated'] and not hasattr(self, '_graduation_announced'):
            print("🎓 축하합니다! GSM을 졸업하셨습니다! 🎓")
            self._graduation_announced = True
    
    def update_game_ui(self):
        '''
            게임 UI를 현재 상태에 맞게 업데이트
        '''
        time_info = self.time_manager.get_current_time_info()
        
        # 시간 라벨 업데이트
        speed_info = f" ({self.time_manager.time_speed}x)"
        self.time_label.set_text(time_info['time_string'] + speed_info)
        
        # 진행도 라벨 업데이트
        progress = time_info['progress']
        progress_text = f"전체 진행도: {progress['total_progress']:.1f}% | 학년 진행도: {progress['year_progress']:.1f}%"
        self.progress_label.set_text(progress_text)
        
        # 졸업 상태 표시
        if time_info['is_graduated']:
            self.graduation_label.set_text("🎓 졸업 완료! 축하합니다! 🎓")
            self.graduation_label.show()
        else:
            self.graduation_label.hide()
        
        # 다른 UI 요소들도 필요에 따라 업데이트
        # self.health_label.set_text(f'체력: {current_health}/100')
        # self.money_label.set_text(f'돈: {current_money:,}원')

    def draw(self):
        '''
            정적인 화면을 출력하는 메서드
        '''
        if self.state == GameState.MAIN_MENU:
            # 메인 메뉴 배경 그라데이션
            for y in range(SCREEN_HEIGHT):
                color_ratio = y / SCREEN_HEIGHT
                r = int(20 + (50 * color_ratio))
                g = int(20 + (30 * color_ratio))
                b = int(40 + (60 * color_ratio))
                pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
        elif self.state == GameState.PLAYING:
            # 게임 화면 배경
            try:
                bg = pygame.image.load('assets/imgs/gsm_meister_highschool_cover.jpeg')
                bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screen.blit(bg, (0, 0))
            except:
                # 이미지가 없으면 학년에 따른 배경색
                time_info = self.time_manager.get_current_time_info()
                if time_info['is_graduated']:
                    self.screen.fill((255, 215, 0))  # 졸업 - 금색
                elif time_info['year'] == 1:
                    self.screen.fill((100, 149, 237))  # 1학년 - 파란색
                elif time_info['year'] == 2:
                    self.screen.fill((60, 179, 113))   # 2학년 - 초록색
                else:
                    self.screen.fill((220, 20, 60))    # 3학년 - 빨간색
            
            # 게임 스프라이트들 그리기
            self.all_sprites.draw(self.screen)
            
            # 졸업 축하 효과
            if self.time_manager.graduation_completed:
                # 간단한 축하 효과 (점점 깜빡이는 텍스트)
                import math
                alpha = int(127 + 127 * math.sin(pygame.time.get_ticks() * 0.01))
                congrat_surface = pygame.Surface((SCREEN_WIDTH, 100))
                congrat_surface.set_alpha(alpha)
                congrat_surface.fill((255, 255, 255))
                
                font = pygame.font.Font(None, 48)
                text = font.render("🎓 CONGRATULATIONS! 🎓", True, (255, 215, 0))
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 50))
                congrat_surface.blit(text, text_rect)
                self.screen.blit(congrat_surface, (0, SCREEN_HEIGHT//2 - 50))
        
        # UI 요소들 그리기 (중요!)
        self.manager.draw_ui(self.screen)
        pygame.display.flip()

    def run(self):
        '''
            게임 루프 메서드
        '''
        while self.running:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)