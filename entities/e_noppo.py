import pyxel
from collision import in_collision, push_back
from .particle import Particle          # 破壊時particle
from .item import Item                  # item
from .enemy_bullet import Enemy_Bullet  # enemyのBulletクラス 

# 敵クラス(固定敵_攻撃なし)
class E_Noppo:
    #定数
    ARMER = 20
    WALK_SPEED = 0.1
    FIND_DISTANCE = 60
    enemy_bullets = []     # 敵の弾のリスト

    # 敵を初期化してゲームに登録する
    def __init__(self, game, x, y, type, dir):
        self.game = game
        self.x = x
        self.y = y
        self.dx = E_Noppo.WALK_SPEED * dir
        self.dy = 0
        self.type = type
        self.dir = dir
        self.armor = E_Noppo.ARMER      # 装甲
        self.fire_timer = 0             # 攻撃タイマー
        self.is_damaged = False         # ダメージを受けたかどうか
        self.isRise = False             # 上昇中flag
        self.isFind = False             # player発見flag
        self.hit_area = (0, -7, 7, 7)    # 当たり判定の領域 (x1,y1,x2,y2) 

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
        # playerとの距離
        dx = self.game.player.x - self.x
        dy = self.game.player.y - self.y
        sq_dist = dx * dx + dy * dy
        dist = pyxel.sqrt(sq_dist)  # プレイヤーの方向速度1の値
        if sq_dist < E_Noppo.FIND_DISTANCE ** 2 and self.isFind == False:  # プレイヤーとの距離がFIND_DISTANCE未満の時
            self.game.particles.append(
                Particle(self.game, self.x + 3, self.y - 14, 0, 11)
            )
            self.isFind = True
        # plater発見で移動開始
        if self.isFind == True:
            dx_tmp = self.dx
        else:
            dx_tmp = 0    # 強制停止

        # 移動単位
        self.dy = min(self.dy + 1, 3)

        # 移動方向を反転させる
        # 床の上にいる時(足元の左右端で判定)
        if in_collision(self.x, self.y + 8) or in_collision(self.x + 7, self.y + 8):
            # 移動先に壁(y+4)があるまたは床(y+8)がない時
            # 左側判定
            if  self.dir < 0 and (in_collision(self.x - 1, self.y + 4) or not in_collision(self.x - 1, self.y + 8)):
                self.dir = 1  # 右に移動する
            # 右側判定
            elif self.dir > 0 and (in_collision(self.x + 8, self.y + 4) or not in_collision(self.x + 8, self.y + 8)):
                self.dir = -1  # 左に移動する

        # player発見して弾の発射タイマーが0になったら攻撃
        if self.isFind == True:
            if self.fire_timer > 0:
                self.fire_timer -= 1
            else:  # 弾を発射する
                self.game.enemy_bullets.append(
                    Enemy_Bullet(self.game, self.x, self.y - 4, 0.8, 0, self.dir, 2)
                )
                # 攻撃タイマーをリセットする
                self.fire_timer = 90

        # 押し戻し処理
        self.x, self.y = push_back(self.x, self.y, dx_tmp, self.dy, self.isRise)
        # 移動
        self.x += dx_tmp
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
            pyxel.blt(self.x, self.y - 8, 1, 32 + u, self.type * 8 + 40, 8 * self.dir, 16, 0, 0, 1.3)
            pyxel.pal() #カラーパレット元に戻す
        else:
            pyxel.blt(self.x, self.y - 8, 0, 32 + u, self.type * 8 + 40, 8 * self.dir, 16, 0)
