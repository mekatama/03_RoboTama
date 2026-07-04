# title: Pyxel Platformer
# author: Takashi Kitao
# desc: A Pyxel platformer example
# site: https://github.com/kitao/pyxel
# license: MIT
# version: 1.0

import pyxel

TRANSPARENT_COLOR = 2
SCROLL_BORDER_X = 80
TILE_FLOOR = (1, 0)     # 下から登れる床
WALL_TILE_X = 4         # 壁全般

scroll_x = 0
player = None

# 指定した座標のタイル種別を取得する
def get_tile(tile_x, tile_y):
    return pyxel.tilemaps[0].pget(tile_x, tile_y)

# キャラクターが壁と重なっているか判定する
def is_colliding(x, y, is_falling):
    # キャラの４角
    x1 = pyxel.floor(x) // 8
    y1 = pyxel.floor(y) // 8
    x2 = (pyxel.ceil(x) + 7) // 8
    y2 = (pyxel.ceil(y) + 7) // 8

    # 壁との接触判定
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if get_tile(xi, yi)[0] >= WALL_TILE_X:
                print("!!!")
                return True

    # 落下中 and y座標が8ドット単位ピッタリの時
    # これかも！！
    if is_falling and y % 8 == 1:
        for xi in range(x1, x2 + 1):
            if get_tile(xi, y1 + 1) == TILE_FLOOR:
                print("!")
                return True

    return False # 壁と床に衝突していない

# 押し戻した座標を返す
def push_back(x, y, dx, dy):
    for _ in range(pyxel.ceil(abs(dy))):
        step = max(-1, min(1, dy))
        if is_colliding(x, y + step, dy > 0):
            # 接触しているので処理終了
            break
        # ここで落下処理を実行している
        y += step
        dy -= step

    for _ in range(pyxel.ceil(abs(dx))):
        step = max(-1, min(1, dx))
        if is_colliding(x + step, y, dy > 0):
            # 接触しているので処理終了
            break
        x += step
        dx -= step

    return x, y


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.direction = 1
        self.is_falling = False

    def update(self):
        global scroll_x
        last_y = self.y     # 落下中判定用

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.dx = -2
            self.direction = -1
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.dx = 2
            self.direction = 1

        self.dy = min(self.dy + 1, 3)

        # jump
        # 接地時のみ判定が無い
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.dy = -6

        # 押し戻した
        self.x, self.y = push_back(self.x, self.y, self.dx, self.dy)

        # スクロール用
        if self.x < scroll_x:
            self.x = scroll_x

        # 横方向の移動を減速する
        self.dx = int(self.dx * 0.8)

        # 直前のy座標と比較して、落下flag判定
        if self.y > last_y:
            self.is_falling = True
        else:
            self.is_falling = False

        # スクロール
        if self.x > scroll_x + SCROLL_BORDER_X:
            last_scroll_x = scroll_x
            scroll_x = min(self.x - SCROLL_BORDER_X, 240 * 8)

    def draw(self):
        u = (2 if self.is_falling else pyxel.frame_count // 3 % 2) * 8
        w = 8 if self.direction > 0 else -8
        pyxel.blt(self.x, self.y, 0, u, 16, w, 8, TRANSPARENT_COLOR)

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Pyxel Platformer")
        pyxel.load("assets/platformer.pyxres")

        global player
        player = Player(0, 0)

        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        player.update()

    def draw(self):
        pyxel.cls(0)

        # Draw level
        pyxel.camera()
        pyxel.bltm(0, 0, 0, (scroll_x // 4) % 128, 128, 128, 128)
        pyxel.bltm(0, 0, 0, scroll_x, 0, 128, 128, TRANSPARENT_COLOR)

        # Draw characters
        pyxel.camera(scroll_x, 0)
        player.draw()

App()
