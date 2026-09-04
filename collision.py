# 衝突処理モジュール
import pyxel
from constants import TILE_NONE, TILE_TO_TILETYPE, TILE_WALL, TILE_ROAD

# 指定した座標のタイル種別を取得する
def get_tile_type(x, y):
    tile = pyxel.tilemaps[3].pget(x // 8, y // 8)
    return TILE_TO_TILETYPE.get(tile, TILE_NONE)

# 指定した座標が壁と重なっているか判定する
def in_collision(x, y):
    return get_tile_type(x, y) == TILE_WALL

# 指定した座標がすり抜け床と重なっているか判定する
def in_collision2(x, y):
    return get_tile_type(x, y) == TILE_ROAD

# キャラクターが壁と重なっているか判定する
def is_character_colliding(x, y, isFalling):
    # キャラクターと重なっているタイル座標の領域を計算する
    x1 = pyxel.floor(x) // 8
    y1 = pyxel.floor(y) // 8
    x2 = (pyxel.ceil(x) + 7) // 8
    y2 = (pyxel.ceil(y) + 7) // 8

    # タイル座標の領域が壁と重なっているかどうかを判定する
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            # TILE_WALLとの接触判定
            if in_collision(xi * 8, yi * 8):
                return True  # 壁と衝突している

    # 落下中 and y座標が8ドット単位ピッタリの時
    if isFalling and y % 8 == 1:
        for xi in range(x1, x2 + 1):
            # TILE_ROADとの接触判定
            if in_collision2(xi * 8, yi * 8):
                return True

    return False  # 壁と衝突していない

# 押し戻した座標を返す
def push_back(x, y, dx, dy, isFalling):
    # 壁と衝突するまで垂直方向に移動する
    for _ in range(pyxel.ceil(abs(dy))):
        step = max(-1, min(1, dy))
        if is_character_colliding(x, y + step, dy > 0):
            # 接触しているので処理終了 = 落下停止
            break

        # ここで落下処理を実行している
        y += step
        dy -= step

    # 壁と衝突するまで水平方向に移動する
    for _ in range(pyxel.ceil(abs(dx))):
        step = max(-1, min(1, dx))
        if is_character_colliding(x + step, y, dy > 0):
            # 接触しているので処理終了 = 左右移動停止
            break
        x += step
        dx -= step

    return x, y
