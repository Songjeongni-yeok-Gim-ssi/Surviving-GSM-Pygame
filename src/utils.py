import pygame

# 이미지 불러오는 함수
def load_image(filepath):
    '''
    지정된 파일 경로에서 이미지를 불러옵니다.    
    '''
    try:
        image = pygame.image.load(filepath)
        return image
    except pygame.error as e:
        print(f"이미지를 {filepath}로부터 로딩할 수 없습니다.: {e}")
        return None

# 충돌 확인하는 함수
def check_collision(rect1, rect2):
    '''
    두 직사각형이 충돌하는지 확인합니다.
    '''
    return rect1.colliderect(rect2)

# 소리 불러오는 함수
def load_sound(filepath):
    '''
    지정된 파일 경로에서 사운드를 불러옵니다.
    '''
    try:
        sound = pygame.mixer.Sound(filepath)
        return sound
    except pygame.error as e:
        print(f"사운드를 {filepath}로부터 로딩할 수 없습니다.: {e}")
        return None

# 표면에 글 나타내는 함수
def draw_text(surface, text, pos, font, color):
    ''' 
    주어진 표면에 텍스트를 그립니다.    
    '''
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)