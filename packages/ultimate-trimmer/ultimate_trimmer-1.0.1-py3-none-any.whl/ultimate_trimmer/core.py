import os, csv

from chardet import detect
from moviepy.editor import *
from ultimate_trimmer.logger import Logger
from ultimate_trimmer.trim_info import TrimInfo
from ultimate_trimmer.option import Option


def trimVideoWithCSV(video_number, csvname):
    Logger.write(f"- {csvname} 動画番号:{video_number}")

    # 入力チェック
    if not os.path.exists(csvname):
        Logger.write(f"  Error: CSVファイルが見つかりませんでした。")
        return

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
    while True:
        if head >= len(trim_infos):
            Logger.write("  Error: 試合動画ファイルが見つかりませんでした。")
            return
        if len(trim_infos[head]) > 0 and os.path.exists(trim_infos[head][0].strip()):
            videoname = trim_infos[head][0].strip()
            head += 1
            break
        head += 1

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
        filename = trim_info.toFilename(video_number, ext)
        save_path = os.path.join(Option.save_dir, filename)

        # 同名のクリップ動画が存在する場合はクリップを生成しない
        if os.path.exists(save_path):
            Logger.write("既にクリップが作成されています。")
            head += 1
            continue

        # クリップ生成
        isSuccess = trimVideo(trim_info, videoname, save_path)
        if isSuccess:
            Logger.write(f"{filename}に保存されました。")
        else:
            Logger.write(f"{filename}動画のトリミング中にエラーが発生しました。")

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
            return False
        if end < 0:
            return False
        if start >= end:
            return False

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
        return False
    finally:
        if video != None:
            video.close()
    return True
