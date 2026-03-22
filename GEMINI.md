# 🚀 Streamlit 기반 GitHub 프로필 대시보드 프로젝트 요약

## 📌 프로젝트 개요
Streamlit과 GitHub REST API를 활용하여 개발자 개인의 GitHub 활동, 통계, 네트워크를 한눈에 보여주는 포트폴리오 웹 대시보드 구축.

## 💡 주요 구현 기능
1. **프로필 요약 및 소셜 링크 연동**
   - GitHub 아바타, 바이오, 소속 기관(Organizations), 외부 블로그 및 SNS 링크 표시
2. **핵심 통계 메트릭 (Metrics)**
   - 총 퍼블릭 레포지토리, 팔로워/팔로잉 수, 전체 받은 Star 개수
   - 작성한 PR 및 Issue 개수 (최근 30일 변동 추이 포함)
3. **GitHub Stats & 외부 위젯 (🏆 랭크 & 잔디 탭)**
   - Vercel GitHub Readme Stats 위젯 연동
   - 백준(Solved.ac) 티어 배지 연동
   - GitHub Contribution Graph (잔디) 이미지 임베딩
4. **데이터 시각화 (📂 레포지토리 분석 탭)**
   - **언어 사용량 도넛 차트**: 상위 레포지토리의 바이트(Bytes) 단위 언어 비율 시각화 (`Plotly`)
   - **기술 스택 트리맵**: 레포지토리에 등록된 Topics 기반 관심 분야 시각화 (`Plotly`)
   - **인기 레포지토리 Top 5**: Star 개수 기준 정렬 및 링크 제공 (Fork된 저장소 필터링)
5. **활동 분석 (🕒 활동 타임라인 탭)**
   - **코딩 시간대 히트맵**: 최근 활동 기준 요일/시간별(KST 적용) 커밋 빈도 시각화 (`Plotly Density Heatmap`)
   - **최근 푸시 내역**: 최근 5개의 Push Event 커밋 내역 및 브랜치 정보 타임라인 표시
6. **인터랙티브 네트워크 (🤝 팔로워 네트워크 탭)**
   - 서로 팔로우하는 '맞팔' 유저들을 노드로 구성한 물리 엔진 적용 네트워크 그래프 구현 (`Pyvis`)

## 🛠️ 기술 스택 및 라이브러리
- **Web Framework**: `streamlit`
- **API 통신**: `requests` (GitHub API 호출 및 `@st.cache_data`를 통한 캐싱/최적화)
- **Data Processing**: `pandas`
- **Visualization**: `plotly`, `pyvis`

## 🏗️ 아키텍처 및 리팩토링 설계 (관심사의 분리)
코드의 가독성과 유지보수성을 높이기 위해 3개의 모듈로 완벽히 분리.
- `github_api.py`: GitHub API 통신 및 데이터 전처리, Streamlit 캐싱 전담 모듈
- `ui_components.py`: Streamlit 화면 UI 렌더링 전담 모듈 (`render_...` 함수들)
- `streamlit_app.py`: 메인 진입점. 레이아웃과 탭(`st.tabs`)을 구성하고 컴포넌트를 조립하는 컨트롤 타워

## 🎨 UI/UX 개선 사항
- **GitHub 다크 모드 테마 적용**: `.streamlit/config.toml`을 통해 GitHub 고유의 색상 코드(#0d1117 등) 반영
- **의존성 패키지 정리**: 클라우드 배포 시 충돌을 방지하기 위해 `requirements.txt`를 핵심 패키지 5개로 경량화
- **Early Return 패턴 적용**: 불필요한 조건문 중첩을 제거하여 파이써닉한 코드로 최적화