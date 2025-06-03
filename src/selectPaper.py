import pygame
import pygame_gui
from pygame.locals import QUIT
from settings import *  # 설정 값 가져오기
from entity import Entity
from game import Game

class SelectPaper:
    def __init__(self, imagePath, title, text, manager : pygame_gui.UIManager, *buttons : pygame_gui.elements.UIButton):
        '''
            title은 이벤트 제목(html태크 없이 순수 문자열로), text는 이벤트 설명, uiManager는 UI를 draw하던 UIManager를 받는다., buttons는 이벤트의 선택지들을 설정, condition은 선택지가 뜨는 조건, imagePath는 이벤트 상황을 표현하는 그림의 경로
        '''
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.width = SCREEN_WIDTH / 1.3
        self.height = SCREEN_HEIGHT / 1.3
        image_rect = pygame.image.load(imagePath).convert_alpha()
        
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((self.x, self.y), (self.width, self.height)),
            starting_height=1,
            manager=manager,
            object_id="#select_paper_panel"
        )
        
        self.image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((self.x, self.y / 2), (self.width / 1.1, self.height / 3)),
            image_surface=image_rect,
            manager=manager,
            container=self.panel,
            object_id="#select_paper_image"
        )
        
        self.title = pygame_gui.elements.UITextBox(
            html_text=f"<h1>{title}</h1>",
            relative_rect=pygame.Rect((self.x, self.y), (self.width, self.width / 10)),
            manager=manager,
            container=self.panel,
            object_id="#select_paper_title"
        )
        
        self.text = pygame_gui.elements.UITextBox(
            html_text=text,
            relative_rect=pygame.Rect((self.x, self.y + 50 + (self.height / 4 - 50)), (self.width, self.height / 2 - 50)),
            manager=manager,
            container=self.panel,
            object_id="#select_paper_text"
        )
        
        self.manager = manager
        self.buttons = buttons
        self.gameInstance = Game()
    
    def kill(self):
        self.panel.kill()
        for button in self.buttons:
            button.kill()