import pyxel

# タイトル画面クラス
class TitleScene:
    # タイトル画面を初期化する
    def __init__(self, game):
        self.game = game  # ゲームクラス

    # タイトル画面を開始する
    def start(self):
        # 自機を削除する
        self.player = None  # プレイヤーを削除
        # 全ての弾と敵とアイテムを削除する

    def update(self):
        # キー入力をチェックする
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            # プレイ画面に切り替える
            self.game.change_scene("play")

    def draw(self):
        # 画面をクリアする
        pyxel.cls(0)
        # テキストを描画する
        pyxel.text(0, 20, "--------------------------------", 7)
        pyxel.text(48, 24, "SKY BOX", 7)
        pyxel.text(0, 28, "--------------------------------", 7)
        pyxel.text(32, 40, "> PRESS ENTER <", 6)
