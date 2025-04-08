
import streamlit as st
import pandas as pd

st.set_page_config(page_title="재고 수불 대시보드", layout="wide")

st.title("📦 재고 수불 대시보드 (Demo)")
uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("파일 업로드 완료 ✅")
    
    st.dataframe(df)

    # 필터
    등급 = st.multiselect("재고등급 필터", options=df["재고등급"].unique())
    if 등급:
        df = df[df["재고등급"].isin(등급)]
    
    st.bar_chart(df.groupby("재고등급")["출고수량"].sum())
    st.dataframe(df)
else:
    st.info("좌측 상단에서 엑셀 파일을 업로드하세요.")
