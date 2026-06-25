import pyxel

# UI数字表示クラス
class Ui_Point:
    #定数

    # アイテムを初期化してゲームに登録する
    def __init__(self, game, x, y, score):
        self.x = x
        self.y = y
        self.score = score
        self.count = 0
        self.is_alive = True

    def update(self):
        self.count += 1
        if self.count < 20:
            self.y -= 0.7
        elif self.count >= 20 and self.count < 40:
            pass
        elif self.count >= 40:
            self.is_alive = False
    def draw(self):
        pyxel.text(self.x, self.y, f"+{self.score:2}", 13)
