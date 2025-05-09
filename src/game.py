import pygame
from pygame.locals import QUIT
from settings import *  # 설정 값 가져오기
from entity import Entity

class Game:
    '''
        Game 실행을 위한 Game 객체 입니다.
    '''
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # 화면 객체를 저장
        
        # 플레이어 엔티티 생성 및 추가
        self.all_sprites = pygame.sprite.Group() # 엔티티 그룹 생성
        self.player = Entity(100, 100, 50, 50, Color.RED.value)  # 빨간색 사각형
        self.all_sprites.add(self.player)


    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

    def update(self):
        # 게임 오브젝트 업데이트 로직을 여기에 추가합니다.
        
        # 모든 스프라이트 업데이트
        self.all_sprites.update()

    def draw(self):
        # 화면을 그리는 로직을 여기에 추가합니다.
        self.screen.fill(Color.BLACK.value)  # 배경색을 검정으로 설정
        
        # 추가적인 그리기 로직을 여기에 작성
        self.all_sprites.draw(self.screen)  # 모든 스프라이트 그리기
        
        pygame.display.flip()  # 화면 업데이트

    def run(self):
        while self.running:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)  # FPS 설정

