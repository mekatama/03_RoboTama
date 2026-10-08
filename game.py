import pyxel
from scenes import GameOverScene, PlayScene, TitleScene, ClearScene
from constants import SCROLL_SPEED

# ゲームクラス
class Game:
    # ゲームを初期化する
    def __init__(self):
        # Pyxelを初期化する
        pyxel.init(128, 128, title="master")
        # リソースファイルを読み込む
        pyxel.load("assets/my_resource20.pyxres")
        pyxel.tilemaps[5].blt(0, 0, 3, 0, 0, 256, 16)  # 変更前のマップ[3]を未使用[5]にコピーする
        # ゲームの状態を初期化する
        self.player = None          # プレイヤー
        self.player_bullets = []    # 自機の弾のリスト
        self.enemies = []           # 敵のリスト
        self.enemy_bullets = []     # 敵の弾のリスト
        self.particles = []         # 破壊時particleのリスト
        self.items = []             # itemのリスト
        self.ui_points = []         # UIポイント表示のリスト

        self.scenes = {                     # シーンの辞書
            "title": TitleScene(self),
            "play": PlayScene(self),
            "gameover": GameOverScene(self),
            "clear": ClearScene(self),
        }
        self.scene_name = None  # 現在のシーン名
        self.screen_x = 0  # フィールド表示範囲の左端のX座標
        self.score = 0  # 得点
        self.isBoss1Kill = False    # Boss1死亡flag
        self.isBoss2Kill = False    # Boss2死亡flag
        self.cam_x = 0              # 多重スクロール用
        self.old_cam_x = 0          # 多重スクロール用
        self.far_x = 0          # 多重スクロール用(遠景)
        self.far2_x = 0          # 多重スクロール用(遠景)
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
        # 多重スクロール
        # プレイヤー追従
        target_cam_x = self.player.x
#        target_cam_x = self.player.x - 60
        if target_cam_x < 0:
            target_cam_x = 0
        # 右移動時のみカメラを更新
        if target_cam_x > self.cam_x:
            self.cam_x = target_cam_x
        #この1フレームの間に、カメラが何ピクセル右に動いたかを計算
        cam_delta = self.cam_x - self.old_cam_x
        # カメラが右に動いた時（cam_delta > 0）だけ、背景の位置を係数倍して進める
        # カメラが左に戻っている時は cam_delta が 0 になるため、背景の位置も完全にピタッとその場で止まります。
        if cam_delta > 0:
            self.far_x -= cam_delta * 0.1  # 0.1倍の速さで動く
            self.far2_x -= cam_delta * 0.2 # 0.2倍の速さで動く
        # 次のフレームのために今のカメラ位置を保存
        self.old_cam_x = self.cam_x

        draw_x1 = self.far_x
        draw_x2 = self.far2_x
        pyxel.bltm(draw_x1, 0, 2, self.screen_x, 0, 256, 128, 15)     # 奥BG
        pyxel.bltm(draw_x2, 0, 4, self.screen_x, 0, 256, 128, 15)     # 奥BG
        pyxel.bltm(0, 0, 3, self.screen_x, 0, 128, 128, 15)  # 手前BG(0番抜け色)

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
    # itemを描画する
    def draw_items(self):
        # カメラ位置(描画の原点)を変更する
        pyxel.camera(self.screen_x, 0)
        # 描画
        for item in self.items:
            item.draw()
        # カメラ位置を戻す
        pyxel.camera()
    # ui_pointを描画する
    def draw_ui_points(self):
        # カメラ位置(描画の原点)を変更する
        pyxel.camera(self.screen_x, 0)
        # 描画
        for ui_point in self.ui_points:
            ui_point.draw()
        # カメラ位置を戻す
        pyxel.camera()

    # ゲームを更新する
    def update(self):
        # 現在のシーンを更新する
        self.scenes[self.scene_name].update()

    # ゲームを描画する
    def draw(self):
        # 現在のシーンを描画する
        self.scenes[self.scene_name].draw()
