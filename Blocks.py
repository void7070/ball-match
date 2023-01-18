import numpy as np

class Blocks:
    def __init__(self, spawn_position,color_num):
        colors=["#00FF00","#0000FF","#FF0000","#FF00FF","#FFFF00","#D3D3D3","#FFFFFF"]
        self.appearance = 'circle'
        self.state = 'alive'
        self.position = np.array([spawn_position[0] - 10, spawn_position[1] - 10, spawn_position[0] + 10, spawn_position[1] + 10])
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#00FF00"
        self.num=color_num
        self.inline = colors[color_num]
    def setcolor(self,color_num):
        colors=["#00FF00","#0000FF","#FF0000","#FF00FF","#FFFF00","#D3D3D3","#FFFFFF"]
        self.num=color_num
        self.inline = colors[color_num]
        if(self.num!=6):
            self.state = 'alive'
        else:
            self.state = 'die'