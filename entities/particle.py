import pyxel
import math

#■Particle
class Particle:
    def __init__(self, game, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.count = 0
        self.speed = 2.5    #速度
        self.aim = 0        #攻撃角度
        self.is_alive = True

    def update(self):
        #一定間隔で角度決定→消滅
        self.count += 1
        if self.count == 1:
            self.aim = pyxel.rndf(0, 2 * math.pi)
        if self.count >= 1 + pyxel.rndi(1, 20):
            self.is_alive = False
        #座標
        self.x += self.speed * math.cos(self.aim)
        self.y += self.speed * -math.sin(self.aim)

    def draw(self):
        pyxel.pset(self.x, self.y, 7)
