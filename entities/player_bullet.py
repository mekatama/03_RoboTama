import pyxel
from .particle import Particle          # 破壊時particle
from .particle_hit import ParticleHit   # 破壊時particle
from collision import get_tile_type, in_collision, push_back
from constants import TILE_SPIKE, TILE_WALL, TILE_ROAD

# 弾クラス
class PlayerBullet:
    #定数
    SHOT_SPEED_X = 4        # shot speed x
    SHOT_SPEED_Y = 4        # shot speed y
    # 弾を初期化してゲームに登録する
    def __init__(self, game, x, y, dir, dir2):
        self.game = game
        self.x = x
        self.y = y
        self.dir = dir      # 左右方向
        self.dir2 = dir2    # 上下方向
        self.life_time = 0  # 生存時間
        self.hit_area = (2, 2, 5, 5)  # 当たり判定領域

     # 弾にダメージを与える
    def add_damage(self):
        # パーティクル出す
        for i in range(10):
            self.game.particles.append(
                Particle(self.game, self.x + 4, self.y + 4)
            )
        # hitパーティクル出す
        self.game.particleHits.append(
            ParticleHit(self.game, self.x + 4, self.y + 4)
        )
        # 弾をリストから削除する
        if self in self.game.player_bullets:    # 自機の弾リストに登録されている時
            self.game.player_bullets.remove(self)

   # 弾を更新する
    def update(self):
        #生存時間カウント
        self.life_time += 1
        # 弾の座標を更新する
        self.x += PlayerBullet.SHOT_SPEED_X * self.dir
        self.y += PlayerBullet.SHOT_SPEED_Y * self.dir2
        
        """
        # 弾が画面外に出たら弾リストから登録を削除する
        if (self.x <= -8 or
            self.x >= pyxel.width or
            self.y <= -8 or
            self.y >= pyxel.height
        ):
            self.game.player_bullets.remove(self)
        """
        # タイルとの当たり判定
        for i in [1, 6]:
            for j in [1, 6]:
                x = self.x + j
                y = self.y + i
                tile_type = get_tile_type(x, y)
                if tile_type == TILE_ROAD:  # 滑走路に触れた時
                    self.add_damage()
                    return

                if tile_type == TILE_SPIKE:  # トゲ又に触れた時
                    self.add_damage()
                    return

                if tile_type == TILE_WALL:  # 壁に触れた時
                    self.add_damage()
                    return
    # 弾を描画する
    def draw(self):
        if self.dir2 == 0:
            pyxel.blt(self.x, self.y, 0, 0, 8, 8 * self.dir, 8, 0)
        elif self.dir2 == 1:
            pyxel.blt(self.x, self.y, 0, 0, 8, 8 * self.dir, 8, 0, rotate = 45)
        elif self.dir2 == -1:
            pyxel.blt(self.x, self.y, 0, 0, 8, 8 * self.dir, 8, 0, rotate = -45)

