import json

with open("volleyball-betman-tracker/data/matches.json", "r", encoding="utf-8") as f:
    data = json.load(f)

json_str = json.dumps(data, ensure_ascii=False, indent=2)

html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>V-리그 배트맨토토 배구 누적 데이터 허브</title>
  <style>
    :root {{
      --bg-main: #0b0f17;
      --bg-card: #151d2a;
      --bg-card-hover: #1c2638;
      --border-color: #222f42;
      --border-active: #38bdf8;
      --text-white: #f8fafc;
      --text-muted: #94a3b8;
      --text-sub: #64748b;
      --primary: #38bdf8;
      --primary-dark: #0284c7;
      --primary-light: rgba(56, 189, 248, 0.12);
      --success: #34d399;
      --success-bg: rgba(52, 211, 153, 0.15);
      --warning: #fbbf24;
      --warning-bg: rgba(251, 191, 36, 0.15);
      --danger: #f87171;
      --danger-bg: rgba(248, 113, 113, 0.15);
      --purple: #a78bfa;
      --purple-bg: rgba(167, 139, 250, 0.15);
      --indigo: #818cf8;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", "Noto Sans KR", Roboto, sans-serif;
    }}

    body {{
      background-color: var(--bg-main);
      color: var(--text-white);
      padding: 24px 16px 80px;
      line-height: 1.5;
    }}

    .container {{
      max-width: 1260px;
      margin: 0 auto;
    }}

    /* Header */
    header {{
      margin-bottom: 24px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-end;
      gap: 16px;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 20px;
    }}

    .title-area h1 {{
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.5px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .title-area h1 span.badge {{
      font-size: 13px;
      background: #1e293b;
      color: var(--primary);
      padding: 3px 8px;
      border-radius: 6px;
      border: 1px solid #334155;
      font-weight: 600;
    }}

    .title-area p {{
      color: var(--text-muted);
      font-size: 14px;
      margin-top: 6px;
    }}

    .updated-time {{
      font-size: 12px;
      color: var(--text-sub);
      background: #111827;
      padding: 6px 12px;
      border-radius: 8px;
      border: 1px solid #1f2937;
    }}

    /* 1st Level: League Nav (남자부 / 여자부) */
    .league-nav {{
      display: flex;
      gap: 12px;
      margin-bottom: 16px;
    }}

    .league-btn {{
      flex: 1;
      padding: 14px 20px;
      border-radius: 12px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s ease;
    }}

    .league-btn:hover {{
      border-color: #334155;
      color: var(--text-white);
    }}

    .league-btn.active {{
      background: #1e3a5f;
      color: #38bdf8;
      border-color: #0284c7;
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.18);
    }}

    /* 2nd Level: Mode Nav (구단별 / 전체) */
    .mode-nav-box {{
      background: #101622;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 6px;
      display: flex;
      gap: 8px;
      margin-bottom: 20px;
    }}

    .mode-btn {{
      flex: 1;
      padding: 12px 16px;
      border-radius: 8px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s;
    }}

    .mode-btn:hover {{
      color: var(--text-white);
    }}

    .mode-btn.active {{
      background: var(--bg-card);
      color: var(--primary);
      border: 1px solid #2d3c52;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    }}

    /* Team Selector Panel (Shown in 구단별 mode) */
    .team-panel {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 18px;
      margin-bottom: 24px;
      display: none;
      animation: fadeIn 0.2s ease-in-out;
    }}

    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(-4px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .team-panel-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      font-size: 14px;
      color: var(--text-muted);
    }}

    .team-panel-header strong {{
      color: var(--text-white);
      font-size: 15px;
    }}

    .team-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap: 10px;
    }}

    .team-btn {{
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 10px;
      padding: 12px 10px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
    }}

    .team-btn:hover {{
      border-color: #38bdf8;
      background: #162238;
    }}

    .team-btn.active {{
      background: #1e3a5f;
      border-color: #38bdf8;
      box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
    }}

    .team-btn-name {{
      font-size: 14px;
      font-weight: 700;
      color: var(--text-white);
    }}

    .team-btn.active .team-btn-name {{
      color: #38bdf8;
    }}

    .team-btn-record {{
      font-size: 11px;
      padding: 2px 6px;
      border-radius: 4px;
      background: #1e293b;
      color: var(--text-muted);
    }}

    .team-btn.active .team-btn-record {{
      background: #0284c7;
      color: #fff;
      font-weight: 700;
    }}

    /* Summary Stats Cards Grid */
    .stats-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 14px;
      margin-bottom: 28px;
    }}

    .stat-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}

    .stat-card .stat-header {{
      font-size: 13px;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .stat-card .stat-val {{
      font-size: 26px;
      font-weight: 800;
      color: var(--text-white);
      letter-spacing: -0.5px;
    }}

    .stat-card .stat-sub {{
      font-size: 12px;
      color: var(--text-sub);
    }}

    /* Controls Bar (Title, Filter, Sort, View toggle) */
    .controls-bar {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
    }}

    .section-title {{
      font-size: 18px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    .view-toggles {{
      display: flex;
      gap: 8px;
      align-items: center;
    }}

    .toggle-btn {{
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 600;
      border-radius: 6px;
      background: #111827;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s;
    }}

    .toggle-btn:hover {{
      color: var(--text-white);
      border-color: #334155;
    }}

    .toggle-btn.active {{
      background: #1e293b;
      color: var(--primary);
      border-color: var(--primary);
    }}

    /* Table View for '전체 일정별 1게임씩 누계' */
    .table-responsive {{
      width: 100%;
      overflow-x: auto;
      border-radius: 14px;
      border: 1px solid var(--border-color);
      background: var(--bg-card);
      margin-bottom: 24px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }}

    .proto-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
      text-align: center;
      min-width: 1020px;
    }}

    .proto-table th {{
      background: #0f172a;
      color: var(--text-muted);
      padding: 13px 10px;
      font-weight: 700;
      border-bottom: 1px solid var(--border-color);
      white-space: nowrap;
    }}

    .proto-table td {{
      padding: 12px 10px;
      border-bottom: 1px solid #1a2333;
      vertical-align: middle;
    }}

    .proto-table tr:hover {{
      background: #182234;
    }}

    .table-num-badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 6px;
      background: #1e293b;
      font-size: 11px;
      font-weight: 800;
      color: var(--primary);
    }}

    .table-match {{
      text-align: left;
      font-weight: 700;
      font-size: 14px;
    }}

    .table-score {{
      font-size: 15px;
      font-weight: 800;
      letter-spacing: 1px;
    }}

    .table-odds-box {{
      display: flex;
      flex-direction: column;
      gap: 3px;
      align-items: center;
    }}

    .table-odds-row {{
      display: flex;
      gap: 6px;
      font-size: 11px;
      color: var(--text-muted);
    }}

    .table-res-tag {{
      display: inline-block;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
    }}

    /* Card View */
    .match-list {{
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .match-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 20px;
      transition: border-color 0.2s;
    }}

    .match-card:hover {{
      border-color: #334155;
    }}

    .match-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px solid #1c2638;
      font-size: 13px;
    }}

    .match-round {{
      color: var(--primary);
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .match-cumul-badge {{
      background: #0284c7;
      color: #fff;
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 4px;
      font-weight: 800;
    }}

    .match-date {{
      color: var(--text-sub);
    }}

    .match-fixture {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 16px;
    }}

    .team-box {{
      flex: 1;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .team-box.away {{
      justify-content: flex-end;
      text-align: right;
    }}

    .team-name {{
      font-size: 17px;
      font-weight: 700;
    }}

    .team-badge {{
      font-size: 11px;
      padding: 2px 6px;
      border-radius: 4px;
      background: #1e293b;
      color: var(--text-muted);
    }}

    .score-box {{
      padding: 6px 16px;
      background: #0f172a;
      border-radius: 10px;
      border: 1px solid #1e293b;
      font-size: 20px;
      font-weight: 800;
      letter-spacing: 2px;
      text-align: center;
      min-width: 90px;
    }}

    .score-detail {{
      font-size: 11px;
      color: var(--text-sub);
      text-align: center;
      margin-top: 4px;
      letter-spacing: 0;
    }}

    /* 3-Column Toto Odds & Results Grid */
    .toto-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-top: 14px;
    }}

    @media (max-width: 768px) {{
      .toto-grid {{
        grid-template-columns: 1fr;
      }}
      .team-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}
    }}

    .toto-cell {{
      background: #0f172a;
      border: 1px solid #1c283c;
      border-radius: 10px;
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}

    .cell-title {{
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .cell-odds-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
      margin-top: 4px;
    }}

    .odds-item {{
      display: flex;
      flex-direction: column;
      align-items: center;
      flex: 1;
      padding: 4px;
      border-radius: 6px;
      background: #162032;
    }}

    .odds-item.win {{
      background: #143224;
      border: 1px solid #059669;
    }}

    .odds-label {{
      font-size: 11px;
      color: var(--text-sub);
    }}

    .odds-val {{
      font-size: 14px;
      font-weight: 700;
      color: var(--text-white);
    }}

    .cell-result-badge {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      font-size: 12px;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 6px;
      margin-top: 4px;
      text-align: center;
    }}

    .badge-win {{ background: var(--success-bg); color: var(--success); border: 1px solid rgba(52, 211, 153, 0.3); }}
    .badge-lose {{ background: var(--danger-bg); color: var(--danger); border: 1px solid rgba(248, 113, 113, 0.3); }}
    .badge-over {{ background: var(--warning-bg); color: var(--warning); border: 1px solid rgba(251, 191, 36, 0.3); }}
    .badge-under {{ background: rgba(129, 140, 248, 0.15); color: #818cf8; border: 1px solid rgba(129, 140, 248, 0.3); }}
    .badge-pending {{ background: #1e293b; color: var(--text-muted); }}

    .empty-state {{
      text-align: center;
      padding: 60px 20px;
      color: var(--text-muted);
      background: var(--bg-card);
      border-radius: 16px;
      border: 1px solid var(--border-color);
    }}
  </style>
</head>
<body>

<div class="container">
  <!-- Header -->
  <header>
    <div class="title-area">
      <h1>
        🏐 V-리그 배트맨토토 데이터 허브
        <span class="badge">KOVO PROTO STATS</span>
      </h1>
      <p>프로토 승부식 [승/패 · 세트 핸디캡 · 총득점 언더/오버] 경기별 자동 축적 & 구단별 심층 통계</p>
    </div>
    <div class="updated-time" id="lastUpdatedText">
      동기화: 불러오는 중...
    </div>
  </header>

  <!-- 1. 리그 선택 (남자부 / 여자부) -->
  <div class="league-nav">
    <button class="league-btn active" id="btnMens" onclick="switchLeague('mens')">
      👨 V-리그 남자부 (KOVO남)
    </button>
    <button class="league-btn" id="btnWomens" onclick="switchLeague('womens')">
      👩 V-리그 여자부 (KOVO여)
    </button>
  </div>

  <!-- 2. 모드 선택: [구단별] / [전체 (일정별 1게임씩 누계)] -->
  <div class="mode-nav-box">
    <button class="mode-btn active" id="modeTeamBtn" onclick="switchMode('team')">
      🛡️ 구단별
    </button>
    <button class="mode-btn" id="modeAllBtn" onclick="switchMode('all')">
      📅 전체 (일정별 1게임씩 누계)
    </button>
  </div>

  <!-- 3. 구단 선택 패널 (구단별 모드 활성화 시 7개 구단 클릭 버튼들) -->
  <div class="team-panel" id="teamPanel">
    <div class="team-panel-header">
      <span>구단을 클릭하여 해당 구단의 누적 기록을 확인하세요:</span>
      <strong id="teamPanelLeagueText">남자부 7개 구단</strong>
    </div>
    <div class="team-grid" id="teamGrid">
      <!-- Populated by JS -->
    </div>
  </div>

  <!-- 4. 통계 요약 지표 카드 그리드 -->
  <div class="stats-grid" id="statsGrid">
    <!-- Populated by JS -->
  </div>

  <!-- 5. 컨트롤 바 (섹션 타이틀, 필터, 정렬, 뷰 전환) -->
  <div class="controls-bar">
    <div class="section-title">
      <span id="matchListTitle">경기 누적 기록</span>
      <span style="font-size: 13px; color: var(--text-sub);" id="matchCountText">0경기</span>
    </div>
    <div class="view-toggles" id="viewToggles">
      <button class="toggle-btn active" id="toggleTableBtn" onclick="setViewMode('table')">📋 누계 테이블</button>
      <button class="toggle-btn" id="toggleCardBtn" onclick="setViewMode('card')">🃏 상세 카드</button>
      <button class="toggle-btn" id="toggleSortBtn" onclick="toggleSort()">⬇️ 최신 일정순</button>
    </div>
  </div>

  <!-- 6-A. 1게임씩 누계 테이블 뷰 (엑셀 스프레드시트 형태) -->
  <div class="table-responsive" id="tableViewContainer">
    <table class="proto-table" id="protoTable">
      <thead>
        <tr>
          <th style="width: 75px;">누계 #</th>
          <th style="width: 135px;">일정 / 회차</th>
          <th>대진 (홈 vs 원정)</th>
          <th style="width: 70px;">세트</th>
          <th style="width: 185px;">[1] 일반 승·패</th>
          <th style="width: 180px;">[2] 세트 핸디캡</th>
          <th style="width: 180px;">[3] 총득점 언더/오버</th>
          <th style="width: 135px;">누계 흐름</th>
        </tr>
      </thead>
      <tbody id="protoTableBody">
        <!-- Populated by JS -->
      </tbody>
    </table>
  </div>

  <!-- 6-B. 상세 카드 뷰 -->
  <div class="match-list" id="matchList">
    <!-- Populated by JS -->
  </div>
</div>

<!-- Embedded Match Data -->
<script id="embedded-data" type="application/json">
{json_str}
</script>

<script>
  let rawData = JSON.parse(document.getElementById('embedded-data').textContent);
  let currentLeague = 'mens'; // 'mens' | 'womens'
  let currentMode = 'team';    // 'team' | 'all'
  let viewMode = 'table';      // 'table' | 'card'
  let sortOrder = 'desc';      // 'desc' (latest first) | 'asc' (oldest first)
  let selectedTeam = '';

  const MENS_TEAMS = [
    "한국전력 빅스톰", "현대캐피탈 스카이워커스", "대한항공 점보스",
    "우리카드 우리WON", "KB손해보험 스타즈", "삼성화재 블루팡스", "OK저축은행 읏맨"
  ];

  const WOMENS_TEAMS = [
    "흥국생명 핑크스파이더스", "한국도로공사 하이패스", "IBK기업은행 알토스",
    "정관장 레드스파크스", "GS칼텍스 서울Kixx", "현대건설 힐스테이트", "페퍼저축은행 AI페퍼스"
  ];

  function init() {{
    document.getElementById('lastUpdatedText').textContent = '동기화: ' + (rawData.last_updated || '최신');
    selectedTeam = MENS_TEAMS[0];
    render();
  }}

  function switchLeague(league) {{
    currentLeague = league;
    document.getElementById('btnMens').classList.toggle('active', league === 'mens');
    document.getElementById('btnWomens').classList.toggle('active', league === 'womens');
    selectedTeam = (league === 'mens' ? MENS_TEAMS[0] : WOMENS_TEAMS[0]);
    render();
  }}

  function switchMode(mode) {{
    currentMode = mode;
    document.getElementById('modeTeamBtn').classList.toggle('active', mode === 'team');
    document.getElementById('modeAllBtn').classList.toggle('active', mode === 'all');
    render();
  }}

  function selectTeam(teamName) {{
    selectedTeam = teamName;
    render();
  }}

  function setViewMode(mode) {{
    viewMode = mode;
    document.getElementById('toggleTableBtn').classList.toggle('active', mode === 'table');
    document.getElementById('toggleCardBtn').classList.toggle('active', mode === 'card');
    renderDisplay();
  }}

  function toggleSort() {{
    sortOrder = (sortOrder === 'desc' ? 'asc' : 'desc');
    document.getElementById('toggleSortBtn').textContent = (sortOrder === 'desc' ? '⬇️ 최신 일정순' : '⬆️ 개막 순차순');
    render();
  }}

  function getBaseMatches() {{
    return [...(rawData[currentLeague] || [])];
  }}

  function renderTeamPanel() {{
    const panel = document.getElementById('teamPanel');
    const headerLeague = document.getElementById('teamPanelLeagueText');
    if (currentMode === 'all') {{
      panel.style.display = 'none';
      return;
    }}
    panel.style.display = 'block';
    headerLeague.textContent = currentLeague === 'mens' ? '남자부 7개 구단 선택' : '여자부 7개 구단 선택';

    const teams = currentLeague === 'mens' ? MENS_TEAMS : WOMENS_TEAMS;
    const allMatches = getBaseMatches();

    const teamGrid = document.getElementById('teamGrid');
    teamGrid.innerHTML = teams.map(t => {{
      const activeClass = (t === selectedTeam ? 'active' : '');
      const completed = allMatches.filter(m => m.status === '종료' && (m.home === t || m.away === t));
      let wins = 0;
      completed.forEach(m => {{
        const isHome = m.home === t;
        if ((isHome && m.win_lose.winner === 'HOME') || (!isHome && m.win_lose.winner === 'AWAY')) {{
          wins++;
        }}
      }});
      const losses = completed.length - wins;
      const recordStr = `${{wins}}승 ${{losses}}패`;

      return `
        <button class="team-btn ${{activeClass}}" onclick="selectTeam('${{t}}')">
          <span class="team-btn-name">${{t.split(' ')[0]}}</span>
          <span class="team-btn-record">${{recordStr}}</span>
        </button>
      `;
    }}).join('');
  }}

  function calculateStats(matches) {{
    const completed = matches.filter(m => m.status === '종료');
    if (completed.length === 0) {{
      return {{ total: 0, pending: matches.length, wins: 0, losses: 0, winRate: 0, handiRate: 0, overRate: 0, avgPoints: 0 }};
    }}

    let wins = 0;
    let handiWins = 0;
    let overs = 0;
    let totalPoints = 0;

    completed.forEach(m => {{
      totalPoints += (m.total_points || 0);

      if (currentMode === 'team') {{
        const isHome = m.home === selectedTeam;
        const won = (isHome && m.win_lose.winner === 'HOME') || (!isHome && m.win_lose.winner === 'AWAY');
        if (won) wins++;

        const handiWon = (isHome && m.handicap.result === 'HOME') || (!isHome && m.handicap.result === 'AWAY');
        if (handiWon) handiWins++;
      }} else {{
        if (m.win_lose.hit_type && m.win_lose.hit_type.includes('정배')) wins++;
        if (m.handicap.result === 'HOME') handiWins++;
      }}

      if (m.under_over.result === 'OVER') overs++;
    }});

    return {{
      total: completed.length,
      pending: matches.length - completed.length,
      wins: wins,
      losses: completed.length - wins,
      winRate: Math.round((wins / completed.length) * 100),
      handiRate: Math.round((handiWins / completed.length) * 100),
      overRate: Math.round((overs / completed.length) * 100),
      avgPoints: (totalPoints / completed.length).toFixed(1)
    }};
  }}

  function renderStats(matches) {{
    const statsGrid = document.getElementById('statsGrid');
    const s = calculateStats(matches);

    if (currentMode === 'team') {{
      const shortName = selectedTeam.split(' ')[0];
      statsGrid.innerHTML = `
        <div class="stat-card">
          <div class="stat-header"><span>🏆 구단 일반 승률</span><span>${{shortName}}</span></div>
          <div class="stat-val" style="color: var(--primary);">${{s.winRate}}%</div>
          <div class="stat-sub">${{s.wins}}승 ${{s.losses}}패 (총 ${{s.total}}경기 완료)</div>
        </div>
        <div class="stat-card">
          <div class="stat-header"><span>⚖️ 세트 핸디 극복률</span><span>마핸/플핸</span></div>
          <div class="stat-val" style="color: var(--success);">${{s.handiRate}}%</div>
          <div class="stat-sub">배트맨 기준점 대비 승리 비율</div>
        </div>
        <div class="stat-card">
          <div class="stat-header"><span>📈 오버 비율 (기준점)</span><span>U/O 경향</span></div>
          <div class="stat-val" style="color: var(--warning);">${{s.overRate}}%</div>
          <div class="stat-sub">언더 비율: ${{100 - s.overRate}}%</div>
        </div>
        <div class="stat-card">
          <div class="stat-header"><span>🎯 경기당 평균 총득점</span><span>합산 점수</span></div>
          <div class="stat-val" style="color: var(--purple);">${{s.avgPoints}}점</div>
          <div class="stat-sub">풀세트 및 셧아웃 합산 평균</div>
        </div>
      `;
    }} else {{
      const leagueName = currentLeague === 'mens' ? '남자부' : '여자부';
      statsGrid.innerHTML = `
        <div class="stat-card">
          <div class="stat-header"><span>📊 리그 누적 경기수</span><span>${{leagueName}} 전체</span></div>
          <div class="stat-val">${{s.total + s.pending}}경기</div>
          <div class="stat-sub">완료 ${{s.total}}경기 · 진행예정 ${{s.pending}}경기</div>
        </div>
        <div class="stat-card">
          <div class="stat-header"><span>🎯 정배당 적중률</span><span>저배당 승리</span></div>
          <div class="stat-val" style="color: var(--primary);">${{s.winRate}}%</div>
          <div class="stat-sub">정배 ${{s.wins}}경기 / 역배 ${{s.losses}}경기</div>
        </div>
        <div class="stat-card">
          <div class="stat-header"><span>⚖️ 홈팀 핸디캡 승률</span><span>홈 기준</span></div>
          <div class="stat-val" style="color: var(--success);">${{s.handiRate}}%</div>
          <div class="stat-sub">원정팀 핸디 승률: ${{100 - s.handiRate}}%</div>
        </div>
        <div class="stat-card">
          <div class="stat-header"><span>📈 리그 오버 비율</span><span>총득점 기준</span></div>
          <div class="stat-val" style="color: var(--warning);">${{s.overRate}}%</div>
          <div class="stat-sub">오버 ${{Math.round(s.total * s.overRate / 100)}}경기 / 언더 ${{s.total - Math.round(s.total * s.overRate / 100)}}경기</div>
        </div>
      `;
    }}
  }}

  function getSortedAndFilteredMatches() {{
    const all = getBaseMatches();
    let matches = [];
    if (currentMode === 'team') {{
      matches = all.filter(m => m.home === selectedTeam || m.away === selectedTeam);
    }} else {{
      matches = [...all];
    }}

    // Chronological sort (oldest first) to assign sequential cumulative indexes & running totals
    const sortedChronological = [...matches].sort((a, b) => new Date(a.date) - new Date(b.date));
    
    let runCompleted = 0;
    let runFavHits = 0;
    let runOvers = 0;

    sortedChronological.forEach((m, idx) => {{
      m._cumulIndex = idx + 1; // 1 to N
      if (m.status === '종료') {{
        runCompleted++;
        if (m.win_lose && m.win_lose.hit_type && m.win_lose.hit_type.includes('정배')) {{
          runFavHits++;
        }}
        if (m.under_over && m.under_over.result === 'OVER') {{
          runOvers++;
        }}
        m._runFavPct = Math.round((runFavHits / runCompleted) * 100);
        m._runOverPct = Math.round((runOvers / runCompleted) * 100);
        m._runFavHits = runFavHits;
        m._runCompleted = runCompleted;
      }} else {{
        m._runFavPct = null;
        m._runOverPct = null;
      }}
    }});

    // Now sort according to user preference
    if (sortOrder === 'asc') {{
      matches.sort((a, b) => new Date(a.date) - new Date(b.date));
    }} else {{
      matches.sort((a, b) => new Date(b.date) - new Date(a.date));
    }}

    return matches;
  }}

  function renderTable(matches) {{
    const tbody = document.getElementById('protoTableBody');
    if (matches.length === 0) {{
      tbody.innerHTML = `<tr><td colspan="8" style="padding: 40px; color: var(--text-muted);">표시할 경기 데이터가 없습니다.</td></tr>`;
      return;
    }}

    tbody.innerHTML = matches.map(m => {{
      const isCompleted = m.status === '종료';
      const homeWon = m.win_lose.winner === 'HOME';
      const awayWon = m.win_lose.winner === 'AWAY';

      // 1. Win/Lose display
      let winLoseHtml = '';
      if (isCompleted) {{
        const hitDesc = homeWon ? '홈승' : '원정승';
        const hitType = m.win_lose.hit_type || '';
        const hitBadgeClass = hitType.includes('역배') ? 'badge-lose' : 'badge-win';
        winLoseHtml = `
          <div class="table-odds-box">
            <div class="table-odds-row">
              <span style="${{homeWon ? 'color: var(--success); font-weight:700;' : ''}}">홈 ${{m.win_lose.home_odds}}</span>
              <span>vs</span>
              <span style="${{awayWon ? 'color: var(--success); font-weight:700;' : ''}}">원정 ${{m.win_lose.away_odds}}</span>
            </div>
            <span class="table-res-tag ${{hitBadgeClass}}">${{hitDesc}} [${{hitType}} ${{m.win_lose.hit_odds}}]</span>
          </div>
        `;
      }} else {{
        winLoseHtml = `
          <div class="table-odds-box">
            <div class="table-odds-row"><span>홈 ${{m.win_lose.home_odds}}</span> vs <span>원정 ${{m.win_lose.away_odds}}</span></div>
            <span class="table-res-tag badge-pending">발매중 (#${{m.win_lose.match_no}})</span>
          </div>
        `;
      }}

      // 2. Handicap display
      let handiHtml = '';
      if (isCompleted) {{
        const desc = m.handicap.desc || (m.handicap.result === 'HOME' ? '홈 플/마핸승' : '원정 플/마핸승');
        handiHtml = `
          <div class="table-odds-box">
            <div class="table-odds-row">
              <span>기준 ${{m.handicap.standard > 0 ? '+' : ''}}${{m.handicap.standard}}</span>
              <span style="color:var(--text-sub);">(${{m.handicap.home_odds}} / ${{m.handicap.away_odds}})</span>
            </div>
            <span class="table-res-tag badge-win">${{desc}}</span>
          </div>
        `;
      }} else {{
        handiHtml = `
          <div class="table-odds-box">
            <div class="table-odds-row"><span>기준 ${{m.handicap.standard > 0 ? '+' : ''}}${{m.handicap.standard}}</span></div>
            <span class="table-res-tag badge-pending">${{m.handicap.home_odds}} / ${{m.handicap.away_odds}}</span>
          </div>
        `;
      }}

      // 3. Under / Over display
      let uoHtml = '';
      if (isCompleted) {{
        const isOver = m.under_over.result === 'OVER';
        const badgeClass = isOver ? 'badge-over' : 'badge-under';
        const label = isOver ? `🔥 오버 (${{m.total_points}}점)` : `🧊 언더 (${{m.total_points}}점)`;
        uoHtml = `
          <div class="table-odds-box">
            <div class="table-odds-row">
              <span>기준 ${{m.under_over.standard}}</span>
              <span style="color:var(--text-sub);">(${{m.under_over.over_odds}} / ${{m.under_over.under_odds}})</span>
            </div>
            <span class="table-res-tag ${{badgeClass}}">${{label}}</span>
          </div>
        `;
      }} else {{
        uoHtml = `
          <div class="table-odds-box">
            <div class="table-odds-row"><span>기준 ${{m.under_over.standard}}</span></div>
            <span class="table-res-tag badge-pending">${{m.under_over.over_odds}} / ${{m.under_over.under_odds}}</span>
          </div>
        `;
      }}

      // 4. Running Cumulative stats display
      let cumulFlowHtml = '';
      if (isCompleted) {{
        cumulFlowHtml = `
          <div style="font-size: 11px; line-height: 1.4;">
            <div style="color: var(--primary);">정배 ${{m._runFavPct}}% <span style="color:var(--text-sub);">(${{m._runFavHits}}/${{m._runCompleted}})</span></div>
            <div style="color: var(--warning);">오버 ${{m._runOverPct}}%</div>
          </div>
        `;
      }} else {{
        cumulFlowHtml = `<span style="font-size: 11px; color: var(--text-sub);">진행예정</span>`;
      }}

      const isHomeTeam = currentMode === 'team' && m.home === selectedTeam;
      const isAwayTeam = currentMode === 'team' && m.away === selectedTeam;

      return `
        <tr>
          <td><span class="table-num-badge">#${{m._cumulIndex}}</span></td>
          <td style="font-size: 12px; color: var(--text-muted); text-align: left;">
            <div style="color: var(--text-white); font-weight:600;">${{m.date}}</div>
            <div style="font-size: 11px; color: var(--text-sub);">${{m.round}}</div>
          </td>
          <td class="table-match">
            <span style="${{isHomeTeam ? 'color: var(--primary); font-weight:800;' : ''}}">${{m.home}}</span>
            <span style="color: var(--text-sub); font-size: 12px; margin: 0 4px;">vs</span>
            <span style="${{isAwayTeam ? 'color: var(--primary); font-weight:800;' : ''}}">${{m.away}}</span>
          </td>
          <td>
            <div class="table-score" style="color: ${{isCompleted ? 'var(--text-white)' : 'var(--text-sub)'}}">${{m.set_score}}</div>
          </td>
          <td>${{winLoseHtml}}</td>
          <td>${{handiHtml}}</td>
          <td>${{uoHtml}}</td>
          <td>${{cumulFlowHtml}}</td>
        </tr>
      `;
    }}).join('');
  }}

  function renderCards(matches) {{
    const listEl = document.getElementById('matchList');
    if (matches.length === 0) {{
      listEl.innerHTML = `<div class="empty-state">해당 조건의 경기 데이터가 없습니다.</div>`;
      return;
    }}

    listEl.innerHTML = matches.map(m => {{
      const isCompleted = m.status === '종료';
      const homeWon = m.win_lose.winner === 'HOME';
      const awayWon = m.win_lose.winner === 'AWAY';

      const isHomeTeam = currentMode === 'team' && m.home === selectedTeam;
      const isAwayTeam = currentMode === 'team' && m.away === selectedTeam;

      let winBadge = `<span class="cell-result-badge badge-pending">발매중</span>`;
      if (isCompleted) {{
        const hitType = m.win_lose.hit_type;
        const hitOdds = m.win_lose.hit_odds;
        const hitDesc = (homeWon ? '홈승' : '원정승') + ` [${{hitType}} ${{hitOdds}}]`;
        const badgeClass = hitType.includes('역배') ? 'badge-lose' : 'badge-win';
        winBadge = `<span class="cell-result-badge ${{badgeClass}}">${{hitDesc}}</span>`;
      }}

      let handiBadge = `<span class="cell-result-badge badge-pending">발매중</span>`;
      if (isCompleted) {{
        const desc = m.handicap.desc || (m.handicap.result === 'HOME' ? '홈 핸승' : '원정 핸승');
        handiBadge = `<span class="cell-result-badge badge-win">${{desc}}</span>`;
      }}

      let uoBadge = `<span class="cell-result-badge badge-pending">발매중</span>`;
      if (isCompleted) {{
        const isOver = m.under_over.result === 'OVER';
        const badgeClass = isOver ? 'badge-over' : 'badge-under';
        const desc = isOver ? `🔥 오버 (${{m.total_points}}점)` : `🧊 언더 (${{m.total_points}}점)`;
        uoBadge = `<span class="cell-result-badge ${{badgeClass}}">${{desc}}</span>`;
      }}

      const setsStr = m.sets_detail && m.sets_detail.length > 0 ? m.sets_detail.join(' / ') : '';

      return `
        <div class="match-card">
          <div class="match-top">
            <span class="match-round">
              <span class="match-cumul-badge">누계 #${{m._cumulIndex}}</span>
              ${{m.round}} · 경기 #${{m.win_lose.match_no}}
            </span>
            <span class="match-date">${{m.date}}</span>
          </div>

          <div class="match-fixture">
            <div class="team-box ${{isHomeTeam ? 'focused' : ''}}">
              <span class="team-badge">홈</span>
              <span class="team-name" style="${{isHomeTeam ? 'color: var(--primary); font-weight:800;' : ''}}">${{m.home}}</span>
            </div>

            <div class="score-container">
              <div class="score-box" style="color: ${{isCompleted ? 'var(--text-white)' : 'var(--text-sub)'}}">
                ${{m.set_score}}
              </div>
              ${{setsStr ? `<div class="score-detail">${{setsStr}}</div>` : ''}}
            </div>

            <div class="team-box away ${{isAwayTeam ? 'focused' : ''}}">
              <span class="team-name" style="${{isAwayTeam ? 'color: var(--primary); font-weight:800;' : ''}}">${{m.away}}</span>
              <span class="team-badge">원정</span>
            </div>
          </div>

          <div class="toto-grid">
            <!-- 1. 일반 승/패 -->
            <div class="toto-cell">
              <div class="cell-title">
                <span>[1] 일반 승·패</span>
                <span style="font-size:10px; color:var(--text-sub)">#${{m.win_lose.match_no}}</span>
              </div>
              <div class="cell-odds-row">
                <div class="odds-item ${{homeWon ? 'win' : ''}}">
                  <span class="odds-label">홈 승</span>
                  <span class="odds-val">${{m.win_lose.home_odds}}</span>
                </div>
                <div style="padding: 0 4px; color: var(--text-sub); font-size:11px;">vs</div>
                <div class="odds-item ${{awayWon ? 'win' : ''}}">
                  <span class="odds-label">원정 승</span>
                  <span class="odds-val">${{m.win_lose.away_odds}}</span>
                </div>
              </div>
              ${{winBadge}}
            </div>

            <!-- 2. 세트 핸디캡 -->
            <div class="toto-cell">
              <div class="cell-title">
                <span>[2] 세트 핸디캡</span>
                <span style="color:var(--primary); font-size:11px;">기준 ${{m.handicap.standard > 0 ? '+' : ''}}${{m.handicap.standard}}</span>
              </div>
              <div class="cell-odds-row">
                <div class="odds-item ${{m.handicap.result === 'HOME' ? 'win' : ''}}">
                  <span class="odds-label">홈 핸디</span>
                  <span class="odds-val">${{m.handicap.home_odds}}</span>
                </div>
                <div style="padding: 0 4px; color: var(--text-sub); font-size:11px;">vs</div>
                <div class="odds-item ${{m.handicap.result === 'AWAY' ? 'win' : ''}}">
                  <span class="odds-label">원정 핸디</span>
                  <span class="odds-val">${{m.handicap.away_odds}}</span>
                </div>
              </div>
              ${{handiBadge}}
            </div>

            <!-- 3. 언더/오버 -->
            <div class="toto-cell">
              <div class="cell-title">
                <span>[3] 총득점 언더/오버</span>
                <span style="color:var(--warning); font-size:11px;">기준 ${{m.under_over.standard}}</span>
              </div>
              <div class="cell-odds-row">
                <div class="odds-item ${{m.under_over.result === 'OVER' ? 'win' : ''}}">
                  <span class="odds-label">오버 ▲</span>
                  <span class="odds-val">${{m.under_over.over_odds}}</span>
                </div>
                <div style="padding: 0 4px; color: var(--text-sub); font-size:11px;">vs</div>
                <div class="odds-item ${{m.under_over.result === 'UNDER' ? 'win' : ''}}">
                  <span class="odds-label">언더 ▼</span>
                  <span class="odds-val">${{m.under_over.under_odds}}</span>
                </div>
              </div>
              ${{uoBadge}}
            </div>
          </div>
        </div>
      `;
    }}).join('');
  }}

  function renderDisplay() {{
    const tableContainer = document.getElementById('tableViewContainer');
    const cardsContainer = document.getElementById('matchList');
    const toggles = document.getElementById('viewToggles');

    toggles.style.display = 'flex';
    if (viewMode === 'table') {{
      tableContainer.style.display = 'block';
      cardsContainer.style.display = 'none';
    }} else {{
      tableContainer.style.display = 'none';
      cardsContainer.style.display = 'flex';
    }}
  }}

  function render() {{
    renderTeamPanel();
    const activeMatches = getSortedAndFilteredMatches();
    renderStats(activeMatches);

    const titleEl = document.getElementById('matchListTitle');
    const countEl = document.getElementById('matchCountText');

    if (currentMode === 'team') {{
      titleEl.textContent = `🛡️ ${{selectedTeam}} 누적 경기 히스토리`;
    }} else {{
      const leagueLabel = currentLeague === 'mens' ? '남자부' : '여자부';
      titleEl.textContent = `📅 ${{leagueLabel}} 전체 경기 (일정별 1게임씩 누계)`;
    }}
    countEl.textContent = `${{activeMatches.length}}경기 누적`;

    renderTable(activeMatches);
    renderCards(activeMatches);
    renderDisplay();
  }}

  init();
</script>

</body>
</html>
"""

with open("volleyball-betman-tracker/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("[OK] volleyball-betman-tracker/index.html updated successfully!")
