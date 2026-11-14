"""
배트맨토토(프로토 승부식) 배구 경기 데이터 수집, 가공 및 대시보드 자동 연동 엔진
- 대상: KOVO V-리그 남자부(7개 구단), 여자부(7개 구단)
- 수집 및 축적 항목:
  1) 일반 승/패: 홈/원정 배당, 경기 결과(승/패), 세트 스코어, 정배/역배 적중 여부
  2) 세트 핸디캡: 기준점(-1.5, +1.5, -2.5 등), 배당, 마핸승/플핸승 판정
  3) 총득점 언더/오버: 기준점(182.5, 178.5 등), 배당, 총득점, 언더/오버 적중 결과
- 기능:
  - 배트맨토토 결과 데이터 정규화 및 누적 병합
  - 누계 러닝 지표(정배 적중률, 오버율, 구단별 마핸/플핸 극복률) 자동 산출
  - 단일 실행 웹 대시보드(index.html) 자동 재빌드
"""

import json
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "matches.json")
HTML_PATH = os.path.join(BASE_DIR, "index.html")

MENS_TEAMS = [
    "한국전력 빅스톰", "현대캐피탈 스카이워커스", "대한항공 점보스",
    "우리카드 우리WON", "KB손해보험 스타즈", "삼성화재 블루팡스", "OK저축은행 읏맨"
]

WOMENS_TEAMS = [
    "흥국생명 핑크스파이더스", "한국도로공사 하이패스", "IBK기업은행 알토스",
    "정관장 레드스파크스", "GS칼텍스 서울Kixx", "현대건설 힐스테이트", "SOOP SOOPers"
]

TEAM_ALIASES = {
    "한국전력": "한국전력 빅스톰",
    "현대캐피": "현대캐피탈 스카이워커스",
    "현대캐피탈": "현대캐피탈 스카이워커스",
    "대한항공": "대한항공 점보스",
    "우리카드": "우리카드 우리WON",
    "KB손보": "KB손해보험 스타즈",
    "KB손해보험": "KB손해보험 스타즈",
    "삼성화재": "삼성화재 블루팡스",
    "OK저축": "OK저축은행 읏맨",
    "OK저축은행": "OK저축은행 읏맨",
    "흥국생명": "흥국생명 핑크스파이더스",
    "도로공사": "한국도로공사 하이패스",
    "한국도로공사": "한국도로공사 하이패스",
    "IBK기업": "IBK기업은행 알토스",
    "IBK기업은행": "IBK기업은행 알토스",
    "정관장": "정관장 레드스파크스",
    "대전정관": "정관장 레드스파크스",
    "GS칼텍스": "GS칼텍스 서울Kixx",
    "현대건설": "현대건설 힐스테이트",
    "페퍼저축": "SOOP SOOPers",
    "페퍼저축은행": "SOOP SOOPers",
    "페퍼저축은행 AI페퍼스": "SOOP SOOPers",
    "SOOP": "SOOP SOOPers",
    "전남광주 SOOP SOOPers": "SOOP SOOPers"
}

def normalize_team(name):
    clean = name.strip()
    return TEAM_ALIASES.get(clean, clean)

def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_updated": "", "mens": [], "womens": []}

def save_data(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] data/matches.json 저장 완료 (남배: {len(data['mens'])}경기, 여배: {len(data['womens'])}경기)")

def rebuild_html():
    cmd = f"python3 {os.path.join(BASE_DIR, 'build_dashboard.py')}"
    os.system(cmd)
    print(f"[OK] index.html 대시보드 동기화 완료 ({HTML_PATH})")

def compute_stats(matches):
    finished = [m for m in matches if m.get("status") == "종료"]
    total = len(finished)
    if total == 0:
        return {"total": 0, "fav_rate": 0, "over_rate": 0}
    
    fav_hits = sum(1 for m in finished if m.get("win_lose", {}).get("hit_type") in ["정배", "극정배"])
    over_hits = sum(1 for m in finished if m.get("under_over", {}).get("result") == "OVER")
    
    return {
        "total": total,
        "fav_hits": fav_hits,
        "fav_rate": round(fav_hits / total * 100, 1),
        "over_hits": over_hits,
        "over_rate": round(over_hits / total * 100, 1)
    }

def print_summary():
    data = load_data()
    print("=" * 60)
    print(f"  🏐 V-리그 배트맨토토 누적 통계 허브 현황 (동기화: {data.get('last_updated', '-')})")
    print("=" * 60)
    
    m_stats = compute_stats(data.get("mens", []))
    w_stats = compute_stats(data.get("womens", []))
    
    print(f"▶ 남자부 (KOVO남) 총 {len(data.get('mens', []))}경기 등록 (종료 {m_stats['total']}경기)")
    print(f"  - 정배 적중률: {m_stats.get('fav_rate', 0)}% ({m_stats.get('fav_hits', 0)}/{m_stats.get('total', 0)})")
    print(f"  - 오버 비율:   {m_stats.get('over_rate', 0)}% ({m_stats.get('over_hits', 0)}/{m_stats.get('total', 0)})")
    print("-" * 60)
    print(f"▶ 여자부 (KOVO여) 총 {len(data.get('womens', []))}경기 등록 (종료 {w_stats['total']}경기)")
    print(f"  - 정배 적중률: {w_stats.get('fav_rate', 0)}% ({w_stats.get('fav_hits', 0)}/{w_stats.get('total', 0)})")
    print(f"  - 오버 비율:   {w_stats.get('over_rate', 0)}% ({w_stats.get('over_hits', 0)}/{w_stats.get('total', 0)})")
    print("=" * 60)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--rebuild":
        rebuild_html()
    elif len(sys.argv) > 1 and sys.argv[1] == "--summary":
        print_summary()
    else:
        print_summary()
        rebuild_html()
