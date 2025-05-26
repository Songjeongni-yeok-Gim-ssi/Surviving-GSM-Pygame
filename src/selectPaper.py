import pygame
from pygame.locals import QUIT
from settings import *  # 설정 값 가져오기
from entity import Entity
from button import Button
from game import Game

class SelectPaper(Entity):
    pause = False
    
    def __init__(self, imagePath, title, text, *buttons : Button, condition, x = SCREEN_WIDTH / 2, y = SCREEN_HEIGHT / 2, width = SCREEN_WIDTH / 1.3, height = SCREEN_HEIGHT / 1.3, color = Color.WHITE):
        '''
            title은 이벤트 제목, text는 이벤트 설명, buttons는 이벤트의 선택지들을 설정, condition은 SelectPaper가 뜨는 조건, imagePath는 이벤트 상황을 표현하는 그림의 경로
        '''
        super().__init__(x, y, width, height, color)
        self.x = x
        self.y = y
        self.image = pygame.image.load(imagePath)
        self.image = pygame.transform.scale(self.image, (width / 1.1, height / 3))
        self.title = title
        self.text = text
        self.buttons = buttons
        self.titleSurface = pygame.font.SysFont(None, bold=True, size=width / 10)
        self.textSurface = pygame.font.SysFont(None, bold=False, size=width / 15)
        self.condition = condition
        self.gameInstance = Game()
        self.gameInstance.all_sprites.add(self)
        for button in buttons:
            button.button_action += self.conditionToFalse
    
    def conditionToFalse(self):
        '''
            선택지에 뜬 버튼을 누를 시 확정적으로 호출될 함수
        '''
        self.condition = False
    
    def drawPaper(self):
        '''
            선택지 화면을 그리는 함수
        '''
        self.gameInstance.screen.blit(self.image, (self.x, self.y / 2))
        self.gameInstance.screen.blit(self.titleSurface, (self.x, self.y))
        self.gameInstance.screen.blit(self.textSurface, (self.x, self.y + 50))
        
        for button in self.buttons:
            button.drawButton()
    
    def update(self):
        if self.condition:
            SelectPaper.pause = True
            self.drawPaper()
        else:
            SelectPaper.pause = False
            self.gameInstance.all_sprites.remove(self)