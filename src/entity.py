import pygame
from abc import abstractmethod

class Entity(pygame.sprite.Sprite):
    '''
      Entity 객체입니다.
    '''
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))  # 엔티티의 이미지(사각형)
        self.image.fill(color)  # 색상 설정
        self.rect = self.image.get_rect()  # 사각형의 위치와 크기
        self.rect.topleft = (x, y)  # 초기 위치 설정

    @abstractmethod
    def update(self):
        # 엔티티의 업데이트 로직 (예: 움직임)
        pass