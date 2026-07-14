import pyxel
from collision import in_collision, push_back
from .enemy_bullet import Enemy_Bullet  # enemyのBulletクラス 
from .particle import Particle          # 破壊時particle
from .item import Item                  # item

# 敵クラス(固定敵_攻撃_狙う)
class E_Maton_ATK_H:
    #定数
    ARMER = 3
    enemy_bullets = []     # 敵の弾のリスト

    # 敵を初期化してゲームに登録する
    def __init__(self, game, x, y, type, dir):
        self.game = game
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.dir = dir                  # 初期の向き(基本的に左向き)
        self.type = type
        self.fire_timer = 0             # 攻撃タイマー
        self.armor = E_Maton_ATK_H.ARMER# 装甲
        self.is_damaged = False         # ダメージを受けたかどうか
        self.isRise = False             # 上昇中flag
        self.hit_area = (0, 0, 7, 7)    # 当たり判定の領域 (x1,y1,x2,y2) 

    # 敵にダメージを与える
    def add_damage(self, power):
        self.armor -= power
        if self.armor <= 0:  # 
            # 爆発エフェクトを生成する
            self.game.particles.append(
                Particle(self.game, self.x + 4, self.y + 4, 0, 6)
            )
            # 爆発(ランダム)エフェクトを生成する
            for i in range(4):
                self.game.particles.append(
                    Particle(self.game, self.x + 8, self.y + 8, 0, 7)
                )
            # 破片
            num_particles = pyxel.rndi(3, 6) # 飛び散る数をランダムに
            for i in range(num_particles):
                self.game.particles.append(
                    Particle(self.game, self.x + 4, self.y + 8, 1, 9)
                )
            num_particles = pyxel.rndi(3, 6) # 飛び散る数をランダムに
            for i in range(num_particles):
                self.game.particles.append(
                    Particle(self.game, self.x + 4, self.y + 8, -1, 9)
                )
            # アイテムを生成する
            # ■■■■後からランダムにする■■■■
            self.game.items.append(
                Item(self.game, self.x, self.y, 1)
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
        # 移動単位
        self.dx = 0
        self.dy = min(self.dy + 1, 3)
        # 弾の発射タイマーが0になったら攻撃
        if self.fire_timer > 0:
            self.fire_timer -= 1
        else:  # 弾を発射する
            # playerとの距離
            dx = self.game.player.x - self.x
            dy = self.game.player.y - self.y
            sq_dist = dx * dx + dy * dy
            dist = pyxel.sqrt(sq_dist)  # プレイヤーの方向速度1の値
            if sq_dist < 90**2:  # プレイヤーとの距離が90未満の時
                self.game.enemy_bullets.append(
#                    Enemy_Bullet(self.game, self.x, self.y, 1, 0, self.dir)
                    Enemy_Bullet(self.game, self.x, self.y, dx / dist, dy / dist, 1, 0)    # 敵の向き不問 
                )
            # 攻撃タイマーをリセットする
            self.fire_timer = 90
        # 押し戻し処理
        self.x, self.y = push_back(self.x, self.y, self.dx, self.dy, self.isRise)
        # 移動
        self.x += self.dx
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
            pyxel.blt(self.x, self.y, 1, 8 + u, self.type * 8 + 88, 8 * self.dir, 8, 0)
            pyxel.pal() #カラーパレット元に戻す
        else:
            pyxel.blt(self.x, self.y, 1, 8 + u, self.type * 8 + 88, 8 * self.dir, 8, 0)
