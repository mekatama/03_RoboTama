# エンティティ(キャラクター)モジュール

# entitiesフォルダのクラスを__init__.pyでインポートすることで
#   from entities.player import Player
# のようにクラスを個別にインポートする代わりに
#   from entities import Player, Enemy1, Enemy2, Enemy3
# のようにまとめてインポートできるようにする

from .player import Player                  # プレイヤークラス
from .player2 import Player2                # newプレイヤークラス
from .enemy1 import Enemy1                  # 旧敵クラス
from .e_maton import E_Maton                # 敵クラス(固定敵_攻撃なし)
from .e_maton_atk_n import E_Maton_ATK_N    # 敵クラス(固定敵_攻撃_横)
from .e_maton_atk_h import E_Maton_ATK_H    # 敵クラス(固定敵_攻撃_狙う)
from .e_maton_atk_p import E_Maton_ATK_P    # 敵クラス(固定敵_攻撃_放物線)
from .e_ugokun import E_Ugokun              # 敵クラス(前進敵_攻撃なし)
from .e_noppo import E_Noppo                # 敵クラス(縦長敵_攻撃なし)
from .e_tobun import E_Tobun                # 敵クラス(飛行敵_攻撃なし)
from .e_hakobun import E_Hakobun            # 敵クラス(輸送敵_攻撃なし)
from .e_maton_carry import E_Maton_Carry    # 敵クラス(運ばれる敵_攻撃_横)
from .e_boss_1 import E_Boss_1              # 敵クラス(ボス1)
