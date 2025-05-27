from abc import ABC, abstractmethod
from statAndStatPoint import Stat
from button import Button
from settings import *

class Study(Button, ABC):
    def __init__(self, x, y, width, height, text, color, hilightColor, buttonAction : function, textColor=Color.BLACK):
        super().__init__(x, y, width, height, text, color, hilightColor, buttonAction, textColor)
    
    @abstractmethod
    def study(self):
        pass
    
    def buy(self, prePoint, price) -> int:
        # 능력치 수정 후 버튼 색 어둡게 물들이고 text내용을 "품절" 로 바꾸기
        return prePoint - price
    
    def fail(self):
        # 스텟 포인트가 부족합니다.
        pass

class FrontStudy(Study):
    def __init__(self, price):
        self.price = price
    
    def study(self):
        if self.price <= Stat.intuitivePoint + Stat.majorSubjectPoint:
            Stat.intuitivePoint = self.buy(Stat.intuitivePoint, self.price)
            if Stat.intuitivePoint < 0:
                Stat.majorSubjectPoint += Stat.intuitivePoint
                Stat.intuitivePoint = 0
        else:
            self.fail()