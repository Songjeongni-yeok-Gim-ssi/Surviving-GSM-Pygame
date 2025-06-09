import pygame
import pygame_gui
from pygame.locals import QUIT
from settings import *  # 설정 값 가져오기
from entity import Entity

class SelectPaper:
    def __init__(self, imagePath, title, text, manager : pygame_gui.UIManager, *buttons : pygame_gui.elements.UIButton):
        '''
            title은 이벤트 제목(html태그 없이 순수 문자열로), text는 이벤트 설명, manager는 UI를 draw하던 UIManager를 받는다., buttons는 이벤트의 선택지들을 설정, condition은 선택지가 뜨는 조건, imagePath는 이벤트 상황을 표현하는 그림의 경로
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
        
        # 이미지 크기 계산 (패널의 60% 너비, 40% 높이)
        image_width = panel_width * 0.6
        image_height = panel_height * 0.4
        image_x = (panel_width - image_width) / 2
        image_y = panel_height * 0.05  # 상단에서 5% 여백
        
        # 이미지 크기 조정
        image_surface = pygame.transform.scale(image_surface, (int(image_width), int(image_height)))
        
        # 이미지 UI 요소 생성
        self.image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((image_x, image_y), (image_width, image_height)),
            image_surface=image_surface,
            manager=manager,
            container=self.panel,
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
            container=self.panel,
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
            container=self.panel,
            object_id="#select_paper_text"
        )
        
        # 버튼 위치 계산 (텍스트 아래 5% 여백)
        button_y = text_y + text_height + panel_height * 0.05
        button_height = panel_height * 0.1
        button_width = panel_width * 0.3
        
        # 버튼들을 수평으로 배치
        for i, button in enumerate(buttons):
            button_x = (panel_width - (button_width * len(buttons))) / 2 + (button_width * i)
            button.relative_rect = pygame.Rect((button_x, button_y), (button_width, button_height))
            button.rebuild()
        
        self.manager = manager
        self.buttons = buttons
    
    def close(self):
        '''선택지를 선택하게 되면 반드시 호출 되어야 합니다.'''
        self.panel.kill()
        for button in self.buttons:
            button.kill()