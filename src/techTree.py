import pygame
import pygame_gui
from pygame.locals import QUIT
from study import *
from settings import *  # 설정 값 가져오기

class TechTree:
    tech_tree_list = [["HTML", "CSS", "JS", "REACT", "NEXT.JS"], ["JAVA", "SPRING", "MYSQL", "KOTLIN", "AWS"], ["학교 내신", "컴활", "한국사", "TOEIC", "NCS"], ["겜개", "로보틱스", "사보", "클라우드", "IT"]]
    
    def __init__(self, manager : pygame_gui.UIManager):
        self.backGround = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)),
            starting_height=200,
            manager=manager,
            object_id="#tech_tree_backGround"
        )
        
        self.panel = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)),
            manager=manager,
            container=self.backGround,
            object_id="#tech_tree_panel"
        )
        
        self.buttons = [[]]
        
        for i in range(4):
            self.buttons.append([])
            for j in range(5):
                self.buttons[i].append(TechNode(manager, Subject(i), j, 100 * (j + 1), self.panel, TechTree.tech_tree_list[i][j]))
        
        self.exitButton = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_WIDTH - 100, 0), (100, 100)),
            text="X",
            manager=manager,
            container=self.backGround,
            object_id="#study_exit_button"
        )
        
        self.panel.set_scrollable_area_dimensions((SCREEN_WIDTH - 20, 300 * len(self.buttons)))
        
        self.hide()
                
    def hide(self):
        self.backGround.hide()
        
    def show(self):
        self.backGround.show()
        
class TechNode:
    def __init__(self, manager : pygame_gui.UIManager, subject : Subject, level, price, container : pygame_gui.elements.UIScrollingContainer, text):
        '''text는 공부하는 기술명을 넣습니다.'''
        self.button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((150 * level, 300 * subject.value), (100, 100)),
            text=f"{price}{subject.name}",
            manager=manager,
            container=container,
            object_id=f"#{subject.name}_{level}"
        )
        
        if Study.studyList[subject.value][level]:
            self.button.set_text("이미 공부함")
        
        self.text = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((150 * level, 300 * subject.value + 100), (100, 100)),
            text=text,
            manager=manager,
            container=container,
            object_id=f"#{subject.name}_{level}_text"
        )
        
        self.subject = subject
        self.level = level
        self.price = price