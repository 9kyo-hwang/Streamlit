import streamlit as st
from github_api import get_user_data
from ui_components import (
    render_profile_summary, 
    render_metrics_section, 
    render_overview_tab, 
    render_repo_tab, 
    render_activity_tab, 
    render_network_tab
)

# 페이지 제목 설정
st.set_page_config(page_title="GitHub 프로필 대시보드", page_icon="💻", layout="wide")

def main():
    st.title("GitHub 프로필 대시보드 💻")
    
    # 사용자 설정
    username = "9kyo-hwang"
    baekjoon_id = "ryghkd507"

    user_data = get_user_data(username)
    if not user_data:
        st.error("GitHub 사용자를 찾을 수 없거나 API 요청 한도를 초과했습니다.")
        return # Early return 적용

    # 1. 프로필 요약
    render_profile_summary(username, user_data)
    st.divider()

    # 2. 핵심 통계
    render_metrics_section(username, user_data)
    st.write("")

    # 3. 탭별 정보
    tab_overview, tab_repo, tab_activity, tab_network = st.tabs([
        "🏆 랭크 & 잔디", "📂 레포지토리 분석", "🕒 활동 타임라인", "🤝 팔로워 네트워크"
    ])
    
    with tab_overview:
        render_overview_tab(username, baekjoon_id)
    with tab_repo:
        render_repo_tab(username)
    with tab_activity:
        render_activity_tab(username)
    with tab_network:
        render_network_tab(username, user_data.get('avatar_url'))

if __name__ == "__main__":
    main()
