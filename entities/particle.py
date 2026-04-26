import pyxel
import math

#■Particle
class Particle:
    #定数
    START_RADIUS = 3    # 弾軌跡開始時の半径
    END_RADIUS = 1      # 弾軌跡終了時の半径
    START_RADIUS_EB = 1 # 敵破壊開始時の半径
    END_RADIUS_EB = 7   # 敵破壊終了時の半径

    def __init__(self, game, x, y, dir, type):
        self.x = x
        self.y = y
        self.dir = dir      # playerの方向
        self.type = type    # 0:全方位 1:弾軌跡 2:dash 3:walk 4:破片 5:hit 6:敵爆発 7:敵爆発(ランダム) 8:item取得
        self.timer = 0
        self.count = 0
        self.speed = 2.5    # 速度
        self.speed_walk = 1.5 #速度
        self.aim = 0        # 攻撃角度
        self.rot = 0        # 破片の回転
        self.vx = 1.5         # 放物線用
        self.vy = -2         # 放物線用
        self.gravity = 0.2  # 放物線用
        self.is_alive = True
        self.radius = Particle.START_RADIUS         # 弾軌跡の半径
        self.radiusEB = Particle.START_RADIUS_EB    # 爆発の半径

    def update(self):
        # 全方位
        if self.type == 0:
            #一定間隔で角度決定→消滅
            self.count += 1
            if self.count == 1:
                self.aim = pyxel.rndf(0, 2 * math.pi)
            if self.count >= 1 + pyxel.rndi(1, 20):
                self.is_alive = False
            #座標
            self.x += self.speed * math.cos(self.aim)
            self.y += self.speed * -math.sin(self.aim)
        # 弾の軌跡
        elif self.type == 1:
            # 半径を小さくする
            self.radius -= 0.3
            # 半径が最小になったらエフェクトリストから登録を削除する
            if self.radius < Particle.END_RADIUS:
                 self.is_alive = False
        # dash
        elif self.type == 2:
            # dash方向の逆に表示
            self.count += 1
            if self.count == 1:
                if self.dir == -1:
                    self.aim = pyxel.rndf(0, 0.9)
                elif self.dir == 1:
                    self.aim = pyxel.rndf(2.2, 3.1)
            if self.count >= 1 + pyxel.rndi(1, 20):
                self.is_alive = False
            #座標
            self.x += self.speed * math.cos(self.aim)
            self.y += self.speed * -math.sin(self.aim)
        # walk
        elif self.type == 3:
            # walkに合わせて表示
            self.count += 1
            if self.count == 1:
                if self.dir == -1:
                    self.aim = pyxel.rndf(0, 0.9)
                elif self.dir == 1:
                    self.aim = pyxel.rndf(2.2, 3.1)
            if self.count >= 1 + pyxel.rndi(1, 5):
                self.is_alive = False
            #座標
            self.x += self.speed_walk * math.cos(self.aim)
            self.y += self.speed_walk * -math.sin(self.aim)
        # 破片
        elif self.type == 4:
            if self.count == 0:
                self.rnd_x = pyxel.rndf(-1, 1)
                self.rnd_y = pyxel.rndf(-1, 1)
            self.count += 1
            self.vy += self.gravity
            #座標
            self.x += (self.vx + self.rnd_x) * self.dir
            self.y += (self.vy + self.rnd_y)
            if self.count > 25 + pyxel.rndi(-5, 5):
                self.is_alive = False
        # hit
        elif self.type == 5:
            self.count += 1
            if self.count >= 5:
                self.is_alive = False
        # 敵爆発
        elif self.type == 6:
            self.count += 1
            # 半径を大きくする
            self.radius += 1
            # 半径が最大になったら爆発エフェクトリストから登録を削除する
            if self.radius > Particle.END_RADIUS_EB:
                self.is_alive = False
        # 敵爆発(ランダム)
        elif self.type == 7:
            if self.count == 0:
                #座標
                self.x += pyxel.rndi(-6, 6)
                self.y += pyxel.rndi(-6, 6)
            self.count += 1
            # 半径を大きくする
            self.radiusEB += 1
            # 半径が最大になったら爆発エフェクトリストから登録を削除する
            if self.radiusEB > Particle.END_RADIUS_EB + pyxel.rndi(-5, -2):
                self.is_alive = False
        # item取得
        elif self.type == 8:
            self.count += 1
            # 半径を大きくする
            self.radius += 1
            # 半径が最大になったら爆発エフェクトリストから登録を削除する
            if self.radius > Particle.END_RADIUS_EB:
                self.is_alive = False

    def draw(self):
        self.rot += 10
        if self.type == 0 or self.type == 2 or self.type == 3:
            pyxel.pset(self.x, self.y, 7)
        elif self.type == 1:
            pyxel.circ(self.x, self.y, self.radius, 7)
        elif self.type == 4:
            pyxel.blt(self.x, self.y, 0, 0, 8, 8 * self.dir , 8, 0, self.rot)
        elif self.type == 5:
            pyxel.circb(self.x, self.y, 2, 7)
        elif self.type == 6:
            pyxel.circ(self.x, self.y, self.radius, 7)
            pyxel.circb(self.x, self.y, self.radius, 9)
        elif self.type == 7:
            pyxel.circ(self.x, self.y, self.radius, 7)
            pyxel.circb(self.x, self.y, self.radius, 10)
        elif self.type == 8:
            pyxel.circb(self.x, self.y, self.radius, 10)

"""
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
"""