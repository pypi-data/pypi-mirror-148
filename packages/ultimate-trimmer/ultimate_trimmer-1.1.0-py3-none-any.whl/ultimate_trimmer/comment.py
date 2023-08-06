import re

from ultimate_trimmer.logger import Logger
from ultimate_trimmer.utils import tryParseSeconds

column_pattern = r"[<＜]([^<>＜＞]+)[>＞]([^<>＜＞]+)"
startend_name_pattern = r"秒数指定"
tag_name_pattern = r"タグ付け"
impressions_name_pattern = r"コメント欄"
time_pattern = r"[0-9]+:[0-9]+:[0-9]+|[0-9]+:[0-9]+"
tag_pattern = r"#([^#\s]+)"


def parseError(comment_str, columns):
    Logger.write(f"パースエラー\ncomment: {comment_str}\nparsed: {columns}")


class Comment:
    @classmethod
    def fromStr(cls, comment_str):
        data = {}
        columns = re.findall(column_pattern, comment_str)
        for column in columns:
            if len(column) != 2:
                parseError(comment_str, columns)
                return None
            name, value = column

            # 開始時間と終了時間をパース
            if re.search(startend_name_pattern, name):
                times = re.findall(time_pattern, value)
                if len(times) < 2:
                    parseError(comment_str, columns)
                    return None
                data["start"] = tryParseSeconds(times[0])
                data["end"] = tryParseSeconds(times[1])
            # タグをパース
            elif re.search(tag_name_pattern, name):
                tags = re.findall(tag_pattern, value)
                data["tags"] = tags
            # 感想をパース
            elif re.search(impressions_name_pattern, name):
                data["impressions"] = value.strip()
        if (
            "start" not in data
            or "end" not in data
            or "tags" not in data
            or "impressions" not in data
            or data["start"] == None
            or data["end"] == None
        ):
            parseError(comment_str, columns)
            return None
        return cls(data["start"], data["end"], data["tags"], data["impressions"])

    def __init__(self, start, end, tags, impressions):
        self.start = start
        self.end = end
        self.tags = tags
        self.impressions = impressions

    @staticmethod
    def getHead():
        return ["開始", "終了", "属性", "感想"]

    def toCSVRow(self):
        tagstr = " ".join(self.tags)
        return [self.start, self.end, tagstr, self.impressions]

    def __repr__(self):
        tagstr = " ".join(self.tags)
        return f"<{self.start}~{self.end}, tags: {tagstr}, impressions: {self.impressions}>"

    def __str__(self):
        return self.__repr__()
