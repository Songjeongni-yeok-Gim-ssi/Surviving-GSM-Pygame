from abc import ABC, abstractmethod
from statAndStatPoint import Stat
from button import Button
from settings import *

class Study(Button, ABC):
    def __init__(self, price, ability : function, x, y, width, height, text, color, hilightColor, buttonAction : function, textColor=Color.BLACK):
        super().__init__(x, y, width, height, text, color, hilightColor, buttonAction, textColor)
        self.ability = ability
        self.price = price
    
    @abstractmethod
    def study(self):
        pass
    
    def buy(self, prePoint) -> int:
        # 능력치 수정 후 버튼 색 어둡게 물들이고 text내용을 "품절" 로 바꾸기
        self.ability()
        return prePoint - self.price
    
    def fail(self):
        # 스텟 포인트가 부족합니다.
        pass

class FrontStudy(Study):
    def __init__(self, price, ability, x, y, width, height, text, color, hilightColor, buttonAction, textColor=Color.BLACK):
        super().__init__(price, ability, x, y, width, height, text, color, hilightColor, buttonAction, textColor)
    
    def study(self):
        if self.price <= Stat.intuitivePoint + Stat.majorSubjectPoint:
            Stat.intuitivePoint = self.buy(Stat.intuitivePoint)
            if Stat.intuitivePoint < 0:
                Stat.majorSubjectPoint += Stat.intuitivePoint
                Stat.intuitivePoint = 0
        else:
            self.fail()