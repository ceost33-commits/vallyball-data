import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "matches.json")
OUTPUT_HTML = os.path.join(BASE_DIR, "index.html")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

MENS_TEAMS = [
    "한국전력 빅스톰", "현대캐피탈 스카이워커스", "대한항공 점보스",
    "우리카드 우리WON", "KB손해보험 스타즈", "삼성화재 블루팡스", "OK저축은행 읏맨"
]

WOMENS_TEAMS = [
    "흥국생명 핑크스파이더스", "한국도로공사 하이패스", "IBK기업은행 알토스",
    "정관장 레드스파크스", "GS칼텍스 서울Kixx", "현대건설 힐스테이트", "SOOP SOOPers"
]

def get_league_handicap_type(m):
    std = m["handicap"]["standard"]
    res = m["handicap"]["result"]
    if res == "HOME":
        return "마핸" if std < 0 else "플핸"
    else:
        return "마핸" if std > 0 else "플핸"

# ---------------------------------------------------------------- 퐁당(교대) 패턴
# 퐁당 = 결과가 A↔B로 번갈아 이어지는 흐름. 최근 경기부터 거꾸로 세어
# 서로 반대 결과가 연달아 나온 길이(교대 경기 수)를 구한다.
# 1사이클(언→옵 / 옵→언) = 2경기 = 1퐁당. 따라서 퐁당 수 = 교대 경기 수 / 2
# (2경기 → 1퐁당, 3경기 → 1.5퐁당, 4경기 → 2퐁당, 5경기 → 2.5퐁당, 6경기 → 3퐁당).
# 1.5퐁당(3경기) 이상일 때만 퐁당으로 강조한다. 'N연속 퐁당' 같은 경기 수 표기는 쓰지 않는다.
HANDI_SYM = {"마핸": "마", "플핸": "플"}
UO_SYM = {"OVER": "오", "UNDER": "언"}
UO_KO = {"OVER": "오버", "UNDER": "언더"}
HANDI_FS = {"마핸": "fs-ma", "플핸": "fs-pl"}
UO_FS = {"OVER": "fs-over", "UNDER": "fs-under"}
PD_MIN = 3


def alt_run_len(seq):
    """최근 결과부터 거꾸로 세어 서로 다른 값이 번갈아 이어진 길이."""
    if not seq:
        return 0
    n = 1
    for i in range(len(seq) - 2, -1, -1):
        if seq[i] != seq[i + 1]:
            n += 1
        else:
            break
    return n


def fmt_pong(alt):
    """교대 경기 수 → 퐁당 수 표기 (2경기 = 1사이클 = 1퐁당)."""
    if alt <= 0:
        return "0퐁당"
    return f"{alt / 2:g}퐁당"


def flow_badges(seq, sym_map, cls_map, keep=6):
    """최근 경기 흐름 기호(오래된 → 최신, 최신은 테두리 강조)."""
    tail = seq[-keep:]
    out = []
    for i, v in enumerate(tail):
        latest = " fs-latest" if i == len(tail) - 1 else ""
        out.append(f'<span class="fs {cls_map[v]}{latest}">{sym_map[v]}</span>')
    return "".join(out)


def pd_card_html(title, pair_label, alt, seq, sym_map, cls_map, streak_n, streak_type):
    """스트릭 영역에 붙는 퐁당 카드 1장."""
    if alt <= 0:
        return (
            f'<div class="streak-card streak-card-gray">'
            f'<div class="streak-card-top"><span class="streak-label">{title}</span>'
            f'<span class="streak-badge-pill pill-gray">-</span></div>'
            f'<div class="streak-val">기록 없음</div></div>'
        )
    on = alt >= PD_MIN
    card_cls = "streak-card-pd" if on else "streak-card-plain"
    pill_cls = "pill-pd" if on else "pill-gray"
    pill_txt = f"🔄 {fmt_pong(alt)}" if on else ("1퐁당" if alt == 2 else "퐁당 없음")
    if on:
        val = f"{fmt_pong(alt)} ({alt}경기)"
    elif alt == 2:
        val = f"1퐁당 ({alt}경기)"
    else:
        val = f"{streak_n}연속 {streak_type} 유지"
    shown = min(len(seq), 6)
    flow = flow_badges(seq, sym_map, cls_map)
    return (
        f'<div class="streak-card {card_cls}">'
        f'<div class="streak-card-top"><span class="streak-label">{title}</span>'
        f'<span class="streak-badge-pill {pill_cls}">{pill_txt}</span></div>'
        f'<div class="streak-val">{val}</div>'
        f'<div class="pd-flow"><span class="pd-flow-lbl">최근 {shown}경기</span>{flow}</div>'
        f'</div>'
    )


def render_pd_teams_box(teams, matches):
    """리그 전체 뷰: 현재 퐁당(1.5퐁당 = 3경기 이상 교대) 진행 중인 구단 요약 박스."""
    rows = []
    for t in teams:
        tms = [m for m in matches if m.get("status") == "종료" and t in (m["home"], m["away"])]
        tms.sort(key=lambda x: x.get("date", ""))
        h_seq = [get_league_handicap_type(m) for m in tms]
        uo_seq = [m["under_over"]["result"] for m in tms]
        ha, ua = alt_run_len(h_seq), alt_run_len(uo_seq)
        if ha >= PD_MIN:
            rows.append((ha, t, pd_chip_html(t.split()[0], "마↔플", ha, h_seq, HANDI_SYM, HANDI_FS, "ma")))
        if ua >= PD_MIN:
            rows.append((ua, t, pd_chip_html(t.split()[0], "언↔오", ua, uo_seq, UO_SYM, UO_FS, "uo")))
    rows.sort(key=lambda r: (-r[0], r[1]))
    chips = "".join(r[2] for r in rows)
    if chips:
        body = f'<div class="pd-teams-chips">{chips}</div>'
        sub = f"1.5퐁당(3경기) 이상 · {len(rows)}건"
    else:
        body = '<div class="pd-teams-empty">현재 1.5퐁당(3경기) 이상 진행 구단 없음</div>'
        sub = "1.5퐁당(3경기) 이상"
    return f"""
      <div class="pd-teams-box">
        <div class="pd-teams-head">
          <span class="pd-teams-title">🔄 현재 퐁당 진행 중 구단</span>
          <span class="pd-teams-sub">{sub}</span>
        </div>
        {body}
      </div>"""


def pd_chip_html(team_short, pair_label, alt, seq, sym_map, cls_map, kind):
    flow = flow_badges(seq, sym_map, cls_map, keep=min(max(alt, 3), 5))
    return (
        f'<span class="pd-chip pd-chip-{kind}">'
        f'<span class="pd-chip-team">{team_short}</span>'
        f'<span class="pd-chip-tag">{pair_label} {fmt_pong(alt)} ({alt}경기)</span>'
        f'<span class="pd-chip-flow">{flow}</span>'
        f'</span>'
    )


def render_team_panel_html(league_key, teams, matches):
    prefix = "mt" if league_key == "mens" else "wt"
    league_title = "남자부 7개 구단 선택" if league_key == "mens" else "여자부 7개 구단 선택"
    buttons = []
    for idx, t in enumerate(teams):
        completed = [m for m in matches if m.get("status") == "종료" and (m.get("home") == t or m.get("away") == t)]
        wins = 0
        for m in completed:
            is_home = (m["home"] == t)
            if (is_home and m["win_lose"]["winner"] == "HOME") or (not is_home and m["win_lose"]["winner"] == "AWAY"):
                wins += 1
        losses = len(completed) - wins
        record_str = f"{wins}승 {losses}패"
        short_name = t.split()[0]
        buttons.append(f"""
          <label for="r-{prefix}-{idx}" class="team-btn" id="lbl-{prefix}-{idx}">
            <span class="team-btn-name">{short_name}</span>
            <span class="team-btn-record">{record_str}</span>
          </label>""")
    return f"""
    <div class="team-panel" id="team-panel-{league_key}">
      <div class="team-panel-header">
        <span>구단을 터치하여 누적 스트릭을 확인하세요:</span>
        <strong>{league_title}</strong>
      </div>
      <div class="team-grid">
        {"".join(buttons)}
      </div>
    </div>"""

def render_match_cards(matches_desc, running_streaks_map, focus_team=None):
    if not matches_desc:
        return '<div class="empty-state">해당 조건의 경기 데이터가 없습니다.</div>'

    total_n = len(matches_desc)
    cards = []
    for idx, m in enumerate(matches_desc):
        is_completed = (m.get("status") == "종료")
        home_won = (m["win_lose"].get("winner") == "HOME")
        away_won = (m["win_lose"].get("winner") == "AWAY")
        is_home_focus = (focus_team is not None and m.get("home") == focus_team)
        is_away_focus = (focus_team is not None and m.get("away") == focus_team)
        cumul_num = total_n - idx
        s_info = running_streaks_map.get(m.get("id"))

        if is_completed:
            hit_desc = "홈승" if home_won else "원정승"
            hit_type = m["win_lose"].get("hit_type", "")
            badge_cls = "badge-lose" if "역배" in hit_type else "badge-win"
            fav_icon = "🎯 정배" if "정배" in hit_type else "⚡ 역배"
            if m["win_lose"].get("cancelled"):
                w_badge = f'<span class="cell-result-badge {badge_cls}">{fav_icon} [승패 취소 · {hit_desc}]</span>'
            else:
                w_badge = f'<span class="cell-result-badge {badge_cls}">{fav_icon} [{hit_desc} {m["win_lose"].get("hit_odds", "")}]</span>'
            w_streak_badge = f'<span class="streak-cell-badge {s_info["fav_cls"]}">{s_info["fav_tag"]}</span>' if s_info else ''
        else:
            if m["win_lose"].get("cancelled"):
                w_badge = '<span class="cell-result-badge badge-pending">승패 미발매</span>'
            else:
                w_badge = '<span class="cell-result-badge badge-pending">발매중</span>'
            w_streak_badge = ''

        if is_completed:
            h_desc = s_info["h_detail_label"] if s_info else (f"⚡ {get_league_handicap_type(m)}" if get_league_handicap_type(m) == "마핸" else f"🛡️ {get_league_handicap_type(m)}")
            h_badge = f'<span class="cell-result-badge badge-win">{h_desc}</span>'
            h_streak_badge = f'<span class="streak-cell-badge {s_info["h_cls"]}">{s_info["h_tag"]}</span>' if s_info else ''
        else:
            h_badge = '<span class="cell-result-badge badge-pending">발매중</span>'
            h_streak_badge = ''

        if is_completed:
            is_over = (m["under_over"].get("result") == "OVER")
            badge_cls = "badge-over" if is_over else "badge-under"
            uo_desc = f"🔥 오버 ({m.get('total_points', 0)}점)" if is_over else f"🧊 언더 ({m.get('total_points', 0)}점)"
            uo_badge = f'<span class="cell-result-badge {badge_cls}">{uo_desc}</span>'
            uo_streak_badge = f'<span class="streak-cell-badge {s_info["uo_cls"]}">{s_info["uo_tag"]}</span>' if s_info else ''
        else:
            uo_badge = '<span class="cell-result-badge badge-pending">발매중</span>'
            uo_streak_badge = ''

        sets_str = " / ".join(m.get("sets_detail", [])) if m.get("sets_detail") else ""

        streak_bar_html = ""
        if s_info:
            w_pill = f'<span class="streak-pill {s_info["w_cls"]}">{s_info["w_tag"]}</span>' if focus_team else ''
            h_pd_pill = (f'<span class="streak-pill pill-pd">🔄 마↔플 {fmt_pong(s_info["h_alt"])} ({s_info["h_alt"]}경기)</span>'
                         if s_info.get("h_alt", 0) >= PD_MIN else '')
            uo_pd_pill = (f'<span class="streak-pill pill-pd">🔄 언↔오 {fmt_pong(s_info["uo_alt"])} ({s_info["uo_alt"]}경기)</span>'
                          if s_info.get("uo_alt", 0) >= PD_MIN else '')
            streak_bar_html = f"""
              <div class="match-streak-pill-bar">
                {w_pill}
                <span class="streak-pill {s_info['fav_cls']}">{s_info['fav_tag']}</span>
                <span class="streak-pill {s_info['h_cls']}">{s_info['h_tag']}</span>
                {h_pd_pill}
                <span class="streak-pill {s_info['uo_cls']}">{s_info['uo_tag']}</span>
                {uo_pd_pill}
              </div>"""

        std = m["handicap"]["standard"]
        std_str = f"+{std}" if std > 0 else f"{std}"

        cards.append(f"""
          <div class="match-card">
            <div class="match-top">
              <div class="match-top-left">
                <span class="match-cumul-badge">누계 #{cumul_num}</span>
                <span class="match-round-text">{m['round']} · #{m['win_lose']['match_no']}</span>
              </div>
              <span class="match-date">{m['date']}</span>
            </div>
            {streak_bar_html}
            <div class="match-fixture">
              <div class="team-box {'focused' if is_home_focus else ''}">
                <span class="team-badge">홈</span>
                <span class="team-name" style="{'color: var(--primary); font-weight:800;' if is_home_focus else ''}">{m['home']}</span>
              </div>
              <div class="score-container">
                <div class="score-box" style="color: {'var(--text-white)' if is_completed else 'var(--text-sub)'}">
                  {m['set_score'] if m.get('set_score') else '-'}
                </div>
                {f'<div class="score-detail">{sets_str}</div>' if sets_str else ''}
              </div>
              <div class="team-box away {'focused' if is_away_focus else ''}">
                <span class="team-name" style="{'color: var(--primary); font-weight:800;' if is_away_focus else ''}">{m['away']}</span>
                <span class="team-badge">원정</span>
              </div>
            </div>
            <div class="toto-grid">
              <div class="toto-cell">
                <div class="cell-title">
                  <span>[1] 일반 승·패</span>
                  <span style="font-size:10px; color:var(--text-sub)">#{m['win_lose']['match_no']}</span>
                </div>
                <div class="cell-odds-row">
                  <div class="odds-item {'win' if home_won else ''}">
                    <span class="odds-label">홈</span>
                    <span class="odds-val">{m['win_lose']['home_odds']}</span>
                  </div>
                  <div style="color:var(--text-sub); font-size:10px;">vs</div>
                  <div class="odds-item {'win' if away_won else ''}">
                    <span class="odds-label">원정</span>
                    <span class="odds-val">{m['win_lose']['away_odds']}</span>
                  </div>
                </div>
                {w_badge}
                {w_streak_badge}
              </div>
              <div class="toto-cell">
                <div class="cell-title">
                  <span>[2] 세트 핸디캡</span>
                  <span style="color:var(--primary); font-size:10px;">홈기준 {std_str}</span>
                </div>
                <div class="cell-odds-row">
                  <div class="odds-item {'win' if m['handicap'].get('result') == 'HOME' else ''}">
                    <span class="odds-label">홈</span>
                    <span class="odds-val">{m['handicap']['home_odds']}</span>
                  </div>
                  <div style="color:var(--text-sub); font-size:10px;">vs</div>
                  <div class="odds-item {'win' if m['handicap'].get('result') == 'AWAY' else ''}">
                    <span class="odds-label">원정</span>
                    <span class="odds-val">{m['handicap']['away_odds']}</span>
                  </div>
                </div>
                {h_badge}
                {h_streak_badge}
              </div>
              <div class="toto-cell">
                <div class="cell-title">
                  <span>[3] 언더/오버</span>
                  <span style="color:var(--warning); font-size:10px;">기준 {m['under_over']['standard']}</span>
                </div>
                <div class="cell-odds-row">
                  <div class="odds-item {'win' if m['under_over'].get('result') == 'OVER' else ''}">
                    <span class="odds-label">오버</span>
                    <span class="odds-val">{m['under_over']['over_odds']}</span>
                  </div>
                  <div style="color:var(--text-sub); font-size:10px;">vs</div>
                  <div class="odds-item {'win' if m['under_over'].get('result') == 'UNDER' else ''}">
                    <span class="odds-label">언더</span>
                    <span class="odds-val">{m['under_over']['under_odds']}</span>
                  </div>
                </div>
                {uo_badge}
                {uo_streak_badge}
              </div>
            </div>
          </div>""")
    return "".join(cards)

def render_team_view_pane(view_id, matches, team):
    team_short = team.split()[0]
    team_matches = [m for m in matches if m.get("home") == team or m.get("away") == team]
    chrono = sorted(team_matches, key=lambda x: x.get("date", ""))
    desc = sorted(team_matches, key=lambda x: x.get("date", ""), reverse=True)

    completed = [m for m in chrono if m.get("status") == "종료"]
    t_total = len(completed)
    t_wins = 0
    t_ma_cnt = t_pl_cnt = 0
    t_overs = 0
    t_pts = 0
    t_fav_hits = t_dog_hits = 0
    t_when_fav_w = t_when_fav_l = t_when_dog_w = t_when_dog_l = 0

    w_streak, w_type = 0, None
    fav_streak, fav_type = 0, None
    h_streak, h_type = 0, None
    uo_streak, uo_type = 0, None
    h_hist, uo_hist = [], []
    running_streaks_map = {}

    for m in completed:
        t_pts += (m.get("total_points") or 0)
        is_home = (m["home"] == team)
        won = (is_home and m["win_lose"]["winner"] == "HOME") or (not is_home and m["win_lose"]["winner"] == "AWAY")
        if won:
            t_wins += 1

        team_is_fav = (m["win_lose"].get("favorite") == ("HOME" if is_home else "AWAY"))
        if team_is_fav:
            if won: t_when_fav_w += 1
            else: t_when_fav_l += 1
        else:
            if won: t_when_dog_w += 1
            else: t_when_dog_l += 1

        is_fav_hit = ("정배" in (m["win_lose"].get("hit_type") or ""))
        if is_fav_hit: t_fav_hits += 1
        else: t_dog_hits += 1

        res_h = get_league_handicap_type(m)
        if res_h == "마핸":
            t_ma_cnt += 1
        else:
            t_pl_cnt += 1

        if m["under_over"]["result"] == "OVER":
            t_overs += 1

        res_w = "W" if won else "L"
        if res_w == w_type: w_streak += 1
        else: w_type = res_w; w_streak = 1

        res_fav = "정배" if is_fav_hit else "역배"
        if res_fav == fav_type: fav_streak += 1
        else: fav_type = res_fav; fav_streak = 1

        if res_h == h_type: h_streak += 1
        else: h_type = res_h; h_streak = 1

        res_uo = m["under_over"]["result"]
        if res_uo == uo_type: uo_streak += 1
        else: uo_type = res_uo; uo_streak = 1

        h_hist.append(res_h)
        uo_hist.append(res_uo)
        h_alt = alt_run_len(h_hist)
        uo_alt = alt_run_len(uo_hist)

        running_streaks_map[m["id"]] = {
            "h_alt": h_alt,
            "uo_alt": uo_alt,
            "w_tag": f"{w_streak}연승 🔥" if w_type == "W" else f"{w_streak}연패 🧊",
            "w_cls": "pill-fire" if w_type == "W" else "pill-ice",
            "fav_tag": f"{fav_streak}연속 {fav_type} {'🎯' if fav_type == '정배' else '⚡'}",
            "fav_cls": "pill-green" if fav_type == "정배" else "pill-fire",
            "h_tag": f"{h_streak}연속 {res_h} {'⚡' if res_h == '마핸' else '🛡️'}",
            "h_cls": "pill-purple" if res_h == "마핸" else "pill-green",
            "h_detail_label": f"⚡ {res_h}" if res_h == "마핸" else f"🛡️ {res_h}",
            "uo_tag": f"{uo_streak}연속 오버 🔥" if uo_type == "OVER" else f"{uo_streak}연속 언더 🧊",
            "uo_cls": "pill-orange" if uo_type == "OVER" else "pill-ice",
        }

    win_rate = round(t_wins / t_total * 100) if t_total else 0
    fav_hit_rate = round(t_fav_hits / t_total * 100) if t_total else 0
    ma_rate = round(t_ma_cnt / t_total * 100) if t_total else 0
    over_rate = round(t_overs / t_total * 100) if t_total else 0
    avg_pts = f"{(t_pts / t_total):.1f}" if t_total else "0.0"

    if t_total == 0:
        win_txt = fav_txt = handi_txt = uo_txt = "기록 없음"
        w_card_cls = fav_card_cls = h_card_cls = uo_card_cls = "streak-card-gray"
        w_pill_cls = fav_pill_cls = h_pill_cls = uo_pill_cls = "pill-gray"
        w_badge_lbl = fav_badge_lbl = h_badge_lbl = uo_badge_lbl = "-"
    else:
        win_txt = f"{w_streak}연승 진행 중 🔥" if w_type == "W" else f"{w_streak}연패 진행 중 🧊"
        w_card_cls = "streak-card-fire" if w_type == "W" else "streak-card-ice"
        w_pill_cls = "pill-fire" if w_type == "W" else "pill-ice"
        w_badge_lbl = "🔥 연승" if w_type == "W" else "🧊 연패"

        fav_txt = f"{fav_streak}경기 연속 정배 🎯" if fav_type == "정배" else f"{fav_streak}경기 연속 역배 ⚡"
        fav_card_cls = "streak-card-green" if fav_type == "정배" else "streak-card-fire"
        fav_pill_cls = "pill-green" if fav_type == "정배" else "pill-fire"
        fav_badge_lbl = "🎯 정배" if fav_type == "정배" else "⚡ 역배"

        handi_txt = f"{h_streak}경기 연속 마핸 ⚡" if h_type == "마핸" else f"{h_streak}경기 연속 플핸 🛡️"
        h_card_cls = "streak-card-purple" if h_type == "마핸" else "streak-card-green"
        h_pill_cls = "pill-purple" if h_type == "마핸" else "pill-green"
        h_badge_lbl = "⚡ 마핸" if h_type == "마핸" else "🛡️ 플핸"

        uo_txt = f"{uo_streak}연속 오버 진행 🔥" if uo_type == "OVER" else f"{uo_streak}연속 언더 진행 🧊"
        uo_card_cls = "streak-card-orange" if uo_type == "OVER" else "streak-card-ice"
        uo_pill_cls = "pill-orange" if uo_type == "OVER" else "pill-ice"
        uo_badge_lbl = "🔥 오버" if uo_type == "OVER" else "🧊 언더"

    pd_cards_html = (
        pd_card_html("마핸/플핸 퐁당", "마핸↔플핸", alt_run_len(h_hist), h_hist, HANDI_SYM, HANDI_FS, h_streak, h_type) +
        pd_card_html("언오버 퐁당", "언더↔오버", alt_run_len(uo_hist), uo_hist, UO_SYM, UO_FS, uo_streak, UO_KO.get(uo_type, uo_type))
    )

    cards_html = render_match_cards(desc, running_streaks_map, focus_team=team)

    return f"""
    <div class="view-pane" id="{view_id}">
      <div class="streak-section">
        <div class="streak-header">
          <span class="streak-title">🔥 <strong>{team_short}</strong> 현재 연속 패턴 (Streak)</span>
          <span class="streak-tag">실시간 누적</span>
        </div>
        <div class="streak-grid">
          <div class="streak-card {w_card_cls}">
            <div class="streak-card-top">
              <span class="streak-label">구단 승패</span>
              <span class="streak-badge-pill {w_pill_cls}">{w_badge_lbl}</span>
            </div>
            <div class="streak-val">{win_txt}</div>
          </div>
          <div class="streak-card {fav_card_cls}">
            <div class="streak-card-top">
              <span class="streak-label">정배/역배 연속</span>
              <span class="streak-badge-pill {fav_pill_cls}">{fav_badge_lbl}</span>
            </div>
            <div class="streak-val">{fav_txt}</div>
          </div>
          <div class="streak-card {h_card_cls}">
            <div class="streak-card-top">
              <span class="streak-label">세트 마핸/플핸</span>
              <span class="streak-badge-pill {h_pill_cls}">{h_badge_lbl}</span>
            </div>
            <div class="streak-val">{handi_txt}</div>
          </div>
          <div class="streak-card {uo_card_cls}">
            <div class="streak-card-top">
              <span class="streak-label">총득점 언더/오버</span>
              <span class="streak-badge-pill {uo_pill_cls}">{uo_badge_lbl}</span>
            </div>
            <div class="streak-val">{uo_txt}</div>
          </div>
          {pd_cards_html}
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-header"><span>🏆 구단 일반 승률</span><span>{team_short}</span></div>
          <div class="stat-val" style="color: var(--primary);">{win_rate}%</div>
          <div class="stat-sub">{t_wins}승 {t_total - t_wins}패 (총 {t_total}경기)</div>
        </div>
        <div class="stat-card">
          <div class="stat-header"><span>🎯 경기 정배 적중률</span><span>승패무관</span></div>
          <div class="stat-val" style="color: var(--success);">{fav_hit_rate}%</div>
          <div class="stat-sub">정배 {t_fav_hits}경기 · 역배 {t_dog_hits}경기</div>
        </div>
        <div class="stat-card">
          <div class="stat-header"><span>⚖️ 경기 마핸/플핸 비율</span><span>핸디캡 결과</span></div>
          <div class="stat-val" style="color: var(--purple);">마핸 {ma_rate}%</div>
          <div class="stat-sub">마핸 {t_ma_cnt}경기 · 플핸 {t_pl_cnt}경기</div>
        </div>
        <div class="stat-card">
          <div class="stat-header"><span>📈 오버 비율 (기준점)</span><span>U/O 경향</span></div>
          <div class="stat-val" style="color: var(--warning);">{over_rate}%</div>
          <div class="stat-sub">언더 비율: {100 - over_rate if t_total else 0}%</div>
        </div>
        <div class="stat-card">
          <div class="stat-header"><span>🎯 경기당 평균 총득점</span><span>합산 점수</span></div>
          <div class="stat-val" style="color: #67e8f9;">{avg_pts}점</div>
          <div class="stat-sub">정배시 {t_when_fav_w}승{t_when_fav_l}패 · 역배시 {t_when_dog_w}승{t_when_dog_l}패</div>
        </div>
      </div>

      <div class="controls-bar">
        <div class="section-title">
          <span>🛡️ {team} 누적 경기 히스토리</span>
          <span style="font-size: 12px; color: var(--text-sub);">{len(desc)}경기 누적</span>
        </div>
        <div class="view-toggles">
          <label for="r-sort-asc" class="toggle-btn">
            <span class="sort-text-desc">⬇️ 최신 일정순</span>
            <span class="sort-text-asc">⬆️ 개막 순차순</span>
          </label>
        </div>
      </div>

      <div class="match-list">
        {cards_html}
      </div>
    </div>"""

def render_all_view_pane(view_id, league_key, matches, teams):
    league_name = "남자부" if league_key == "mens" else "여자부"
    chrono = sorted(matches, key=lambda x: x.get("date", ""))
    desc = sorted(matches, key=lambda x: x.get("date", ""), reverse=True)
    completed = [m for m in chrono if m.get("status") == "종료"]
    t_total = len(completed)
    pending = len(matches) - t_total

    fav_hits = ma_wins = pl_wins = overs = 0
    fav_streak, fav_type = 0, None
    h_streak, h_type = 0, None
    uo_streak, uo_type = 0, None
    h_hist, uo_hist = [], []
    running_streaks_map = {}

    for m in completed:
        is_fav = ("정배" in (m["win_lose"].get("hit_type") or ""))
        if is_fav: fav_hits += 1
        res_fav = "정배" if is_fav else "역배"
        if res_fav == fav_type: fav_streak += 1
        else: fav_type = res_fav; fav_streak = 1

        res_h = get_league_handicap_type(m)
        if res_h == "마핸": ma_wins += 1
        else: pl_wins += 1
        if res_h == h_type: h_streak += 1
        else: h_type = res_h; h_streak = 1

        res_uo = m["under_over"]["result"]
        if res_uo == "OVER": overs += 1
        if res_uo == uo_type: uo_streak += 1
        else: uo_type = res_uo; uo_streak = 1

        h_hist.append(res_h)
        uo_hist.append(res_uo)

        running_streaks_map[m["id"]] = {
            "h_alt": alt_run_len(h_hist),
            "uo_alt": alt_run_len(uo_hist),
            "w_tag": "",
            "w_cls": "",
            "fav_tag": f"{fav_streak}연속 {fav_type} {'🎯' if is_fav else '⚡'}",
            "fav_cls": "pill-green" if is_fav else "pill-fire",
            "h_tag": f"{h_streak}연속 {res_h} {'⚡' if res_h == '마핸' else '🛡️'}",
            "h_cls": "pill-purple" if res_h == "마핸" else "pill-green",
            "h_detail_label": f"⚡ {res_h}" if res_h == "마핸" else f"🛡️ {res_h}",
            "uo_tag": f"{uo_streak}연속 오버 🔥" if uo_type == "OVER" else f"{uo_streak}연속 언더 🧊",
            "uo_cls": "pill-orange" if uo_type == "OVER" else "pill-ice",
        }

    fav_rate = round(fav_hits / t_total * 100) if t_total else 0
    ma_rate = round(ma_wins / t_total * 100) if t_total else 0
    over_rate = round(overs / t_total * 100) if t_total else 0

    if t_total == 0:
        fav_txt = flow_txt = handi_txt = uo_txt = "기록 없음"
        fav_card_cls = h_card_cls = uo_card_cls = "streak-card-gray"
        fav_pill_cls = h_pill_cls = uo_pill_cls = "pill-gray"
        fav_badge_lbl = h_badge_lbl = uo_badge_lbl = "-"
    else:
        fav_txt = f"{fav_streak}경기 연속 정배 적중 🎯" if fav_type == "정배" else f"{fav_streak}경기 연속 역배 발생 ⚡"
        flow_txt = "정배 흐름 유지 중 🎯" if fav_type == "정배" else "역배 흐름 터지는 중 ⚡"
        fav_card_cls = "streak-card-green" if fav_type == "정배" else "streak-card-fire"
        fav_pill_cls = "pill-green" if fav_type == "정배" else "pill-fire"
        fav_badge_lbl = "🎯 정배" if fav_type == "정배" else "⚡ 역배"

        handi_txt = f"{h_streak}경기 연속 마핸 ⚡" if h_type == "마핸" else f"{h_streak}경기 연속 플핸 🛡️"
        h_card_cls = "streak-card-purple" if h_type == "마핸" else "streak-card-green"
        h_pill_cls = "pill-purple" if h_type == "마핸" else "pill-green"
        h_badge_lbl = "⚡ 마핸" if h_type == "마핸" else "🛡️ 플핸"

        uo_txt = f"{uo_streak}경기 연속 오버 기록 🔥" if uo_type == "OVER" else f"{uo_streak}경기 연속 언더 행진 🧊"
        uo_card_cls = "streak-card-orange" if uo_type == "OVER" else "streak-card-ice"
        uo_pill_cls = "pill-orange" if uo_type == "OVER" else "pill-ice"
        uo_badge_lbl = "🔥 오버" if uo_type == "OVER" else "🧊 언더"

    pd_cards_html = (
        pd_card_html("마핸/플핸 퐁당", "마핸↔플핸", alt_run_len(h_hist), h_hist, HANDI_SYM, HANDI_FS, h_streak, h_type) +
        pd_card_html("언오버 퐁당", "언더↔오버", alt_run_len(uo_hist), uo_hist, UO_SYM, UO_FS, uo_streak, UO_KO.get(uo_type, uo_type))
    )
    pd_teams_box = render_pd_teams_box(teams, matches)

    cards_html = render_match_cards(desc, running_streaks_map, focus_team=None)

    return f"""
    <div class="view-pane" id="{view_id}">
      <div class="streak-section">
        <div class="streak-header">
          <span class="streak-title">🔥 <strong>{league_name} 리그 전체</strong> 실시간 연속 패턴 (Streak)</span>
          <span class="streak-tag">실시간 누적</span>
        </div>
        <div class="streak-grid">
          <div class="streak-card {fav_card_cls}">
            <div class="streak-card-top">
              <span class="streak-label">정배/역배 연속</span>
              <span class="streak-badge-pill {fav_pill_cls}">{fav_badge_lbl}</span>
            </div>
            <div class="streak-val">{fav_txt}</div>
          </div>
          <div class="streak-card {fav_card_cls}">
            <div class="streak-card-top">
              <span class="streak-label">배당 흐름</span>
              <span class="streak-badge-pill {fav_pill_cls}">{fav_badge_lbl}</span>
            </div>
            <div class="streak-val">{flow_txt}</div>
          </div>
          <div class="streak-card {h_card_cls}">
            <div class="streak-card-top">
              <span class="streak-label">리그 마핸/플핸 흐름</span>
              <span class="streak-badge-pill {h_pill_cls}">{h_badge_lbl}</span>
            </div>
            <div class="streak-val">{handi_txt}</div>
          </div>
          <div class="streak-card {uo_card_cls}">
            <div class="streak-card-top">
              <span class="streak-label">총득점 언더/오버</span>
              <span class="streak-badge-pill {uo_pill_cls}">{uo_badge_lbl}</span>
            </div>
            <div class="streak-val">{uo_txt}</div>
          </div>
          {pd_cards_html}
        </div>
      </div>

      {pd_teams_box}

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-header"><span>📊 리그 누적 경기수</span><span>{league_name} 전체</span></div>
          <div class="stat-val">{len(matches)}경기</div>
          <div class="stat-sub">완료 {t_total} · 진행예정 {pending}</div>
        </div>
        <div class="stat-card">
          <div class="stat-header"><span>🎯 정배당 적중률</span><span>저배당 승리</span></div>
          <div class="stat-val" style="color: var(--primary);">{fav_rate}%</div>
          <div class="stat-sub">정배 {fav_hits} / 역배 {t_total - fav_hits}</div>
        </div>
        <div class="stat-card">
          <div class="stat-header"><span>⚖️ 리그 마핸 vs 플핸 비율</span><span>핸디캡 결과</span></div>
          <div class="stat-val" style="color: var(--success);">마핸 {ma_rate}%</div>
          <div class="stat-sub">마핸 {ma_wins}경기 / 플핸 {pl_wins}경기</div>
        </div>
        <div class="stat-card">
          <div class="stat-header"><span>📈 리그 오버 비율</span><span>총득점 기준</span></div>
          <div class="stat-val" style="color: var(--warning);">{over_rate}%</div>
          <div class="stat-sub">오버 {overs} / 언더 {t_total - overs}</div>
        </div>
      </div>

      <div class="controls-bar">
        <div class="section-title">
          <span>📅 {league_name} 전체 경기 (일정별 1게임씩 누계)</span>
          <span style="font-size: 12px; color: var(--text-sub);">{len(desc)}경기 누적</span>
        </div>
        <div class="view-toggles">
          <label for="r-sort-asc" class="toggle-btn">
            <span class="sort-text-desc">⬇️ 최신 일정순</span>
            <span class="sort-text-asc">⬆️ 개막 순차순</span>
          </label>
        </div>
      </div>

      <div class="match-list">
        {cards_html}
      </div>
    </div>"""

mens_matches = data.get("mens", [])
womens_matches = data.get("womens", [])

team_panels_html = (
    render_team_panel_html("mens", MENS_TEAMS, mens_matches) +
    render_team_panel_html("womens", WOMENS_TEAMS, womens_matches)
)

views_html_parts = []
for idx, t in enumerate(MENS_TEAMS):
    views_html_parts.append(render_team_view_pane(f"view-mens-{idx}", mens_matches, t))
views_html_parts.append(render_all_view_pane("view-mens-all", "mens", mens_matches, MENS_TEAMS))

for idx, t in enumerate(WOMENS_TEAMS):
    views_html_parts.append(render_team_view_pane(f"view-womens-{idx}", womens_matches, t))
views_html_parts.append(render_all_view_pane("view-womens-all", "womens", womens_matches, WOMENS_TEAMS))

views_html = "".join(views_html_parts)

mt_radios = "\n".join(
    f'  <input type="radio" name="mens-team" id="r-mt-{i}" class="state-input"{" checked" if i == 0 else ""}>'
    for i in range(len(MENS_TEAMS))
)
wt_radios = "\n".join(
    f'  <input type="radio" name="womens-team" id="r-wt-{i}" class="state-input"{" checked" if i == 0 else ""}>'
    for i in range(len(WOMENS_TEAMS))
)

mt_active_selectors = ",\n".join(f"    #r-mt-{i}:checked ~ #teamPanelWrapper #lbl-mt-{i}" for i in range(len(MENS_TEAMS)))
wt_active_selectors = ",\n".join(f"    #r-wt-{i}:checked ~ #teamPanelWrapper #lbl-wt-{i}" for i in range(len(WOMENS_TEAMS)))

mt_view_rules = "\n".join(
    f"    #r-league-mens:checked ~ #r-mode-team:checked ~ #r-mt-{i}:checked ~ #viewsContainer #view-mens-{i} {{ display: block; }}"
    for i in range(len(MENS_TEAMS))
)
wt_view_rules = "\n".join(
    f"    #r-league-womens:checked ~ #r-mode-team:checked ~ #r-wt-{i}:checked ~ #viewsContainer #view-womens-{i} {{ display: block; }}"
    for i in range(len(WOMENS_TEAMS))
)

mens_teams_json = json.dumps(MENS_TEAMS, ensure_ascii=False)
womens_teams_json = json.dumps(WOMENS_TEAMS, ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>V-리그 배트맨토토 배구 누적 데이터 허브</title>
  <style>
    :root {{
      --bg-main: #070a10;
      --bg-card: #121927;
      --bg-card-hover: #192336;
      --border-color: #1e2c40;
      --border-active: #38bdf8;
      --text-white: #f8fafc;
      --text-muted: #94a3b8;
      --text-sub: #64748b;
      --primary: #38bdf8;
      --primary-dark: #0284c7;
      --primary-light: rgba(56, 189, 248, 0.15);
      --success: #34d399;
      --success-bg: rgba(52, 211, 153, 0.15);
      --warning: #fbbf24;
      --warning-bg: rgba(251, 191, 36, 0.15);
      --danger: #f87171;
      --danger-bg: rgba(248, 113, 113, 0.15);
      --purple: #c084fc;
      --purple-bg: rgba(192, 132, 252, 0.15);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", "Noto Sans KR", Roboto, sans-serif;
      -webkit-tap-highlight-color: rgba(56, 189, 248, 0.25);
    }}

    html, body {{
      max-width: 100%;
      overflow-x: hidden;
      background-color: var(--bg-main);
      color: var(--text-white);
      touch-action: manipulation;
    }}

    body {{
      padding: 16px 12px 80px;
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }}

    .container {{
      width: 100%;
      max-width: 1100px;
      margin: 0 auto;
    }}

    /* Hidden state radio/checkbox inputs for 100% JS-free & iOS QuickLook-safe interaction */
    .state-input {{
      display: none;
    }}

    /* Header */
    header {{
      margin-bottom: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 14px;
    }}

    .title-area h1 {{
      font-size: 21px;
      font-weight: 800;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}

    .title-area h1 span.badge {{
      font-size: 11px;
      background: #1e293b;
      color: var(--primary);
      padding: 2px 7px;
      border-radius: 6px;
      border: 1px solid #334155;
      font-weight: 700;
    }}

    .title-area p {{
      color: var(--text-muted);
      font-size: 12px;
      margin-top: 4px;
    }}

    .header-sub-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
    }}

    .updated-time {{
      font-size: 11px;
      color: #38bdf8;
      background: #0f172a;
      padding: 5px 10px;
      border-radius: 6px;
      border: 1px solid #1e293b;
      font-weight: 700;
    }}

    /* 1st Level: League Nav */
    .league-nav {{
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
    }}

    .league-btn {{
      flex: 1;
      padding: 12px 10px;
      border-radius: 10px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      user-select: none;
      -webkit-user-select: none;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.15s ease;
    }}

    #r-league-mens:checked ~ .league-nav #lbl-league-mens,
    #r-league-womens:checked ~ .league-nav #lbl-league-womens {{
      background: #1e3a5f;
      color: #38bdf8;
      border-color: #0284c7;
      box-shadow: 0 0 14px rgba(56, 189, 248, 0.2);
    }}

    /* 2nd Level: Mode Nav */
    .mode-nav-box {{
      background: #0e1422;
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 4px;
      display: flex;
      gap: 6px;
      margin-bottom: 14px;
    }}

    .mode-btn {{
      flex: 1;
      padding: 10px 12px;
      border-radius: 7px;
      border: 1px solid transparent;
      background: transparent;
      color: var(--text-muted);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      user-select: none;
      -webkit-user-select: none;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.15s;
    }}

    #r-mode-team:checked ~ .mode-nav-box #lbl-mode-team,
    #r-mode-all:checked ~ .mode-nav-box #lbl-mode-all {{
      background: var(--bg-card);
      color: var(--primary);
      border-color: #2d3c52;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }}

    /* Team Selector Panel */
    .team-panel {{
      display: none;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 12px;
      margin-bottom: 16px;
    }}

    #r-league-mens:checked ~ #r-mode-team:checked ~ #teamPanelWrapper #team-panel-mens,
    #r-league-womens:checked ~ #r-mode-team:checked ~ #teamPanelWrapper #team-panel-womens {{
      display: block;
    }}

    .team-panel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      font-size: 12px;
      color: var(--text-muted);
    }}

    .team-panel-header strong {{
      color: var(--text-white);
      font-size: 13px;
    }}

    .team-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(105px, 1fr));
      gap: 6px;
    }}

    .team-btn {{
      background: #0b101a;
      border: 1px solid #1a2536;
      border-radius: 8px;
      padding: 8px 6px;
      text-align: center;
      cursor: pointer;
      user-select: none;
      -webkit-user-select: none;
      transition: all 0.15s;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
    }}

    .team-btn-name {{
      font-size: 12px;
      font-weight: 700;
      color: var(--text-white);
    }}

    .team-btn-record {{
      font-size: 10px;
      padding: 2px 5px;
      border-radius: 4px;
      background: #172233;
      color: var(--text-muted);
    }}

{mt_active_selectors},
{wt_active_selectors} {{
      background: #1a3252;
      border-color: #38bdf8;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.3);
    }}

    #r-mt-0:checked ~ #teamPanelWrapper #lbl-mt-0 .team-btn-name,
    #r-mt-1:checked ~ #teamPanelWrapper #lbl-mt-1 .team-btn-name,
    #r-mt-2:checked ~ #teamPanelWrapper #lbl-mt-2 .team-btn-name,
    #r-mt-3:checked ~ #teamPanelWrapper #lbl-mt-3 .team-btn-name,
    #r-mt-4:checked ~ #teamPanelWrapper #lbl-mt-4 .team-btn-name,
    #r-mt-5:checked ~ #teamPanelWrapper #lbl-mt-5 .team-btn-name,
    #r-mt-6:checked ~ #teamPanelWrapper #lbl-mt-6 .team-btn-name,
    #r-wt-0:checked ~ #teamPanelWrapper #lbl-wt-0 .team-btn-name,
    #r-wt-1:checked ~ #teamPanelWrapper #lbl-wt-1 .team-btn-name,
    #r-wt-2:checked ~ #teamPanelWrapper #lbl-wt-2 .team-btn-name,
    #r-wt-3:checked ~ #teamPanelWrapper #lbl-wt-3 .team-btn-name,
    #r-wt-4:checked ~ #teamPanelWrapper #lbl-wt-4 .team-btn-name,
    #r-wt-5:checked ~ #teamPanelWrapper #lbl-wt-5 .team-btn-name,
    #r-wt-6:checked ~ #teamPanelWrapper #lbl-wt-6 .team-btn-name {{
      color: #38bdf8;
    }}

    #r-mt-0:checked ~ #teamPanelWrapper #lbl-mt-0 .team-btn-record,
    #r-mt-1:checked ~ #teamPanelWrapper #lbl-mt-1 .team-btn-record,
    #r-mt-2:checked ~ #teamPanelWrapper #lbl-mt-2 .team-btn-record,
    #r-mt-3:checked ~ #teamPanelWrapper #lbl-mt-3 .team-btn-record,
    #r-mt-4:checked ~ #teamPanelWrapper #lbl-mt-4 .team-btn-record,
    #r-mt-5:checked ~ #teamPanelWrapper #lbl-mt-5 .team-btn-record,
    #r-mt-6:checked ~ #teamPanelWrapper #lbl-mt-6 .team-btn-record,
    #r-wt-0:checked ~ #teamPanelWrapper #lbl-wt-0 .team-btn-record,
    #r-wt-1:checked ~ #teamPanelWrapper #lbl-wt-1 .team-btn-record,
    #r-wt-2:checked ~ #teamPanelWrapper #lbl-wt-2 .team-btn-record,
    #r-wt-3:checked ~ #teamPanelWrapper #lbl-wt-3 .team-btn-record,
    #r-wt-4:checked ~ #teamPanelWrapper #lbl-wt-4 .team-btn-record,
    #r-wt-5:checked ~ #teamPanelWrapper #lbl-wt-5 .team-btn-record,
    #r-wt-6:checked ~ #teamPanelWrapper #lbl-wt-6 .team-btn-record {{
      background: #0284c7;
      color: #fff;
      font-weight: 700;
    }}

    /* View Panes controlled purely by CSS :checked */
    .view-pane {{
      display: none;
    }}

    #r-league-mens:checked ~ #r-mode-all:checked ~ #viewsContainer #view-mens-all,
    #r-league-womens:checked ~ #r-mode-all:checked ~ #viewsContainer #view-womens-all {{
      display: block;
    }}

{mt_view_rules}
{wt_view_rules}

    /* Sort state controlled purely by CSS :checked */
    .sort-text-asc {{ display: none; }}
    .sort-text-desc {{ display: inline; }}
    #r-sort-asc:checked ~ #viewsContainer .sort-text-asc {{ display: inline; }}
    #r-sort-asc:checked ~ #viewsContainer .sort-text-desc {{ display: none; }}
    #r-sort-asc:checked ~ #viewsContainer .match-list {{ flex-direction: column-reverse; }}

    /* STREAK SECTION */
    .streak-section {{
      background: linear-gradient(135deg, #0e1728 0%, #0a101c 100%);
      border: 1px solid #233854;
      border-radius: 12px;
      padding: 14px;
      margin-bottom: 16px;
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.5);
    }}

    .streak-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      font-size: 13px;
    }}

    .streak-title {{
      color: var(--text-white);
      font-weight: 700;
    }}

    .streak-title strong {{
      color: #38bdf8;
      font-weight: 800;
    }}

    .streak-tag {{
      font-size: 10px;
      background: #1a2a40;
      color: #38bdf8;
      padding: 2px 7px;
      border-radius: 4px;
      font-weight: 700;
      border: 1px solid #284163;
    }}

    .streak-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 10px;
    }}

    .streak-card {{
      border-radius: 10px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      border: 1.5px solid transparent;
    }}

    .streak-card-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 6px;
    }}

    .streak-label {{
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 700;
    }}

    .streak-badge-pill {{
      font-size: 10px;
      padding: 1px 6px;
      border-radius: 4px;
      font-weight: 800;
      letter-spacing: -0.3px;
      white-space: nowrap;
      flex-shrink: 0;
    }}

    .streak-val {{
      font-size: 14px;
      font-weight: 800;
      letter-spacing: -0.3px;
    }}

    .streak-card-fire {{
      background: linear-gradient(135deg, rgba(239, 68, 68, 0.18), rgba(249, 115, 22, 0.22));
      border-color: #f97316;
      box-shadow: 0 0 12px rgba(249, 115, 22, 0.25);
    }}
    .streak-card-fire .streak-val {{ color: #fdba74; }}

    .streak-card-ice {{
      background: linear-gradient(135deg, rgba(2, 132, 199, 0.18), rgba(56, 189, 248, 0.22));
      border-color: #38bdf8;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
    }}
    .streak-card-ice .streak-val {{ color: #bae6fd; }}

    .streak-card-green {{
      background: linear-gradient(135deg, rgba(5, 150, 105, 0.18), rgba(16, 185, 129, 0.22));
      border-color: #10b981;
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.25);
    }}
    .streak-card-green .streak-val {{ color: #a7f3d0; }}

    .streak-card-orange {{
      background: linear-gradient(135deg, rgba(217, 119, 6, 0.18), rgba(245, 158, 11, 0.22));
      border-color: #f59e0b;
      box-shadow: 0 0 12px rgba(245, 158, 11, 0.25);
    }}
    .streak-card-orange .streak-val {{ color: #fde68a; }}

    .streak-card-purple {{
      background: linear-gradient(135deg, rgba(147, 51, 234, 0.18), rgba(192, 132, 252, 0.22));
      border-color: #c084fc;
      box-shadow: 0 0 12px rgba(192, 132, 252, 0.25);
    }}
    .streak-card-purple .streak-val {{ color: #f3e8ff; }}

    .streak-card-gray {{
      background: #172233;
      border-color: #2b3e59;
      color: var(--text-muted);
    }}
    .streak-card-gray .streak-val {{ color: #cbd5e1; }}

    /* STREAK PILLS */
    .match-streak-pill-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      margin: 2px 0 6px;
    }}

    .streak-pill {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 10px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      letter-spacing: -0.3px;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    }}

    .pill-fire {{
      background: linear-gradient(135deg, #dc2626, #ea580c);
      color: #ffffff;
      border: 1px solid #ff7849;
      box-shadow: 0 0 8px rgba(234, 88, 12, 0.4);
    }}

    .pill-ice {{
      background: linear-gradient(135deg, #0284c7, #2563eb);
      color: #ffffff;
      border: 1px solid #60a5fa;
      box-shadow: 0 0 8px rgba(37, 99, 235, 0.4);
    }}

    .pill-green {{
      background: linear-gradient(135deg, #059669, #0d9488);
      color: #ffffff;
      border: 1px solid #34d399;
      box-shadow: 0 0 8px rgba(13, 148, 136, 0.4);
    }}

    .pill-orange {{
      background: linear-gradient(135deg, #d97706, #f59e0b);
      color: #1e1b18;
      border: 1px solid #fde047;
      box-shadow: 0 0 8px rgba(245, 158, 11, 0.4);
    }}

    .pill-purple {{
      background: linear-gradient(135deg, #7c3aed, #9333ea);
      color: #ffffff;
      border: 1px solid #c084fc;
      box-shadow: 0 0 8px rgba(147, 51, 234, 0.4);
    }}

    .pill-gray {{
      background: #1e293b;
      color: #94a3b8;
      border: 1px solid #334155;
    }}

    /* 퐁당(교대) 패턴 */
    .pill-pd {{
      background: linear-gradient(135deg, #0d9488, #7c3aed);
      color: #ffffff;
      border: 1px solid #5eead4;
      box-shadow: 0 0 8px rgba(94, 234, 212, 0.35);
    }}

    .streak-card-pd {{
      background: linear-gradient(135deg, rgba(13, 148, 136, 0.2), rgba(124, 58, 237, 0.24));
      border-color: #2dd4bf;
      box-shadow: 0 0 12px rgba(45, 212, 191, 0.25);
    }}
    .streak-card-pd .streak-val {{ color: #99f6e4; }}

    .streak-card-plain {{
      background: #131c2b;
      border-color: #2b3e59;
    }}
    .streak-card-plain .streak-val {{ color: #cbd5e1; }}

    .pd-flow {{
      display: flex;
      align-items: center;
      flex-wrap: wrap;
      gap: 3px;
      margin-top: 1px;
    }}

    .pd-flow-lbl {{
      font-size: 9px;
      color: var(--text-sub);
      font-weight: 700;
      margin-right: 2px;
    }}

    .fs {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-width: 17px;
      height: 17px;
      padding: 0 3px;
      border-radius: 4px;
      font-size: 9.5px;
      font-weight: 800;
      line-height: 1;
    }}
    .fs-ma {{ background: rgba(192, 132, 252, 0.16); color: #c084fc; border: 1px solid rgba(192, 132, 252, 0.35); }}
    .fs-pl {{ background: rgba(52, 211, 153, 0.14); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); }}
    .fs-over {{ background: rgba(251, 191, 36, 0.14); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.35); }}
    .fs-under {{ background: rgba(129, 140, 248, 0.14); color: #818cf8; border: 1px solid rgba(129, 140, 248, 0.35); }}
    .fs-latest {{ box-shadow: 0 0 0 1.5px rgba(248, 250, 252, 0.55); }}

    .pd-teams-box {{
      border: 1px solid #2a4a5c;
      background: linear-gradient(135deg, rgba(13, 148, 136, 0.12), rgba(124, 58, 237, 0.12));
      border-radius: 12px;
      padding: 12px;
      margin-bottom: 16px;
    }}

    .pd-teams-head {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 6px;
      margin-bottom: 8px;
      flex-wrap: wrap;
    }}

    .pd-teams-title {{
      font-size: 13px;
      font-weight: 800;
      color: #99f6e4;
    }}

    .pd-teams-sub {{
      font-size: 10px;
      color: var(--text-sub);
      font-weight: 700;
    }}

    .pd-teams-chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}

    .pd-chip {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      background: #0b101a;
      border: 1px solid #1e3050;
      border-radius: 8px;
      padding: 4px 7px;
      font-size: 11px;
      font-weight: 700;
      color: var(--text-white);
    }}
    .pd-chip-ma {{ border-color: #6d28d9; box-shadow: inset 2px 0 0 #a855f7; }}
    .pd-chip-uo {{ border-color: #0f766e; box-shadow: inset 2px 0 0 #2dd4bf; }}
    .pd-chip-team {{ font-weight: 800; color: #f8fafc; }}
    .pd-chip-tag {{ font-size: 10px; color: var(--text-muted); }}
    .pd-chip-flow {{ display: inline-flex; gap: 2px; }}
    .pd-chip-flow .fs {{ min-width: 15px; height: 15px; font-size: 9px; }}

    .pd-teams-empty {{
      font-size: 11.5px;
      color: var(--text-muted);
    }}

    .streak-cell-badge {{
      font-size: 10px;
      font-weight: 800;
      padding: 2px 5px;
      border-radius: 4px;
      text-align: center;
      margin-top: 3px;
      display: block;
    }}

    /* Summary Stats Cards Grid */
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 8px;
      margin-bottom: 18px;
    }}

    .stat-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .stat-card .stat-header {{
      font-size: 11px;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .stat-card .stat-val {{
      font-size: 19px;
      font-weight: 800;
      color: var(--text-white);
      letter-spacing: -0.5px;
    }}

    .stat-card .stat-sub {{
      font-size: 10px;
      color: var(--text-sub);
    }}

    /* Controls Bar */
    .controls-bar {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
      margin-bottom: 12px;
    }}

    .section-title {{
      font-size: 15px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }}

    .view-toggles {{
      display: flex;
      gap: 6px;
    }}

    .toggle-btn {{
      padding: 6px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      cursor: pointer;
      user-select: none;
      -webkit-user-select: none;
      display: inline-flex;
      align-items: center;
    }}

    /* Match List & Cards */
    .match-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      width: 100%;
    }}

    .match-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      width: 100%;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
    }}

    .match-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 11px;
      color: var(--text-muted);
      border-bottom: 1px solid #1a2232;
      padding-bottom: 8px;
    }}

    .match-top-left {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .match-cumul-badge {{
      background: #1e293b;
      color: var(--primary);
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 800;
      font-size: 10px;
    }}

    .match-round-text {{
      font-weight: 600;
      color: #94a3b8;
    }}

    .match-fixture {{
      display: grid;
      grid-template-columns: 1fr auto 1fr;
      align-items: center;
      gap: 8px;
      text-align: center;
    }}

    .team-box {{
      display: flex;
      align-items: center;
      gap: 6px;
      min-width: 0;
    }}

    .team-box.away {{
      justify-content: flex-end;
    }}

    .team-badge {{
      font-size: 10px;
      padding: 1px 5px;
      border-radius: 4px;
      background: #1e293b;
      color: var(--text-sub);
      flex-shrink: 0;
    }}

    .team-name {{
      font-size: 13px;
      font-weight: 700;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .score-container {{
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1px;
      padding: 0 4px;
    }}

    .score-box {{
      font-size: 20px;
      font-weight: 800;
      letter-spacing: 1px;
    }}

    .score-detail {{
      font-size: 10px;
      color: var(--text-sub);
    }}

    /* 3 Toto Cells Grid */
    .toto-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
      background: #0b101a;
      padding: 8px;
      border-radius: 8px;
      width: 100%;
    }}

    @media (max-width: 480px) {{
      .toto-grid {{
        grid-template-columns: 1fr;
        gap: 6px;
      }}
    }}

    .toto-cell {{
      background: #141e2e;
      border: 1px solid #202e42;
      border-radius: 6px;
      padding: 6px 8px;
      display: flex;
      flex-direction: column;
      gap: 3px;
      min-width: 0;
    }}

    .cell-title {{
      font-size: 10px;
      color: var(--text-muted);
      font-weight: 700;
      display: flex;
      justify-content: space-between;
    }}

    .cell-odds-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 10px;
    }}

    .odds-item {{
      background: #090e17;
      padding: 2px 4px;
      border-radius: 4px;
      display: flex;
      gap: 3px;
    }}

    .odds-item.win {{
      background: var(--primary-light);
      color: var(--primary);
      font-weight: 700;
    }}

    .cell-result-badge {{
      font-size: 10px;
      font-weight: 700;
      padding: 2px 5px;
      border-radius: 4px;
      text-align: center;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}

    .badge-win {{ background: var(--success-bg); color: var(--success); border: 1px solid rgba(52, 211, 153, 0.3); }}
    .badge-lose {{ background: var(--danger-bg); color: var(--danger); border: 1px solid rgba(248, 113, 113, 0.3); }}
    .badge-over {{ background: var(--warning-bg); color: var(--warning); border: 1px solid rgba(251, 191, 36, 0.3); }}
    .badge-under {{ background: rgba(129, 140, 248, 0.15); color: #818cf8; border: 1px solid rgba(129, 140, 248, 0.3); }}
    .badge-pending {{ background: #1e293b; color: var(--text-muted); }}

    .empty-state {{
      text-align: center;
      padding: 40px 16px;
      color: var(--text-muted);
      background: var(--bg-card);
      border-radius: 12px;
      border: 1px solid var(--border-color);
      font-size: 13px;
    }}
  </style>
</head>
<body>

<div class="container">
  <!-- Pure CSS State Inputs (Work in iOS QuickLook without JS, Safari, Chrome, and Pickle Widget) -->
  <input type="radio" name="league" id="r-league-mens" class="state-input" checked>
  <input type="radio" name="league" id="r-league-womens" class="state-input">
  <input type="radio" name="mode" id="r-mode-team" class="state-input" checked>
  <input type="radio" name="mode" id="r-mode-all" class="state-input">
{mt_radios}
{wt_radios}
  <input type="checkbox" id="r-sort-asc" class="state-input">

  <!-- Header -->
  <header>
    <div class="title-area">
      <h1>
        🏐 V-리그 배트맨토토 데이터 허브
        <span class="badge">KOVO PROTO STATS</span>
      </h1>
      <p>프로토 승부식 [승/패 · 정배/역배 · 마핸/플핸 · 총득점 언더/오버] 누적 축적 & 구단별 스트릭 분석</p>
    </div>
    <div class="header-sub-row">
      <div class="updated-time" id="lastUpdatedText">
        동기화: {data.get('last_updated', '최신')}
      </div>
      <div style="font-size:11px; color:var(--text-sub);">
        📱 모바일 노스크롤 최적화
      </div>
    </div>
  </header>

  <!-- 1. 리그 선택 (남자부 / 여자부) -->
  <div class="league-nav">
    <label for="r-league-mens" class="league-btn" id="lbl-league-mens">
      👨 V-리그 남자부 (KOVO남)
    </label>
    <label for="r-league-womens" class="league-btn" id="lbl-league-womens">
      👩 V-리그 여자부 (KOVO여)
    </label>
  </div>

  <!-- 2. 모드 선택: [구단별] / [전체] -->
  <div class="mode-nav-box">
    <label for="r-mode-team" class="mode-btn" id="lbl-mode-team">
      🛡️ 구단별 스트릭 분석
    </label>
    <label for="r-mode-all" class="mode-btn" id="lbl-mode-all">
      📅 리그 전체 누계 흐름
    </label>
  </div>

  <!-- 3. 구단 선택 패널 (남자부 / 여자부 각각 사전 렌더링) -->
  <div id="teamPanelWrapper">
    {team_panels_html}
  </div>

  <!-- 4. 16개 전체 뷰 패널 (남녀 각 7구단 + 각 전체 뷰) -->
  <div id="viewsContainer">
    {views_html}
  </div>
</div>

<script>
  (function() {{
    var MENS_TEAMS = {mens_teams_json};
    var WOMENS_TEAMS = {womens_teams_json};

    if (typeof window !== 'undefined' && window.pickle && window.pickle.widget) {{
      window.pickle.widget.oncommand = function(command) {{
        var parts = String(command || '').trim().split(/\\s+/);
        var word = parts[0];
        var arg = parts.slice(1).join(' ');
        if (word === 'switch_league') {{
          var el = document.getElementById(arg === 'womens' ? 'r-league-womens' : 'r-league-mens');
          if (el) el.checked = true;
        }} else if (word === 'switch_mode') {{
          var el2 = document.getElementById(arg === 'all' ? 'r-mode-all' : 'r-mode-team');
          if (el2) el2.checked = true;
        }} else if (word === 'select_team') {{
          var mIdx = MENS_TEAMS.indexOf(arg);
          if (mIdx >= 0) {{
            document.getElementById('r-league-mens').checked = true;
            document.getElementById('r-mode-team').checked = true;
            document.getElementById('r-mt-' + mIdx).checked = true;
          }} else {{
            var wIdx = WOMENS_TEAMS.indexOf(arg);
            if (wIdx >= 0) {{
              document.getElementById('r-league-womens').checked = true;
              document.getElementById('r-mode-team').checked = true;
              document.getElementById('r-wt-' + wIdx).checked = true;
            }}
          }}
        }}
      }};
    }}
  }})();
</script>

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html)

WIDGET_DIR = os.path.join(BASE_DIR, "..", "widgets", "volleyball-betman", "bundle")
os.makedirs(WIDGET_DIR, exist_ok=True)
WIDGET_HTML = os.path.join(WIDGET_DIR, "index.html")
with open(WIDGET_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Generated JS-free CSS-driven dashboard successfully! Size: {len(html)} bytes")
