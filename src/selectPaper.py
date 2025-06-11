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
        self.x = SCREEN_WIDTH / 8
        self.y = SCREEN_HEIGHT / 10
        self.width = SCREEN_WIDTH / 1.3
        self.height = SCREEN_HEIGHT / 1.3
        self.manager = manager  # manager 저장
        
        # 이미지 로드 및 1:1 비율 처리
        original_image = pygame.image.load(imagePath).convert_alpha()
        image_size = min(self.width / 1.1, self.height / 3) * 2  # 1:1 비율을 위한 크기 계산 (2배로 증가)
        image_surface = pygame.Surface((image_size, image_size), pygame.SRCALPHA)
        image_surface.fill((0, 0, 0, 0))  # 투명 배경
        
        # 이미지 크기 조정
        img_width, img_height = original_image.get_size()
        scale = min(image_size / img_width, image_size / img_height)
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        scaled_image = pygame.transform.smoothscale(original_image, (new_width, new_height))
        
        # 이미지를 중앙에 배치
        x_offset = (image_size - new_width) // 2
        y_offset = (image_size - new_height) // 2
        image_surface.blit(scaled_image, (x_offset, y_offset))
        
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((self.x, self.y), (self.width, self.height)),
            starting_height=100,
            manager=manager,
            object_id="#select_paper_panel"
        )
        
        self.scrollingContainer = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect((self.x, self.y), (self.width, self.height)),
            starting_height=101,
            manager=manager,
            object_id="#select_paper_panel"
        )
        
        self.image = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect((self.width/2 - image_size/2, self.y / 8), (image_size, image_size)),
            image_surface=image_surface,
            manager=manager,
            container=self.scrollingContainer,
            object_id="#select_paper_image"
        )
        
        self.title = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((-3, self.y / 8 + image_size + 20), (self.width, self.width / 10)),
            text=title,
            manager=manager,
            container=self.scrollingContainer,
            object_id="#select_paper_title"
        )
        
        self.text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((-3, self.y / 8 + image_size + self.width / 10 + 40), (self.width - 20, self.height / 2)),
            html_text=text,
            manager=self.manager,
            container=self.scrollingContainer,
            object_id="#select_paper_text"
        )
        
        self.buttons = []
        
        for i in range(buttonTexts.__len__()):
            self.buttons.append(pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((0, self.y / 8 + image_size + self.width / 10 + self.height / 2 + 60 + (self.width / 10 + 10) * i), (self.width, self.width / 10)),
                text=buttonTexts[i],
                manager=manager,
                container=self.scrollingContainer,
                object_id="#select_paper_button_group"
            ))
        
        self.scrollingContainer.set_scrollable_area_dimensions((self.width - 20, self.y / 8 + image_size + self.width / 10 + self.height / 2 + 60 + (self.width / 10 + 10) * buttonTexts.__len__()))
    
    def close(self):
        '''선택지를 선택하게 되면 반드시 호출 되어야 합니다.'''
        # 모든 UI 요소 정리
        self.panel.kill()
        self.scrollingContainer.kill()