import numpy as np

class Character:
    def __init__(self, width, height):
        self.appearance = 'circle'
        self.state = None
        self.position = np.array([width/2 - 12, height/2 - 12, width/2 + 12, height/2 + 12])
        #위치 판별을 위한 캐릭터 중앙 점 번지수 추가
        self.center = np.array([(self.position[0] + self.position[2]) / 2,(self.position[1] + self.position[3]) / 2])
        self.xy=np.array([(((self.position[0] + self.position[2]) / 2)-20)/25,(((self.position[1] + self.position[3]) / 2)-30)/25])
        self.outline = "#00FF80"

    def move(self, command = None):
        if command['move'] == False:
            self.state = None
            self.outline = "#00FF80" #초록색상 코드!
        
        else:
            self.state = 'move'
            self.outline = "#FF0000" #빨강색상 코드!

            if command['up_pressed']:
                if(self.position[1]>20):
                    self.position[1] -= 25
                    self.position[3] -= 25

            if command['down_pressed']:
                if(self.position[1]<150):
                    self.position[1] += 25
                    self.position[3] += 25

            if command['left_pressed']:
                if(self.position[0]>20):
                    self.position[0] -= 25
                    self.position[2] -= 25
                
            if command['right_pressed']:
                if(self.position[0]<150):
                    self.position[0] += 25
                    self.position[2] += 25
                
        #center update
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2]) 
        self.xy=np.array([(((self.position[0] + self.position[2]) / 2)-20)/25,(((self.position[1] + self.position[3]) / 2)-30)/25])