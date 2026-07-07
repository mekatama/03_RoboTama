import pyxel
from collision import get_tile_type, in_collision, in_collision2, push_back
from constants import TILE_EXIT, TILE_GEM, TILE_SPIKE, TILE_WALL, TILE_ROAD, SCROLL_SPEED

from .player_bullet import PlayerBullet # playerのBulletクラス 

# プレイヤークラス
class Player2:
    #定数
    MOVE_SPEED = 2          # 移動速度
    DASH_SPEED = 10         # 特殊移動速度
    SHOT_INTERVAL0 = 8      # 弾の発射間隔
    SHOT_INTERVAL1 = 40     # 弾の発射間隔
    SHOT_INTERVAL2 = 5      # 弾の発射間隔
    DASH_INTERVAL = 2       # dash間隔
    HP = 3                  # 初期HP
    IS_ATK = True           # 攻撃flag
    # プレイヤーの目の前に 8x8 くらいの判定エリアを作る
    RANGE_WIDTH = 20
    RANGE_HEIGHT = 8
    
    # プレイヤーを初期化する
    def __init__(self, game, x, y):
        self.game = game        # ゲームへの参照
        self.x = x              # X座標
        self.y = y              # Y座標
        self.dx = 0             # X軸方向の移動距離
        self.dy = 0             # Y軸方向の移動距離
        self.dir = 1            # 1:right -1:left
        self.type = 0           # 0:通常弾 1:近接攻撃 2:連射弾
        self.type_tmp = 0       # 攻撃type一時保存
        self.isAtk = Player2.IS_ATK  # 攻撃flag
        self.isDead = False     # 死亡flag
        self.isDown = False     # しゃがみflag
        self.isUp = False       # 上向きflag
        self.isFalling = False  # 落下中flag
        self.isMelee = False    # 近接攻撃flag
        self.shot_timer = 0     # 弾発射までの残り時間
        self.jump_counter = 0   # ジャンプ時間
        self.hp = Player2.HP    # HP
        self.bulletNum = 0      # 残弾数
        self.sensor_x = 0       # 近接攻撃判定座標
        self.sensor_y = 0       # 近接攻撃判定座標
        self.hit_area = (0, 0, 7, 7)  # 当たり判定の領域 (x1,y1,x2,y2) 

    # プレイヤーを更新する
    def update(self):
        last_y = self.y     # 落下中判定用

        # キー入力で左右移動させる
        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx = -1 * Player2.MOVE_SPEED
            self.dir = -1
            self.sensor_x = self.x - Player2.RANGE_WIDTH  # プレイヤーの左端から近接攻撃判定
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.dx = 1 * Player2.MOVE_SPEED
            self.dir = 1
            self.sensor_x = self.x + 8  # プレイヤーの右端から近接攻撃判定
        else:
            self.dx = 0
        # しゃがみ
        if pyxel.btn(pyxel.KEY_DOWN):
            self.dx = 0
            self.hit_area = (0, 4, 7, 7)  # しゃがみ当たり判定の領域 (x1,y1,x2,y2) 
            self.isDown = True
        elif pyxel.btnr(pyxel.KEY_DOWN):
            self.hit_area = (0, 0, 7, 7)  # 立ち当たり判定の領域 (x1,y1,x2,y2) 
            self.isDown = False
        # 上向き
        if pyxel.btn(pyxel.KEY_UP):
            self.dx = 0
            self.isUp = True
        elif pyxel.btnr(pyxel.KEY_UP):
            self.isUp = False
        # 近接攻撃判定y座標
        self.sensor_y = self.y  # プレイヤーの左端から近接攻撃判定

        # 下方向に加速する
        if self.jump_counter > 0:  # ジャンプ中
            self.jump_counter -= 1  # ジャンプ時間を減らす
        else:  # ジャンプしていない時
            self.dy = min(self.dy + 1, 4)  # 下方向に加速する
        
        # ジャンプする
            # スペースキーまたはゲームパッドのBボタンが押された時
        if (    self.dy >= 0 and
                ((in_collision(self.x, self.y + 8) or in_collision(self.x + 7, self.y + 8)) or
                 (in_collision2(self.x, self.y + 8) or in_collision2(self.x + 7, self.y + 8))) and
                (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B))):
            self.dy = -4.5
            self.jump_counter = 3

        # 押し戻し処理
        self.x, self.y = push_back(self.x, self.y, self.dx, self.dy, self.isFalling)

        # 横方向の移動を減速する
        self.dx = int(self.dx * 0.8)

        # 直前のy座標と比較して、落下flag判定
        if self.y > last_y:
            self.isFalling = True
        else:
            self.isFalling = False

        # 弾の発射間隔timer制御
        if self.shot_timer > 0:  # 弾発射までの残り時間を減らす
            self.shot_timer -= 1
        
        # auto攻撃
        if self.shot_timer == 0 and self.isAtk == True:
            # 近接攻撃出した後にもとに戻す
            if self.type == 1:
                self.type = self.type_tmp
            # 近接攻撃
            if self.isMelee == True:
                self.type_tmp = self.type   # 近接攻撃直前のtypeを一時保存
                self.type = 1
                # しゃがみ判定
                if self.isDown == True:
                    self.game.player_bullets.append(
                        PlayerBullet(self.game, self.x + 8, self.y + 1, self.dir, 0, self.type)
                    )
                else:
                    self.game.player_bullets.append(
                        PlayerBullet(self.game, self.x + 8, self.y -2, self.dir, 0, self.type)
                    )
                self.isMelee = False

            # 射撃攻撃
            else:
                if self.isUp == True:
                    self.game.player_bullets.append(
                        PlayerBullet(self.game, self.x, self.y - 6, self.dir, -1, self.type)
                    )
                else:
                    # 向きで分岐
                    if self.dir == 1:
                        # しゃがみ判定
                        if self.isDown == True:
                            self.game.player_bullets.append(
                                PlayerBullet(self.game, self.x + 8, self.y + 1, self.dir, 0, self.type)
                            )
                        else:
                            self.game.player_bullets.append(
                                PlayerBullet(self.game, self.x + 8, self.y -2, self.dir, 0, self.type)
                            )
                    elif self.dir == -1:
                        # しゃがみ判定
                        if self.isDown == True:
                            self.game.player_bullets.append(
                                PlayerBullet(self.game, self.x - 10, self.y + 1, self.dir, 0, self.type)
                            )
                        else:
                            self.game.player_bullets.append(
                                PlayerBullet(self.game, self.x - 10, self.y - 2, self.dir, 0, self.type)
                            )
                # 残弾の判定
                if self.type == 2:
                    self.bulletNum -= 1
                    # 残弾数ゼロでtype0に戻す
                    if self.bulletNum <= 0:
                        self.type = 0

            # 次の弾発射までの残り時間をtypeで変更する
            if self.type == 0:
                self.shot_timer = Player2.SHOT_INTERVAL0
            elif self.type == 1:
                self.shot_timer = Player2.SHOT_INTERVAL1
            elif self.type == 2:
                self.shot_timer = Player2.SHOT_INTERVAL2
        
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

                if tile_type == TILE_ROAD:  # すり抜け床に触れた時
                    pass

                if tile_type == TILE_SPIKE:  # トゲ又に触れた時
                    self.isDead = True
                    self.game.change_scene("gameover")
                    return

    # 描画
    def draw(self):
        # 4フレーム周期で0と8を交互に繰り返す
        u = pyxel.frame_count  // 4 % 2 * 8
        if self.isUp == True:
            pyxel.blt(self.x, self.y, 0, 16, 24 + u, 8 * self.dir, 8, 0)
        if self.isDown == True:
            pyxel.blt(self.x, self.y, 0, 8, 24 + u, 8 * self.dir, 8, 0)
        elif self.isDown == False and self.isUp == False:
            pyxel.blt(self.x, self.y, 0, 0, 24 + u, 8 * self.dir, 8, 0)
#        pyxel.text(self.x - 4,  self.y - 6, "HP:%i" %self.hp, 7)

        # 残弾数表示
        if self.type == 2:
            pyxel.text(self.x - 4,  self.y - 6, "%i" %self.bulletNum, 7)

        # デバッグ用：センサーの範囲を薄い赤で表示  
#        pyxel.rectb(self.sensor_x, self.sensor_y, Player.RANGE_WIDTH, Player.RANGE_HEIGHT, 8)