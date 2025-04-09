
import streamlit as st
import pandas as pd

st.set_page_config(page_title="재고 수불 대시보드", layout="wide")
st.title("📦 재고 수불 대시보드")

# 기본 마스터데이터 파일 불러오기
@st.cache_data
def load_data():
    df = pd.read_excel("분석용_마스터데이터_통합_최종.xlsx")
    return df

df = load_data()

# 필터 영역 (좌측 사이드바)
with st.sidebar:
    st.header("🔎 필터")
    등급옵션 = st.multiselect("재고등급", options=df["재고등급"].dropna().unique())
    카테고리옵션 = st.multiselect("카테고리", options=df["카테고리"].dropna().unique())
    팀옵션 = st.multiselect("판매팀명", options=pd.Series(sum(df["판매팀목록"].dropna().tolist(), [])).unique())

# 필터 적용
if 등급옵션:
    df = df[df["재고등급"].isin(등급옵션)]
if 카테고리옵션:
    df = df[df["카테고리"].isin(카테고리옵션)]
if 팀옵션:
    df = df[df["판매팀목록"].apply(lambda x: any(team in x for team in 팀옵션) if isinstance(x, list) else False)]

# KPI 표시
st.subheader("📊 주요 지표 요약")
col1, col2, col3, col4 = st.columns(4)
col1.metric("총 입고수량", f"{df['입고수량'].sum():,.0f}")
col2.metric("총 출고수량", f"{df['출고수량'].sum():,.0f}")
col3.metric("총 매출", f"{df['총매출'].sum():,.0f} 원")
col4.metric("총 순수익", f"{df['순수익'].sum():,.0f} 원")

# 차트 탭
st.markdown("---")
tab1, tab2, tab3 = st.tabs(["📈 등급별 재고 분포", "💸 팀별 매출 차트", "📦 전체 데이터 테이블"])

with tab1:
    st.subheader("재고등급별 상품 수량")
    st.bar_chart(df["재고등급"].value_counts().sort_index())

with tab2:
    st.subheader("판매팀별 총매출")
    exploded = df.explode("판매팀목록")
    if not exploded.empty:
        team_sales = exploded.groupby("판매팀목록")["총매출"].sum().sort_values(ascending=False)
        st.bar_chart(team_sales)

with tab3:
    st.subheader("전체 상품 데이터")
    st.dataframe(df)

st.caption("ⓒ 2025. SecondHome Inventory Dashboard")
