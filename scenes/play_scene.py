import pyxel
from entities import Player, Enemy1

from collision import get_tile_type
from constants import (
    SCROLL_BORDER_X,
    TILE_ENEMY1_POINT,
    TILE_ENEMY2_POINT,
    TILE_ENEMY3_POINT,
    TILE_ENEMY4_POINT,
)

# 当たり判定用の関数
#   タプルで設定した当たり判定領域を使用して判定
def check_collision(entity1, entity2):
    #キャラクター1の当たり判定座標を設定
    entity1_x1 = entity1.x + entity1.hit_area[0]
    entity1_y1 = entity1.y + entity1.hit_area[1]
    entity1_x2 = entity1.x + entity1.hit_area[2]
    entity1_y2 = entity1.y + entity1.hit_area[3]

    #キャラクター2の当たり判定座標を設定
    entity2_x1 = entity2.x + entity2.hit_area[0]
    entity2_y1 = entity2.y + entity2.hit_area[1]
    entity2_x2 = entity2.x + entity2.hit_area[2]
    entity2_y2 = entity2.y + entity2.hit_area[3]

    # キャラクター1の左端がキャラクター2の右端より右にある
    if entity1_x1 > entity2_x2: #成立すれば衝突していない
        return False
    # キャラクター1の右端がキャラクター2の左端より左にある
    if entity1_x2 < entity2_x1: #成立すれば衝突していない
        return False
    # キャラクター1の上端がキャラクター2の下端より下にある
    if entity1_y1 > entity2_y2: #成立すれば衝突していない
        return False
    # キャラクター1の下端がキャラクター2の上端より上にある
    if entity1_y2 < entity2_y1: #成立すれば衝突していない
        return False
    # 上記のどれでもなければ重なっている
    return True #衝突している

# プレイ画面クラス
class PlayScene:
    # プレイ画面を初期化する
    def __init__(self, game):
        self.game = game
    # プレイ画面を開始する
    def start(self):
        # 変更前のマップに戻す
        pyxel.tilemaps[0].blt(0, 0, 2, 0, 0, 256, 16)
        # プレイ画面の状態を初期化する
        game = self.game        # ゲームクラス
        game.score = 0          # スコア
        game.screen_x = 0
        game.player = Player(game, 16, 54)  # プレイヤー
        # 敵を出現させる
        self.spawn_enemy(0, 127)    #画面x座標0～127が表示されたら

    # 敵を出現させる
    def spawn_enemy(self, left_x, right_x):
        game = self.game
        enemies = game.enemies
        # 判定範囲のタイルを計算する
        left_x = pyxel.ceil(left_x / 8)     # x 以上の最小の整数を返す
        right_x = pyxel.floor(right_x / 8)  # x 以下の最大の整数を返す

        # 判定範囲のタイルに応じて敵とボスを出現させる
        for tx in range(left_x, right_x + 1):
            for ty in range(16):
                x = tx * 8
                y = ty * 8
                tile_type = get_tile_type(x, y)

                if tile_type == TILE_ENEMY1_POINT:  # 出現位置の時
                    enemies.append(Enemy1(game, x, y, 0))
                elif tile_type == TILE_ENEMY2_POINT:  # 出現位置の時
                    enemies.append(Enemy1(game, x, y, 1))
                elif tile_type == TILE_ENEMY3_POINT:  # 出現位置の時
                    enemies.append(Enemy1(game, x, y, 2))
                elif tile_type == TILE_ENEMY4_POINT:  # 出現位置の時
                    enemies.append(Enemy1(game, x, y, 3))
                else:
                    continue
                # 出現位置タイルを消す
                pyxel.tilemaps[0].pset(tx, ty, (0, 0))

    # プレイ画面を更新する
    def update(self):
        game = self.game
        player = game.player
        player_bullets = game.player_bullets
        enemies = game.enemies
        enemy_bullets = game.enemy_bullets
        particles = game.particles
        items = game.items

        # プレイヤーを更新する
        if player is not None: #NONE使用時は判定方法が特殊
            player.update()

        # プレイヤーの移動範囲を制限する
        player.x = min(max(player.x, game.screen_x), 1020)   # mapの全幅-8
 #       player.x = max(max(player.x, game.screen_x), 0)
        player.y = max(player.y, 0)

        # プレイヤーがスクロール境界を越えたら画面をスクロールする
        if player.x > game.screen_x + SCROLL_BORDER_X:
            last_screen_x = game.screen_x
            game.screen_x = min(player.x - SCROLL_BORDER_X, 240 * 8)
            # 240タイル分以上は右にスクロールさせない

        # スクロールした幅に応じて敵を出現させる
        self.spawn_enemy(game.screen_x + 128, game.screen_x + 128)

        # 弾(プレイヤー)を更新する
        for player_bullet in player_bullets.copy():
            player_bullet.update()
            # 弾(プレイヤー)と敵が接触したら消去
            for enemy in enemies.copy():
                if check_collision(enemy, player_bullet):
                    player_bullet.add_damage()  # 自機の弾にダメージを与える
                    enemy.add_damage()          # 敵にダメージを与える

        # 敵を更新する
        for enemy in enemies.copy():
            enemy.update()
            # プレイヤーと敵が接触したらゲームオーバー
            if player is not None:
                if check_collision(enemy, player):
                    player.isDead == True
                    game.change_scene("gameover")
                    return

            # 敵が画面の左端または下端から外に出たら削除する
            if (
                enemy.x < game.screen_x - 8
                or enemy.x > game.screen_x + 160
                or enemy.y > 160
            ):
                if enemy in enemies:  # 敵リストに登録されている時
                    enemies.remove(enemy)

        # 敵の弾を更新する
        for enemy_bullet in enemy_bullets.copy():
            enemy_bullet.update()
            # 弾(enemy)とplayerが接触したら消去
            if player is not None and check_collision(player, enemy_bullet):
                player.isDead == True
                enemy_bullet.add_damage()         # 敵の弾にダメージを与える
                game.change_scene("gameover")
                return

            # 敵の弾が画面の左端または下端から外に出たら削除する
            if (
                enemy_bullet.x < game.screen_x - 8
                or enemy_bullet.x > game.screen_x + 160
                or enemy_bullet.y > 160
            ):
                if enemy_bullet in enemy_bullets:  # 敵リストに登録されている時
                    enemy_bullets.remove(enemy_bullet)

         # 破壊時particlesを更新する
        for particle in particles.copy():
            particle.update()
            # flag onで消す処理入れたい
            if particle.is_alive == False:
                if particle in particles:  # リストに登録されている時
                    particles.remove(particle)

        # itemを更新する
        for item in items.copy():
            item.update()
            # itemとplayerが接触したら消去
            if player is not None and check_collision(player, item):
                item.add_damage()         # itemにダメージを与える
            # flag onで消す処理入れたい
            if item.is_alive == False:
                if item in items:  # リストに登録されている時
                    items.remove(item)

        # [debug]キー入力をチェックする
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            # プレイ画面に切り替える
            self.game.change_scene("gameover")

    # プレイ画面を描画する
    def draw(self):
        # 画面をクリアする
        pyxel.cls(0)
        # フィールドを描画する
        self.game.draw_field()
        # プレイヤーを描画する
        self.game.draw_player()
        # 弾(プレイヤー)を描画する
        self.game.draw_player_bullets()
        # 敵を描画する
        self.game.draw_enemies()
        # 敵の弾を描画する
        self.game.draw_enemy_bullets()
        # 破壊時particleを描画する
        self.game.draw_particles()
        # itemを描画する
        self.game.draw_items()

        # スコアを描画する
#        pyxel.text(39, 4, f"SCORE {self.score:5}", 7)

        if self.game.player.isGoal == True:
            # テキストを描画する
            pyxel.text(36, 64, "- CLEAR !!! -", 1)
