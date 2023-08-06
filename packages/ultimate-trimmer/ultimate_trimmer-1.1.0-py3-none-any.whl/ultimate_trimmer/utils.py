# 文字列を10進数整数に変換する
# 失敗したらNone
def tryParseInt(s):
    try:
        parsed = int(s, 10)
    except ValueError:
        return None
    return parsed


# %H:%M:%S形式の時間を秒数に変換する
# 失敗したらNone
# 対応形式
# %S
# %M:%S
# %H:%M:%S
def tryParseSeconds(s):
    hours = 0
    minutes = 0
    seconds = 0

    ss = s.split(":")

    # %Sの場合
    if len(ss) == 1:
        seconds = tryParseInt(ss[0])

    # %M:%Sの場合
    elif len(ss) == 2:
        minutes = tryParseInt(ss[0])
        seconds = tryParseInt(ss[1])

    # %H:%M:%Sの場合
    elif len(ss) == 3:
        hours = tryParseInt(ss[0])
        minutes = tryParseInt(ss[1])
        seconds = tryParseInt(ss[2])

    # フォーマットに合わないので破棄
    else:
        return None

    # チェック
    if hours == None or minutes == None or seconds == None:
        return None

    return hours * 3600 + minutes * 60 + seconds
