from abc import ABC, abstractmethod
from statAndStatPoint import Stat
from settings import *
from enum import Enum
import pygame

class Subject(Enum):
    FrontEnd = 0
    BackEnd = 1
    PublicCor = 2
    FunctionClass = 3

class Study:
    '''공부 테크 트리를 관리하는 클래스 입니다.'''
    studyList = {{False, False, False, False, False}, {False, False, False, False, False}, {False, False, False, False, False}, {False, False, False, False, False}}
    '''이미 찍은 테크 트리인지 아직 찍지 않은 테크 트리인지 알려주는 역할을 합니다. (바깥 리스트는 과목, 내부 리스트는 레벨)'''
    
    def study(self, subject : Subject, level, price):
        '''subject는 과목, level은 해당 과목 테크 트리의 레벨 price는 해당 테크를 해제하는데 드는 비용'''
        if subject == Subject.FrontEnd:
            self.Front(subject, level, price)
        elif subject == Subject.BackEnd:
            self.Back(subject, level, price)
        elif subject == Subject.PublicCor:
            self.PublicCor(subject, level, price)
        elif subject == Subject.FunctionClass:
            self.Function(subject, level, price)
    
    def Front(self, subject : Subject, level, price):
        if price <= Stat.intuitivePoint + Stat.majorSubjectPoint:
            Stat.intuitivePoint = Stat.intuitivePoint - price
            if Stat.intuitivePoint < 0:
                Stat.majorSubjectPoint += Stat.intuitivePoint
                Stat.intuitivePoint = 0
            
            Study.studyList[subject][level] = True
            
        else:
            self.fail()
    
    def Back(self, subject : Subject, level, price):
        if price <= Stat.interpretPoint + Stat.majorSubjectPoint:
            Stat.interpretPoint = Stat.interpretPoint - price
            if Stat.interpretPoint < 0:
                Stat.majorSubjectPoint += Stat.interpretPoint
                Stat.interpretPoint = 0
            
            Study.studyList[subject][level] = True
        else:
            self.fail()
    
    def PublicCor(self, subject : Subject, level, price):
        if price <= Stat.normalSubjectPoint:
            Stat.normalSubjectPoint = Stat.normalSubjectPoint - price
            
            Study.studyList[subject][level] = True
        else:
            self.fail()
    
    def Function(self, subject : Subject, level, price):
        if price <= Stat.normalSubjectPoint:
            Stat.normalSubjectPoint = Stat.normalSubjectPoint - price
            
            Study.studyList[subject][level] = True
        else:
            self.fail()
    
    def fail(self):
        # 스탯 포인트가 부족합니다.
        pass