#!/usr/bin/env python3
"""生成AI実践コース プレゼンテーション資料生成スクリプト"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# カラーパレット（青ベース・爽やか）
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK_BLUE = RGBColor(0x1A, 0x3C, 0x6E)
MEDIUM_BLUE = RGBColor(0x2B, 0x5E, 0xA7)
LIGHT_BLUE = RGBColor(0x4A, 0x90, 0xD9)
ACCENT_BLUE = RGBColor(0x5B, 0xA8, 0xE6)
VERY_LIGHT_BLUE = RGBColor(0xE8, 0xF1, 0xFA)
PALE_BLUE = RGBColor(0xF0, 0xF6, 0xFC)
TEXT_DARK = RGBColor(0x2C, 0x2C, 0x2C)
TEXT_GRAY = RGBColor(0x55, 0x55, 0x55)
BORDER_BLUE = RGBColor(0xB0, 0xD0, 0xF0)
ICON_BLUE = RGBColor(0x3A, 0x7C, 0xC2)
CHECK_GREEN = RGBColor(0x2E, 0x8B, 0x57)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def add_background(slide, color=WHITE):
    """スライド背景を白に設定"""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, left, top, width, height, fill_color=None, line_color=None, line_width=None):
    """矩形シェイプを追加"""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.line.fill.background()
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.fill.solid()
        shape.line.color.rgb = line_color
        if line_width:
            shape.line.width = line_width
    return shape


def add_rounded_rect(slide, left, top, width, height, fill_color=None, line_color=None, line_width=None):
    """角丸矩形を追加"""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.line.fill.background()
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if line_color:
        shape.line.fill.solid()
        shape.line.color.rgb = line_color
        if line_width:
            shape.line.width = line_width
    return shape


def set_text(shape, text, font_size=14, color=TEXT_DARK, bold=False, alignment=PP_ALIGN.LEFT, font_name="Yu Gothic"):
    """シェイプ内テキストを設定"""
    tf = shape.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].text = text
    tf.paragraphs[0].alignment = alignment
    for run in tf.paragraphs[0].runs:
        run.font.size = Pt(font_size)
        run.font.color.rgb = color
        run.font.bold = bold
        run.font.name = font_name


def add_textbox(slide, left, top, width, height, text="", font_size=14, color=TEXT_DARK,
                bold=False, alignment=PP_ALIGN.LEFT, font_name="Yu Gothic"):
    """テキストボックスを追加"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = alignment
    run = p.runs[0] if p.runs else p.add_run()
    if not p.runs[0].text:
        run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = font_name
    return txBox


def add_multiline_textbox(slide, left, top, width, height, lines, font_name="Yu Gothic"):
    """複数行テキストボックス: lines = [(text, size, color, bold, align), ...]"""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line_info in enumerate(lines):
        text, size, color, bold, align = line_info
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = text
        p.alignment = align
        p.space_after = Pt(2)
        p.space_before = Pt(0)
        for run in p.runs:
            run.font.size = Pt(size)
            run.font.color.rgb = color
            run.font.bold = bold
            run.font.name = font_name
    return txBox


def add_top_bar(slide):
    """スライド上部の青い装飾バー"""
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.08), fill_color=MEDIUM_BLUE)


def add_bottom_bar(slide):
    """スライド下部の青い装飾バー"""
    add_rect(slide, Inches(0), SLIDE_H - Inches(0.08), SLIDE_W, Inches(0.08), fill_color=MEDIUM_BLUE)


def add_slide_title_bar(slide, title_text):
    """3枚目以降の固定タイトルバー"""
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, Inches(1.0), fill_color=DARK_BLUE)
    add_textbox(slide, Inches(0.6), Inches(0.15), Inches(12), Inches(0.7),
                title_text, font_size=26, color=WHITE, bold=True,
                alignment=PP_ALIGN.LEFT)


def add_page_number(slide, num, total=7):
    """ページ番号"""
    add_textbox(slide, SLIDE_W - Inches(1.2), SLIDE_H - Inches(0.5), Inches(1.0), Inches(0.3),
                f"{num} / {total}", font_size=10, color=TEXT_GRAY, alignment=PP_ALIGN.RIGHT)


# ============================================================
# スライド1: タイトルスライド
# ============================================================
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
add_background(slide1)

# 上部のグラデーション風バー
add_rect(slide1, Inches(0), Inches(0), SLIDE_W, Inches(0.12), fill_color=MEDIUM_BLUE)
add_rect(slide1, Inches(0), Inches(0.12), SLIDE_W, Inches(0.04), fill_color=LIGHT_BLUE)

# 下部のバー
add_rect(slide1, Inches(0), SLIDE_H - Inches(0.12), SLIDE_W, Inches(0.12), fill_color=MEDIUM_BLUE)
add_rect(slide1, Inches(0), SLIDE_H - Inches(0.16), SLIDE_W, Inches(0.04), fill_color=LIGHT_BLUE)

# 中央の装飾ライン
add_rect(slide1, Inches(3), Inches(2.2), Inches(7.333), Inches(0.02), fill_color=ACCENT_BLUE)

# メインタイトル
add_textbox(slide1, Inches(1.5), Inches(2.4), Inches(10.333), Inches(1.0),
            "生成AI実践コース", font_size=48, color=DARK_BLUE, bold=True,
            alignment=PP_ALIGN.CENTER)

# サブタイトル
add_textbox(slide1, Inches(1.5), Inches(3.3), Inches(10.333), Inches(0.6),
            "（初級・中級・上級）", font_size=28, color=MEDIUM_BLUE, bold=False,
            alignment=PP_ALIGN.CENTER)

# 装飾ライン
add_rect(slide1, Inches(3), Inches(4.1), Inches(7.333), Inches(0.02), fill_color=ACCENT_BLUE)

# 提案文
add_textbox(slide1, Inches(1.5), Inches(4.4), Inches(10.333), Inches(0.8),
            "リスキリング研修のご提案", font_size=30, color=DARK_BLUE, bold=True,
            alignment=PP_ALIGN.CENTER)

# 左右の装飾アクセント
add_rect(slide1, Inches(0), Inches(2.0), Inches(0.15), Inches(3.5), fill_color=ACCENT_BLUE)
add_rect(slide1, SLIDE_W - Inches(0.15), Inches(2.0), Inches(0.15), Inches(3.5), fill_color=ACCENT_BLUE)

add_page_number(slide1, 1)


# ============================================================
# スライド2: 会社紹介
# ============================================================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide2)
add_top_bar(slide2)
add_bottom_bar(slide2)

# タイトル
add_rect(slide2, Inches(0), Inches(0.3), SLIDE_W, Inches(1.2), fill_color=DARK_BLUE)
add_textbox(slide2, Inches(0.6), Inches(0.55), Inches(12), Inches(0.7),
            "会社紹介", font_size=34, color=WHITE, bold=True,
            alignment=PP_ALIGN.CENTER)

# 装飾ライン
add_rect(slide2, Inches(4.5), Inches(1.7), Inches(4.333), Inches(0.03), fill_color=ACCENT_BLUE)

# 会社情報カード
card = add_rounded_rect(slide2, Inches(2.5), Inches(2.2), Inches(8.333), Inches(4.5),
                        fill_color=PALE_BLUE, line_color=BORDER_BLUE, line_width=Pt(1.5))

# 会社名
add_textbox(slide2, Inches(3.2), Inches(2.5), Inches(7), Inches(0.7),
            "合同会社N DESIGN", font_size=32, color=DARK_BLUE, bold=True,
            alignment=PP_ALIGN.CENTER)

# 装飾ライン
add_rect(slide2, Inches(5), Inches(3.3), Inches(3.333), Inches(0.02), fill_color=ACCENT_BLUE)

# 会社情報の詳細
info_lines = [
    ("代表", "熱田直央"),
    ("電話番号", "080-2373-5119"),
    ("所在地", "東京都千代田区神田和泉町1番地6-16ヤマトビル405"),
]

y_start = 3.6
for label, value in info_lines:
    # ラベル
    add_textbox(slide2, Inches(3.5), Inches(y_start), Inches(2.2), Inches(0.5),
                label, font_size=16, color=MEDIUM_BLUE, bold=True,
                alignment=PP_ALIGN.RIGHT)
    # 値
    add_textbox(slide2, Inches(5.9), Inches(y_start), Inches(5), Inches(0.5),
                value, font_size=16, color=TEXT_DARK, bold=False,
                alignment=PP_ALIGN.LEFT)
    y_start += 0.65

# 左装飾
add_rect(slide2, Inches(2.5), Inches(2.2), Inches(0.08), Inches(4.5), fill_color=MEDIUM_BLUE)

add_page_number(slide2, 2)


# ============================================================
# スライド3: なぜ生成AIの活用が必要なのか
# ============================================================
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide3)
add_slide_title_bar(slide3, "なぜ生成AIの活用が必要なのか")
add_bottom_bar(slide3)

# サブタイトルライン
add_rect(slide3, Inches(0.6), Inches(1.2), Inches(12.133), Inches(0.015), fill_color=BORDER_BLUE)

# 3カラムレイアウト
col_data = [
    {
        "title": "業務効率化が\n経営の生命線",
        "body": "議事録作成・資料作成など、\n従来1時間かかる作業を5分に\n短縮。生産性を大幅に向上。\n\n効率化により、社員はより\n価値の高い業務に集中でき、\n組織全体の成果が向上します。",
        "icon": "⚡"
    },
    {
        "title": "キャリアの\n分岐点を支える",
        "body": "AI活用スキルはこれから必須。\n早期習得でキャリアの幅を\n広げ、自律的な成長を促進。\n\n習得の遅れは「スキル格差」を\n生み、社内外での競争力を失う\nリスクにもつながります。",
        "icon": "🎯"
    },
    {
        "title": "変化に強い\n組織づくり",
        "body": "属人化を防ぎ、市場や働き方の\n変化に柔軟対応できる人材を育成。\n新しい挑戦を恐れない組織文化を醸成。\n\n変化に対応できることで、企業は長期的な\n競争優位を維持できます。",
        "icon": "🏢"
    }
]

col_width = Inches(3.6)
col_gap = Inches(0.4)
start_x = Inches(0.85)
card_top = Inches(1.5)
card_height = Inches(5.5)

for i, col in enumerate(col_data):
    x = start_x + (col_width + col_gap) * i

    # カード背景
    card_shape = add_rounded_rect(slide3, x, card_top, col_width, card_height,
                                  fill_color=WHITE, line_color=BORDER_BLUE, line_width=Pt(1))

    # 上部アクセントバー
    add_rect(slide3, x, card_top, col_width, Inches(0.06), fill_color=MEDIUM_BLUE)

    # アイコン円
    icon_circle = add_rounded_rect(slide3, x + Inches(1.3), card_top + Inches(0.3),
                                   Inches(1.0), Inches(1.0),
                                   fill_color=VERY_LIGHT_BLUE, line_color=LIGHT_BLUE, line_width=Pt(1))
    set_text(icon_circle, col["icon"], font_size=32, alignment=PP_ALIGN.CENTER)
    icon_circle.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # タイトル
    add_multiline_textbox(slide3, x + Inches(0.3), card_top + Inches(1.5), col_width - Inches(0.6), Inches(1.0),
                          [(col["title"], 20, DARK_BLUE, True, PP_ALIGN.CENTER)])

    # 区切りライン
    add_rect(slide3, x + Inches(0.8), card_top + Inches(2.6), col_width - Inches(1.6), Inches(0.015),
             fill_color=ACCENT_BLUE)

    # 本文
    add_multiline_textbox(slide3, x + Inches(0.3), card_top + Inches(2.8), col_width - Inches(0.6), Inches(2.5),
                          [(col["body"], 13, TEXT_GRAY, False, PP_ALIGN.LEFT)])

add_page_number(slide3, 3)


# ============================================================
# スライド4: 結果の出る生成AI活用に必要な知識の研修
# ============================================================
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide4)
add_slide_title_bar(slide4, "結果の出る生成AI活用に必要な知識の研修")
add_bottom_bar(slide4)

add_rect(slide4, Inches(0.6), Inches(1.2), Inches(12.133), Inches(0.015), fill_color=BORDER_BLUE)

col4_data = [
    {
        "title": "AIリテラシー基礎",
        "items": [
            "AIの仕組みと活用事例",
            "チャットや要約の実践",
            "日常業務での応用方法",
            "AI利用におけるリスク理解"
        ],
        "color": LIGHT_BLUE,
        "icon": "📖"
    },
    {
        "title": "業務活用実践",
        "items": [
            "社内文書・マニュアル作成",
            "データ整理と分析支援",
            "マーケティング施策の効率化",
            "顧客対応・FAQ自動化"
        ],
        "color": MEDIUM_BLUE,
        "icon": "💼"
    },
    {
        "title": "戦略的活用と\nDX推進",
        "items": [
            "部署横断でのAI活用設計",
            "業務フロー自動化の構築",
            "カスタマイズAIの導入",
            "DX人材としての\nマネジメント力"
        ],
        "color": DARK_BLUE,
        "icon": "🚀"
    }
]

start_x4 = Inches(0.85)
card_top4 = Inches(1.5)
card_height4 = Inches(5.5)

for i, col in enumerate(col4_data):
    x = start_x4 + (col_width + col_gap) * i

    # カード
    add_rounded_rect(slide4, x, card_top4, col_width, card_height4,
                     fill_color=WHITE, line_color=BORDER_BLUE, line_width=Pt(1))
    add_rect(slide4, x, card_top4, col_width, Inches(0.06), fill_color=col["color"])

    # アイコン
    icon_c = add_rounded_rect(slide4, x + Inches(1.3), card_top4 + Inches(0.3),
                              Inches(1.0), Inches(1.0),
                              fill_color=VERY_LIGHT_BLUE, line_color=LIGHT_BLUE, line_width=Pt(1))
    set_text(icon_c, col["icon"], font_size=32, alignment=PP_ALIGN.CENTER)
    icon_c.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # タイトル
    add_multiline_textbox(slide4, x + Inches(0.3), card_top4 + Inches(1.5), col_width - Inches(0.6), Inches(1.0),
                          [(col["title"], 20, DARK_BLUE, True, PP_ALIGN.CENTER)])

    # 区切り
    add_rect(slide4, x + Inches(0.8), card_top4 + Inches(2.6), col_width - Inches(1.6), Inches(0.015),
             fill_color=col["color"])

    # チェックリスト
    items_text = "\n".join(["✓  " + item for item in col["items"]])
    add_multiline_textbox(slide4, x + Inches(0.4), card_top4 + Inches(2.8), col_width - Inches(0.8), Inches(2.5),
                          [(items_text, 14, TEXT_DARK, False, PP_ALIGN.LEFT)])

add_page_number(slide4, 4)


# ============================================================
# スライド5: 社内で成果を出すための AI×DX 人材育成研修
# ============================================================
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide5)
add_slide_title_bar(slide5, "社内で成果を出すための AI×DX 人材育成研修")
add_bottom_bar(slide5)

add_rect(slide5, Inches(0.6), Inches(1.2), Inches(12.133), Inches(0.015), fill_color=BORDER_BLUE)

# 左側：説明カード
left_card = add_rounded_rect(slide5, Inches(0.7), Inches(1.6), Inches(5.8), Inches(5.3),
                             fill_color=PALE_BLUE, line_color=BORDER_BLUE, line_width=Pt(1))
add_rect(slide5, Inches(0.7), Inches(1.6), Inches(0.08), Inches(5.3), fill_color=MEDIUM_BLUE)

add_textbox(slide5, Inches(1.2), Inches(1.9), Inches(5.0), Inches(0.8),
            "生成AIを正しく\n使える人材育成", font_size=26, color=DARK_BLUE, bold=True)

add_rect(slide5, Inches(1.2), Inches(3.0), Inches(4.5), Inches(0.015), fill_color=ACCENT_BLUE)

body5 = ("外部委託ではなく社内でAIを運用\n"
         "できる人材を育てることで、独自の\n"
         "ナレッジが蓄積され、持続的に成果\n"
         "を出せる体制を構築できます。")
add_multiline_textbox(slide5, Inches(1.2), Inches(3.3), Inches(5.0), Inches(3.0),
                      [(body5, 15, TEXT_GRAY, False, PP_ALIGN.LEFT)])

# 右側：メリットカード
right_card = add_rounded_rect(slide5, Inches(6.8), Inches(1.6), Inches(5.8), Inches(5.3),
                              fill_color=WHITE, line_color=BORDER_BLUE, line_width=Pt(1))
add_rect(slide5, Inches(6.8), Inches(1.6), SLIDE_W - Inches(6.8), Inches(0.06), fill_color=MEDIUM_BLUE)

# メリットタイトル
merit_title = add_rounded_rect(slide5, Inches(8.5), Inches(1.9), Inches(2.5), Inches(0.6),
                               fill_color=MEDIUM_BLUE)
set_text(merit_title, "メリット", font_size=20, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
merit_title.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

merits = [
    "最新のAI活用スキルを体系的に習得",
    "業務効率化から戦略設計まで幅広くカバー",
    "社内に「教える人材」が育ち自走できる",
    "DX推進に直結するスキルを獲得"
]

merit_y = Inches(2.8)
for m in merits:
    # チェックマーク付き
    add_multiline_textbox(slide5, Inches(7.3), merit_y, Inches(5.0), Inches(0.5),
                          [("✓  " + m, 15, TEXT_DARK, False, PP_ALIGN.LEFT)])
    merit_y += Inches(0.65)

add_page_number(slide5, 5)


# ============================================================
# スライド6: 生成AI実践コース
# ============================================================
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide6)
add_slide_title_bar(slide6, "生成AI実践コース")
add_bottom_bar(slide6)

add_rect(slide6, Inches(0.6), Inches(1.2), Inches(12.133), Inches(0.015), fill_color=BORDER_BLUE)

courses = [
    {
        "level": "初級",
        "purpose": "LLMの基礎と活用方法を学び、文章\n生成演習と多様なAIツールを体験",
        "price": "327,800円（税込）/人",
        "hours": "11時間",
        "format": "e-ラーニング",
        "items": [
            "生成AIの技術理解と注意点",
            "生成AIツールの活用力を高めるポイント",
            "プロンプトエンジニアリング",
            "様々なテキスト生成のポイントと実践",
            "様々な分野に特化した生成AIツールの理解"
        ],
        "color": LIGHT_BLUE
    },
    {
        "level": "中級",
        "purpose": "AIの社会影響を理解し、\nプロンプト力と人間の思考力を強化",
        "price": "327,800円（税込）/人",
        "hours": "11時間10分",
        "format": "e-ラーニング",
        "items": [
            "生成AIの発展と社会に与えるインパクト",
            "プロンプトスキル向上のための応用知識",
            "生成AIを用いた業務改善",
            "生成AIをより上手く活用するための\n論理的思考力の醸成",
            "生成AI時代に求められる人間の思考力"
        ],
        "color": MEDIUM_BLUE
    },
    {
        "level": "上級",
        "purpose": "課題発見力を磨き、生成AIを\n戦略的に活用して実務効率化へ",
        "price": "327,800円（税込）/人",
        "hours": "11時間30分",
        "format": "e-ラーニング",
        "items": [
            "DXに対する基本理解と生成AI活用の未来",
            "企業と個人のDXを実践するために\n「課題」の解像度を高める",
            "生成AI活用力の向上と業務改善への道筋",
            "個人DXを実現する生成AI活用と具体事例"
        ],
        "color": DARK_BLUE
    }
]

col6_width = Inches(3.6)
col6_gap = Inches(0.4)
start_x6 = Inches(0.85)
card_top6 = Inches(1.4)

for i, course in enumerate(courses):
    x = start_x6 + (col6_width + col6_gap) * i

    # カード全体
    add_rounded_rect(slide6, x, card_top6, col6_width, Inches(5.3),
                     fill_color=WHITE, line_color=BORDER_BLUE, line_width=Pt(1))

    # レベルヘッダー
    header = add_rounded_rect(slide6, x, card_top6, col6_width, Inches(0.55),
                              fill_color=course["color"])
    # 角丸が下だけ直線にならないのでオーバーレイ
    set_text(header, course["level"], font_size=22, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    header.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    y = card_top6 + Inches(0.7)

    # 目的
    add_multiline_textbox(slide6, x + Inches(0.2), y, col6_width - Inches(0.4), Inches(0.3),
                          [("目的", 11, MEDIUM_BLUE, True, PP_ALIGN.LEFT)])
    y += Inches(0.25)
    add_multiline_textbox(slide6, x + Inches(0.2), y, col6_width - Inches(0.4), Inches(0.65),
                          [(course["purpose"], 11, TEXT_DARK, False, PP_ALIGN.LEFT)])
    y += Inches(0.65)

    # 料金
    add_multiline_textbox(slide6, x + Inches(0.2), y, col6_width - Inches(0.4), Inches(0.3),
                          [("料金", 11, MEDIUM_BLUE, True, PP_ALIGN.LEFT)])
    y += Inches(0.22)
    add_multiline_textbox(slide6, x + Inches(0.2), y, col6_width - Inches(0.4), Inches(0.3),
                          [(course["price"], 12, TEXT_DARK, True, PP_ALIGN.LEFT)])
    y += Inches(0.30)

    # 時間・形態
    add_multiline_textbox(slide6, x + Inches(0.2), y, Inches(1.7), Inches(0.3),
                          [("標準学習時間", 11, MEDIUM_BLUE, True, PP_ALIGN.LEFT)])
    add_multiline_textbox(slide6, x + Inches(1.9), y, Inches(1.5), Inches(0.3),
                          [(course["hours"], 11, TEXT_DARK, False, PP_ALIGN.LEFT)])
    y += Inches(0.25)
    add_multiline_textbox(slide6, x + Inches(0.2), y, Inches(1.7), Inches(0.3),
                          [("受講形態", 11, MEDIUM_BLUE, True, PP_ALIGN.LEFT)])
    add_multiline_textbox(slide6, x + Inches(1.9), y, Inches(1.5), Inches(0.3),
                          [(course["format"], 11, TEXT_DARK, False, PP_ALIGN.LEFT)])
    y += Inches(0.35)

    # 区切り
    add_rect(slide6, x + Inches(0.3), y, col6_width - Inches(0.6), Inches(0.01), fill_color=BORDER_BLUE)
    y += Inches(0.15)

    # 内容抜粋
    add_multiline_textbox(slide6, x + Inches(0.2), y, col6_width - Inches(0.4), Inches(0.3),
                          [("内容抜粋", 11, MEDIUM_BLUE, True, PP_ALIGN.LEFT)])
    y += Inches(0.25)

    for item in course["items"]:
        add_multiline_textbox(slide6, x + Inches(0.3), y, col6_width - Inches(0.5), Inches(0.45),
                              [("✓  " + item, 10, TEXT_DARK, False, PP_ALIGN.LEFT)])
        # アイテムの行数に応じて高さ調整
        line_count = item.count("\n") + 1
        y += Inches(0.28 * line_count)

# LMS注記
add_rect(slide6, Inches(0.6), SLIDE_H - Inches(0.75), Inches(12.133), Inches(0.015), fill_color=BORDER_BLUE)
lms_text = "本講座はLMS（学習管理システム）を用いて提供しています。\nLMSでは、受講者の進捗管理や認定証の発行を行うことができます。"
add_multiline_textbox(slide6, Inches(0.8), SLIDE_H - Inches(0.7), Inches(12), Inches(0.55),
                      [(lms_text, 11, TEXT_GRAY, False, PP_ALIGN.CENTER)])

add_page_number(slide6, 6)


# ============================================================
# スライド7: 生成AI実践コース 目次
# ============================================================
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
add_background(slide7)
add_slide_title_bar(slide7, "生成AI実践コース 目次")
add_bottom_bar(slide7)

add_rect(slide7, Inches(0.6), Inches(1.2), Inches(12.133), Inches(0.015), fill_color=BORDER_BLUE)

# サブタイトル
add_textbox(slide7, Inches(0.7), Inches(1.3), Inches(4), Inches(0.4),
            "研修内容抜粋", font_size=14, color=MEDIUM_BLUE, bold=True)

# 3カラム（初級・中級・上級）
toc_col_width = Inches(3.8)
toc_col_gap = Inches(0.3)
toc_start_x = Inches(0.55)
toc_card_top = Inches(1.75)

# 初級
beginner_items = [
    "イントロダクション",
    "生成AI活用による個人DX推進のための基本概要 (1) 1〜5",
    "生成AI活用による個人DX推進のための基本概要 (2) 1〜7",
    "生成AI活用による個人DX推進のための基本概要 (3) 1〜6",
    "生成AIの技術理解と注意点 (1)〜(4)",
    "生成AIツールの活用力を高めるポイントとプロンプトエンジニアリング (1) 1〜11 ケーススタディ1",
    "生成AIツールの活用力を高めるポイントとプロンプトエンジニアリング (2) 1〜6 ケーススタディ1",
    "生成AI活用力の向上 (1),(2) 1〜8 (1),(2) ケーススタディ12",
    "生成AI活用力の向上 (3) 1〜12 ケーススタディ123",
    "様々な分野に特化した生成AIツールの理解 (1) 1〜7",
    "様々な分野に特化した生成AIツールの理解 (2) 1〜4",
    "様々な分野に特化した生成AIツールの理解 (3) 1〜6",
]

# 中級
intermediate_items = [
    "イントロダクション",
    "生成AIの発展と社会に与えるインパクト (1) 1〜4",
    "生成AIの発展と社会に与えるインパクト (2) 1〜5",
    "生成AIの発展と社会に与えるインパクト (3),(4) 1〜3",
    "プロンプトスキル向上のための応用知識 (1) 1〜6",
    "プロンプトスキル向上のための応用知識 (2)〜(5) 1〜2 (2)〜(5) ケーススタディ1",
    "プロンプトスキル向上のための応用知識 (6) 1〜6 ケーススタディ1",
    "生成AIを用いた業務改善 (1)〜(12) ケーススタディ1234567",
    "生成AIをより上手く活用するための論理的思考力の醸成 (1)",
    "生成AIをより上手く活用するための論理的思考力の醸成 (2) 1〜6 ケーススタディ1",
    "生成AIをより上手く活用するための論理的思考力の醸成 (3) 1〜4 ケーススタディ1",
    "生成AIをより上手く活用するための論理的思考力の醸成 (4) 1〜3 ケーススタディ1",
    "生成AI時代に求められる人間の思考力 (1)〜(3) 1〜6 (1)〜(3) ケーススタディ1",
]

# 上級
advanced_items = [
    "イントロダクション",
    "DXに対する基本理解と生成AI活用の未来 (1)〜(7)",
    "企業と個人のDXを実現するために「課題」の解像度を高める (1),(3),(4) 1〜8 (1),(3) ケーススタディ1 (4) ケーススタディ12",
    "企業と個人のDXを実現するために「課題」の解像度を高める (2),(5) 1〜7 (2) ケーススタディ1 (5) ケーススタディ123",
    "生成AI活用力の向上と業務改善への道筋 (1) 1〜6 ケーススタディ1",
    "生成AI活用力の向上と業務改善への道筋 (2) 1〜8 ケーススタディ123",
    "生成AI活用力の向上と業務改善への道筋 (3) 1〜9 ケーススタディ123",
    "生成AI活用力の向上と業務改善への道筋 (4) 1〜8 ケーススタディ12",
    "個人DXを実現する生成AI活用と具体事例 (1),(2) 1〜5",
    "個人DXを実現する生成AI活用と具体事例 (3) 1〜7",
    "個人DXを実現する生成AI活用と具体事例 (4) 1〜6",
]

all_toc = [
    ("初級", beginner_items, LIGHT_BLUE),
    ("中級", intermediate_items, MEDIUM_BLUE),
    ("上級", advanced_items, DARK_BLUE),
]

for i, (level, items, color) in enumerate(all_toc):
    x = toc_start_x + (toc_col_width + toc_col_gap) * i

    # カード
    add_rounded_rect(slide7, x, toc_card_top, toc_col_width, Inches(5.3),
                     fill_color=WHITE, line_color=BORDER_BLUE, line_width=Pt(1))

    # レベルヘッダー
    hdr = add_rounded_rect(slide7, x, toc_card_top, toc_col_width, Inches(0.45),
                           fill_color=color)
    set_text(hdr, level, font_size=16, color=WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    hdr.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    # アイテムリスト
    txBox = slide7.shapes.add_textbox(x + Inches(0.15), toc_card_top + Inches(0.55),
                                      toc_col_width - Inches(0.3), Inches(4.7))
    tf = txBox.text_frame
    tf.word_wrap = True

    for j, item in enumerate(items):
        if j == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = "• " + item
        p.space_after = Pt(2)
        p.space_before = Pt(1)
        for run in p.runs:
            run.font.size = Pt(7.5)
            run.font.color.rgb = TEXT_DARK
            run.font.name = "Yu Gothic"

add_page_number(slide7, 7)


# ============================================================
# 保存
# ============================================================
output_path = "/home/user/naoatsuta/生成AI実践コース_研修提案.pptx"
prs.save(output_path)
print(f"プレゼンテーションを保存しました: {output_path}")
