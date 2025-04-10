import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="재고등급 분석 대시보드", layout="wide")

st.title("📦 재고등급 분석 대시보드")

# 엑셀 파일 업로드
uploaded_file = st.file_uploader("📁 재고등급 분석 결과 엑셀 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 🔍 사이드바 필터
    with st.sidebar:
        st.header("🎛️ 필터")
        등급옵션 = df["재고등급"].unique().tolist()
        선택등급 = st.multiselect("재고등급 선택", options=등급옵션, default=등급옵션)

    # 필터 적용
    df_filtered = df[df["재고등급"].isin(선택등급)]

    # 📌 주요 지표 요약
    st.subheader("📌 주요 지표 요약")
    col1, col2, col3 = st.columns(3)
    col1.metric("총 상품 수", len(df_filtered))
    col2.metric("평균 회전율", f"{df_filtered['회전율'].mean() * 100:.1f}%")
    col3.metric("평균 소진일수", f"{df_filtered['소진일수'].mean():.0f}일")

    # 📊 등급별 출고수량 차트
    st.subheader("📊 등급별 출고 수량")
    chart = df_filtered.groupby("재고등급")["출고수량"].sum().sort_index()
    st.bar_chart(chart)

    # 🔍 상세 테이블
    st.subheader("🔍 상세 재고등급 데이터")
    st.dataframe(df_filtered, use_container_width=True)

else:
    st.info("왼쪽 상단에서 분석 결과 엑셀 파일을 업로드해주세요.")
