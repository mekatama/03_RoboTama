import pyxel
from collision import in_collision, push_back
from .enemy_bullet import Enemy_Bullet  # enemyのBulletクラス 
from .particle import Particle          # 破壊時particle
from .item import Item                  # item

# 敵クラス(固定敵_攻撃なし)
class E_Boss_1:
    enemy_bullets = []     # 敵の弾のリスト

    # 敵を初期化してゲームに登録する
    def __init__(self, game, x, y, type, dir):
        self.game = game
        self.x = x
        self.y = y - 16                 # 初期位置を画面外へ
        self.dx = 1
        self.dy = 1
        self.type = type
        self.dir = dir    
        self.fire_timer = 0             # 攻撃タイマー
        self.countMove = 0              # 移動制御用のカウント
        self.armor = 20                 # 装甲
        self.is_damaged = False         # ダメージを受けたかどうか
        self.isRise = False             # 上昇中flag
        self.hit_area = (0, 0, 32, 16)    # 当たり判定の領域 (x1,y1,x2,y2) 

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
            Item(self.game, self.x, self.y)
        )
        # BOSS1死亡flag立てる
        if self.game.isBoss1Kill == False:
            self.game.isBoss1Kill = True
        # 敵をリストから削除する
        if self in self.game.enemies:  # 敵リストに登録されている時
            self.game.enemies.remove(self)
        # スコアを加算する
#        self.game.score += self.level * 10

    # 敵を更新する
    def update(self):
        self.countMove += 1
        # 移動単位
        self.dx = 1
        # 登場
        if self.countMove > 60:
            self.y += self.dy
            if self.y > 40:
                self.dy = 0
        # 左右移動
        if self.y > 40:
            if self.x >= 224:   # ここは実測した値を入れる
                self.dir = -1
            elif self.x <= 128:   # ここは実測した値を入れる
                self.dir = 1
            # 移動
            self.x += self.dx * self.dir

        # 弾の発射タイマーが0になったら攻撃
        if self.fire_timer > 0:
            self.fire_timer -= 1
        else:  # 弾を発射する
            self.game.enemy_bullets.append(
                Enemy_Bullet(self.game, self.x + 16, self.y + 16, 0, 1, self.dir, 0)
            )
            # 攻撃タイマーをリセットする
            if self.armor > 10:
                self.fire_timer = 20
            elif self.armor <= 10:
                self.fire_timer = 10


    # 敵を描画する
    def draw(self):
        # 4フレーム周期で0と8を交互に繰り返す
        u = pyxel.frame_count  // 4 % 2 * 8
        if self.is_damaged:
            #ダメージ演出
            self.is_damaged = False
            for i in range(1, 15):
                pyxel.pal(i, 15)    #カラーパレットの色を置き換える
 #           pyxel.blt(self.x, self.y, 1, 8 + u, self.type * 8 + 120, 8 * self.dir, 8, 0)
            pyxel.blt(self.x, self.y, 0, 0, 40, 32, 16, 0)
            pyxel.pal() #カラーパレット元に戻す
        else:
#            pyxel.blt(self.x, self.y, 1, 8 + u, self.type * 8 + 120, 8 * self.dir, 8, 0)
            pyxel.blt(self.x, self.y, 0, 0, 40, 32, 16, 0)
