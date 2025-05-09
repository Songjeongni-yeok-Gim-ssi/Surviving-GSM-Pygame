import sys
import pygame
from settings import *  # 설정 값 가져오기
from game import Game

def main():
    pygame.init()
    pygame.display.set_caption("송정리역 김씨 | GSM에서 살아남기")  # 창 제목 설정
    
    game = Game()  # Game 객체 생성
    game.run()  # 게임 실행

if __name__ == "__main__":
    main()