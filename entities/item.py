import pyxel
from .particle import Particle  # particle

# アイテムクラス
class Item:
    #定数
#    ADD_HP = 20     # playerHP回復量
    LIFE_TIME = 60  # 生存時間

    # アイテムを初期化してゲームに登録する
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.life_time = 0
        self.is_alive = True
        self.hit_area = (0, 0, 7, 7)    # 当たり判定の領域

    # アイテムにダメージを与える
    def add_damage(self):
#        self.game.player.hp += Item.ADD_HP
        # 爆発エフェクトを生成する
        self.game.particles.append(
            Particle(self.game, self.x + 4, self.y + 4, 0, 8)
        )
        # アイテムをリストから削除する
        if self in self.game.items:  # 爆弾リストに登録されている時
            self.game.items.remove(self)

    # アイテムを更新するgame.
    def update(self):
        #生存時間カウント
        self.life_time += 1
        # 座標を更新する
#        self.x += 2
#        self.y += 2
        # 削除する
        if self.life_time >= Item.LIFE_TIME + 32:
            self.is_alive = False

    # アイテムを描画する
    def draw(self):
        # 4フレーム周期で0と8を交互に繰り返す
        u = pyxel.frame_count  // 6 % 2 * 8
        if self.life_time >= Item.LIFE_TIME:
            pyxel.blt(self.x, self.y, 0, 0 + u, 40, 8, 8, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 40, 8, 8, 0)
