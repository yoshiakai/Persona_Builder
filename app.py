import streamlit as st

st.set_page_config(
    page_title="イベントペルソナ作成支援ツール",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 イベントペルソナ作成支援ツール")
st.caption("イベント情報から、生成AIに渡すためのペルソナ作成プロンプトを作成します。")

st.info(
    "このツールが作成するペルソナは、イベント情報から導いた仮説です。"
    "実在する参加者の分析結果ではありません。"
)

with st.form("event_form"):
    st.subheader("イベント情報")

    event_name = st.text_input("イベント名")
    event_overview = st.text_area("イベント概要", height=120)
    purpose = st.text_area("開催目的", height=100)

    col1, col2 = st.columns(2)

    with col1:
        target = st.text_area("想定参加者", height=100)
        venue = st.text_input("開催場所")
        date = st.text_input("開催日時")
        fee = st.text_input("参加費")

    with col2:
        benefits = st.text_area("参加者が得られる価値", height=100)
        requirements = st.text_area("参加に必要な知識・経験", height=100)
        atmosphere = st.text_area("イベントの雰囲気", height=100)

    motivation = st.text_area("想定される参加動機", height=100)
    barriers = st.text_area("参加を妨げる要因・不安", height=100)
    problems = st.text_area("想定される参加者の課題", height=100)
    additional = st.text_area("その他、学生による自由記述", height=120)

    submitted = st.form_submit_button("プロンプトを作成")

def value(text):
    return text.strip() if text and text.strip() else "未入力"

def make_prompt():
    return f"""
あなたはマーケティングリサーチとペルソナ設計の専門家です。

以下のイベント情報をもとに、イベントへの参加が想定される代表的な参加者像を設計してください。

重要事項：
- これは実在する参加者の分析ではなく、イベント情報から作成する仮説ペルソナです。
- イベント情報にない内容は断定しないでください。
- 推定した内容には「推定」と記載してください。
- 性別、職業、年収などは必要性がある場合のみ設定してください。
- ステレオタイプや過度な一般化を避けてください。

【イベント情報】

イベント名：
{value(event_name)}

イベント概要：
{value(event_overview)}

開催目的：
{value(purpose)}

想定参加者：
{value(target)}

開催場所：
{value(venue)}

開催日時：
{value(date)}

参加費：
{value(fee)}

参加者が得られる価値：
{value(benefits)}

参加に必要な知識・経験：
{value(requirements)}

イベントの雰囲気：
{value(atmosphere)}

想定される参加動機：
{value(motivation)}

参加を妨げる要因・不安：
{value(barriers)}

想定される参加者の課題：
{value(problems)}

その他の情報：
{value(additional)}

以下の順番で出力してください。

## 1. 客観的ペルソナ
- 基本属性
- 行動特性
- 参加条件
- イベントとの接点
- 参加によって得たいもの
- 根拠となるイベント情報

## 2. 主観的ペルソナ
- 参加動機
- 抱えている悩み
- 期待
- 不安・障壁
- 価値観
- 理想の状態
- 推定である部分

## 3. 統合ペルソナ
以下の項目を含めて、1人の仮想参加者として具体化してください。

- ペルソナ名
- 年齢層
- 生活・学習・仕事の状況
- イベントを知ったきっかけ
- 参加前の課題
- 参加を決める理由
- 参加中の行動
- 参加後に期待する変化
- 代表的な一言
- ペルソナの根拠
- 仮説・不確実な点

## 4. 画像生成用プロンプト
統合ペルソナをもとに、画像生成AIに入力するプロンプトを作成してください。

以下を含めてください。

- 年齢層
- 外見的特徴
- 服装
- 表情
- 姿勢
- イベント会場の様子
- 背景
- 光
- 構図
- 画風
- 過度なステレオタイプを避ける注意

最後に、画像生成時に避けるべき表現や要素も記載してください。
"""

if submitted:
    if not event_name and not event_overview and not target:
        st.warning("イベント名、イベント概要、想定参加者のいずれかを入力してください。")
    else:
        prompt = make_prompt()

        st.success("プロンプトを作成しました。")
        st.subheader("生成AI用プロンプト")
        st.text_area(
            "以下をコピーしてChatGPT、Gemini、Claudeなどに貼り付けてください。",
            prompt,
            height=700
        )

        st.download_button(
            label="プロンプトをテキストファイルで保存",
            data=prompt,
            file_name="event_persona_prompt.txt",
            mime="text/plain"
        )