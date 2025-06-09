import pygame
import pygame_gui
from pygame.locals import QUIT
from settings import *  # 설정 값 가져오기
from entity import Entity

class SelectPaper:
    def __init__(self, imagePath, title, text, manager : pygame_gui.UIManager, *buttonTexts : str):
        '''
            title은 이벤트 제목(html태그 없이 순수 문자열로), text는 이벤트 설명, manager는 UI를 draw하던 UIManager를 받는다., buttonTexts는 이벤트의 선택지 내용을 설정, condition은 선택지가 뜨는 조건, imagePath는 이벤트 상황을 표현하는 그림의 경로
        '''
        # 패널 크기와 위치 계산
        panel_width = SCREEN_WIDTH * 0.8
        panel_height = SCREEN_HEIGHT * 0.8
        panel_x = (SCREEN_WIDTH - panel_width) / 2
        panel_y = (SCREEN_HEIGHT - panel_height) / 2
        
        # 이미지 로드
        image_surface = pygame.image.load(imagePath).convert_alpha()
        
        # 패널 생성
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((panel_x, panel_y), (panel_width, panel_height)),
            starting_height=10,  # z-index를 높게 설정하여 다른 UI 요소들을 가리도록 함
            manager=manager,
            object_id="#select_paper_panel"
        )
        
        self.scrollingContainer = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect((self.x, self.y), (self.width, self.height)),
            starting_height=2,
            manager=manager,
            object_id="#select_paper_panel"
        )
        
        self.image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((image_x, image_y), (image_width, image_height)),
            image_surface=image_surface,
            manager=manager,
            container=self.scrollingContainer,
            object_id="#select_paper_image"
        )
        
        # 제목 위치 계산 (이미지 아래 5% 여백)
        title_y = image_y + image_height + panel_height * 0.05
        title_height = panel_height * 0.1
        
        # 제목 UI 요소 생성
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, title_y), (panel_width, title_height)),
            text=title,
            manager=manager,
            container=self.scrollingContainer,
            object_id="#select_paper_title"
        )
        
        # 텍스트 위치 계산 (제목 아래 5% 여백)
        text_y = title_y + title_height + panel_height * 0.05
        text_height = panel_height * 0.3
        
        # 텍스트 UI 요소 생성
        self.text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((0, text_y), (panel_width, text_height)),
            html_text=text,
            manager=manager,
            container=self.scrollingContainer,
            object_id="#select_paper_text"
        )
        
        self.buttons = []
        
        for i in range(buttonTexts.__len__()):
            self.buttons.append(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((0, self.y * 8 + (self.width / 10 + 10) * i), (self.width, self.width / 10)),
                text=buttonTexts[i],
                manager=manager,
                container=self.scrollingContainer,
                object_id="#select_paper_button_group"
            ))
        
        self.scrollingContainer.set_scrollable_area_dimensions((self.width - 20, self.y * 8 + (self.width / 10 + 10) * buttonTexts.__len__()))
        
        self.manager = manager
    
    def close(self):
        '''선택지를 선택하게 되면 반드시 호출 되어야 합니다.'''
        self.panel.kill()
        for button in self.buttons:
            button.kill()