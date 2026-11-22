import re
from pypinyin import pinyin, Style, load_phrases_dict
PUNCT = set("，。？！、；：「」（）")
# 臺灣教育部讀音（和大陸普通話不同的字）
TW = {"微":"ㄨㄟˊ","危":"ㄨㄟˊ","帆":"ㄈㄢˊ","期":"ㄑㄧˊ","夕":"ㄒㄧˋ","息":"ㄒㄧˊ","惜":"ㄒㄧˊ","昔":"ㄒㄧˊ","擊":"ㄐㄧˊ","寂":"ㄐㄧˋ","跡":"ㄐㄧ","迹":"ㄐㄧ","質":"ㄓˊ","擁":"ㄩㄥˇ",
      "暫":"ㄓㄢˋ","液":"ㄧˋ","涯":"ㄧㄚˊ","慨":"ㄎㄞˇ","雀":"ㄑㄩㄝˋ","研":"ㄧㄢˊ","企":"ㄑㄧˋ","溪":"ㄒㄧ","伺":"ㄙˋ","髮":"ㄈㄚˇ","癌":"ㄧㄢˊ","垃":"ㄌㄜˋ","蝸":"ㄍㄨㄚ","偶":"ㄡˇ","骰":"ㄊㄡˊ","殼":"ㄎㄜˊ","識":"ㄕˋ","場":"ㄔㄤˊ","泊":"ㄅㄛˊ","似":"ㄙˋ","藉":"ㄐㄧㄝˋ","盡":"ㄐㄧㄣˋ","鸛":"ㄍㄨㄢˋ","彈":"ㄊㄢˊ","不":"ㄅㄨˋ","子":"ㄗˇ","誰":"ㄕㄟˊ"}
def zy_line(line, over=None):
    over = over or {}
    py = pinyin(line, style=Style.BOPOMOFO, errors=lambda x: [""]*len(x))
    out = []
    for i, ch in enumerate(line):
        if ch in PUNCT: out.append(""); continue
        z = py[i][0] if i < len(py) else ""
        if ch in TW: z = TW[ch]
        if ch in over: z = over[ch]
        if (i, ch) in over: z = over[(i, ch)]
        out.append(z)
    return out
