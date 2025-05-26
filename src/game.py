import pygame
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
            self.running = True
            self.clock = pygame.time.Clock()
            self.state = GameState.MAIN_MENU 
            self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
            self.all_sprites = pygame.sprite.Group()
            cls._init = True

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
            bg = pygame.image.load('assets/imgs/gsm_meister_highschool_cover.jpeg')
            bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            bg_rect = bg.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(bg, bg_rect)
            
            game_title = self.font.render("GSM에서 살아남기", True, Color.BLACK.value)
            game_title_rect = game_title.get_rect()
            game_title_rect.centerx = round(SCREEN_WIDTH / 2)
            game_title_rect.y = 300
            self.screen.blit(game_title, game_title_rect)
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

