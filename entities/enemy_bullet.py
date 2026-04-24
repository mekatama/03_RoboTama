import pyxel

# 弾クラス
class Enemy_Bullet:
    #定数

    # 弾を初期化してゲームに登録する
    def __init__(self, game, x, y, dx, dy):
        self.game = game
        self.x = x
        self.y = y
        self.dx = dx    # x方向の移動量
        self.dy = dy    # y方向の移動量
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
        # 位置を更新する
        self.x += self.dx * self.bullet_speed
        self.y += self.dy * self.bullet_speed

    # 弾を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 16, 8, 8, 0)
