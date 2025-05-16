import pygame
from pygame.locals import QUIT
from settings import *  # 설정 값 가져오기
from entity import Entity

class Button:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    '''
        text는 버튼 위에 쓸 text를 입력, color는 평소 색, hilightColor는 마우스가 위에 있을 때의 색
    '''
    def __init__(self, x, y, width, height, text, color, hilightColor, textColor):
        self.button_color = color
        self.button_hilightColor = hilightColor
        self.text_color = textColor
        self.button = pygame.Rect(x, y, width, height)
        self.button_text = text
    
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
    
    