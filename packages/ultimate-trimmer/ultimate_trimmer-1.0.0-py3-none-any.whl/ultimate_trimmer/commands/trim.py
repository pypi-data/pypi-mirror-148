import argparse

from ultimate_trimmer.core import trimVideoWithCSV
from ultimate_trimmer.logger import Logger
from ultimate_trimmer.option import Option


def ultrim():
    parser = argparse.ArgumentParser(description="ビデオを切り抜くスクリプトです。CSVファイルを引数に指定してください。")
    parser.add_argument("csv", help="切り抜きのCSVファイルを指定してください。", nargs="*")
    parser.add_argument("--save", help="保存ディレクトリを指定してください。", default="trim/")
    parser.add_argument(
        "--expand", help="クリップの前後の拡張秒数を指定してください。", default=[3, 3], nargs=2, type=int
    )
    parser.add_argument(
        "--altnum", help="タイトルを感想で代用する際の先頭文字数を指定してください。", default=5, type=int
    )
    args = parser.parse_args()

    csvnames = args.csv

    # オプションを設定
    Option.setOpt(args.save, args.expand, args.altnum)

    try:
        # 実行
        for i in range(len(csvnames)):
            csvname = csvnames[i]
            trimVideoWithCSV(i, csvname)
    except Exception as e:
        import traceback

        traceback.print_exc()
    finally:
        # 設定情報を出力
        Logger.write(Option.getInfo(), end="")

        print(Logger.getLog(), end="")
