import pyxel
from collision import in_collision, push_back
from .particle import Particle              # 破壊時particle
from .item import Item                      # item
from .enemy_bullet import Enemy_Bullet      # enemyのBulletクラス 
from .e_maton_carry import E_Maton_Carry    # ここだけ個別インポート

# 敵クラス(輸送機)
class E_Hakobun:
    #定数
    ARMER = 3
    # 敵を初期化してゲームに登録する
    def __init__(self, game, x, y, type, dir):
        self.game = game
        self.x = x
        self.y = y
        self.dx = 0.2 * dir
        self.dy = 0
        self.type = type                # 運ぶ敵 0:e_matonn 1:
        self.dir = dir
        self.armor = E_Hakobun.ARMER    # 装甲
        self.is_damaged = False         # ダメージを受けたかどうか
        self.isRise = False             # 上昇中flag
        self.isReleased = False         # 運んでいる敵との接続flag
        self.hit_area = (0, 0, 7, 7)    # 当たり判定の領域 (x1,y1,x2,y2) 
        # 輸送する敵を生成
        enemies = game.enemies
        # 自分自身＝self を親として渡す
        enemies.append(E_Maton_Carry(game, self.x, self.y + 8, 0, -1 ,self))

    # 敵にダメージを与える
    def add_damage(self, power):
        self.armor -= power
        if self.armor <= 0:  # 
            # 爆発エフェクトを生成する
            self.game.particles.append(
                Particle(self.game, self.x + 4, self.y + 4, 0, 6)
            )
            self.game.particles.append(
                Particle(self.game, self.x + 4, self.y + 4, 0, 8)
            )
            # 破片
            num_particles = pyxel.rndi(5, 10) # 飛び散る数をランダムに
            for i in range(num_particles):
                self.game.particles.append(
                    Particle(self.game, self.x + 4, self.y + 14, 1, 9)
                )
            num_particles = pyxel.rndi(5, 10) # 飛び散る数をランダムに
            for i in range(num_particles):
                self.game.particles.append(
                    Particle(self.game, self.x + 4, self.y + 14, -1, 9)
                )
            # アイテムを生成する
            # ■■■■後からランダムにする■■■■
            self.game.items.append(
                Item(self.game, self.x, self.y - 8, 1)
            )
            # 敵をリストから削除する
            if self in self.game.enemies:  # 敵リストに登録されている時
                self.game.enemies.remove(self)
            # スコアを加算する
    #        self.game.score += self.level * 10
        else:
            self.is_damaged = True
            # ダメージ音を再生する
#            pyxel.play(2, 1, resume=True)   # チャンネル2で割り込み再生させる
            return                          # 処理終了

    # 敵を更新する
    def update(self):
#        if self.isReleased == False:
#            self.isReleased = True
        pass
        # 移動単位
#        self.dx = 0
#        self.dy = min(self.dy + 1, 3)
        # 押し戻し処理
#        self.x, self.y = push_back(self.x, self.y, self.dx, self.dy, self.isRise)
        # 移動
#        self.x += self.dx
        # Y方向の移動はpush_backで制御している

    # 敵を描画する
    def draw(self):
        # 4フレーム周期で0と8を交互に繰り返す
        u = pyxel.frame_count  // 4 % 2 * 8
        if self.is_damaged:
            #ダメージ演出
            self.is_damaged = False
            for i in range(1, 15):
                pyxel.pal(i, 15)    #カラーパレットの色を置き換える
            pyxel.blt(self.x, self.y, 1, 8 + u, self.type * 8 + 136, 8 * self.dir, 8, 0, 0, 1.3)
            pyxel.pal() #カラーパレット元に戻す
        else:
            pyxel.blt(self.x, self.y, 1, 8 + u, self.type * 8 + 136, 8 * self.dir, 8, 0)
