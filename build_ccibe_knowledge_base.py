from __future__ import annotations

import argparse
import html
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple
from xml.sax.saxutils import escape as xml_escape


CATEGORY_DIRS: Dict[str, str] = {
    "admission": "01_招生录取_分数线",
    "colleges": "02_学院与教学",
    "life": "03_校园生活_食堂宿舍",
    "admin": "04_行政服务机构",
    "calendar": "05_校历与规定",
    "traffic": "06_交通与地图",
    "culture": "07_校园文化",
    "personal": "08_个人整理文档",
    "pending": "09_待核实信息",
}

PERSONAL_SOURCE_DIRNAME = "已整理"
PERSONAL_MERGED_NAME = "来自个人文档.txt"
INDEX_NAME = "知识库索引.html"


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def append_text(path: Path, content: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(content)


def make_docx_document(path: Path, paragraphs: Sequence[str]) -> None:
    body = []
    for paragraph in paragraphs:
        safe = xml_escape(paragraph)
        if not safe:
            safe = ""
        body.append(
            "<w:p><w:r><w:t xml:space=\"preserve\">"
            + safe
            + "</w:t></w:r></w:p>"
        )
    body_xml = "".join(body) or "<w:p/>"
    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
 xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
 xmlns:v="urn:schemas-microsoft-com:vml"
 xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:w10="urn:schemas-microsoft-com:office:word"
 xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
 xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
 xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
 xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
 xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
 mc:Ignorable="w14 wp14">
  <w:body>
    {body_xml}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
      <w:cols w:space="720"/>
      <w:docGrid w:linePitch="360"/>
    </w:sectPr>
  </w:body>
</w:document>
"""
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
"""
    core = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>重庆对外经贸学院知识库</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
</cp:coreProperties>
"""
    app = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Office Word</Application>
</Properties>
"""
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", rels)
        archive.writestr("docProps/core.xml", core)
        archive.writestr("docProps/app.xml", app)
        archive.writestr("word/document.xml", document_xml)


def extract_docx_text(path: Path) -> str:
    try:
        import docx  # type: ignore

        document = docx.Document(str(path))
        text = "\n".join(p.text for p in document.paragraphs)
        return normalize_whitespace(text)
    except Exception:
        pass

    try:
        with zipfile.ZipFile(path) as archive:
            data = archive.read("word/document.xml").decode("utf-8", errors="ignore")
    except Exception as exc:
        return f"[无法读取 {path.name}: {exc}]"

    data = re.sub(r"</w:p>", "\n", data)
    data = re.sub(r"<[^>]+>", "", data)
    return normalize_whitespace(html.unescape(data))


KEYWORD_RULES: List[Tuple[str, List[str]]] = [
    ("life", ["食堂", "宿舍", "热水", "卫生间", "门禁", "关门", "卫浴", "洗衣机"]),
    ("traffic", ["交通", "地图", "校区地址", "路线", "公交", "地铁", "打车", "火车站", "机场", "客运中心"]),
    ("admission", ["分数线", "录取", "专升本", "高考", "招生"]),
    ("admin", ["教务处", "学生处", "保卫处", "后勤处", "图书馆", "招生办", "联系电话", "办公邮箱"]),
    ("calendar", ["校历", "假期", "学期", "规定", "放假"]),
    ("culture", ["校训", "精神", "文化", "活动", "作孚", "行知"]),
    ("colleges", ["学院", "专业", "教学", "教研", "教师"]),
]


def classify_personal_text(text: str, source_name: str = "") -> str:
    combined = f"{source_name}\n{text}".lower()
    best_category = "personal"
    best_score = 0
    for category, keywords in KEYWORD_RULES:
        score = sum(combined.count(keyword.lower()) for keyword in keywords)
        if source_name and any(keyword.lower() in source_name.lower() for keyword in keywords):
            score += 10
        if score > best_score:
            best_category = category
            best_score = score
    return best_category


@dataclass
class FileSpec:
    relative_dir: str
    filename: str
    content: str
    kind: str = "text"


def build_admission_doc() -> str:
    lines = [
        "重庆对外经贸学院 2025 年普通高考录取分数线（已自动整理的公开可解析部分）",
        "",
        "说明：",
        "1. 学校招生网已发布《重庆对外经贸学院2025年外省（市、区）录取分数》《重庆对外经贸学院2025年重庆本科批专业录取分数》，但当前公开页面主体以图片形式展示，自动解析不完整。",
        "2. 本文件先整理已能稳定读取的公开分数，供快速参考；其余省份见同目录待补充文件。",
        "3. 第三方汇总仅作索引，最终核对以学校招生网原始页面为准。",
        "",
        "公开可解析分数：",
        "- 河北：历史类最低 510 分，物理类最低 492 分。",
        "- 贵州：历史类最低 485 分，物理类最低 432 分。",
        "- 湖南：历史类最低 473 分，物理类最低 436 分。",
        "- 四川：历史类最低 504 分，物理类最低 463 分。",
        "- 海南：最低 500 分；其中公开摘要显示专业组 02 为 545 分、专业组 03 为 500 分。",
        "- 广西：历史类最低 425 分，物理类最低 395 分。",
        "- 宁夏：历史类最低 440 分，物理类最低 403 分。",
        "- 内蒙古：历史类最低 467 分，物理类最低 421 分。",
        "- 山西：历史类最低 477 分，物理类最低 436 分。",
        "- 重庆：历史类最低 449 分，物理类最低 437 分。",
        "",
        "已确认的官方来源：",
        "- 学校 2025 年普通高校招生录取工作顺利收官（2025-08-11）：https://zs.ccibe.edu.cn/info/1011/2471.htm",
        "- 重庆对外经贸学院 2025 年外省（市、区）录取分数（2025-09-01）：https://zs.ccibe.edu.cn/info/1013/2531.htm",
        "- 重庆对外经贸学院 2025 年重庆本科批专业录取分数（2025-09-01）：https://zs.ccibe.edu.cn/info/1013/2551.htm 或招生网历年分数栏目",
        "",
        "已读取的公开汇总页：",
        "- 高考100《重庆对外经贸学院2025录取分数线（全国各省最低分汇总）》：https://www.gk100.com/read_943721110118.htm",
        "",
        "更新建议：",
        "- 后续若能接入 OCR 或学校将图片分数改为文本/表格页，可直接补齐完整 2025 各省数据。"
    ]
    return "\n".join(lines)


def build_college_doc() -> str:
    rows = [
        "重庆对外经贸学院二级学院校区与联系方式（首轮整理）",
        "",
        "说明：",
        "1. 校区字段优先写学院主页底部地址；若页面只出现教学楼或活动地点，则标记为“推断”或“待核实”。",
        "2. 邮箱优先采用学校官网“意见信箱”或学院主页公开邮箱。",
        "",
        "1. 跨境商务学院：合川B校区；邮箱 kjswxy@163.com；电话未在已解析页面检出。",
        "2. 管理学院：学院主页同时列出合川校区、铜梁校区；邮箱 ccibeglxy@163.com；电话 023-42748576。",
        "3. 外语外贸学院：学院主页同时列出合川校区、铜梁校区；邮箱 wywm2021@163.com；电话未检出。",
        "4. 文学与创意传播学院：推断位于合川A校区（学院主页写第6教学楼，教学新闻出现 A 校区 6208）；邮箱 swsmwcxy@163.com；电话未检出。",
        "5. 数学与计算机科学学院：合川A校区（学府路88号）；邮箱 dwjmsjxy@163.com；电话 023-64289893。",
        "6. 大数据与智能工程学院/工业软件产业学院：合川A校区（学府路88号）；邮箱 dsjyzngcxy@163.com；电话未检出。",
        "7. 重庆超大城市数字化治理学院：公开报道显示成立大会在 B 校区举行，教学活动又出现 A 校区 9101，暂记为 A/B 两校区协同，邮箱与电话待核实。",
        "8. 音乐舞蹈学院：学院主页底部仅写第五教学楼、邮编 401520，暂记为合川校区，具体 A/B 待核实；邮箱 dwjmyywd@163.com；电话未检出。",
        "9. 艺术设计学院：学院主页公开地址为合川区学府路9号，可归入合川A校区线索；邮箱 dwjmyssj@163.com；电话 023-64289346。",
        "10. 影视融媒体学院：学院介绍页公开地址为合川区学府路10号，且多篇活动稿写明合川A校区；邮箱 cqdwjmxy_ysrmtxy@163.com，另有历史页邮箱 swsmysrmt@163.com；电话未检出。",
        "11. 教育学院：学院主页公开地址为合川区学府路9号；邮箱 383467309@qq.com，另有学院页邮箱 xqjyxy@ccibe.edu.cn；电话未检出。",
        "12. 体育与健康学院：主页底部仅写第一教学楼，校区未明；邮箱 ccibetyyjkxy@163.com；电话未检出。",
        "13. 马克思主义学院：合川A校区（学府路88号）；邮箱 3287567936@qq.com；电话 023-64289880。",
        "",
        "主要来源：",
        "- 学校机构设置页：https://www.ccibe.edu.cn/xqzl/jgsz.htm",
        "- 学校意见信箱页：https://www.ccibe.edu.cn/yjxx.htm",
        "- 各学院主页或学院介绍页（如 jm.ccibe.edu.cn、gl.ccibe.edu.cn、wy.ccibe.edu.cn、sj.ccibe.edu.cn、ysrmt.ccibe.edu.cn 等）。"
    ]
    return "\n".join(rows)


def build_life_doc() -> str:
    lines = [
        "重庆对外经贸学院校园生活信息（已核对到的公开线索）",
        "",
        "一、食堂与宿舍公开线索",
        "- 学校官网“校园风光”栏目明确展示了 A 校区食堂、B 校区食堂、A 校区宿舍、B 校区宿舍页面。",
        "- 招生网首页校园风光区也出现了“合川B校区学生食堂”“学生宿舍”等图片条目。",
        "- 当前公开网页未稳定给出食堂数量、食堂正式名称、各栋宿舍详细配置，因此未在此处硬填。",
        "",
        "二、与住宿相关的公开服务线索",
        "- 信息技术中心服务指南公开了“合川A、B校区电费充值流程”。",
        "- 信息技术中心服务指南公开了“合川A校区礼园7舍、8舍热水水控使用操作流程”。",
        "- 信息技术中心服务指南公开了“合川B校区智能门锁使用操作流程”。",
        "- 信息技术中心服务指南公开了“合川A、B校区门禁使用操作流程”。",
        "",
        "三、目前仍未自动核实的关键项",
        "- 食堂共有几个、每个食堂名称及对应校区。",
        "- 宿舍是否配独立卫生间。",
        "- 热水供应时间段。",
        "- 宿舍统一关门时间或不同楼栋门禁时段。",
        "",
        "主要来源：",
        "- 学校官网校园风光栏目：https://www.ccibe.edu.cn/xqzl/xyfg/3.htm",
        "- 招生网首页：https://zs.ccibe.edu.cn/",
        "- 信息技术中心服务指南：https://itc.ccibe.edu.cn/fwzn.htm"
    ]
    return "\n".join(lines)


def build_admin_doc() -> str:
    lines = [
        "重庆对外经贸学院行政服务机构联系方式（首轮整理）",
        "",
        "1. 党政办公室：电话 023-64289208；邮箱 cqdwjmxydzbgs@163.com。",
        "2. 教务处：电话 023-64289211；邮箱 360198634@qq.com。",
        "3. 学生处：电话 023-64289915、023-64289985（同站点不同位置均有出现）；邮箱 1586249471@qq.com。",
        "4. 招生工作处：电话 023-42888768、023-42897897、023-42888798；夜间值班 15723231118；短信平台 15723238118；邮箱 ccibezs@sohu.com。",
        "5. 后勤处：邮箱 cqdwjmhqc@163.com；电话待核实。",
        "6. 保卫处：邮箱 dwjmbwc@163.com；电话待核实。",
        "7. 图书馆：邮箱 lib_my@163.com；电话待核实。",
        "8. 信息技术中心：A 校区电话 023-64289890，B 校区电话 023-42749858；邮箱 xxjszx@ccibe.edu.cn；意见信箱邮箱 117623157@qq.com。",
        "",
        "补充说明：",
        "- 学校总机/党政办公开联系电话：023-64289208。",
        "- 校纪委监督电话在 2025 招生章程中公开为 023-64289311。",
        "",
        "主要来源：",
        "- 学校联系方式页：https://www.ccibe.edu.cn/xqzl/lxfs.htm",
        "- 学校意见信箱页：https://www.ccibe.edu.cn/yjxx.htm",
        "- 教务处主页与联系我们页：https://jwc.ccibe.edu.cn/",
        "- 学生处主页：https://xsc.ccibe.edu.cn/",
        "- 招生网联系我们与招生章程页：https://zs.ccibe.edu.cn/info/1041/1086.htm"
    ]
    return "\n".join(lines)


def build_traffic_doc() -> str:
    lines = [
        "重庆对外经贸学院校区地址与交通线索",
        "",
        "一、校区地址",
        "- 合川A校区：重庆市合川区学府路88号。",
        "- 合川B校区：重庆市合川区濮湖大道168号（学校官网联系方式页）；招生章程等页也出现 368 号写法，建议后续以学校当年最新章程再次核对门牌号。",
        "- 铜梁校区：重庆市铜梁区学府大道304号。",
        "",
        "二、官方公开的到校交通线索",
        "- 2024 级新生报到通知显示，学校曾在以下点位安排迎新接站：重庆西站、重庆北站（南广场/北广场）、重庆江北机场（T1/T2、T3）、合川火车站、合川汽车客运中心、合川A校区、合川B校区。",
        "- 对新生或访客而言，这些点位可作为官方公开过的主要到校交通节点参考。",
        "",
        "三、需要后续补齐的常用路线",
        "- 各校区从重庆北站/重庆西站/江北机场的日常公共交通方案。",
        "- 各校区附近公交、轨道站点与打车落客点。",
        "",
        "主要来源：",
        "- 学校联系方式页：https://www.ccibe.edu.cn/xqzl/lxfs.htm",
        "- 招生章程页：https://zs.ccibe.edu.cn/info/1011/2151.htm",
        "- 2024级萌新大揭秘：https://zs.ccibe.edu.cn/info/1011/1901.htm"
    ]
    return "\n".join(lines)


def build_culture_doc() -> str:
    lines = [
        "重庆对外经贸学院校园文化与学校概览",
        "",
        "1. 学校官网首页写明：学校“立足重庆、面向全国、服务‘一带一路’”。",
        "2. 学校官网首页写明：学校以经济学、管理学为主体，以跨文化传播和跨境商贸专业、数智化工科专业为两翼，工学、理学、文学、艺术学、教育学多学科协调发展。",
        "3. 官网首页公开数据：成立于 2002 年，拥有 53 个本科专业，全日制在校生 29000 余人。",
        "4. 学校成人教育招生简章与多篇官方报道中反复出现的文化关键词包括：行知思想、作孚精神、培元致新。",
        "5. 重庆超大城市数字化治理学院、影视融媒体学院、创客学院等内容能体现学校近年的产教融合与应用型办学特色。",
        "",
        "主要来源：",
        "- 学校官网首页：https://www.ccibe.edu.cn/",
        "- 2025年成人高等教育招生简章：https://cqxdjy.ccibe.edu.cn/info/1117/7206.htm"
    ]
    return "\n".join(lines)


def build_pending_summary() -> str:
    return "\n".join(
        [
            "重庆对外经贸学院知识库待核实清单",
            "",
            "1. 2025 年普通高考完整各省录取分数线表：学校已发布，但网页主体为图片，需 OCR 或人工核对。",
            "2. 2025 年普通专升本分专业录取最低分：学校历年分数栏目已有对应页面标题，需进入原页核对分专业数据。",
            "3. 2025-2026 学年校历：建议关注教务处“贸院校历”栏目或党政办公室通知。",
            "4. 食堂数量、名称、所在校区：建议关注后勤处、迎新指南、校园服务号或实地拍照确认。",
            "5. 宿舍关门时间、独立卫生间、热水供应时段：建议关注宿管通知、后勤处、信息技术中心服务指南或学生手册。",
            "6. 后勤处、保卫处、图书馆公开电话：官网已检出邮箱，但电话仍建议在部门主页或总机转接核实。",
            "7. 部分学院联系电话与精确校区：管理学院、外语外贸学院出现多校区地址；超大城市数字化治理学院、体育与健康学院、音乐舞蹈学院仍需精确到 A/B/C。"
        ]
    )


def build_file_specs() -> List[FileSpec]:
    specs: List[FileSpec] = [
        FileSpec(CATEGORY_DIRS["admission"], "2025年普通高考录取分数线_公开可解析版.docx", build_admission_doc(), "docx"),
        FileSpec(
            CATEGORY_DIRS["admission"],
            "待补充_2025年普通高考录取分数线_其余省份.txt",
            "\n".join(
                [
                    "当前官方来源：",
                    "1. https://zs.ccibe.edu.cn/info/1013/2531.htm 《重庆对外经贸学院2025年外省（市、区）录取分数》",
                    "2. 招生网历年分数栏目：https://zs.ccibe.edu.cn/tzgg/lnfs.htm",
                    "",
                    "待补内容：",
                    "- 官方图片页中未自动解析出的其余省份最低分/位次。",
                    "",
                    "建议：",
                    "- 2025 年秋季后以学校招生网历年分数栏目为准，必要时人工比对图片表格。"
                ]
            ),
        ),
        FileSpec(
            CATEGORY_DIRS["admission"],
            "待补充_2025年普通专升本分专业录取最低分.txt",
            "\n".join(
                [
                    "当前已确认：",
                    "- 招生网通知公告页已出现《重庆对外经贸学院2025年普通专升本分专业录取最低分》条目。",
                    "- 招生网历年分数栏目可作为后续核对入口。",
                    "",
                    "建议查询来源：",
                    "1. https://zs.ccibe.edu.cn/tzgg/lnfs.htm",
                    "2. 学校招生网通知公告 / 历年分数栏目",
                    "",
                    "补充方式：",
                    "- 按专业类别摘录最低分和公布日期。",
                    "- 若页面继续为图片形式，建议人工 OCR 后复核。"
                ]
            ),
        ),
        FileSpec(
            CATEGORY_DIRS["admission"],
            "待补充_2025年专升本收集模板.txt",
            "\n".join(
                [
                    "请补充以下问题：",
                    "1. 2025 年普通专升本各专业最低录取分是多少？",
                    "2. 是否区分普通毕业年级考生 / 原建档立卡考生 / 免试生？",
                    "3. 各专业对应的专业类别是什么？",
                    "4. 公布链接、发布日期和截图存档位置是什么？"
                ]
            ),
        ),
        FileSpec(CATEGORY_DIRS["colleges"], "二级学院校区与联系方式.docx", build_college_doc(), "docx"),
        FileSpec(CATEGORY_DIRS["life"], "食堂与宿舍_公开线索.docx", build_life_doc(), "docx"),
        FileSpec(
            CATEGORY_DIRS["life"],
            "收集模板.txt",
            "\n".join(
                [
                    "请人工补充以下宿舍与生活信息：",
                    "1. 学校共有几个食堂？每个食堂名称分别是什么？",
                    "2. 每个食堂分别位于哪个校区、哪栋楼？",
                    "3. 各类宿舍是否配备独立卫生间？请按楼栋或宿舍类型填写。",
                    "4. 热水供应时间段是什么？是否分 A/B/C 校区或分楼栋？",
                    "5. 宿舍晚间关门时间是什么？是否统一 23:00，还是分楼栋执行？",
                    "6. 是否有门禁、晚归登记、节假日特殊时段说明？"
                ]
            ),
        ),
        FileSpec(
            CATEGORY_DIRS["life"],
            "待补充_食堂数量与名称.txt",
            "\n".join(
                [
                    "自动采集未稳定取得食堂总数和正式名称。",
                    "建议查询来源：",
                    "1. 学校后勤处官网或后勤公众号",
                    "2. 新生入学指南 / 迎新手册",
                    "3. 校园地图或食堂充值系统页面"
                ]
            ),
        ),
        FileSpec(CATEGORY_DIRS["admin"], "行政服务机构联系方式.docx", build_admin_doc(), "docx"),
        FileSpec(
            CATEGORY_DIRS["admin"],
            "待补充_部门公开电话.txt",
            "\n".join(
                [
                    "以下部门邮箱已核到，但电话仍建议继续核实：",
                    "- 后勤处",
                    "- 保卫处",
                    "- 图书馆",
                    "",
                    "建议查询来源：",
                    "1. 各部门子站“联系我们”栏目",
                    "2. 学校总机 023-64289208 转接",
                    "3. 学校企业微信/服务大厅通讯录"
                ]
            ),
        ),
        FileSpec(
            CATEGORY_DIRS["calendar"],
            "待补充_2025-2026学年校历.txt",
            "\n".join(
                [
                    "当前未自动解析到完整校历表。",
                    "建议查询来源：",
                    "1. 教务处主页“贸院校历”栏目：https://jwc.ccibe.edu.cn/",
                    "2. 党政办公室通知",
                    "3. 校内教务系统或服务大厅",
                    "",
                    "建议补录字段：",
                    "- 秋季学期开学报到时间",
                    "- 秋季学期开课时间",
                    "- 国庆/寒假安排",
                    "- 春季学期开学报到时间",
                    "- 春季学期开课时间",
                    "- 五一/端午等放假安排",
                    "- 期末考试周与放假时间"
                ]
            ),
        ),
        FileSpec(
            CATEGORY_DIRS["calendar"],
            "收集模板.txt",
            "\n".join(
                [
                    "请填写：",
                    "1. 每学期报到时间和正式上课时间。",
                    "2. 期中教学检查时间。",
                    "3. 期末考试时间段。",
                    "4. 寒暑假起止时间。",
                    "5. 节假日调休说明。",
                    "6. 学生请假、调课、补考等相关制度链接。"
                ]
            ),
        ),
        FileSpec(CATEGORY_DIRS["traffic"], "校区地址与交通线索.docx", build_traffic_doc(), "docx"),
        FileSpec(
            CATEGORY_DIRS["traffic"],
            "待补充_日常交通路线.txt",
            "\n".join(
                [
                    "建议后续补充：",
                    "1. 重庆北站 -> 合川A/B/C 校区的轨道/公交/打车方案。",
                    "2. 重庆西站 -> 各校区方案。",
                    "3. 江北机场 -> 各校区方案。",
                    "4. 合川火车站 / 汽车客运中心 -> 合川A/B校区方案。",
                    "5. 各校区附近公交站、轨道站、校门别名。"
                ]
            ),
        ),
        FileSpec(CATEGORY_DIRS["culture"], "校园文化与学校概览.docx", build_culture_doc(), "docx"),
        FileSpec(
            CATEGORY_DIRS["personal"],
            "导入说明.txt",
            "\n".join(
                [
                    "本目录用于记录个人整理文档的导入说明。",
                    f"请把你整理好的 Word 文档放入根目录下的 {PERSONAL_SOURCE_DIRNAME} 文件夹。",
                    "脚本会自动读取其中的 .docx 文档，按关键词分类后追加到对应分类目录下的《来自个人文档.txt》。"
                ]
            ),
        ),
        FileSpec(CATEGORY_DIRS["pending"], "待核实清单.txt", build_pending_summary()),
    ]
    return specs


def import_personal_documents(root: Path) -> List[str]:
    messages: List[str] = []
    personal_source_dir = root / PERSONAL_SOURCE_DIRNAME
    if not personal_source_dir.exists():
        ensure_directory(personal_source_dir)
        messages.append(f"请将你整理好的Word文档放入此文件夹后重新运行脚本：{personal_source_dir}")
        return messages

    docx_files = sorted(personal_source_dir.glob("*.docx"))
    if not docx_files:
        messages.append(f"未在 {personal_source_dir} 中发现 .docx 文件。")
        return messages

    for category_dir in CATEGORY_DIRS.values():
        merged_file = root / category_dir / PERSONAL_MERGED_NAME
        if merged_file.exists():
            merged_file.unlink()

    for docx_file in docx_files:
        text = extract_docx_text(docx_file)
        category = classify_personal_text(text, docx_file.stem)
        target_dir = root / CATEGORY_DIRS[category]
        merged_file = target_dir / PERSONAL_MERGED_NAME
        snippet = [
            f"来源文件：{docx_file.name}",
            text or "[文档未提取到正文]",
            "",
            "=" * 60,
            "",
        ]
        append_text(merged_file, "\n".join(snippet))
        messages.append(f"已导入：{docx_file.name} -> {CATEGORY_DIRS[category]}")
    return messages


def build_index(root: Path) -> None:
    sections: List[str] = []
    for dir_name in [*CATEGORY_DIRS.values(), PERSONAL_SOURCE_DIRNAME]:
        folder = root / dir_name
        if not folder.exists():
            continue
        items = []
        for child in sorted(folder.iterdir(), key=lambda item: item.name):
            href = child.name
            label = child.name
            items.append(f'<li><a href="{html.escape(dir_name)}/{html.escape(href)}">{html.escape(label)}</a></li>')
        items_html = "\n".join(items) or "<li>暂无文件</li>"
        sections.append(
            f"""
            <section>
              <h2>{html.escape(dir_name)}</h2>
              <ul>
                {items_html}
              </ul>
            </section>
            """
        )

    body = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>重庆对外经贸学院知识库索引</title>
  <style>
    body {{
      font-family: "Microsoft YaHei", sans-serif;
      margin: 32px auto;
      max-width: 1000px;
      padding: 0 16px 48px;
      line-height: 1.6;
      color: #1f2937;
      background: #f7f7f5;
    }}
    h1, h2 {{
      color: #0f3b57;
    }}
    section {{
      background: #ffffff;
      border: 1px solid #d7dde4;
      border-radius: 10px;
      padding: 16px 20px;
      margin-bottom: 16px;
      box-shadow: 0 2px 8px rgba(15, 59, 87, 0.05);
    }}
    a {{
      color: #0f5c8f;
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <h1>重庆对外经贸学院知识库索引</h1>
  <p>此页面由脚本自动生成，用于浏览各分类目录及文件。</p>
  {''.join(sections)}
</body>
</html>
"""
    write_text(root / INDEX_NAME, body)


def write_file_specs(root: Path, specs: Iterable[FileSpec]) -> None:
    for spec in specs:
        target_dir = root / spec.relative_dir
        ensure_directory(target_dir)
        target_path = target_dir / spec.filename
        if spec.kind == "docx":
            paragraphs = spec.content.splitlines()
            make_docx_document(target_path, paragraphs)
        else:
            write_text(target_path, spec.content)


def create_root_structure(root: Path) -> None:
    ensure_directory(root)
    for folder_name in CATEGORY_DIRS.values():
        ensure_directory(root / folder_name)


def main() -> None:
    parser = argparse.ArgumentParser(description="构建重庆对外经贸学院知识库")
    parser.add_argument(
        "--output",
        default=r"F:\知识库",
        help="知识库根目录，默认 F:\\知识库",
    )
    args = parser.parse_args()

    root = Path(args.output)
    create_root_structure(root)
    write_file_specs(root, build_file_specs())

    import_messages = import_personal_documents(root)
    if import_messages:
        write_text(root / CATEGORY_DIRS["personal"] / "导入日志.txt", "\n".join(import_messages))

    build_index(root)

    print(f"知识库已生成：{root}")
    for message in import_messages:
        print(message)


if __name__ == "__main__":
    main()
