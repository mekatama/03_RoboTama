import pyxel
from constants import GRAVITY, TERMINAL_VELOCITY

# 弾クラス
class Enemy_Bullet:
    #定数

    # 弾を初期化してゲームに登録する
    def __init__(self, game, x, y, dx, dy, dir, type):
        self.game = game
        self.x = x
        self.y = y
        self.dx = dx        # x方向の移動量
        self.dy = dy        # y方向の移動量
        self.dir = dir      # 敵の向き
        self.type = type    # 0:等速直進 1:放物線 2:等速直進(大)
        self.bullet_speed = 1.5           # 弾のspeed
        self.life_time = 0  # 生存時間
        self.hit_area = (2, 2, 5, 5)  # 当たり判定領域

     # 弾にダメージを与える
    def add_damage(self):
        # 弾をリストから削除する
        if self in self.game.enemy_bullets:    # 自機の弾リストに登録されている時
            self.game.enemy_bullets.remove(self)

   # 弾を更新する
    def update(self):
        #生存時間カウント
        self.life_time += 1
        # 0:等速直進
        if self.type == 0:
            # 位置を更新する
            self.x += self.dx * self.bullet_speed * self.dir
            self.y += self.dy * self.bullet_speed
        # 1:放物線
        elif self.type == 1:
             # 重力を加算して放物線にする
            self.dy = min(self.dy + GRAVITY, TERMINAL_VELOCITY)
            # 座標を更新
            self.x += self.dx * self.dir
            self.y += self.dy
        # 2:等速直進(大)
        if self.type == 2:
            # 当たり判定領域
            self.hit_area = (1, 1, 6, 6)
            # 位置を更新する
            self.x += self.dx * self.bullet_speed * self.dir
            self.y += self.dy * self.bullet_speed
       
    # 弾を描画する
    def draw(self):
        if self.type == 2:
            pyxel.blt(self.x, self.y, 0, 24, 16, 8, 8, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 16, 8, 8, 0)
