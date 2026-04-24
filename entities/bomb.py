import pyxel
from collision import get_tile_type, in_collision, push_back
from constants import TILE_EXIT, TILE_GEM, TILE_BOMB, TILE_SPIKE, TILE_WALL, TILE_ROAD
from .particle import Particle          # 破壊時particle
from .particle_hit import ParticleHit   # 破壊時particle

# 爆弾クラス
class Bomb:
    #定数

    # 爆弾を初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.hit_area = (3, 0, 4, 7)    # 当たり判定の領域

    # 爆弾にダメージを与える
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
        # 爆弾をリストから削除する
        if self in self.game.player_bombs:  # 爆弾リストに登録されている時
            print("bom dead")
            self.game.player_bombs.remove(self)
            self.game.player.isBombGo = False

    # 爆弾を更新するgame.
    def update(self):
        #生存時間カウント
#        self.life_time += 1
        # 弾の座標を更新する
        if self.game.player.isBombGo == False:
            self.x = self.game.player.x
            self.y = self.game.player.y + 7
        else:
            self.y += 2
            # タイルとの当たり判定
            for i in [1, 6]:
                for j in [1, 6]:
                    x = self.x + j
                    y = self.y + i
                    tile_type = get_tile_type(x, y)

                    if tile_type == TILE_ROAD:  # 滑走路に触れた時
                        self.add_damage()
                        print("road")
                        return

                    if tile_type == TILE_SPIKE:  # トゲ又に触れた時
                        self.add_damage()
                        print("toge")
                        return

                    if tile_type == TILE_WALL:  # 壁に触れた時
                        self.add_damage()
                        print("wall")
                        return
    # 爆弾を描画する
    def draw(self):
        pyxel.blt(self.x, self.y, 1, 24, 0, 8, 8, 0)
