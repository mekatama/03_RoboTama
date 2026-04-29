import pyxel
#from collision import in_collision, push_back
from .enemy_bullet import Enemy_Bullet  # enemyのBulletクラス 
from .particle import Particle          # 破壊時particle

# 敵クラス
class Enemy1:
    #定数
    KIND_A = 0  # 敵A(空中)
    KIND_B = 1  # 敵B(地上停止)
    KIND_C = 2  # 敵C(地上停止_45°攻撃)
    KIND_D = 3  # 敵D(空中_狙う攻撃)
    enemy_bullets = []     # 敵の弾のリスト

    # 敵を初期化してゲームに登録する
    def __init__(self, game, x, y, type):
        self.game = game
        self.x = x
        self.y = y
        self.type = type
        self.fire_timer = 0             # 攻撃タイマー
        self.hit_area = (0, 0, 7, 7)    # 当たり判定の領域
        self.armor = 3                  # 装甲
        self.is_damaged = False         # ダメージを受けたかどうか
        self.hit_area = (0, 0, 7, 7)    # 当たり判定の領域 (x1,y1,x2,y2) 

    # 敵にダメージを与える
    def add_damage(self):
        if self.armor > 1:  # 装甲が残っている時
            self.armor -= 1
            self.is_damaged = True
            # ダメージ音を再生する
#            pyxel.play(2, 1, resume=True)   # チャンネル2で割り込み再生させる
            return                          # 処理終了
        # 爆発エフェクトを生成する
        self.game.particles.append(
            Particle(self.game, self.x + 4, self.y + 4, 0, 6)
        )
        """
        # アイテムを生成する
        # ■■■■後からランダムにする■■■■
        Item(self.game, self.x, self.y)
        """
        # 敵をリストから削除する
        if self in self.game.enemies:  # 敵リストに登録されている時
            self.game.enemies.remove(self)
        # スコアを加算する
#        self.game.score += self.level * 10

    # 敵を更新する
    def update(self):
        # 弾の発射タイマーが0になったら花粉を発射する
        if self.fire_timer > 0:
            self.fire_timer -= 1
        else:  # 弾を発射する
            # playerとの距離
            dx = self.game.player.x - self.x
            dy = self.game.player.y - self.y
            sq_dist = dx * dx + dy * dy
            # プレイヤーの方向に向けて速度1で花粉を発射する
            dist = pyxel.sqrt(sq_dist)  # 
            # 敵typeで攻撃を分岐
            if self.type == Enemy1.KIND_A:
                self.game.enemy_bullets.append(
                    Enemy_Bullet(self.game, self.x, self.y, -1, 0)
                )
            elif self.type == Enemy1.KIND_B:
                self.game.enemy_bullets.append(
                    Enemy_Bullet(self.game, self.x, self.y, -1, -1)
                )
            elif self.type == Enemy1.KIND_C:
                pass
            elif self.type == Enemy1.KIND_D:
                self.game.enemy_bullets.append(
                    Enemy_Bullet(self.game, self.x, self.y, dx / dist, dy / dist) 
                )
            # 花粉の発射タイマーをリセットする
            self.fire_timer = 90

        # 移動処理
        # 敵A(空中)を更新する
        if self.type == Enemy1.KIND_A:
            self.x -= 0.5
        # 敵B(地上停止)を更新する
        elif self.type == Enemy1.KIND_B:
            pass
        # 敵C(地上停止)を更新する
        elif self.type == Enemy1.KIND_C:
            pass
        # 敵D(空中狙う攻撃)を更新する
        elif self.type == Enemy1.KIND_D:
            self.x -= 0.1

    # 敵を描画する
    def draw(self):
#        pyxel.blt(self.x, self.y, 0, 32, 40, 8, 8, 0)
        # 4フレーム周期で0と8を交互に繰り返す
        u = pyxel.frame_count  // 4 % 2 * 8
        if self.is_damaged:
            #ダメージ演出
            self.is_damaged = False
            for i in range(1, 15):
                pyxel.pal(i, 15)    #カラーパレットの色を置き換える
            pyxel.blt(self.x, self.y, 1, 8 + u, self.type * 8 + 80, -8, 8, 0)
            pyxel.pal() #カラーパレット元に戻す
        else:
            pyxel.blt(self.x, self.y, 1, 8 + u, self.type * 8 + 80, -8, 8, 0)

