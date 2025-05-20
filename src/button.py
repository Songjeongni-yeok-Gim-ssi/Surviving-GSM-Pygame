import pygame
from pygame.locals import QUIT
from settings import *  # 설정 값 가져오기
from entity import Entity

class Button:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    buttonList = [] # 현재 생성된 버튼 객체가 들어있는 리스트
    
    '''
        text는 버튼 위에 쓸 text를 입력, color는 평소 색, hilightColor는 마우스가 위에 있을 때의 색, buttonAction은 버튼을 눌렀을 때 실행할 함수 혹은 람다식
    '''
    def __init__(self, x, y, width, height, text, color, hilightColor, textColor, buttonAction):
        self.button_color = color
        self.button_hilightColor = hilightColor
        self.text_color = textColor
        self.button = pygame.Rect(x, y, width, height)
        self.button_text = text
        self.button_action = buttonAction
        Button.buttonList.append(self)
    
    '''
        버튼을 그리는 함수
    '''
    def drawButton(self):
        if self.button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(Button.screen, self.button_hilightColor, self.button)
        else:
            pygame.draw.rect(Button.screen, self.button_color, self.button)

        # 텍스트 가운데 정렬
        text_rect = self.text.get_rect(center=self.button.center)
        Button.screen.blit(self.text, text_rect)
    
    '''
        버튼 실행을 감지하는 함수
    '''
    def excuteButton(self, event, *args):
        if event.type == pygame.MOUSEBUTTONDOWN and self.button.collidepoint(event.pos):
            self.button_action(args)
    
    def deleteButton(self):
        Button.buttonList.remove(self)
