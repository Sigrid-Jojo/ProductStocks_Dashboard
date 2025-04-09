
import streamlit as st
import pandas as pd

st.set_page_config(page_title="재고 대시보드", layout="wide")
st.title("📦 재고 수불 대시보드")

uploaded_file = st.file_uploader("📤 재고등급 포함 엑셀 업로드", type=["xlsx"])

# 기본 엑셀 파일 설정
if uploaded_file is None:
    uploaded_file = "Streamlit_재고등급_포함.xlsx"

try:
    df = pd.read_excel(uploaded_file)
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')

    # KPI 지표
    total_input = df['입고수량'].sum()
    total_output = df['출고수량'].sum()
    avg_rotation = round((total_output / total_input) * 100, 2) if total_input > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("총 입고수량", f"{int(total_input):,}")
    col2.metric("총 출고수량", f"{int(total_output):,}")
    col3.metric("평균 회전율 (%)", f"{avg_rotation}%")

    st.markdown("---")

    # 등급 분포 바 차트
    st.subheader("📊 재고등급별 상품 분포")
    grade_counts = df['재고등급'].value_counts().sort_index()
    st.bar_chart(grade_counts)

    # 월별 출고 트렌드
    st.subheader("📈 월별 출고량 추이")
    df['월'] = df['날짜'].dt.to_period("M").astype(str)
    monthly_output = df.groupby('월')['출고수량'].sum()
    st.line_chart(monthly_output)

    # 팀별 출고수량
    if "판매팀명" in df.columns:
        st.subheader("🏷️ 판매팀별 출고 수량")
        team_summary = df.groupby("판매팀명")["출고수량"].sum().sort_values(ascending=False)
        st.bar_chart(team_summary)

    # 등급 필터링 및 데이터 확인
    st.subheader("🔍 재고등급별 상세 내역 확인")
    등급선택 = st.multiselect("등급 선택", options=df["재고등급"].unique())
    if 등급선택:
        필터링 = df[df["재고등급"].isin(등급선택)]
        st.dataframe(필터링)
    else:
        st.dataframe(df)

except Exception as e:
    st.error(f"파일을 불러오는 중 오류가 발생했습니다: {e}")
