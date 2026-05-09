# 定数モジュール
SCROLL_SPEED = 1  # スクロールspeed

# プレイヤーがこの座標を超えたらスクロールさせる
SCROLL_BORDER_X = 80      # スクロール境界

# タイル種別
TILE_NONE = 0  # 何もない
TILE_GEM = 1  # 宝石
TILE_EXIT = 2  # 出口
TILE_SPIKE = 4  # ダメージ
TILE_WALL = 5  # ダメージ
TILE_ROAD = 6  # すり抜け床
TILE_ENEMY1_POINT = 7  # ENEMY1出現位置
TILE_ENEMY2_POINT = 8  # ENEMY2出現位置
TILE_ENEMY3_POINT = 9  # ENEMY3出現位置
TILE_ENEMY4_POINT = 10 # ENEMY4出現位置

# タイル→タイル種別変換テーブル
TILE_TO_TILETYPE = {
    (1, 0): TILE_GEM,
    (2, 0): TILE_EXIT,
#    (3, 0): TILE_BOMB,
    (4, 0): TILE_SPIKE,
    (1, 2): TILE_WALL,
    (2, 2): TILE_WALL,
    (3, 2): TILE_WALL,
    (4, 2): TILE_WALL,
    (1, 3): TILE_WALL,
    (2, 3): TILE_WALL,
    (1, 4): TILE_WALL,
    (1, 5): TILE_WALL,
    (1, 6): TILE_ROAD,
    (0, 10): TILE_ENEMY1_POINT,
    (0, 11): TILE_ENEMY2_POINT,
    (0, 12): TILE_ENEMY3_POINT,
    (0, 13): TILE_ENEMY4_POINT,
}
# このテーブルにないタイルはTILE_NONEとして判定する
