import pygame
import pygame_gui
from pygame.locals import *
from settings import *

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
        
        # 게임 화면용 UI 패널 (반투명 배경)
        self.game_ui_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(50, 50, 300, 200),
            manager=self.manager,
            object_id='#game_ui_panel'
        )
        
        # 게임 상태 라벨들
        self.time_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 280, 30),
            text='시간: 오전 12:00',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        self.health_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 50, 280, 30),
            text='체력: 100/100',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        self.money_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 90, 280, 30),
            text='돈: 10,000원',
            manager=self.manager,
            container=self.game_ui_panel
        )
        
        # 선택지 버튼들
        self.choice_button1 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(SCREEN_WIDTH//2 - 150, 500, 300, 50),
            text='기숙사 가기',
            manager=self.manager
        )
        
        self.choice_button2 = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(SCREEN_WIDTH//2 - 150, 560, 300, 50),
            text='늦지 않게 공부하기',
            manager=self.manager
        )
        
        # 처음에는 메인 메뉴만 보이게
        self.show_main_menu_ui()

    def hide_all_ui(self):
        '''
            모든 UI 요소를 숨기는 메서드
        '''
        # 메인 메뉴 UI 숨기기
        self.title_label.hide()
        self.start_button.hide()
        self.help_button.hide()
        self.exit_button.hide()
        
        # 게임 UI 숨기기
        self.game_ui_panel.hide()
        self.choice_button1.hide()
        self.choice_button2.hide()

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
                    self.show_game_ui()
                    
                elif event.ui_element == self.help_button:
                    print("도움말 열기!")
                    # 도움말 화면 로직 추가 가능
                    
                elif event.ui_element == self.exit_button:
                    print("게임 종료!")
                    self.running = False
                    
                elif event.ui_element == self.choice_button1:
                    print("기숙사로 이동!")
                    # 선택지 1 처리
                    
                elif event.ui_element == self.choice_button2:
                    print("공부하기 선택!")
                    # 선택지 2 처리
            
            # 기존 키보드 이벤트도 유지 (백업용)
            elif self.state == GameState.MAIN_MENU and event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # ESC로 메인 메뉴로 돌아가기
                    if self.state == GameState.PLAYING:
                        self.state = GameState.MAIN_MENU
                        self.show_main_menu_ui()
            
            # UI 매니저에 이벤트 전달 (중요!)
            self.manager.process_events(event)
        
        # UI 매니저 업데이트 (중요!)
        self.manager.update(time_delta)

    def update(self):
        '''
            동적 객체를 표현하기 위한 메서드
        '''
        if self.state == GameState.PLAYING:
            self.all_sprites.update()
            # 게임 상태 업데이트 예시
            # self.update_game_stats()

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
                # 이미지가 없으면 단색 배경
                self.screen.fill(Color.BLUE.value)
            
            # 게임 스프라이트들 그리기
            self.all_sprites.draw(self.screen)
        
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