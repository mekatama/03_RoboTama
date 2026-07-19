import pyxel
from .particle import Particle  # particle
from .ui_point import Ui_Point  # particle

# アイテムクラス
class Item:
    #定数
    LIFE_TIME = 60          # 生存時間
    BULLED_NUM_TYPE2 = 10   # type2の残弾数

    # アイテムを初期化してゲームに登録する
    def __init__(self, game, x, y, type):
        self.game = game
        self.x = x
        self.y = y
        self.y_ini = y          # 生成時のy座標
        self.type = type        # 0:PowerUp 1:Point 
        self.life_time = 0
        self.is_alive = True
        self.hit_area = (0, 0, 7, 7)    # 当たり判定の領域

    # アイテムにダメージを与える
    def add_damage(self):
        if self.type == 0:
            # playerの設定変更
            self.game.player.type = 2
            self.game.player.bulletNum = Item.BULLED_NUM_TYPE2
        elif self.type == 1:
            # スコアを加算する
            # ■■■スコア計算未定■■■
            self.game.score += 10
            # スコア表示を生成する
            self.game.ui_points.append(
                Ui_Point(self.game, self.x + 4, self.y + 4, 11)
            )

        # 取得エフェクトを生成する
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
        if self.y - self.y_ini < 8:
            self.y += 2
        else:
            pass
        # 削除する
        if self.life_time >= Item.LIFE_TIME + 32:
            self.is_alive = False

    # アイテムを描画する
    def draw(self):
        # 4フレーム周期で0と1を交互に繰り返す
        u = pyxel.frame_count  // 6 % 2 * 1
        if self.life_time >= Item.LIFE_TIME:
            pyxel.blt(self.x, self.y, 0, 8, 16, 8, 8, 0, 0,  u)
        else:
            pyxel.blt(self.x, self.y, 0, 8, 16, 8, 8, 0)
