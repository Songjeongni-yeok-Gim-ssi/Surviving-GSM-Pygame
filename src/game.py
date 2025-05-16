import pygame
from pygame.locals import *
from settings import *

class Game:
    '''
        Game 실행을 위한 Game 객체 입니다.
    '''
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.state = GameState.MAIN_MENU 
        self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

        # 실제 게임에서 사용할 변수들
        self.all_sprites = pygame.sprite.Group()

        
    def process_events(self):
        '''
            사용자의 Input을 토대로 이벤트를 발생시키는 메서드
        '''
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif self.state == GameState.MAIN_MENU and event.type == KEYDOWN:
                self.state = GameState.PLAYING

    def update(self):
        '''
            동적 객체를 표현하기 위한 메서드
        '''
        if self.state == GameState.PLAYING:
            self.all_sprites.update()

    def draw(self):
        '''
            정적인 화면을 출력하는 메서드
        '''
        if self.state == GameState.MAIN_MENU:
            self.screen.fill(Color.BLACK.value)
    
        elif self.state == GameState.PLAYING:
            self.screen.fill(Color.WHITE.value)
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

