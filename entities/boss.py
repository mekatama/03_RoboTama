import pyxel
#from collision import in_collision, push_back
from .enemy_blast import Enemy_Blast    # enemyの爆発effectクラス 
from .enemy_bullet import Enemy_Bullet  # enemyのBulletクラス 

# BOSSクラス
class Boss:
    #定数
    KIND_A = 0  # BOSS(左)
    KIND_B = 1  # BOSS(中央)
    KIND_C = 2  # BOSS(右)
    enemy_bullets = []     # 敵の弾のリスト

    # 敵を初期化してゲームに登録する
    def __init__(self, game, x, y, type):
        self.game = game
        self.x = x
        self.y = y
        self.type = type                # パーツ判別[0: 1: 2:]
        self.fire_timer = 0             # 攻撃タイマー
        self.armor = 0                  # 装甲
        self.is_damaged = False         # ダメージを受けたかどうか
        self.is_centerDead = False      # boss中央破壊flag
        self.hit_area = (0, 0, 7, 7)    # 当たり判定の領域 (x1,y1,x2,y2) 

    # BOSS破壊
    def boss_dead(self):
        # 爆発エフェクトを生成する
        self.game.enemy_blasts.append(
           Enemy_Blast(self.game, self.x + 4, self.y + 4)
        )
        self.game.bosses.remove(self)

    # BOSSにダメージを与える
    def add_damage(self):
        if self.armor > 0:  # 装甲が残っている時
            self.armor -= 1
            self.is_damaged = True
            # ダメージ音を再生する
#            pyxel.play(2, 1, resume=True)   # チャンネル2で割り込み再生させる
            return                          # 処理終了
        # 爆発エフェクトを生成する
        self.game.enemy_blasts.append(
           Enemy_Blast(self.game, self.x + 4, self.y + 4)
        )
        """
        # アイテムを生成する
        # ■■■■後からランダムにする■■■■
        Item(self.game, self.x, self.y)
        """
        # bossをリストから削除する
        if self in self.game.bosses:  # bossリストに登録されている時
            print(self.type)
            if self.type == 1:
                    self.is_centerDead = True
            self.game.bosses.remove(self)
        # スコアを加算する
#        self.game.score += self.level * 10
            
    # 敵を更新する
    def update(self):
        # 弾の発射タイマーが0になったら花粉を発射する
        if self.fire_timer > 0:
            self.fire_timer -= 1
        else:  # 弾を発射する
            # boss(左)を更新する
            if self.type == Boss.KIND_A:
                self.game.enemy_bullets.append(
                    Enemy_Bullet(self.game, self.x, self.y, -1, -1)
                )

            # boss(中央)を更新する
            elif self.type == Boss.KIND_B:
                pass

            # boss(右)を更新する
            elif self.type == Boss.KIND_C:
                self.game.enemy_bullets.append(
                    Enemy_Bullet(self.game, self.x, self.y, 1, -1)
                )
            # 発射タイマーをリセットする
            self.fire_timer = 20

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
            pyxel.blt(self.x, self.y, 0, 8 + 32, 56 + u, 8, 8, 0)
            pyxel.pal() #カラーパレット元に戻す
        else:
            pyxel.blt(self.x, self.y, 1, 8 + u, 112 + (self.type * 8), 8, 8, 0)
#            pyxel.blt(self.x, self.y, 0, 32, 40 + u, 8, 8, 0)
#            pyxel.blt(self.x, self.y, 0, self.kind * 8 + 32, 40 + u, 8 * self.dir, 8, 0)

