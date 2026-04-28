import pyxel
from scenes import GameOverScene, PlayScene, TitleScene
from constants import SCROLL_SPEED

# ゲームクラス
class Game:
    # ゲームを初期化する
    def __init__(self):
        # Pyxelを初期化する
        pyxel.init(128, 128, title="master")
        # リソースファイルを読み込む
        pyxel.load("assets/my_resource20.pyxres")
        pyxel.tilemaps[2].blt(0, 0, 0, 0, 0, 256, 16)  # 変更前のマップをコピーする
        # ゲームの状態を初期化する
        self.player = None          # プレイヤー
        self.player_bullets = []    # 自機の弾のリスト
        self.enemies = []           # 敵のリスト
        self.enemy_bullets = []     # 敵の弾のリスト
        self.particles = []         # 破壊時particleのリスト

        self.scenes = {                     # シーンの辞書
            "title": TitleScene(self),
            "play": PlayScene(self),
            "gameover": GameOverScene(self),
        }
        self.scene_name = None  # 現在のシーン名
        self.screen_x = 0  # フィールド表示範囲の左端のX座標
        self.score = 0  # 得点

        # シーンをタイトル画面に変更する
        self.change_scene("title")

        # ゲームの実行を開始する
        pyxel.run(self.update, self.draw)

    # シーンを変更する
    def change_scene(self, scene_name):
        self.scene_name = scene_name
        self.scenes[self.scene_name].start()

    # フィールドを描画する
    def draw_field(self):
        pyxel.bltm(0, 0, 1, self.screen_x, 0, 128, 128)     # 奥BG
        pyxel.bltm(0, 0, 0, self.screen_x, 0, 128, 128, 0)  # 手前BG(0番抜け色)

    # プレイヤーを描画する
    def draw_player(self):
        # カメラ位置(描画の原点)を変更する
        pyxel.camera(self.screen_x, 0)
        # 描画
        if self.player is not None:  # プレイヤーが存在する時
            self.player.draw()
        # カメラ位置を戻す
        pyxel.camera()
    # 弾(プレイヤー)を描画する
    def draw_player_bullets(self):
        # カメラ位置(描画の原点)を変更する
        pyxel.camera(self.screen_x, 0)
        # 描画
        for player_bullet in self.player_bullets:
            player_bullet.draw()
        # カメラ位置を戻す
        pyxel.camera()
    # 敵を描画する
    def draw_enemies(self):
        # カメラ位置(描画の原点)を変更する
        pyxel.camera(self.screen_x, 0)
        # 描画
        for enemy in self.enemies:
            enemy.draw()
        # カメラ位置を戻す
        pyxel.camera()
    # 敵の弾を描画する
    def draw_enemy_bullets(self):
        # カメラ位置(描画の原点)を変更する
        pyxel.camera(self.screen_x, 0)
        # 描画
        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.draw()
        # カメラ位置を戻す
        pyxel.camera()
    # 破壊時particleを描画する
    def draw_particles(self):
        # カメラ位置(描画の原点)を変更する
        pyxel.camera(self.screen_x, 0)
        # 描画
        for particle in self.particles:
            particle.draw()
        # カメラ位置を戻す
        pyxel.camera()

    # ゲームを更新する
    def update(self):
        """
        if self.player is not None:  # プレイヤーが存在する時
            # playerがgoalしていない
            if self.player.isGoal == False:
                if self.is_play == True:
                    # 強制スクロール
                    self.screen_x += SCROLL_SPEED
        """
        # 現在のシーンを更新する
        self.scenes[self.scene_name].update()

    # ゲームを描画する
    def draw(self):
        # 現在のシーンを描画する
        self.scenes[self.scene_name].draw()
