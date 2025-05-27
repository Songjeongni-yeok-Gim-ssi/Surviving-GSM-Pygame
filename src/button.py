import pygame
from pygame.locals import QUIT
from settings import *  # 설정 값 가져오기
from entity import Entity
from pygame.event import Event
from game import Game

class Button(Entity):
    buttonList = [] # 현재 생성된 버튼 객체가 들어있는 리스트
    
    def __init__(self, x, y, width, height, text, color, hilightColor, buttonAction : function, textColor = Color.BLACK):
        '''
        text는 버튼 위에 쓸 text를 입력, color는 평소 색, hilightColor는 마우스가 위에 있을 때의 색, buttonAction은 버튼을 눌렀을 때 실행할 함수 혹은 람다식
        '''
        self.isActive = True
        self.button_color = color
        self.button_hilightColor = hilightColor
        self.text_color = textColor
        self.button = pygame.Rect(x, y, width, height)
        self.button_text = text
        self.button_action = buttonAction
        self.gameInstance = Game()
        self.gameInstance.all_sprites.add(self)
        Button.buttonList.append(self)
    
    def drawButton(self):
        '''
        버튼을 그리는 함수
        '''
        if self.button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(Button.screen, self.button_hilightColor, self.button)
        else:
            pygame.draw.rect(Button.screen, self.button_color, self.button)

        # 텍스트 가운데 정렬
        text_rect = self.text.get_rect(center=self.button.center)
        self.gameInstance.screen.blit(self.text, text_rect)
    
    def excuteButton(self, event : Event):
        '''
        버튼 실행을 감지하는 함수
        '''
        if event.type == pygame.MOUSEBUTTONDOWN and self.button.collidepoint(event.pos):
            # 소리도 추가할 예정
            self.button_action()
    
    def deleteButton(self):
        '''
            버튼이 사라지게 하는 함수
        '''
        Button.buttonList.remove(self)
        self.gameInstance.all_sprites.remove(self)
    
    def clearButton(self):    
        '''
            버튼을 모두 사라지게 하는 함수
        '''
        for button in Button.buttonList:
            self.gameInstance.all_sprites.remove(button)
        Button.buttonList.clear()
    
    def getIndex(self):    
        '''
            버튼이 리스트 내에서 몇 번째 인덱스에 있는지를 반환하는 함수
        '''
        return Button.buttonList.index(self)

    def update(self):
        self.drawButton()
        for event in pygame.event.get():
            self.excuteButton(event)
