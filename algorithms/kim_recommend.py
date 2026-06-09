# =============================================================================
# GYMlog — 김동현: 그래프 + 해시맵, 그리디 + 위상 정렬
# =============================================================================
# [팀명]  GYMlog (2팀)
# [담당]  202439731 김동현
#
# [자료구조]
#   - 그래프 (DAG, 방향 비순환 그래프): 운동 간 선행 관계 표현
#   - 해시맵 (dict): 목표별 운동 효율 점수, 진입차수 저장
#
# [알고리즘]
#   - 그리디 (Greedy): 효율(점수/시간) 높은 순으로 운동 선택 → 시간 내 최대화
#   - 위상 정렬 (Topological Sort, Kahn's Algorithm): 운동 순서 결정
#
# [시간복잡도]
#   그리디 정렬:  O(N log N)
#   위상 정렬:    O(V + E)  (V=운동 수, E=선행 관계 수)
# =============================================================================

from collections import deque


# ── 자료구조 1: 그래프(DAG) — 운동 선행 관계 ───────────────────────────────
# key: 선행 운동, value: 이 운동이 끝나야 할 수 있는 운동 목록
EXERCISE_DEPS = {
    "바벨 백스쿼트":       ["레그 프레스", "레그 컬"],
    "레그 프레스":         ["레그 컬", "레그 익스텐션"],
    "벤치프레스":          ["스탠딩 케이블 플라이", "펙덱 플라이 머신"],
    "인클라인 벤치프레스": ["인클라인 덤벨 플라이"],
    "랫풀다운":            ["시티드 케이블 로우"],
    "오버헤드 프레스":     ["덤벨 레터럴 레이즈", "페이스 풀"],
    "컨벤셔널 데드리프트": ["루마니안 데드리프트"],
    "루마니안 데드리프트": ["레그 컬"],
    "바벨 힙 쓰러스트":   ["힙 쓰러스트"],
}

# ── 자료구조 2: 해시맵 — 목표별 부위 효율 점수 ─────────────────────────────
GOAL_SCORE = {
    "다이어트": {"유산소": 3, "전신": 2, "하체": 1, "가슴": 1, "등": 1, "어깨": 1, "팔": 1, "복근": 1},
    "근성장":   {"가슴": 3, "등": 3, "하체": 3, "어깨": 2, "팔": 2, "전신": 2, "유산소": 1, "복근": 1},
    "유지":     {"전신": 3, "가슴": 2, "등": 2, "하체": 2, "어깨": 2, "유산소": 2, "팔": 1, "복근": 1},
}

LEVEL_FILTER = {
    "초급": {"초급"},
    "중급": {"초급", "중급"},
    "고급": {"초급", "중급", "고급"},
}

LEVEL_SETS = {"초급": 3, "중급": 4, "고급": 5}


# ── 알고리즘 1: 그리디 — 제한 시간 내 효율 최대화 ──────────────────────────
def greedy_select(
    data: dict,
    goal: str,
    part: str,
    level: str,
    time_limit: int,
) -> list[dict]:
    """
    그리디 알고리즘으로 제한 시간 내 효율(점수/소요시간) 최대 운동 목록 선택.

    Args:
        data:       exercises.json 전체 데이터
        goal:       목표 ('다이어트' | '근성장' | '유지')
        part:       부위 ('전신' | '가슴' | '등' | '하체' | '어깨' | '팔' | '복근')
        level:      난이도 ('초급' | '중급' | '고급')
        time_limit: 총 운동 가능 시간 (분)

    Returns:
        선택된 운동 목록 (dict 리스트)
    """
    score_map  = GOAL_SCORE.get(goal, GOAL_SCORE["근성장"])
    lv_filter  = LEVEL_FILTER.get(level, LEVEL_FILTER["중급"])
    lv_sets    = LEVEL_SETS.get(level, 4)

    # 후보 운동 수집 (리스트 컴프리헨션)
    candidates = []
    for _, parts in data.items():
        for part_name, exs in parts.items():
            if part != "전신" and part_name != part:
                continue
            score = score_map.get(part_name, 1)
            for ex in exs:
                if ex["level"] not in lv_filter:
                    continue
                tps   = ex.get("time_per_set", 3)
                total = lv_sets * tps
                candidates.append({
                    **ex,
                    "part":     part_name,
                    "rec_sets": lv_sets,
                    "rec_time": total,
                    "score":    score,
                    "eff":      score / total if total > 0 else 0,
                })

    # 중복 제거 (첫 출현만 유지)
    seen   = set()
    unique = [ex for ex in candidates
              if ex["name"] not in seen and not seen.add(ex["name"])]

    # ── 그리디 핵심: 효율(점수/시간) 내림차순 정렬 ──
    unique.sort(key=lambda e: e["eff"], reverse=True)

    # 시간 내 최대 선택
    selected, remaining = [], time_limit
    for ex in unique:
        if remaining >= ex["rec_time"]:
            selected.append(ex)
            remaining -= ex["rec_time"]

    return selected


# ── 알고리즘 2: 위상 정렬 (Kahn's Algorithm) ────────────────────────────────
def topological_sort(selected: list[dict]) -> list[dict]:
    """
    선택된 운동 목록에 위상 정렬 적용, 선행 운동이 먼저 오도록 순서 결정.

    Kahn's Algorithm:
      1. 진입차수(in-degree) 초기화
      2. 진입차수 0인 노드를 큐에 삽입
      3. 큐에서 꺼내 결과에 추가, 인접 노드 진입차수 감소
      4. 큐 빌 때까지 반복

    시간복잡도: O(V + E)
    """
    names   = [ex["name"] for ex in selected]
    ex_map  = {ex["name"]: ex for ex in selected}

    # ── 진입차수 초기화 (해시맵 활용) ──
    in_deg = {n: 0 for n in names}

    # 선행 관계에서 진입차수 계산
    for name in names:
        for neighbor in EXERCISE_DEPS.get(name, []):
            if neighbor in in_deg:
                in_deg[neighbor] += 1

    # 큐: 진입차수 0부터 시작
    queue  = deque(n for n in names if in_deg[n] == 0)
    sorted_result = []

    while queue:
        cur = queue.popleft()
        sorted_result.append(ex_map[cur])
        for neighbor in EXERCISE_DEPS.get(cur, []):
            if neighbor in in_deg:
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)

    # 위상정렬 누락 운동 추가 (사이클 없는 독립 노드)
    sorted_names = {ex["name"] for ex in sorted_result}
    sorted_result.extend(ex for ex in selected if ex["name"] not in sorted_names)

    return sorted_result


# ── 통합: 루틴 추천 ─────────────────────────────────────────────────────────
def recommend_routine(
    data: dict,
    goal: str = "근성장",
    part: str = "전신",
    level: str = "중급",
    time_limit: int = 60,
) -> list[dict]:
    """그리디로 운동 선택 → 위상 정렬로 순서 결정."""
    selected = greedy_select(data, goal, part, level, time_limit)
    ordered  = topological_sort(selected)
    return ordered


# ── 데모 함수 ────────────────────────────────────────────────────────────────
def demo_kim(data: dict, sep=None) -> None:
    if sep:
        sep("김동현 — 그래프 + 해시맵 / 그리디 + 위상 정렬")

    scenarios = [
        ("근성장", "가슴", "중급", 45),
        ("다이어트", "전신", "초급", 60),
        ("유지",   "하체", "고급", 30),
    ]

    for goal, part, level, time in scenarios:
        print(f"\n[루틴 추천] 목표={goal}, 부위={part}, 난이도={level}, 시간={time}분")
        routine = recommend_routine(data, goal, part, level, time)
        total_t = sum(ex["rec_time"] for ex in routine)
        print(f"  → {len(routine)}개 운동, 총 {total_t}분")
        for i, ex in enumerate(routine, 1):
            print(f"  {i:2d}. {ex['name']:25s}  {ex['rec_sets']}세트 × {ex.get('time_per_set',3)}분  [eff={ex['eff']:.3f}]")
