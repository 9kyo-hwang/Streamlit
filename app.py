import streamlit as st

# 페이지 제목 설정
st.set_page_config(page_title="나의 첫 Streamlit 앱", page_icon="🎈")

st.title("나의 첫 Streamlit 앱 🎈")
st.write("Github 레포지토리에서 성공적으로 배포되었습니다!")

# 간단한 상호작용 위젯 추가
name = st.text_input("이름을 입력해 보세요:")
if name:
    st.success(f"반갑습니다, {name}님! Streamlit의 세계에 오신 것을 환영합니다.")
