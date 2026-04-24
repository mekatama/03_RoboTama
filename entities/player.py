import pyxel
from collision import get_tile_type, in_collision, push_back
from constants import TILE_EXIT, TILE_GEM, TILE_BOMB, TILE_SPIKE, TILE_WALL, TILE_ROAD, SCROLL_SPEED

from .bomb import Bomb                  # ボムクラス
from .player_bullet import PlayerBullet # playerのBulletクラス 

# プレイヤークラス
class Player:
    #定数
    MOVE_SPEED = 2          # 移動速度
    DASH_SPEED = 10         # 特殊移動速度
    SHOT_INTERVAL = 6       # 弾の発射間隔
    DASH_INTERVAL = 2       # dash間隔
    HP = 3                  # 初期HP

    # プレイヤーを初期化する
    def __init__(self, game, x, y):
        self.game = game        # ゲームへの参照
        self.x = x              # X座標
        self.y = y              # Y座標
        self.dir = 1            # 1:right -1:left
        self.dir2 = 0           # 0:水平 1:down -1:up
        self.bombState = 0      # Bombのflag 0:未所持 1:所持 2:投下
        self.isBombGo = False   # Bomb使用flag
        self.isGoal = False     # 着地flag
        self.isDead = False     # 死亡flag
        self.shot_timer = 0     # 弾発射までの残り時間
        self.goalDemo_time = 60 # goal demo時間
        self.hp = Player.HP     # HP
        self.hit_area = (0, 0, 7, 7)  # 当たり判定の領域 (x1,y1,x2,y2) 

    # プレイヤーを更新する
    def update(self):
        if self.isGoal == False:    # 着地していない
            if self.game.is_play == True:
                # 強制前進
                self.x += 1
                # キー入力で自機を移動させる
                if pyxel.btn(pyxel.KEY_LEFT):
                    self.x -= Player.MOVE_SPEED
                    self.dir2 = 0
                if pyxel.btn(pyxel.KEY_RIGHT):
                    self.x += Player.MOVE_SPEED
                    self.dir = 1
                    self.dir2 = 0
                if pyxel.btn(pyxel.KEY_UP):
                    self.y -= Player.MOVE_SPEED
                    self.dir2 = -1
                if pyxel.btn(pyxel.KEY_DOWN):
                    self.y += Player.MOVE_SPEED
                    self.dir2 = 1
                if pyxel.btnr(pyxel.KEY_UP) or pyxel.btnr(pyxel.KEY_DOWN):
                    self.dir2 = 0
        else:
            self.x += 0
            self.y = 104        # 強制的にy座標固定
        
        # 弾の発射間隔timer制御
        if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
            self.shot_timer -= 1
        
        # auto攻撃
        if self.isGoal == False:    # 着地していない
            if self.shot_timer == 0:
                self.game.player_bullets.append(
                    PlayerBullet(self.game, self.x, self.y, self.dir, self.dir2)
                )
                # 次の弾発射までの残り時間を設定する
                self.shot_timer = Player.SHOT_INTERVAL

        # 爆弾所持
        if self.bombState == 1:
            self.game.player_bombs.append(
                Bomb(self.game, self.x, self.y + 8)
            )
            self.bombState = 2
        # 爆弾所持で、Sキー入力で爆弾発射
        if pyxel.btnp(pyxel.KEY_S) and self.bombState == 2:
            self.isBombGo = True    # Bombの方でfalseにして
            self.bombState = 0

        # 爆弾未所持で、Sキー入力で特殊移動
#        if pyxel.btnp(pyxel.KEY_S) and self.isBombGo == False:
#            pass

        """
        # 自機が画面外に出ないようにする(一画面用)
        self.x = max(self.x, 0)                 #大きい数値を使う
        self.x = min(self.x, pyxel.width - 8)   #小さい数値を使う
        self.y = max(self.y, 0)                 #大きい数値を使う
        self.y = min(self.y, pyxel.height - 8)   #小さい数値を使う
        """
        # タイルとの当たり判定
        for i in [1, 6]:
            for j in [1, 6]:
                x = self.x + j
                y = self.y + i
                tile_type = get_tile_type(x, y)

                if tile_type == TILE_GEM:  # 宝石に触れた時
                    # スコアを加算する
                    self.game.score += 10
                    # 宝石タイルを消す
                    pyxel.tilemaps[0].pset(x // 8, y // 8, (0, 0))
                    # 効果音を再生する
#                    pyxel.play(3, 1)

                if tile_type == TILE_BOMB:  # BOMBに触れた時
                    self.bombState = 1
                    # タイルを消す
                    pyxel.tilemaps[0].pset(x // 8, y // 8, (0, 0))

#                if tile_type == TILE_EXIT:  # ゴールに到達した時
#                    self.game.change_scene("clear")
#                    return

                if tile_type == TILE_ROAD:  # 滑走路に触れた時
                    print("touch down")
                    self.isGoal = True  #
                    return

                if tile_type == TILE_SPIKE:  # トゲ又に触れた時
                    self.isDead = True
                    self.game.change_scene("gameover")
                    return

                if tile_type == TILE_WALL:  # 壁に触れた時
                    self.isDead = True
                    self.game.change_scene("gameover")
                    return
        #goal処理
        if self.isGoal:
            self.goalDemo_time -= 1
            if self.goalDemo_time < 0: 
                self.game.change_scene("title")

    # プレイヤーを描画する
    def draw(self):
        # 4フレーム周期で0と8を交互に繰り返す
        u = pyxel.frame_count  // 4 % 2 * 8
        if self.dir2 == 0:
            pyxel.blt(self.x, self.y, 0, 0, 24 + u, 8 * self.dir, 8, 0)
        elif self.dir2 == -1:
            pyxel.blt(self.x, self.y, 0, 8, 24 + u, 8 * self.dir, 8, 0)
        elif self.dir2 == 1:
            pyxel.blt(self.x, self.y, 0, 16, 24 + u, 8 * self.dir, 8, 0)
#        pyxel.blt(self.x, self.y, 0, 0, 24 + u, 8 * self.dir, 8, 0, rotate = 45)
#        pyxel.text(self.x - 4,  self.y - 6, "HP:%i" %self.hp, 7)
