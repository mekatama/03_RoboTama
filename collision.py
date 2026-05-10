# 衝突処理モジュール
import pyxel
from constants import TILE_NONE, TILE_TO_TILETYPE, TILE_WALL, TILE_ROAD

# 指定した座標のタイル種別を取得する
def get_tile_type(x, y):
    tile = pyxel.tilemaps[0].pget(x // 8, y // 8)
    return TILE_TO_TILETYPE.get(tile, TILE_NONE)

# 指定した座標が壁と重なっているか判定する
def in_collision(x, y):
    return get_tile_type(x, y) == TILE_WALL

# 指定した座標がすり抜け床と重なっているか判定する
def in_collision2(x, y):
    return get_tile_type(x, y) == TILE_ROAD

# キャラクターが壁と重なっているか判定する
def is_character_colliding(x, y, isRise):
    # キャラクターと重なっているタイル座標の領域を計算する
    x1 = pyxel.floor(x) // 8
    y1 = pyxel.floor(y) // 8
    x2 = (pyxel.ceil(x) + 7) // 8
    y2 = (pyxel.ceil(y) + 7) // 8

    # TILE_ROADと頭上判定時は強制False
    if isRise == True:
        return False
    
    # タイル座標の領域が壁と重なっているかどうかを判定する
    for yi in range(y1, y2 + 1):
        for xi in range(x1, x2 + 1):
            if in_collision(xi * 8, yi * 8) or in_collision2(xi * 8, yi * 8):
                return True  # 壁 or すり抜け床 と衝突している

    return False  # 壁と衝突していない

# 押し戻した座標を返す
def push_back(x, y, dx, dy, isRise):
    # 壁と衝突するまで垂直方向に移動する
    for _ in range(pyxel.ceil(abs(dy))):
        step = max(-1, min(1, dy))
        if is_character_colliding(x, y + step, isRise):
            break
        y += step
        dy -= step

    # 壁と衝突するまで水平方向に移動する
    for _ in range(pyxel.ceil(abs(dx))):
        step = max(-1, min(1, dx))
        if is_character_colliding(x + step, y, isRise):
            break
        x += step
        dx -= step

    return x, y
