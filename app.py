import streamlit as st
import pandas as pd

st.set_page_config(page_title="재고등급 분석 대시보드", layout="wide")
st.title("📦 재고등급 분석 대시보드")

uploaded_file = st.file_uploader("📁 재고등급 분석 결과 엑셀 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("📌 주요 지표 요약")
    col1, col2, col3 = st.columns(3)
    col1.metric("총 상품 수", len(df))
    col2.metric("평균 회전율 (%)", f"{df['회전율'].mean() * 100:.1f}%")
    col3.metric("평균 소진일수", f"{df['소진일수'].mean():.0f}일")

    st.subheader("📊 등급별 출고 수량 차트")
    st.bar_chart(df.groupby("재고등급")["출고수량"].sum())

    st.subheader("🔍 상세 데이터")
    st.dataframe(df, use_container_width=True)

else:
    st.info("왼쪽에서 재고등급 포함 엑셀파일을 업로드하세요.")
