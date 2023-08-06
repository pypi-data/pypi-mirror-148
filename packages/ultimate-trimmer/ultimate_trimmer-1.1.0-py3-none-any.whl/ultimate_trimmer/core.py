import os, csv, re
import requests
import configparser
import urllib.parse as parse

from chardet import detect
from moviepy.editor import *
from ultimate_trimmer.logger import Logger
from ultimate_trimmer.trim_info import TrimInfo
from ultimate_trimmer.option import Option
from ultimate_trimmer.comment import Comment


def trimVideoWithCSV(csvname):
    Logger.write(f"- {csvname}", end="")

    # 入力チェック
    if not os.path.exists(csvname):
        Logger.write(f"\n  Error: CSVファイルが見つかりませんでした。")
        return

    # CSVファイルのディレクトリ
    csv_dir = os.path.dirname(os.path.abspath(csvname))

    # 文字コード判別
    with open(csvname, "rb") as f:
        b = f.read()
    encoding = detect(b)["encoding"]

    # トリミングデータの読み込み
    with open(csvname, encoding=encoding) as f:
        reader = csv.reader(f)
        trim_infos = [row for row in reader]

    # 動画ファイルを見つける
    head = 0
    videoname = ""
    video_id = ""
    while True:
        if head >= len(trim_infos):
            Logger.write("\n  Error: 試合動画ファイルが見つかりませんでした。")
            return
        if len(trim_infos[head]) < 2:
            head += 1
            continue
        videoname_tmp = trim_infos[head][0].strip()
        # 相対パスの場合はcsv_dirからパスを計算する
        if not os.path.isabs(videoname_tmp):
            videoname_tmp = os.path.abspath(os.path.join(csv_dir, videoname_tmp))
        # パスが存在するかチェック
        if os.path.exists(videoname_tmp):
            # 試しに動画ファイルとして開いてみる
            try:
                VideoFileClip(videoname_tmp)
            except:
                head += 1
                continue
            videoname = videoname_tmp
            video_id = trim_infos[head][1].strip()
            head += 1
            break
        head += 1

    Logger.write(f" 動画ID:{video_id}")

    # 動画ファイルの拡張子を取得
    try:
        ext = os.path.splitext(videoname)[1]
    except:
        Logger.write(f"  Error: 動画ファイル名の拡張子が見つかりませんでした。")
        return

    # 保存ディレクトリの作成
    if not os.path.exists(Option.save_dir):
        os.mkdir(Option.save_dir)

    # 各行を解析して指定部分のクリップ動画を保存
    while True:
        # ファイルの最後に到達したら終了
        if head >= len(trim_infos):
            return
        # LOG
        Logger.write(f"  {head + 1}行目：", end="")

        # 行の解析
        trim_info = TrimInfo.fromList(trim_infos[head])
        if trim_info == None or not trim_info.is_valid:
            Logger.write(f"フォーマットエラーでスキップされました。")
            head += 1
            continue

        # ファイル名変換
        filename = trim_info.toFilename(video_id, ext)
        save_path = os.path.join(Option.save_dir, filename)

        # 同名のクリップ動画が存在する場合はクリップを生成しない
        if os.path.exists(save_path):
            Logger.write("既にクリップが作成されています。")
            head += 1
            continue

        # クリップ生成
        isSuccess, mes = trimVideo(trim_info, videoname, save_path)
        if isSuccess:
            Logger.write(f"保存されました。ファイル名: {filename}")
        else:
            Logger.write(f"トリミングできませんでした。{mes}")

        # 次の行へ
        head += 1


# 動画をトリミングする
# 成功：True，失敗：False
def trimVideo(trim_info, videoname, output):
    video = None
    try:
        start = trim_info.start - Option.trim_expansion[0]
        end = trim_info.end + Option.trim_expansion[1]

        video = VideoFileClip(videoname)

        # クリップ生成が出来ない場合は失敗
        if start >= video.duration:
            return False, "開始時間が動画時間を越しています。"
        if end < 0:
            return False, "終了時間が0秒以下です。"
        if start >= end:
            return False, "終了時間が開始時間よりも前です。"

        # 動画の長さを超える場合は収まるように秒数を変更
        if start < 0:
            start = 0
        if end > video.duration:
            end = video.duration

        video.subclip(start, end).write_videofile(
            output,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
        )
    except Exception as e:
        print(e)
        return False, "原因不明のエラーが発生しました。"
    finally:
        if video != None:
            video.close()
    return True, ""


def getUserConfig():
    rc_path = os.path.join(os.path.expanduser("~"), ".ultrimrc")
    config = configparser.ConfigParser()
    save_flag = False

    # ファイルがある場合は読み込む
    if os.path.exists(rc_path):
        config.read(rc_path)

    data = config["BASE"] if "BASE" in config else {}

    # 足りない設定をユーザ入力で取得
    if "API_KEY" not in data:
        data["API_KEY"] = input("API KEY >")
        save_flag = True

    if save_flag:
        config["BASE"] = data
        with open(rc_path, "w", encoding="utf=8") as f:
            config.write(f)

    return data


movie_id_pattern = (
    r"https://www.youtube.com/watch\?v=([^&]+)[&.*]*|https://youtu.be/([^&]+)[&.*]*"
)


def getMovieId(movie_url):
    mached = re.match(movie_id_pattern, movie_url)
    movie_id = None
    if mached:
        for m in mached.groups():
            if m:
                movie_id = m
    return movie_id


def downloadComments(movie_url, csvname, config):
    movie_id = getMovieId(movie_url)
    if not movie_id:
        movie_id = movie_url

    comments = [Comment.getHead()]
    ext_comments = [["コメント", "ユーザ名"]]

    # Youtube APIを使用してコメントを取得
    API_KEY = config["API_KEY"]
    URL_HEAD = "https://www.googleapis.com/youtube/v3/commentThreads?"
    nextPageToken = ""
    exe_num = 1  # 最大回数(一度に100件取得)
    for _ in range(exe_num):
        # APIパラメータセット
        param = {
            "key": API_KEY,
            "part": "snippet",
            "videoId": movie_id,
            "maxResults": "100",
            "moderationStatus": "published",
            "order": "relevance",
            "pageToken": nextPageToken,
            "searchTerms": "",
            "textFormat": "plainText",
        }
        # データ取得
        res = requests.get(URL_HEAD + (parse.urlencode(param))).json()
        # データが取得できたかチェック
        if "items" not in res:
            Logger.write("コメントを取得できませんでした。コメントが付いていないか、動画IDが間違っている可能性があります。")
            return
        # コメント情報をパース
        for item in res["items"]:
            comment = Comment.fromStr(
                str(item["snippet"]["topLevelComment"]["snippet"]["textOriginal"])
            )
            if comment:
                comments.append(comment.toCSVRow())
            else:
                ext_comments.append(
                    [
                        str(
                            item["snippet"]["topLevelComment"]["snippet"][
                                "textOriginal"
                            ]
                        ),
                        str(
                            item["snippet"]["topLevelComment"]["snippet"][
                                "authorDisplayName"
                            ]
                        ),
                    ]
                )
        # nextPageTokenがなくなったら処理ストップ
        if "nextPageToken" in res:
            nextPageToken = res["nextPageToken"]
        else:
            break

    # Commentを開始時間と終了時間でソート
    comments = [comments[0]] + sorted(comments[1:], key=lambda v: (v[0], v[1]))

    # CSVに保存
    movie_info = [["動画ファイル名", "動画ID"], ["", movie_id]]
    with open(csvname, "w", encoding="SJIS", newline="", errors="replace") as f:
        writer = csv.writer(f)
        writer.writerows(movie_info + [""] + comments + [""] + ext_comments)
    Logger.write(f"{len(comments) + len(ext_comments) - 2}件のコメントが{csvname}に保存されました。")
