import pyxel

# クリア画面クラス
class ClearScene:
    # クリア画面を初期化する
    def __init__(self, game):
        self.game = game

    # クリア画面を開始する
    def start(self):
        # 画面表示時間を設定する
        self.display_timer = 60

    # クリア画面を更新する
    def update(self):
        # クリア画面の表示時間を設定する
        if self.display_timer > 0:  # 画面表示時間が残っている時
            self.display_timer -= 1
        else:                       # 画面表示時間が0になった時
            self.game.change_scene("title")

    # クリア画面を描画する
    def draw(self):
        # 画面をクリアする
        pyxel.cls(0)
        # テキストを描画する
        pyxel.text(43, 64, "CREAR", 8)
