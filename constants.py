# 定数モジュール
SCROLL_SPEED = 1        # スクロールspeed
GRAVITY = 0.1           # 
#GRAVITY = 0.12           # 
TERMINAL_VELOCITY = 80  # 

# プレイヤーがこの座標を超えたらスクロールさせる
SCROLL_BORDER_X = 40      # スクロール境界

# タイル種別
TILE_NONE = 0  # 何もない
TILE_GEM = 1  # 宝石
TILE_EXIT = 2  # 出口
TILE_SPIKE = 4  # ダメージ
TILE_WALL = 5  # ダメージ
TILE_ROAD = 6  # すり抜け床
TILE_ENEMY1_POINT = 7  # E_Maton出現位置
TILE_ENEMY2_POINT = 8  # E_Maton_ATK_N出現位置
TILE_ENEMY3_POINT = 9  # E_Maton_ATK_H出現位置
TILE_ENEMY4_POINT = 10 # E_Ugokun出現位置
TILE_ENEMY5_POINT = 11 # E_Maton_ATK_P出現位置
TILE_ENEMY6_POINT = 12 # E_Noppo出現位置
TILE_ENEMY7_POINT = 13 # E_Tobun出現位置
TILE_ENEMY8_POINT = 14 # E_Hakobun出現位置
TILE_BOSS1_POINT = 20  # BOSS1出現位置

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
    (5, 2): TILE_WALL,
    (1, 3): TILE_WALL,
    (2, 3): TILE_WALL,
    (1, 4): TILE_WALL,
    (1, 5): TILE_WALL,
    (1, 6): TILE_ROAD,
    (0, 10): TILE_ENEMY1_POINT,
    (0, 11): TILE_ENEMY2_POINT,
    (0, 12): TILE_ENEMY3_POINT,
    (0, 13): TILE_ENEMY4_POINT,
    (0, 14): TILE_ENEMY5_POINT,
    (0, 15): TILE_ENEMY6_POINT,
    (0, 16): TILE_ENEMY7_POINT,
    (0, 17): TILE_ENEMY8_POINT,
    (0, 18): TILE_BOSS1_POINT,
}
# このテーブルにないタイルはTILE_NONEとして判定する
