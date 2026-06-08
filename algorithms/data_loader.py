# =============================================================================
# GYMlog — 공통: exercises.json 로드
# =============================================================================
# [팀명]  GYMlog (2팀)
# [팀원]  202439731 김동현 / 202439741 남현욱 / 202439742 박민석
# =============================================================================

import json
import os

# 내장 샘플 데이터 (exercises.json 없을 때 사용)
SAMPLE_DATA = {
    "헬스": {
        "하체": [
            {"name": "바벨 백스쿼트",   "level": "중급", "time_per_set": 3, "muscle": "대퇴사두",  "equipment": "바벨"},
            {"name": "레그 프레스",      "level": "초급", "time_per_set": 3, "muscle": "대퇴사두",  "equipment": "레그프레스 머신"},
            {"name": "레그 컬",          "level": "초급", "time_per_set": 2, "muscle": "햄스트링",  "equipment": "레그컬 머신"},
            {"name": "레그 익스텐션",    "level": "초급", "time_per_set": 2, "muscle": "대퇴사두",  "equipment": "레그익스텐션 머신"},
            {"name": "루마니안 데드리프트","level": "중급","time_per_set": 3, "muscle": "햄스트링",  "equipment": "바벨"},
            {"name": "컨벤셔널 데드리프트","level": "고급","time_per_set": 4, "muscle": "전신",      "equipment": "바벨"},
            {"name": "힙 쓰러스트",      "level": "초급", "time_per_set": 3, "muscle": "둔근",      "equipment": "맨몸"},
            {"name": "바벨 힙 쓰러스트", "level": "중급", "time_per_set": 3, "muscle": "둔근",      "equipment": "바벨"},
        ],
        "가슴": [
            {"name": "벤치프레스",        "level": "중급", "time_per_set": 3, "muscle": "가슴",     "equipment": "바벨"},
            {"name": "덤벨 벤치프레스",   "level": "초급", "time_per_set": 3, "muscle": "가슴",     "equipment": "덤벨"},
            {"name": "인클라인 벤치프레스","level": "중급", "time_per_set": 3, "muscle": "가슴 상부","equipment": "바벨"},
            {"name": "푸시업",            "level": "초급", "time_per_set": 2, "muscle": "가슴",     "equipment": "맨몸"},
            {"name": "펙덱 플라이 머신",  "level": "초급", "time_per_set": 2, "muscle": "가슴",     "equipment": "펙덱 머신"},
            {"name": "스탠딩 케이블 플라이","level":"초급", "time_per_set": 2, "muscle": "가슴",     "equipment": "케이블 머신"},
        ],
        "등": [
            {"name": "랫풀다운",         "level": "초급", "time_per_set": 2, "muscle": "광배근",    "equipment": "랫풀다운 머신"},
            {"name": "시티드 케이블 로우","level": "초급", "time_per_set": 2, "muscle": "등",        "equipment": "케이블 머신"},
            {"name": "덤벨 로우",        "level": "초급", "time_per_set": 2, "muscle": "등",        "equipment": "덤벨"},
            {"name": "풀업",             "level": "중급", "time_per_set": 2, "muscle": "등",        "equipment": "철봉"},
        ],
        "어깨": [
            {"name": "오버헤드 프레스",   "level": "중급", "time_per_set": 3, "muscle": "어깨",     "equipment": "바벨"},
            {"name": "덤벨 숄더 프레스", "level": "초급", "time_per_set": 3, "muscle": "어깨",     "equipment": "덤벨"},
            {"name": "덤벨 레터럴 레이즈","level": "초급", "time_per_set": 2, "muscle": "측면 삼각근","equipment": "덤벨"},
            {"name": "페이스 풀",        "level": "초급", "time_per_set": 2, "muscle": "후면 삼각근","equipment": "케이블 머신"},
        ],
        "팔": [
            {"name": "바벨 컬",          "level": "초급", "time_per_set": 2, "muscle": "이두",      "equipment": "바벨"},
            {"name": "덤벨 해머 컬",     "level": "초급", "time_per_set": 2, "muscle": "이두",      "equipment": "덤벨"},
            {"name": "케이블 푸시 다운", "level": "초급", "time_per_set": 2, "muscle": "삼두",      "equipment": "케이블 머신"},
            {"name": "스컬 크러셔",      "level": "중급", "time_per_set": 2, "muscle": "삼두",      "equipment": "바벨"},
        ],
        "복근": [
            {"name": "플랭크",           "level": "초급", "time_per_set": 2, "muscle": "복근",      "equipment": "맨몸"},
            {"name": "크런치",           "level": "초급", "time_per_set": 2, "muscle": "복근",      "equipment": "맨몸"},
            {"name": "레그 레이즈",      "level": "초급", "time_per_set": 2, "muscle": "하복근",    "equipment": "맨몸"},
        ],
    },
    "유산소": {
        "전신": [
            {"name": "트레드밀",         "level": "초급", "time_per_set": 20, "muscle": "유산소",   "equipment": "트레드밀"},
            {"name": "싸이클",           "level": "초급", "time_per_set": 20, "muscle": "유산소",   "equipment": "사이클 머신"},
            {"name": "걷기",             "level": "초급", "time_per_set": 30, "muscle": "유산소",   "equipment": "맨몸"},
            {"name": "달리기",           "level": "초급", "time_per_set": 20, "muscle": "유산소",   "equipment": "맨몸"},
            {"name": "줄넘기",           "level": "초급", "time_per_set": 10, "muscle": "유산소",   "equipment": "줄넘기"},
        ],
    },
}


def load_exercises(path: str = None) -> dict:
    """
    exercises.json 로드.
    파일이 없으면 내장 샘플 데이터 반환.
    """
    if path is None:
        # 현재 스크립트 기준 상위 폴더에서 찾기
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, "exercises.json")

    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            total = sum(
                len(exs)
                for parts in data.values()
                for exs in parts.values()
            )
            print(f"[data_loader] exercises.json 로드 완료 — {total}개 운동")
            return data
        except Exception as e:
            print(f"[data_loader] JSON 파싱 오류: {e} → 샘플 데이터 사용")
    else:
        print(f"[data_loader] exercises.json 없음 → 내장 샘플 데이터 사용")

    return SAMPLE_DATA
