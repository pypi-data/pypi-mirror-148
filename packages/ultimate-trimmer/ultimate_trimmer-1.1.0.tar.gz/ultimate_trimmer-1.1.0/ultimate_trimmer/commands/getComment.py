import argparse

from ultimate_trimmer.core import downloadComments, getUserConfig
from ultimate_trimmer.logger import Logger


def ultcom():
    parser = argparse.ArgumentParser(
        description="Youtubeの動画についているコメントを取得してCSVにまとめるスクリプトです。"
    )
    parser.add_argument("url", help="コメントを取得する動画のURLまたは動画IDを指定してください。")
    parser.add_argument("--save", help="保存ファイル名を指定してください。", default="comments.csv")
    args = parser.parse_args()

    movie = args.url
    filename = args.save

    try:
        # 実行
        config = getUserConfig()
        downloadComments(movie, filename, config)
    except Exception as e:
        import traceback

        traceback.print_exc()
    finally:
        print(Logger.getLog(), end="")
