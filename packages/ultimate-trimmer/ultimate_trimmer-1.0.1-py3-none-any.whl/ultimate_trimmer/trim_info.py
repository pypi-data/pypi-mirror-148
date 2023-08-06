import re
from ultimate_trimmer.option import Option

from ultimate_trimmer.utils import tryParseSeconds


class TrimInfo:
    @classmethod
    def fromList(cls, l):
        if len(l) < 5:
            return None

        # 開始秒
        start = tryParseSeconds(l[0])
        if not start:
            return None

        # 終了秒
        end = tryParseSeconds(l[1])
        if not end:
            return None

        # 感想
        impression = l[4]
        if impression == "":
            impression = "特に感想はありません"

        # 属性
        tags = l[3].split()
        if len(tags) == 0:
            tags = ["NoTagged"]

        # タイトル
        title = re.sub(Option.bad_pattern, "", l[2])
        if title == "":
            title = impression[: Option.alt_impression_head]

        instance = cls(start, end, title, tags, impression)
        instance.validate()

        return instance

    def __init__(self, start, end, title, tags, impression):
        self.start = start
        self.end = end
        self.title = title
        self.tags = tags
        self.impression = impression

        # validation
        self.is_valid = self.validate()

    def validate(self):
        # 開始秒
        if type(self.start) is not int:
            return False

        # 終了秒
        if type(self.end) is not int:
            return False

        # タイトル
        title = re.sub(Option.bad_pattern, "", self.title)
        if title == "":
            return False

        # 属性
        if len(self.tags) == 0:
            return False

        return True

    def toFilename(self, video_number, ext):
        tagstr = "-".join(sorted(self.tags))
        filename = f"{video_number}_{self.start}_{self.title}_{tagstr}{ext}"
        return re.sub(Option.bad_pattern, "", filename)
