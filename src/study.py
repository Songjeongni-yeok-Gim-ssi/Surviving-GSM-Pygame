from abc import ABC, abstractmethod
from statAndStatPoint import Stat
from settings import *
from enum import Enum
import pygame

class Subject(Enum):
    FE = 0
    BE = 1
    PC = 2
    FC = 3

class Study:
    '''공부 테크 트리를 관리하는 클래스 입니다.'''
    studyList = [[False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False], [False, False, False, False, False]]
    '''이미 찍은 테크 트리인지 아직 찍지 않은 테크 트리인지 알려주는 역할을 합니다. 이미 배운 공부한 내용(True)은 밝게 표시, 아직 공부하지 않은 내용(False)은 어둡게 표시 (바깥 리스트는 과목, 내부 리스트는 레벨)'''
    
    @classmethod
    def study(self, subject : Subject, level, price):
        '''subject는 과목, level은 해당 과목 테크 트리의 레벨 price는 해당 테크를 해제하는데 드는 비용'''
        if not Study.studyList[subject.value][level]:
            if subject == Subject.FE:
                self.Front(subject, level, price)
            elif subject == Subject.BE:
                self.Back(subject, level, price)
            elif subject == Subject.PC:
                self.PublicCor(subject, level, price)
            elif subject == Subject.FC:
                self.Function(subject, level, price)
    
    @classmethod
    def Front(self, subject : Subject, level, price):
        '''프론트엔드를 공부하는 함수'''
        if price <= Stat.intuitivePoint + Stat.majorSubjectPoint:
            Stat.intuitivePoint = Stat.intuitivePoint - price
            if Stat.intuitivePoint < 0:
                Stat.majorSubjectPoint += Stat.intuitivePoint
                Stat.intuitivePoint = 0
            
            Study.studyList[subject.value][level] = True
            from game import Game
            game = Game()
            game.techTree.buttons[subject.value][level].button.set_text("이미 공부함")
            
        else:
            self.fail()
    
    @classmethod
    def Back(self, subject : Subject, level, price):
        '''백엔드를 공부하는 함수'''
        if price <= Stat.interpretPoint + Stat.majorSubjectPoint:
            Stat.interpretPoint = Stat.interpretPoint - price
            if Stat.interpretPoint < 0:
                Stat.majorSubjectPoint += Stat.interpretPoint
                Stat.interpretPoint = 0
            
            Study.studyList[subject.value][level] = True
            from game import Game
            game = Game()
            game.techTree.buttons[subject.value][level].button.set_text("이미 공부함")
        else:
            self.fail()
    
    @classmethod
    def PublicCor(self, subject : Subject, level, price):
        '''공기업 쪽을 공부하는 함수'''
        if price <= Stat.normalSubjectPoint:
            Stat.normalSubjectPoint = Stat.normalSubjectPoint - price
            
            Study.studyList[subject.value][level] = True
            from game import Game
            game = Game()
            game.techTree.buttons[subject.value][level].button.set_text("이미 공부함")
        else:
            self.fail()
    
    @classmethod
    def Function(self, subject : Subject, level, price):
        '''기능반 쪽을 공부하는 함수'''
        if price <= Stat.normalSubjectPoint:
            Stat.normalSubjectPoint = Stat.normalSubjectPoint - price
            
            Study.studyList[subject.value][level] = True
            from game import Game
            game = Game()
            game.techTree.buttons[subject.value][level].button.set_text("이미 공부함")
        else:
            self.fail()
    
    @classmethod
    def fail(self):
        print("스탯 포인트가 부족합니다.")
        pass