import sys
import pygame
from settings import *  # 설정 값 가져오기
from game import Game

def main():
    window_icon = pygame.image.load('assets/imgs/logo.png')
    
    pygame.init()
    pygame.display.set_caption("GSM에서 살아남기")  # 창 제목 설정
    pygame.display.set_icon(window_icon)
    
    game = Game()  # Game 객체 생성
    game.run()  # 게임 실행

if __name__ == "__main__":
    main()