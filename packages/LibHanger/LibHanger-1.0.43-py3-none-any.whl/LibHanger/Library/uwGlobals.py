import LibHanger.Library.uwLogger as Logger
from LibHanger.Library.uwConfig import cmnConfig

class globalValues:

    """
    オブジェクト共有クラス
    """

    def __init__(self):
        
        """
        コンストラクタ
        """

        self.config = None
        """ 共通設定 """

        self.platForm = self.platFormStruct()
        """ プラットフォーム構造体 """

    class platFormStruct:

        """
        プラットフォーム構造体クラス
        """

        def __init__(self):

            """
            コンストラクタ
            """

            self.win = 'Windows'
            """ Windows """

            self.mac = 'Darwin'
            """ Mac """

            self.linux = 'Linux'
            """ Linux """

# インスタンス生成(import時に実行される)
gv = globalValues()

def configer(__file__):
    
    # 共通設定(ノーマル)
    ccfg = cmnConfig()
    ccfg.getConfig(__file__, 'TestConfig')

    # ロガー設定
    Logger.setting(ccfg)

    # 共通設定
    gv.config = ccfg
