import pyxel
from collision import in_collision, in_collision2, push_back
from .particle import Particle          # 破壊時particle
from .item import Item                  # item

# 敵クラス(固定敵_攻撃なし)
class E_Maton_Carry:
    #定数
    ARMER = 3
    WALK_SPEED = 0.2
    FIND_DISTANCE = 40

    # 敵を初期化してゲームに登録する
    def __init__(self, game, x, y, type, dir, parent):
        self.game = game
        self.x = x
        self.y = y
        self.dx = E_Maton_Carry.WALK_SPEED * dir
        self.dy = 0
        self.type = type
        self.dir = dir
        self.parent = parent            # 生成先の輸送機
        self.armor = E_Maton_Carry.ARMER# 装甲
        self.is_damaged = False         # ダメージを受けたかどうか
        self.isRise = False             # 上昇中flag
        self.isFind = False             # player発見flag
        self.isLanding = False          # 着地flag
        self.hit_area = (0, 0, 7, 7)    # 当たり判定の領域 (x1,y1,x2,y2) 

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
        # 輸送機の切り離しflagを監視
        if self.parent.isReleased == False:
            # 輸送中
            self.x = self.parent.x
            self.y = self.parent.y + 8
        else:
            # 着地判定したい(敵の足元中央で簡易判定)
            if self.isLanding == False:
                if in_collision(self.x + 4, self.y + 8) or in_collision2(self.x + 4, self.y + 8):
                    self.isLanding = True
                    print("landing")
            # 切り離し、空中
            if self.isLanding == False:
                dx_tmp = 0    # 真下に投下
            # 着地後、移動
            else:
                dx_tmp = self.dx

            # 移動単位
            self.dy = min(self.dy + 1, 3)
            # 押し戻し処理
            self.x, self.y = push_back(self.x, self.y, dx_tmp, self.dy, self.isRise)
            # 移動
            self.x += dx_tmp
            # Y方向の移動はpush_backで制御している

            # playerとの距離
            dx = self.game.player.x - self.x
            dy = self.game.player.y - self.y
            sq_dist = dx * dx + dy * dy
            if sq_dist < E_Maton_Carry.FIND_DISTANCE ** 2 and self.isFind == False:  # プレイヤーとの距離がFIND_DISTANCE未満の時
                self.game.particles.append(
                    Particle(self.game, self.x + 3, self.y - 6, 0, 11)
                )
                self.isFind = True

    # 敵を描画する
    def draw(self):
        # 着地したらアニメーション再生
        if self.isLanding == False:
            u = 0
        else:
            # 4フレーム周期で0と8を交互に繰り返す
            u = pyxel.frame_count  // 4 % 2 * 8

        if self.is_damaged:
            #ダメージ演出
            self.is_damaged = False
            for i in range(1, 15):
                pyxel.pal(i, 15)    #カラーパレットの色を置き換える
            pyxel.blt(self.x, self.y, 1, 8 + u, self.type * 8 + 80, 8 * self.dir, 8, 0, 0, 1.3)
            pyxel.pal() #カラーパレット元に戻す
        else:
            pyxel.blt(self.x, self.y, 1, 8 + u, self.type * 8 + 80, 8 * self.dir, 8, 0)
