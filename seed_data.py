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
            "desc": "홈 -1.5 마핸승 (셧아웃)"
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
        "sets_detail": ["25:21", "20:25", "18:25", "21:25"],
        "total_points": 180,
        "win_lose": {
            "match_no": "3105",
            "home_odds": 2.25,
            "away_odds": 1.42,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.42,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "3106",
            "standard": 1.5,
            "home_odds": 1.68,
            "away_odds": 1.82,
            "result": "AWAY",
            "desc": "원정 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "3107",
            "standard": 182.5,
            "over_odds": 1.74,
            "under_odds": 1.76,
            "result": "UNDER",
            "desc": "180점 언더"
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
        "sets_detail": ["25:23", "22:25", "25:21", "19:25", "15:12"],
        "total_points": 212,
        "win_lose": {
            "match_no": "2980",
            "home_odds": 2.45,
            "away_odds": 1.35,
            "winner": "HOME",
            "favorite": "AWAY",
            "hit_odds": 2.45,
            "hit_type": "역배"
        },
        "handicap": {
            "match_no": "2981",
            "standard": 1.5,
            "home_odds": 1.75,
            "away_odds": 1.73,
            "result": "HOME",
            "desc": "홈 +1.5 플핸승"
        },
        "under_over": {
            "match_no": "2982",
            "standard": 183.5,
            "over_odds": 1.78,
            "under_odds": 1.72,
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
        "sets_detail": ["21:25", "19:25", "22:25"],
        "total_points": 137,
        "win_lose": {
            "match_no": "2855",
            "home_odds": 1.55,
            "away_odds": 2.01,
            "winner": "AWAY",
            "favorite": "HOME",
            "hit_odds": 2.01,
            "hit_type": "역배"
        },
        "handicap": {
            "match_no": "2856",
            "standard": -1.5,
            "home_odds": 2.05,
            "away_odds": 1.52,
            "result": "AWAY",
            "desc": "원정 +1.5 플핸승"
        },
        "under_over": {
            "match_no": "2857",
            "standard": 180.5,
            "over_odds": 1.75,
            "under_odds": 1.75,
            "result": "UNDER",
            "desc": "137점 언더"
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
        "sets_detail": ["25:21", "25:23", "20:25", "25:22"],
        "total_points": 186,
        "win_lose": {
            "match_no": "2720",
            "home_odds": 1.38,
            "away_odds": 2.38,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.38,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2721",
            "standard": -1.5,
            "home_odds": 1.72,
            "away_odds": 1.78,
            "result": "HOME",
            "desc": "홈 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "2722",
            "standard": 182.5,
            "over_odds": 1.76,
            "under_odds": 1.74,
            "result": "OVER",
            "desc": "186점 오버"
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
            "match_no": "3913",
            "home_odds": 1.23,
            "away_odds": 2.97,
            "winner": None,
            "favorite": "HOME"
        },
        "handicap": {
            "match_no": "3914",
            "standard": -1.5,
            "home_odds": 1.47,
            "away_odds": 2.13,
            "result": None
        },
        "under_over": {
            "match_no": "3915",
            "standard": 177.5,
            "over_odds": 2.07,
            "under_odds": 1.50,
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
        "sets_detail": ["22:25", "21:25", "19:25"],
        "total_points": 137,
        "win_lose": {
            "match_no": "3817",
            "home_odds": 4.47,
            "away_odds": 1.08,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.08,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "3818",
            "standard": 2.5,
            "home_odds": 1.88,
            "away_odds": 1.62,
            "result": "AWAY",
            "desc": "원정 -2.5 마핸승 (3:0)"
        },
        "under_over": {
            "match_no": "3819",
            "standard": 169.5,
            "over_odds": 1.70,
            "under_odds": 1.80,
            "result": "UNDER",
            "desc": "137점 언더"
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
        "sets_detail": ["23:25", "20:25", "22:25"],
        "total_points": 140,
        "win_lose": {
            "match_no": "3742",
            "home_odds": 3.57,
            "away_odds": 1.15,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.15,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "3743",
            "standard": 1.5,
            "home_odds": 2.25,
            "away_odds": 1.42,
            "result": "AWAY",
            "desc": "원정 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "3744",
            "standard": 172.5,
            "over_odds": 1.72,
            "under_odds": 1.78,
            "result": "UNDER",
            "desc": "140점 언더"
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
        "sets_detail": ["25:21", "25:23", "21:25", "25:22"],
        "total_points": 187,
        "win_lose": {
            "match_no": "3394",
            "home_odds": 1.71,
            "away_odds": 1.77,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.71,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "3395",
            "standard": -1.5,
            "home_odds": 2.20,
            "away_odds": 1.45,
            "result": "HOME",
            "desc": "홈 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "3396",
            "standard": 181.5,
            "over_odds": 1.75,
            "under_odds": 1.75,
            "result": "OVER",
            "desc": "187점 오버"
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
        "sets_detail": ["21:25", "25:22", "18:25", "19:25"],
        "total_points": 180,
        "win_lose": {
            "match_no": "3225",
            "home_odds": 3.10,
            "away_odds": 1.21,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.21,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "3226",
            "standard": 1.5,
            "home_odds": 2.05,
            "away_odds": 1.52,
            "result": "AWAY",
            "desc": "원정 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "3227",
            "standard": 176.5,
            "over_odds": 1.78,
            "under_odds": 1.72,
            "result": "OVER",
            "desc": "180점 오버"
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
        "sets_detail": ["25:22", "20:25", "25:21", "22:25", "15:10"],
        "total_points": 210,
        "win_lose": {
            "match_no": "3118",
            "home_odds": 1.62,
            "away_odds": 1.90,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.62,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "3119",
            "standard": -1.5,
            "home_odds": 2.10,
            "away_odds": 1.50,
            "result": "AWAY",
            "desc": "원정 +1.5 플핸승"
        },
        "under_over": {
            "match_no": "3120",
            "standard": 180.5,
            "over_odds": 1.74,
            "under_odds": 1.76,
            "result": "OVER",
            "desc": "210점 오버"
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
        "sets_detail": ["25:19", "25:22", "25:20"],
        "total_points": 136,
        "win_lose": {
            "match_no": "2870",
            "home_odds": 1.32,
            "away_odds": 2.65,
            "winner": "HOME",
            "favorite": "HOME",
            "hit_odds": 1.32,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2871",
            "standard": -1.5,
            "home_odds": 1.58,
            "away_odds": 1.95,
            "result": "HOME",
            "desc": "홈 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "2872",
            "standard": 178.5,
            "over_odds": 1.72,
            "under_odds": 1.78,
            "result": "UNDER",
            "desc": "136점 언더"
        }
    },
    {
        "id": "W20261102",
        "date": "2026-11-02 16:00",
        "round": "프로토 승부식 129회차",
        "league": "KOVO여",
        "home": "페퍼저축은행 AI페퍼스",
        "away": "한국도로공사 하이패스",
        "status": "종료",
        "set_score": "0:3",
        "sets_detail": ["18:25", "21:25", "19:25"],
        "total_points": 133,
        "win_lose": {
            "match_no": "2610",
            "home_odds": 3.45,
            "away_odds": 1.18,
            "winner": "AWAY",
            "favorite": "AWAY",
            "hit_odds": 1.18,
            "hit_type": "정배"
        },
        "handicap": {
            "match_no": "2611",
            "standard": 1.5,
            "home_odds": 2.30,
            "away_odds": 1.40,
            "result": "AWAY",
            "desc": "원정 -1.5 마핸승"
        },
        "under_over": {
            "match_no": "2612",
            "standard": 171.5,
            "over_odds": 1.70,
            "under_odds": 1.80,
            "result": "UNDER",
            "desc": "133점 언더"
        }
    }
]

os.makedirs("volleyball-betman-tracker/data", exist_ok=True)
data = {
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    "mens": seed_mens,
    "womens": seed_womens
}

with open("volleyball-betman-tracker/data/matches.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Generated matches.json successfully!")
