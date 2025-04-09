import streamlit as st
import pandas as pd

st.set_page_config(page_title="재고 수불 대시보드", layout="wide")

st.title("📦 재고 수불 대시보드")

uploaded_file = st.file_uploader("📤 엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    try:
        # 1️⃣ 시트 선택
        sheet = st.selectbox("📄 시트를 선택하세요", pd.ExcelFile(uploaded_file).sheet_names)

        # 2️⃣ 선택한 시트 불러오기
        df = pd.read_excel(uploaded_file, sheet_name=sheet)

        st.success(f"✅ '{sheet}' 시트를 성공적으로 불러왔습니다.")
        st.dataframe(df)

        # 3️⃣ 선택한 시트가 '일별수불이력상품' 또는 등급/출고수량 포함 시만 실행
        if "재고등급" in df.columns and "출고수량" in df.columns:
            st.markdown("### 📊 등급별 출고수량 차트")

            # 등급 필터
            등급 = st.multiselect("재고등급 필터", options=df["재고등급"].unique())
            if 등급:
                df = df[df["재고등급"].isin(등급)]

            # 차트
            st.bar_chart(df.groupby("재고등급")["출고수량"].sum())
            st.dataframe(df)

    except Exception as e:
        st.error(f"파일 로드 중 오류 발생: {e}")

else:
    st.info("⬆️ 왼쪽 상단에서 엑셀 파일을 업로드하세요.")
