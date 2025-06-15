import pygame
import pygame_gui
from pygame.locals import QUIT
from study import *
from settings import *  # 설정 값 가져오기

class TechTree:
    def __init__(self, manager : pygame_gui.UIManager):
        self.panel = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)),
            starting_height=200,
            manager=manager,
            object_id="#tech_tree_panel"
        )
        
        self.buttons = [[]]
        
        for i in range(4):
            self.buttons.append([])
            for j in range(5):
                self.buttons[i].append(TechNode(manager, Subject(i), j, 100 * (j + 1), self.panel))
        
        self.hide()
                
    def hide(self):
        self.panel.hide()
        
    def show(self):
        self.panel.show()
        
class TechNode:
    def __init__(self, manager : pygame_gui.UIManager, subject : Subject, level, price, container : pygame_gui.elements.UIScrollingContainer, text):
        '''text는 공부하는 기술명을 넣습니다.'''
        self.button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((100 * level, 300 * subject.value), (100, 100)),
            text=price + subject.name,
            manager=manager,
            container=container,
            object_id=f"#{subject.name}_{level}"
        )
        
        if Study.studyList[subject.value][level]:
            self.button.text = "이미 공부함"
        
        self.text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((100 * level, 300 * subject.value + 100), (100, 100)),
            text=text,
            manager=manager,
            container=container,
            object_id=f"#{subject.name}_{level}_text"
        )