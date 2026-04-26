# エンティティ(キャラクター)モジュール

# entitiesフォルダのクラスを__init__.pyでインポートすることで
#   from entities.player import Player
# のようにクラスを個別にインポートする代わりに
#   from entities import Player, Enemy1, Enemy2, Enemy3
# のようにまとめてインポートできるようにする

from .player import Player          # プレイヤークラス
from .zako1 import Zako1            # 敵クラス
from .boss import Boss              # ボスクラス
