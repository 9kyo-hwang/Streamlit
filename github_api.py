import streamlit as st
import requests

@st.cache_data(ttl=3600) # 1시간 동안 API 결과 캐싱 (API 호출 제한 방지 및 속도 향상)
def get_user_data(username):
    res = requests.get(f"https://api.github.com/users/{username}")
    return res.json() if res.status_code == 200 else None

@st.cache_data(ttl=3600)
def get_repo_data(username):
    res = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100&sort=pushed")
    if res.status_code == 200:
        return [repo for repo in res.json() if not repo.get('fork', False)] # Fork된 레포지토리 제외
    return None

@st.cache_data(ttl=3600)
def get_recent_events(username):
    res = requests.get(f"https://api.github.com/users/{username}/events/public?per_page=30")
    return res.json() if res.status_code == 200 else None

@st.cache_data(ttl=3600)
def get_repo_languages(username, repo_name):
    res = requests.get(f"https://api.github.com/repos/{username}/{repo_name}/languages")
    return res.json() if res.status_code == 200 else {}

@st.cache_data(ttl=3600)
def get_search_data(query):
    res = requests.get(f"https://api.github.com/search/issues?q={query}")
    return res.json() if res.status_code == 200 else None

@st.cache_data(ttl=3600)
def get_follow_data(username, follow_type):
    res = requests.get(f"https://api.github.com/users/{username}/{follow_type}?per_page=100")
    return res.json() if res.status_code == 200 else []

@st.cache_data(ttl=3600)
def get_social_accounts(username):
    res = requests.get(f"https://api.github.com/users/{username}/social_accounts")
    return res.json() if res.status_code == 200 else []

@st.cache_data(ttl=3600)
def get_user_orgs(username):
    res = requests.get(f"https://api.github.com/users/{username}/orgs")
    return res.json() if res.status_code == 200 else []