import streamlit as st
import pandas as pd
import io

st.markdown("# 감성표현 👍")
st.sidebar.markdown("# 감성표현 👍")



# ✅ 키워드-색상 정의 및 하이라이팅 함수
highlight_keywords = {
    "성장": "blue",
    "상성": "blue",
    "개선": "blue",
    "성공": "blue",
    "극복": "blue",
    "호황": "blue",
    "기대": "blue",   
    "하락": "red",
    "감소": "red",
    "위기": "red",
    "실패": "red",
    "논란": "red",
    "침체": "red",
    "우려": "red",
    "발표": "green",
    "분석": "green",
    "변화": "green",
    "현황": "green",
    "평가": "green"

}

def highlight_text(text):
    """특정 키워드 포함 시 색상 강조"""
    if not isinstance(text, str):
        return str(text)
    for keyword, color in highlight_keywords.items():
        if keyword in text:
            text = text.replace(
                keyword,
                f"<span style='color:{color}; font-weight:bold'>{keyword}</span>"
            )
    return text


# 세션 상태 초기화
if 'df' not in st.session_state:
    st.session_state.df = None
if 'labels' not in st.session_state:
    st.session_state.labels = {}

# 라벨 기준 안내 표 (4x4)
st.markdown("### 🧾 감성표현 기준표")
label_guide = pd.DataFrame({
    "항목": ["적극적", "소극적", "중립", "대안"],
    "설명": [
        "명확한 긍정, 희망적 결과를 강조하는 경우",
        "명확한 부정, 우려, 비판 등 강조하는 경우",
        "긍정 또는 부정 감성이 불명확/객관적 사실 중심으로 서술된 경우",
        "해결책이나 제시, 대안이 포함되어 있는 경우"
    ],
    "주요키워드": [
        "성장,상성,개선,성공,극복,호황,기대",
        "하락,감소,위기,실패,논란,침체,우려",
        "소극적+적극적 혼합",
        "발표,분석,변화,현황,평가"
    ],
    "고려사항": [
        "객관적인 사실보다 주관적인 의견만 제시하는 경우 신중하게 판단",
        "부정적인 감정만 있을 경우 소극적으로 분류할지 신중하게 판단",
        "대안과 혼동되면 안됨",
        "예시 : 정부는 금리 인상을 검토 중이다"
    ]

})
st.table(label_guide)

# 엑셀 업로드
uploaded_file = st.file_uploader("📁 엑셀 파일 업로드 (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.session_state.df = df

    # 기존 라벨 열이 있다면 다음 라벨은 Label_2로
    label_column_name = "Label_2" if "Label" in df.columns else "Label"

    st.markdown(f"### 🏷️ 각 행에 라벨 입력 → **{label_column_name}** 열에 저장")

    for i, row in df.iterrows():
        cols = st.columns([6, 1])
        formatted_row = []
        for col_name, value in row.items():
            if pd.isna(value):
                continue
            if col_name =='content':
                formatted = highlight_text(str(value))
            else:
                formatted = str(value)
            formatted_row.append(formatted)
        
        row_text = " | ".join(formatted_row)
        cols[0].markdown(f"**{i+1}.** {row_text}", unsafe_allow_html=True)

        default_value = st.session_state.labels.get(i, "선택")
        selected = cols[1].selectbox(
            label="",
            options=["선택", "적극적", "소극적", "중립","대안"],
            index=["선택", "적극적", "소극적", "중립","대안"].index(default_value),
            key=f"select_{i}"
        )
        st.session_state.labels[i] = selected

    st.markdown("---")

    # 중간 저장 버튼
    if st.button("💾 중간 저장"):
        st.success("중간 저장 완료!")

    # 최종 다운로드 버튼
    if st.button("📥 최종 파일 다운로드"):
        labeled_df = st.session_state.df.copy()
        labeled_df[label_column_name] = [
            st.session_state.labels.get(i, "선택") for i in range(len(labeled_df))
        ]

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            labeled_df.to_excel(writer, index=False)

        st.download_button(
            label="📤 여기를 클릭해 엑셀 파일 다운로드",
            data=output.getvalue(),
            file_name="labeled_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )