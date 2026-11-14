import json
import os
from datetime import datetime

seed_mens = [
    {
        "id": "M20261113",
        "date": "2026-11-13 19:00",
        "round": "프로토 승부식 135회차",
        "league": "KOVO남",
        "home": "한국전력 빅스톰",
        "away": "KB손해보험 스타즈",
        "status": "진행예정",
        "set_score": "-",
        "sets_detail": [],
        "total_points": None,
        "win_lose": {
            "match_no": "3909",
            "home_odds": 1.24,
            "away_odds": 2.92,
            "winner": None,
            "favorite": "HOME"
        },
        "handicap": {
            "match_no": "3910",
            "standard": -1.5,
            "home_odds": 1.45,
            "away_odds": 2.18,
            "result": None
        },
        "under_over": {
            "match_no": "3911",
            "standard": 183.5,
            "over_odds": 1.85,
            "under_odds": 1.64,
            "result": None
        }
    },
    {
        "id": "M20261112",
        "date": "2026-11-12 19:00",
        "round": "프로토 승부식 134회차",
        "league": "KOVO남",
        "home": "OK저축은행 읏맨",
        "away": "현대캐피탈 스카이워커스",
        "status": "종료",
        "set_score": "1:3",
        "sets_detail": ["25:21", "19:25", "20:25", "22:25"],
        "total_points": 182,
        "win_lose": {
            "match_no": "3813",
            "home_odds": 2.81,
            "away_odds": 1.26,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.26,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "3814",
            "standard": 1.5,
            "home_odds": 1.82,
            "away_odds": 1.66,
            "result": "AWAY",
            "desc": "원정 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "3815",
            "standard": 180.5,
            "over_odds": 1.78,
            "under_odds": 1.72,
            "result": "OVER",
            "desc": "182점 오버"
        }
    },
    {
        "id": "M20261111",
        "date": "2026-11-11 19:00",
        "round": "프로토 승부식 134회차",
        "league": "KOVO남",
        "home": "우리카드 우리WON",
        "away": "대한항공 점보스",
        "status": "종료",
        "set_score": "3:2",
        "sets_detail": ["25:22", "23:25", "21:25", "25:23", "15:13"],
        "total_points": 217,
        "win_lose": {
            "match_no": "3738",
            "home_odds": 2.15,
            "away_odds": 1.46,
            "winner": "HOME",
            "favorite": "AWAY",
            "hit_odds": 2.15,
            "hit_type": "역배"
        },
        "handicap": {
            "match_no": "3739",
            "standard": 1.5,
            "home_odds": 1.62,
            "away_odds": 1.88,
            "result": "HOME",
            "desc": "홈 +1.5 플핸승"
        },
        "under_over": {
            "match_no": "3740",
            "standard": 184.5,
            "over_odds": 1.75,
            "under_odds": 1.75,
            "result": "OVER",
            "desc": "217점 오버"
        }
    },
    {
        "id": "M20261110",
        "date": "2026-11-10 19:00",
        "round": "프로토 승부식 133회차",
        "league": "KOVO남",
        "home": "삼성화재 블루팡스",
        "away": "한국전력 빅스톰",
        "status": "종료",
        "set_score": "1:3",
        "sets_detail": ["22:25", "25:22", "21:25", "18:25"],
        "total_points": 183,
        "win_lose": {
            "match_no": "3676",
            "home_odds": 2.09,
            "away_odds": 1.49,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.49,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "3677",
            "standard": 1.5,
            "home_odds": 1.58,
            "away_odds": 1.95,
            "result": "AWAY",
            "desc": "원정 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "3678",
            "standard": 181.5,
            "over_odds": 1.80,
            "under_odds": 1.70,
            "result": "OVER",
            "desc": "183점 오버"
        }
    },
    {
        "id": "M20261108",
        "date": "2026-11-08 14:00",
        "round": "프로토 승부식 132회차",
        "league": "KOVO남",
        "home": "현대캐피탈 스카이워커스",
        "away": "KB손해보험 스타즈",
        "status": "종료",
        "set_score": "3:1",
        "sets_detail": ["25:18", "21:25", "25:20", "25:19"],
        "total_points": 178,
        "win_lose": {
            "match_no": "3373",
            "home_odds": 1.18,
            "away_odds": 3.31,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.18,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "3374",
            "standard": -1.5,
            "home_odds": 1.42,
            "away_odds": 2.25,
            "result": "HOME",
            "desc": "홈 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "3375",
            "standard": 179.5,
            "over_odds": 1.72,
            "under_odds": 1.78,
            "result": "UNDER",
            "desc": "178점 언더"
        }
    },
    {
        "id": "M20261107",
        "date": "2026-11-07 14:00",
        "round": "프로토 승부식 132회차",
        "league": "KOVO남",
        "home": "대한항공 점보스",
        "away": "OK저축은행 읏맨",
        "status": "종료",
        "set_score": "3:0",
        "sets_detail": ["25:20", "25:19", "25:21"],
        "total_points": 135,
        "win_lose": {
            "match_no": "3210",
            "home_odds": 1.22,
            "away_odds": 3.05,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.22,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "3211",
            "standard": -1.5,
            "home_odds": 1.45,
            "away_odds": 2.20,
            "result": "HOME",
            "desc": "홈 -1.5 마핸승 (3:0)"
        },
        "under_over": {
            "match_no": "3212",
            "standard": 178.5,
            "over_odds": 1.70,
            "under_odds": 1.80,
            "result": "UNDER",
            "desc": "135점 언더"
        }
    },
    {
        "id": "M20261106",
        "date": "2026-11-06 19:00",
        "round": "프로토 승부식 131회차",
        "league": "KOVO남",
        "home": "KB손해보험 스타즈",
        "away": "우리카드 우리WON",
        "status": "종료",
        "set_score": "1:3",
        "sets_detail": ["22:25", "25:21", "20:25", "19:25"],
        "total_points": 182,
        "win_lose": {
            "match_no": "3104",
            "home_odds": 2.30,
            "away_odds": 1.41,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.41,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "3105",
            "standard": 1.5,
            "home_odds": 1.70,
            "away_odds": 1.78,
            "result": "AWAY",
            "desc": "원정 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "3106",
            "standard": 181.5,
            "over_odds": 1.75,
            "under_odds": 1.75,
            "result": "OVER",
            "desc": "182점 오버"
        }
    },
    {
        "id": "M20261105",
        "date": "2026-11-05 19:00",
        "round": "프로토 승부식 131회차",
        "league": "KOVO남",
        "home": "한국전력 빅스톰",
        "away": "현대캐피탈 스카이워커스",
        "status": "종료",
        "set_score": "3:2",
        "sets_detail": ["25:23", "20:25", "25:21", "21:25", "15:12"],
        "total_points": 212,
        "win_lose": {
            "match_no": "3015",
            "home_odds": 2.45,
            "away_odds": 1.35,
            "winner": "HOME",
            "favorite": "AWAY",
            "hit_odds": 2.45,
            "hit_type": "역배"
        },
        "handicap": {
            "match_no": "3016",
            "standard": 1.5,
            "home_odds": 1.85,
            "away_odds": 1.65,
            "result": "HOME",
            "desc": "홈 +1.5 플핸승"
        },
        "under_over": {
            "match_no": "3017",
            "standard": 182.5,
            "over_odds": 1.80,
            "under_odds": 1.70,
            "result": "OVER",
            "desc": "212점 오버"
        }
    },
    {
        "id": "M20261104",
        "date": "2026-11-04 19:00",
        "round": "프로토 승부식 130회차",
        "league": "KOVO남",
        "home": "OK저축은행 읏맨",
        "away": "삼성화재 블루팡스",
        "status": "종료",
        "set_score": "0:3",
        "sets_detail": ["21:25", "19:25", "23:25"],
        "total_points": 138,
        "win_lose": {
            "match_no": "2910",
            "home_odds": 1.65,
            "away_odds": 1.85,
            "winner": "AWAY",
            "favorite": "HOME",
            "hit_odds": 1.85,
            "hit_type": "역배"
        },
        "handicap": {
            "match_no": "2911",
            "standard": -1.5,
            "home_odds": 2.10,
            "away_odds": 1.48,
            "result": "AWAY",
            "desc": "원정 +1.5 플핸승"
        },
        "under_over": {
            "match_no": "2912",
            "standard": 182.5,
            "over_odds": 1.72,
            "under_odds": 1.78,
            "result": "UNDER",
            "desc": "138점 언더"
        }
    },
    {
        "id": "M20261103",
        "date": "2026-11-03 19:00",
        "round": "프로토 승부식 130회차",
        "league": "KOVO남",
        "home": "대한항공 점보스",
        "away": "우리카드 우리WON",
        "status": "종료",
        "set_score": "3:1",
        "sets_detail": ["26:24", "25:21", "22:25", "25:18"],
        "total_points": 186,
        "win_lose": {
            "match_no": "2815",
            "home_odds": 1.30,
            "away_odds": 2.65,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.30,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2816",
            "standard": -1.5,
            "home_odds": 1.55,
            "away_odds": 2.05,
            "result": "HOME",
            "desc": "홈 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "2817",
            "standard": 181.5,
            "over_odds": 1.82,
            "under_odds": 1.68,
            "result": "OVER",
            "desc": "186점 오버"
        }
    },
    {
        "id": "M20261101",
        "date": "2026-11-01 14:00",
        "round": "프로토 승부식 129회차",
        "league": "KOVO남",
        "home": "삼성화재 블루팡스",
        "away": "현대캐피탈 스카이워커스",
        "status": "종료",
        "set_score": "0:3",
        "sets_detail": ["19:25", "22:25", "18:25"],
        "total_points": 134,
        "win_lose": {
            "match_no": "2650",
            "home_odds": 3.10,
            "away_odds": 1.21,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.21,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2651",
            "standard": 1.5,
            "home_odds": 2.15,
            "away_odds": 1.45,
            "result": "AWAY",
            "desc": "원정 -1.5 마핸승 (3:0)"
        },
        "under_over": {
            "match_no": "2652",
            "standard": 177.5,
            "over_odds": 1.70,
            "under_odds": 1.80,
            "result": "UNDER",
            "desc": "134점 언더"
        }
    },
    {
        "id": "M20261031",
        "date": "2026-10-31 14:00",
        "round": "프로토 승부식 129회차",
        "league": "KOVO남",
        "home": "KB손해보험 스타즈",
        "away": "대한항공 점보스",
        "status": "종료",
        "set_score": "2:3",
        "sets_detail": ["25:23", "20:25", "26:24", "18:25", "12:15"],
        "total_points": 213,
        "win_lose": {
            "match_no": "2580",
            "home_odds": 2.95,
            "away_odds": 1.24,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.24,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2581",
            "standard": 1.5,
            "home_odds": 1.95,
            "away_odds": 1.58,
            "result": "HOME",
            "desc": "홈 +1.5 플핸승 (풀세트)"
        },
        "under_over": {
            "match_no": "2582",
            "standard": 180.5,
            "over_odds": 1.80,
            "under_odds": 1.70,
            "result": "OVER",
            "desc": "213점 오버"
        }
    },
    {
        "id": "M20261030",
        "date": "2026-10-30 19:00",
        "round": "프로토 승부식 128회차",
        "league": "KOVO남",
        "home": "우리카드 우리WON",
        "away": "한국전력 빅스톰",
        "status": "종료",
        "set_score": "1:3",
        "sets_detail": ["25:21", "21:25", "19:25", "23:25"],
        "total_points": 184,
        "win_lose": {
            "match_no": "2490",
            "home_odds": 1.70,
            "away_odds": 1.80,
            "winner": "AWAY",
            "favorite": "HOME",
            "hit_odds": 1.80,
            "hit_type": "역배"
        },
        "handicap": {
            "match_no": "2491",
            "standard": -1.5,
            "home_odds": 2.15,
            "away_odds": 1.47,
            "result": "AWAY",
            "desc": "원정 +1.5 플핸승"
        },
        "under_over": {
            "match_no": "2492",
            "standard": 182.5,
            "over_odds": 1.76,
            "under_odds": 1.74,
            "result": "OVER",
            "desc": "184점 오버"
        }
    },
    {
        "id": "M20261029",
        "date": "2026-10-29 19:00",
        "round": "프로토 승부식 128회차",
        "league": "KOVO남",
        "home": "현대캐피탈 스카이워커스",
        "away": "OK저축은행 읏맨",
        "status": "종료",
        "set_score": "3:0",
        "sets_detail": ["25:17", "25:20", "25:22"],
        "total_points": 134,
        "win_lose": {
            "match_no": "2410",
            "home_odds": 1.25,
            "away_odds": 2.90,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.25,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2411",
            "standard": -1.5,
            "home_odds": 1.48,
            "away_odds": 2.15,
            "result": "HOME",
            "desc": "홈 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "2412",
            "standard": 178.5,
            "over_odds": 1.70,
            "under_odds": 1.80,
            "result": "UNDER",
            "desc": "134점 언더"
        }
    },
    {
        "id": "M20261028",
        "date": "2026-10-28 19:00",
        "round": "프로토 승부식 127회차",
        "league": "KOVO남",
        "home": "한국전력 빅스톰",
        "away": "삼성화재 블루팡스",
        "status": "종료",
        "set_score": "3:1",
        "sets_detail": ["25:20", "25:23", "20:25", "25:19"],
        "total_points": 182,
        "win_lose": {
            "match_no": "2330",
            "home_odds": 1.42,
            "away_odds": 2.30,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.42,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2331",
            "standard": -1.5,
            "home_odds": 1.75,
            "away_odds": 1.72,
            "result": "HOME",
            "desc": "홈 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "2332",
            "standard": 181.5,
            "over_odds": 1.75,
            "under_odds": 1.75,
            "result": "OVER",
            "desc": "182점 오버"
        }
    },
    {
        "id": "M20261026",
        "date": "2026-10-26 19:00",
        "round": "프로토 승부식 127회차",
        "league": "KOVO남",
        "home": "대한항공 점보스",
        "away": "현대캐피탈 스카이워커스",
        "status": "종료",
        "set_score": "3:2",
        "sets_detail": ["25:22", "21:25", "25:23", "20:25", "15:13"],
        "total_points": 214,
        "win_lose": {
            "match_no": "2210",
            "home_odds": 1.55,
            "away_odds": 2.05,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.55,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2211",
            "standard": -1.5,
            "home_odds": 1.95,
            "away_odds": 1.58,
            "result": "AWAY",
            "desc": "원정 +1.5 플핸승 (풀세트)"
        },
        "under_over": {
            "match_no": "2212",
            "standard": 183.5,
            "over_odds": 1.82,
            "under_odds": 1.68,
            "result": "OVER",
            "desc": "214점 오버"
        }
    }
]

seed_womens = [
    {
        "id": "W20261113",
        "date": "2026-11-13 19:00",
        "round": "프로토 승부식 135회차",
        "league": "KOVO여",
        "home": "IBK기업은행 알토스",
        "away": "흥국생명 핑크스파이더스",
        "status": "진행예정",
        "set_score": "-",
        "sets_detail": [],
        "total_points": None,
        "win_lose": {
            "match_no": "3912",
            "home_odds": 2.45,
            "away_odds": 1.35,
            "winner": None,
            "favorite": "AWAY"
        },
        "handicap": {
            "match_no": "3913",
            "standard": 1.5,
            "home_odds": 1.75,
            "away_odds": 1.72,
            "result": None
        },
        "under_over": {
            "match_no": "3914",
            "standard": 178.5,
            "over_odds": 1.74,
            "under_odds": 1.74,
            "result": None
        }
    },
    {
        "id": "W20261112",
        "date": "2026-11-12 19:00",
        "round": "프로토 승부식 134회차",
        "league": "KOVO여",
        "home": "정관장 레드스파크스",
        "away": "한국도로공사 하이패스",
        "status": "종료",
        "set_score": "0:3",
        "sets_detail": ["22:25", "20:25", "19:25"],
        "total_points": 136,
        "win_lose": {
            "match_no": "3816",
            "home_odds": 1.50,
            "away_odds": 2.10,
            "winner": "AWAY",
            "favorite": "HOME",
            "hit_odds": 2.10,
            "hit_type": "역배"
        },
        "handicap": {
            "match_no": "3817",
            "standard": -1.5,
            "home_odds": 1.88,
            "away_odds": 1.62,
            "result": "AWAY",
            "desc": "원정 +1.5 플핸승 (0:3)"
        },
        "under_over": {
            "match_no": "3818",
            "standard": 179.5,
            "over_odds": 1.72,
            "under_odds": 1.78,
            "result": "UNDER",
            "desc": "136점 언더"
        }
    },
    {
        "id": "W20261111",
        "date": "2026-11-11 19:00",
        "round": "프로토 승부식 134회차",
        "league": "KOVO여",
        "home": "현대건설 힐스테이트",
        "away": "GS칼텍스 서울Kixx",
        "status": "종료",
        "set_score": "0:3",
        "sets_detail": ["23:25", "21:25", "22:25"],
        "total_points": 141,
        "win_lose": {
            "match_no": "3741",
            "home_odds": 1.15,
            "away_odds": 3.65,
            "winner": "AWAY",
            "favorite": "HOME",
            "hit_odds": 3.65,
            "hit_type": "대역배"
        },
        "handicap": {
            "match_no": "3742",
            "standard": -1.5,
            "home_odds": 1.35,
            "away_odds": 2.45,
            "result": "AWAY",
            "desc": "원정 +1.5 플핸승"
        },
        "under_over": {
            "match_no": "3743",
            "standard": 175.5,
            "over_odds": 1.70,
            "under_odds": 1.80,
            "result": "UNDER",
            "desc": "141점 언더"
        }
    },
    {
        "id": "W20261108",
        "date": "2026-11-08 16:00",
        "round": "프로토 승부식 132회차",
        "league": "KOVO여",
        "home": "한국도로공사 하이패스",
        "away": "흥국생명 핑크스파이더스",
        "status": "종료",
        "set_score": "3:1",
        "sets_detail": ["25:21", "20:25", "25:22", "25:20"],
        "total_points": 183,
        "win_lose": {
            "match_no": "3376",
            "home_odds": 2.75,
            "away_odds": 1.28,
            "winner": "HOME",
            "favorite": "AWAY",
            "hit_odds": 2.75,
            "hit_type": "역배"
        },
        "handicap": {
            "match_no": "3377",
            "standard": 1.5,
            "home_odds": 1.85,
            "away_odds": 1.65,
            "result": "HOME",
            "desc": "홈 +1.5 플핸승"
        },
        "under_over": {
            "match_no": "3378",
            "standard": 177.5,
            "over_odds": 1.76,
            "under_odds": 1.74,
            "result": "OVER",
            "desc": "183점 오버"
        }
    },
    {
        "id": "W20261107",
        "date": "2026-11-07 16:00",
        "round": "프로토 승부식 132회차",
        "league": "KOVO여",
        "home": "페퍼저축은행 AI페퍼스",
        "away": "IBK기업은행 알토스",
        "status": "종료",
        "set_score": "1:3",
        "sets_detail": ["19:25", "25:22", "18:25", "20:25"],
        "total_points": 179,
        "win_lose": {
            "match_no": "3213",
            "home_odds": 2.90,
            "away_odds": 1.25,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.25,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "3214",
            "standard": 1.5,
            "home_odds": 1.88,
            "away_odds": 1.62,
            "result": "AWAY",
            "desc": "원정 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "3215",
            "standard": 176.5,
            "over_odds": 1.75,
            "under_odds": 1.75,
            "result": "OVER",
            "desc": "179점 오버"
        }
    },
    {
        "id": "W20261106",
        "date": "2026-11-06 19:00",
        "round": "프로토 승부식 131회차",
        "league": "KOVO여",
        "home": "GS칼텍스 서울Kixx",
        "away": "정관장 레드스파크스",
        "status": "종료",
        "set_score": "3:2",
        "sets_detail": ["25:23", "21:25", "25:20", "22:25", "15:11"],
        "total_points": 212,
        "win_lose": {
            "match_no": "3107",
            "home_odds": 1.82,
            "away_odds": 1.68,
            "winner": "HOME",
            "favorite": "AWAY",
            "hit_odds": 1.82,
            "hit_type": "역배"
        },
        "handicap": {
            "match_no": "3108",
            "standard": 1.5,
            "home_odds": 1.52,
            "away_odds": 2.05,
            "result": "HOME",
            "desc": "홈 +1.5 플핸승"
        },
        "under_over": {
            "match_no": "3109",
            "standard": 181.5,
            "over_odds": 1.80,
            "under_odds": 1.70,
            "result": "OVER",
            "desc": "212점 오버"
        }
    },
    {
        "id": "W20261105",
        "date": "2026-11-05 19:00",
        "round": "프로토 승부식 131회차",
        "league": "KOVO여",
        "home": "현대건설 힐스테이트",
        "away": "페퍼저축은행 AI페퍼스",
        "status": "종료",
        "set_score": "3:0",
        "sets_detail": ["25:16", "25:18", "25:19"],
        "total_points": 128,
        "win_lose": {
            "match_no": "3018",
            "home_odds": 1.10,
            "away_odds": 4.50,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.10,
            "hit_type": "극정배"
        },
        "handicap": {
            "match_no": "3019",
            "standard": -2.5,
            "home_odds": 1.60,
            "away_odds": 1.95,
            "result": "HOME",
            "desc": "홈 -2.5 마핸승 (3:0 셧아웃)"
        },
        "under_over": {
            "match_no": "3020",
            "standard": 168.5,
            "over_odds": 1.75,
            "under_odds": 1.75,
            "result": "UNDER",
            "desc": "128점 언더"
        }
    },
    {
        "id": "W20261104",
        "date": "2026-11-04 19:00",
        "round": "프로토 승부식 130회차",
        "league": "KOVO여",
        "home": "흥국생명 핑크스파이더스",
        "away": "현대건설 힐스테이트",
        "status": "종료",
        "set_score": "3:0",
        "sets_detail": ["25:20", "25:19", "25:23"],
        "total_points": 137,
        "win_lose": {
            "match_no": "2913",
            "home_odds": 1.40,
            "away_odds": 2.35,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.40,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2914",
            "standard": -1.5,
            "home_odds": 1.70,
            "away_odds": 1.78,
            "result": "HOME",
            "desc": "홈 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "2915",
            "standard": 178.5,
            "over_odds": 1.72,
            "under_odds": 1.78,
            "result": "UNDER",
            "desc": "137점 언더"
        }
    },
    {
        "id": "W20261103",
        "date": "2026-11-03 19:00",
        "round": "프로토 승부식 130회차",
        "league": "KOVO여",
        "home": "한국도로공사 하이패스",
        "away": "IBK기업은행 알토스",
        "status": "종료",
        "set_score": "3:1",
        "sets_detail": ["25:22", "23:25", "25:20", "25:19"],
        "total_points": 184,
        "win_lose": {
            "match_no": "2818",
            "home_odds": 1.62,
            "away_odds": 1.95,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.62,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2819",
            "standard": -1.5,
            "home_odds": 2.05,
            "away_odds": 1.55,
            "result": "HOME",
            "desc": "홈 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "2820",
            "standard": 179.5,
            "over_odds": 1.78,
            "under_odds": 1.72,
            "result": "OVER",
            "desc": "184점 오버"
        }
    },
    {
        "id": "W20261101",
        "date": "2026-11-01 16:00",
        "round": "프로토 승부식 129회차",
        "league": "KOVO여",
        "home": "정관장 레드스파크스",
        "away": "페퍼저축은행 AI페퍼스",
        "status": "종료",
        "set_score": "3:1",
        "sets_detail": ["25:18", "22:25", "25:17", "25:21"],
        "total_points": 178,
        "win_lose": {
            "match_no": "2653",
            "home_odds": 1.28,
            "away_odds": 2.80,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.28,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2654",
            "standard": -1.5,
            "home_odds": 1.52,
            "away_odds": 2.05,
            "result": "HOME",
            "desc": "홈 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "2655",
            "standard": 175.5,
            "over_odds": 1.76,
            "under_odds": 1.74,
            "result": "OVER",
            "desc": "178점 오버"
        }
    },
    {
        "id": "W20261031",
        "date": "2026-10-31 16:00",
        "round": "프로토 승부식 129회차",
        "league": "KOVO여",
        "home": "IBK기업은행 알토스",
        "away": "GS칼텍스 서울Kixx",
        "status": "종료",
        "set_score": "1:3",
        "sets_detail": ["23:25", "25:21", "20:25", "18:25"],
        "total_points": 182,
        "win_lose": {
            "match_no": "2583",
            "home_odds": 1.85,
            "away_odds": 1.65,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.65,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2584",
            "standard": 1.5,
            "home_odds": 1.55,
            "away_odds": 2.00,
            "result": "AWAY",
            "desc": "원정 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "2585",
            "standard": 180.5,
            "over_odds": 1.75,
            "under_odds": 1.75,
            "result": "OVER",
            "desc": "182점 오버"
        }
    },
    {
        "id": "W20261030",
        "date": "2026-10-30 19:00",
        "round": "프로토 승부식 128회차",
        "league": "KOVO여",
        "home": "흥국생명 핑크스파이더스",
        "away": "정관장 레드스파크스",
        "status": "종료",
        "set_score": "3:1",
        "sets_detail": ["25:21", "25:23", "20:25", "25:18"],
        "total_points": 182,
        "win_lose": {
            "match_no": "2493",
            "home_odds": 1.35,
            "away_odds": 2.50,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.35,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2494",
            "standard": -1.5,
            "home_odds": 1.60,
            "away_odds": 1.95,
            "result": "HOME",
            "desc": "홈 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "2495",
            "standard": 179.5,
            "over_odds": 1.75,
            "under_odds": 1.75,
            "result": "OVER",
            "desc": "182점 오버"
        }
    },
    {
        "id": "W20261029",
        "date": "2026-10-29 19:00",
        "round": "프로토 승부식 128회차",
        "league": "KOVO여",
        "home": "페퍼저축은행 AI페퍼스",
        "away": "한국도로공사 하이패스",
        "status": "종료",
        "set_score": "0:3",
        "sets_detail": ["18:25", "21:25", "19:25"],
        "total_points": 133,
        "win_lose": {
            "match_no": "2413",
            "home_odds": 3.45,
            "away_odds": 1.18,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.18,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2414",
            "standard": 1.5,
            "home_odds": 2.30,
            "away_odds": 1.40,
            "result": "AWAY",
            "desc": "원정 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "2415",
            "standard": 171.5,
            "over_odds": 1.70,
            "under_odds": 1.80,
            "result": "UNDER",
            "desc": "133점 언더"
        }
    },
    {
        "id": "W20261025",
        "date": "2026-10-25 16:00",
        "round": "프로토 승부식 127회차",
        "league": "KOVO여",
        "home": "현대건설 힐스테이트",
        "away": "흥국생명 핑크스파이더스",
        "status": "종료",
        "set_score": "1:3",
        "sets_detail": ["25:23", "20:25", "22:25", "21:25"],
        "total_points": 186,
        "win_lose": {
            "match_no": "2213",
            "home_odds": 1.80,
            "away_odds": 1.70,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.70,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2214",
            "standard": 1.5,
            "home_odds": 1.50,
            "away_odds": 2.10,
            "result": "AWAY",
            "desc": "원정 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "2215",
            "standard": 180.5,
            "over_odds": 1.78,
            "under_odds": 1.72,
            "result": "OVER",
            "desc": "186점 오버"
        }
    }
]

data = {
    "last_updated": "2026-11-13 19:30",
    "mens": seed_mens,
    "womens": seed_womens
}

with open("volleyball-betman-tracker/data/matches.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated data/matches.json successfully!")
