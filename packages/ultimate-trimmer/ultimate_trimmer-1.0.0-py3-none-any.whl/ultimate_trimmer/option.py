class Option:
    # 保存ディレクトリ
    save_dir = "trim/"
    # トリミングを前後何秒間拡張するか指定
    trim_expansion = [3, 3]
    # タイトル未指定の場合に使用する感想の先頭文字数
    alt_impression_head = 5
    # ファイル名に使用不可の文字を設定
    bad_pattern = (
        r"\\|\/|:|\*|\?|\"|>|<|\||&|\(|\)|\[|\]|\{|\}|\^|=|;|!|'|\+|,|`|~|\r|\n|\r\n"
    )

    @classmethod
    def setOpt(cls, save_dir, trim_expansion, alt_impression_head):
        cls.setSaveDir(save_dir)
        cls.setTrimExpansion(trim_expansion)
        cls.setAltImpressionHead(alt_impression_head)

    @classmethod
    def setSaveDir(cls, save_dir):
        cls.save_dir = save_dir

    @classmethod
    def setTrimExpansion(cls, trim_expansion):
        cls.trim_expansion = trim_expansion

    @classmethod
    def setAltImpressionHead(cls, alt_impression_head):
        cls.alt_impression_head = alt_impression_head

    @classmethod
    def getInfo(cls):
        return (
            f"【Option】\n"
            + f"保存ディレクトリ: {cls.save_dir}\n"
            + f"トリミング拡張: {cls.trim_expansion[0]}秒 <> {cls.trim_expansion[0]}秒\n"
            + f"感想代用時の先頭文字数: {cls.alt_impression_head}\n"
        )
