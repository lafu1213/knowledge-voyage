import sys, json, importlib, glob
sys.path.insert(0, '.')
from zy import zy_line
import intro
STATIONS = [(1, "初唐啟航港", "🌱"), (2, "田園邊塞灣", "🏞️"), (3, "詩佛竹林", "🎋"), (4, "詩仙月光島", "🌙"), (5, "詩聖草堂", "🏡"),
            (6, "楓橋夜泊港", "⛵"), (7, "中唐名家岬", "🍂"), (8, "白居易西湖", "🌊"), (9, "杜牧江南岸", "🏯"), (10, "晚唐夕照灣", "🌇")]
THEME = {"山水": "山水田園", "田園": "山水田園", "四季": "四季景物", "思鄉": "思鄉思親", "思念": "思鄉思親", "親情": "思鄉思親",
         "送別": "送別友情", "友情": "送別友情", "懷古": "懷古懷舊", "懷舊": "懷古懷舊", "憂國": "社會憂國", "社會": "社會憂國",
         "抒懷": "抒懷言志", "哲理": "抒懷言志", "志向": "抒懷言志", "童趣": "童趣民俗", "音樂": "童趣民俗", "民歌": "童趣民俗", "神話": "童趣民俗",
         "詠物": "詠物", "邊塞": "邊塞", "節令": "節令"}
poems, authors = [], {}
for f in sorted(glob.glob('poems*.py')):
    m = importlib.import_module(f[:-3])
    authors.update(m.AUTHORS)
    for p in m.POEMS:
        over = p.get('zy', {})
        q = {k: p[k] for k in ('n', 't', 'a', 'era', 'form', 'theme', 'style', 'lines', 'notes', 'trans', 'appr', 'scene')}
        q['sub'] = p.get('sub', '')
        q['tag'] = p['theme']
        q['theme'] = THEME.get(p['theme'], p['theme'])
        q['zy'] = [zy_line(l, over) for l in p['lines']]
        q['tzy'] = zy_line(p['t'], over); q['azy'] = zy_line(p['a'], p.get('azy', {}))
        q['qs'] = [list(x) for x in p['qs']]
        poems.append(q)
poems.sort(key=lambda p: p['n'])
for p in poems:
    assert all(len(l) == len(z) for l, z in zip(p['lines'], p['zy']))
    for x in p['qs']: assert 0 <= x[2] < len(x[1]) == 4, (p['n'], x[0])
data = {"lessons": intro.LESSONS, "quiz": [list(x) for x in intro.QUIZ], "authors": authors,
        "stations": [{"n": n, "name": nm, "icon": ic} for n, nm, ic in STATIONS], "poems": poems}
out = "// 唐詩島資料（由 tools/tang/build.py 產生）：入門課程、100 首唐詩（注音、注釋、翻譯、賞析、閱讀測驗）\nwindow.TANG = " + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ";\n"
open(sys.argv[1], 'w').write(out)
print(len(poems), "poems,", sum(len(p['qs']) for p in poems), "questions,", len(intro.QUIZ), "intro qs,", len(out)//1024, "KB")
