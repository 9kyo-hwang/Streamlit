import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os

# 분리해둔 API 모듈에서 필요한 함수들을 가져옵니다.
from github_api import (
    get_repo_data, get_recent_events, get_repo_languages,
    get_search_data, get_follow_data, get_social_accounts, get_user_orgs
)

def render_profile_summary(username, user_data):
    col_img, col_info = st.columns([1, 4])
    with col_img:
        if user_data.get('avatar_url'):
            st.image(user_data.get('avatar_url'), width=200)
    with col_info:
        st.subheader(user_data.get('name') or username)
        st.write(user_data.get('bio') or '소개가 없습니다.')
        
        blog_url = user_data.get('blog')
        if blog_url:
            if not blog_url.startswith(('http://', 'https://')):
                blog_url = 'https://' + blog_url
            st.write(f"🌐 [웹사이트/블로그]({blog_url})")
                
        company = user_data.get('company')
        if company: st.write(f"🏢 {company}")
            
        location = user_data.get('location')
        if location: st.write(f"📍 {location}")
            
        socials = get_social_accounts(username)
        for social in socials:
            provider = social.get('provider', 'Link').capitalize()
            st.write(f"🔗 [{provider}]({social.get('url')})")
            
        orgs = get_user_orgs(username)
        if orgs:
            st.write("")
            st.write("**🏢 Organizations**")
            org_html = "".join([f"<a href='https://github.com/{org['login']}' target='_blank'><img src='{org['avatar_url']}' width='35' style='border-radius:5px; margin-right:5px;' title='{org['login']}'></a>" for org in orgs])
            st.markdown(org_html, unsafe_allow_html=True)

def render_metrics_section(username, user_data):
    pr_data = get_search_data(f"author:{username}+type:pr")
    issue_data = get_search_data(f"author:{username}+type:issue")
    
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    recent_pr_data = get_search_data(f"author:{username}+type:pr+created:>={thirty_days_ago}")
    recent_issue_data = get_search_data(f"author:{username}+type:issue+created:>={thirty_days_ago}")
    
    recent_pr_count = recent_pr_data.get('total_count', 0) if recent_pr_data else 0
    recent_issue_count = recent_issue_data.get('total_count', 0) if recent_issue_data else 0
    
    repos_data = get_repo_data(username)
    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data) if repos_data else 0
    
    stat1, stat2, stat3, stat4, stat5, stat6 = st.columns(6)
    stat1.metric("퍼블릭 레포지토리", user_data.get('public_repos', 0))
    stat2.metric("팔로워", user_data.get('followers', 0))
    stat3.metric("팔로잉", user_data.get('following', 0))
    stat4.metric("받은 별(Stars)", total_stars)
    stat5.metric("작성한 PR", pr_data.get('total_count', 0) if pr_data else 0, 
                 delta=f"{recent_pr_count} (최근 30일)", delta_color="normal" if recent_pr_count > 0 else "off")
    stat6.metric("작성한 이슈", issue_data.get('total_count', 0) if issue_data else 0, 
                 delta=f"{recent_issue_count} (최근 30일)", delta_color="normal" if recent_issue_count > 0 else "off")

def render_overview_tab(username, baekjoon_id):
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.markdown(f'''
            <div style="text-align: center;">
                <a href="https://github.com/{username}">
                    <img src="https://github-readme-stats.vercel.app/api?username={username}&theme=radical&show_icons=true&hide_border=true&bg_color=0d1117" alt="GitHub Stats" style="max-width: 100%;">
                </a>
            </div>
        ''', unsafe_allow_html=True)
        
    with stat_col2:
        st.markdown(f'''
            <div style="text-align: center;">
                <a href="https://solved.ac/profile/{baekjoon_id}">
                    <img src="https://mazassumnida.wtf/api/v2/generate_badge?boj={baekjoon_id}" alt="Solved.ac Profile" style="max-width: 100%;">
                </a>
            </div>
        ''', unsafe_allow_html=True)
        
    st.write("")
    st.markdown(f'''
        <div style="background-color: #161b22; padding: 20px; border-radius: 10px; text-align: center;">
            <img src="https://ghchart.rshah.org/2ea043/{username}" alt="{username}의 깃허브 잔디" style="max-width: 100%;">
        </div>
    ''', unsafe_allow_html=True)

def render_repo_tab(username):
    repos_data = get_repo_data(username)
    if not repos_data:
        st.info("레포지토리 정보가 없습니다.")
        return

    df = pd.DataFrame(repos_data)
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("💻 실제 사용 언어 비율 (Bytes)")
        lang_bytes = {}
        for repo_name in df.head(5)['name']:
            langs = get_repo_languages(username, repo_name)
            for lang, b_count in langs.items():
                lang_bytes[lang] = lang_bytes.get(lang, 0) + b_count
        
        if lang_bytes:
            lang_df = pd.DataFrame(list(lang_bytes.items()), columns=['language', 'bytes'])
            fig_lang = px.pie(lang_df, values='bytes', names='language', hole=0.4)
            st.plotly_chart(fig_lang, width='stretch')
        else:
            st.info("언어 데이터가 없습니다.")
    
    with chart_col2:
        st.subheader("☁️ 주요 기술 스택 (Topics)")
        all_topics = [topic for topics in df.get('topics', []).dropna() for topic in topics]
        topic_counts = pd.Series(all_topics, dtype='object').value_counts().reset_index()
        topic_counts.columns = ['topic', 'count']
        
        if not topic_counts.empty:
            fig_topic = px.treemap(topic_counts, path=['topic'], values='count')
            st.plotly_chart(fig_topic, width='stretch')
        else:
            st.info("등록된 토픽이 없습니다.")
            
    st.subheader("⭐ 인기 레포지토리 (Top 5)")
    top_repos = df[['name', 'stargazers_count', 'html_url']].sort_values(by='stargazers_count', ascending=False).head(5)
    for _, repo in top_repos.iterrows():
        st.markdown(f"- **[{repo['name']}]({repo['html_url']})** (⭐ {repo['stargazers_count']})")

def render_activity_tab(username):
    events_data = get_recent_events(username)
    if not events_data:
        st.info("최근 활동이 없습니다.")
        return

    heatmap_data = []
    for event in events_data:
        dt_utc = datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        dt_kst = dt_utc + timedelta(hours=9)
        heatmap_data.append({'day': dt_kst.strftime('%A'), 'hour': dt_kst.hour})
        
    if heatmap_data:
        heat_df = pd.DataFrame(heatmap_data)
        heat_summary = heat_df.groupby(['day', 'hour']).size().reset_index(name='count')
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        st.subheader("🔥 코딩 시간대 히트맵 (최근 30개 활동)")
        fig_heat = px.density_heatmap(
            heat_summary, x='hour', y='day', z='count', 
            color_continuous_scale="Greens",
            range_color=[0, max(heat_summary['count'].max(), 2)],
            labels={'hour': '시간 (KST)', 'day': '요일', 'count': '활동 수'}
        )
        fig_heat.update_layout(
            yaxis={'categoryorder':'array', 'categoryarray':days_order[::-1]},
            xaxis={'tickmode': 'linear', 'dtick': 1, 'range': [-0.5, 23.5]}
        )
        st.plotly_chart(fig_heat, width='stretch')

    st.subheader("📦 최근 푸시 내역")
    push_events = [event for event in events_data if event.get('type') == 'PushEvent']
    if push_events:
        for event in push_events[:5]:
            repo_name = event['repo']['name']
            created_at = event['created_at'][:10]
            commits = event['payload'].get('commits', [])
            branch = event['payload'].get('ref', '').split('/')[-1]
            
            with st.container():
                st.markdown(f"**{created_at}** | 📦 **{repo_name}** (🌿 `{branch}`)")
                if commits:
                    for commit in commits:
                        msg = commit['message'].split('\n')[0]
                        st.markdown(f"> [`{commit['sha'][:7]}`](https://github.com/{repo_name}/commit/{commit['sha']}) {msg}")
                else:
                    st.markdown("> *새로운 브랜치 푸시 등 커밋 상세 내용이 없는 이벤트입니다.*")
                st.write("")
    else:
        st.info("최근 커밋 활동이 없습니다.")

def render_network_tab(username, avatar_url):
    followers = get_follow_data(username, "followers")
    following = get_follow_data(username, "following")
    if not followers or not following:
        st.info("팔로워 정보를 가져올 수 없습니다.")
        return

    follower_logins = {user['login']: user for user in followers}
    following_logins = {user['login']: user for user in following}
    mutual_logins = set(follower_logins.keys()).intersection(set(following_logins.keys()))
    
    if mutual_logins:
        st.write(f"🤝 **상호 팔로워 (맞팔) 네트워크 ({len(mutual_logins)}명)**")
        net = Network(height='500px', width='100%', bgcolor='#0d1117', font_color='#c9d1d9')
        net.add_node(username, label=username, title=username, shape='circularImage', image=avatar_url, size=35)
        
        for login in list(mutual_logins)[:20]:
            avatar = follower_logins[login]['avatar_url']
            net.add_node(login, label=login, title=login, shape='circularImage', image=avatar, size=25)
            net.add_edge(username, login, color="#2ea043")
            
        net.repulsion(node_distance=100, spring_length=100)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp:
            tmp_path = tmp.name
        net.save_graph(tmp_path)
        with open(tmp_path, 'r', encoding='utf-8') as f:
            html_data = f.read()
        os.remove(tmp_path)
        
        components.html(html_data, height=510)
    else:
        st.info("상호 팔로워 네트워크를 구성할 수 없습니다.")