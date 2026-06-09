# =============================================================================
# GYMlog — 남현욱: 큐 + Max-Heap, FIFO + 힙 정렬
# =============================================================================
# [팀명]  GYMlog (2팀)
# [담당]  202439741 남현욱
#
# [자료구조]
#   - 큐 (deque): 기구 대기열 — FIFO 방식으로 사용자 순서 관리
#   - Max-Heap: 운동 빈도 기반 Top-K 추출
#
# [알고리즘]
#   - FIFO 큐 스케줄링: 선입선출 방식으로 기구 대기열 처리
#   - 힙 정렬 (Heap Sort): Max-Heap으로 Top5 운동 추출
#
# [시간복잡도]
#   FIFO enqueue/dequeue: O(1)
#   힙 삽입 (heapInsert):   O(log N)
#   힙 추출 (heapExtract):  O(log N)
#   Top-K 추출:             O(N log N) 삽입 + O(K log N) 추출
# =============================================================================

from collections import deque
import time as _time


# ══════════════════════════════════════════════════════════════════════════════
# 자료구조 1: 큐 (FIFO 기구 대기열)
# ══════════════════════════════════════════════════════════════════════════════

class User:
    """대기열에 등록되는 사용자 정보."""
    __slots__ = ('user_id', 'sets', 'time_per_set', 'est_time', 'enqueued_at')

    def __init__(self, user_id: str, sets: int, time_per_set: int = 3):
        self.user_id      = user_id
        self.sets         = sets
        self.time_per_set = time_per_set
        self.est_time     = sets * time_per_set   # 예상 소요 시간(분)
        self.enqueued_at  = _time.time()

    def __repr__(self):
        return f"User({self.user_id}, {self.sets}세트, ~{self.est_time}분)"


class EquipmentQueue:
    """
    기구 하나의 대기열을 관리하는 클래스.
    내부적으로 deque를 사용해 FIFO 보장.
    """

    def __init__(self, name: str):
        self.name         = name
        self.queue        = deque()       # 대기 큐 (FIFO)
        self.current_user = None          # 현재 사용자
        self.status       = "available"   # available | in_use

    # ── FIFO enqueue ─────────────────────────────────────────────────────────
    def reserve(self, user: User) -> str:
        """
        예약 처리.
        - 사용 가능: 즉시 사용 시작
        - 사용 중:   대기열 뒤에 추가 (FIFO)
        """
        if self.status == "available":
            self.current_user = user
            self.status       = "in_use"
            return f"✅ '{self.name}' 즉시 사용 시작 — {user.sets}세트"
        else:
            self.queue.append(user)       # O(1) enqueue
            wait = self.calc_wait()
            return f"⏳ 대기열 등록 — 대기 {len(self.queue)}번째, 예상 {wait}분"

    # ── FIFO dequeue ─────────────────────────────────────────────────────────
    def complete(self) -> str:
        """
        사용 완료 처리.
        대기열에서 다음 사용자를 dequeue해 current_user로 이동.
        """
        if not self.current_user:
            return "현재 사용자 없음"
        prev = self.current_user.user_id
        if self.queue:
            next_user         = self.queue.popleft()   # O(1) dequeue
            self.current_user = next_user
            return f"'{prev}' 완료 → '{next_user.user_id}' 사용 시작"
        else:
            self.current_user = None
            self.status       = "available"
            return f"'{prev}' 완료 — 기구 사용 가능"

    # ── 대기 시간 계산 ────────────────────────────────────────────────────────
    def calc_wait(self) -> int:
        """현재 사용자 + 대기열 전체 예상 대기 시간(분) 합산."""
        cur   = self.current_user.est_time if self.current_user else 0
        queue = sum(u.est_time for u in self.queue)
        return cur + queue

    def __repr__(self):
        q_str = ", ".join(str(u) for u in self.queue)
        return (
            f"EqQueue('{self.name}' | "
            f"현재={self.current_user} | "
            f"대기=[{q_str}])"
        )


# ══════════════════════════════════════════════════════════════════════════════
# 자료구조 2: Max-Heap (힙 정렬 Top-K)
# ══════════════════════════════════════════════════════════════════════════════

class MaxHeap:
    """
    Max-Heap 자료구조.
    heapify-up / heapify-down으로 힙 속성 유지.
    """

    def __init__(self):
        self._heap = []   # 내부 배열

    # ── 삽입: heapify-up O(log N) ─────────────────────────────────────────────
    def insert(self, item: dict) -> None:
        """
        아이템 삽입 후 heapify-up으로 힙 속성 복원.
        item: {'name': str, 'cnt': int}
        """
        self._heap.append(item)
        self._heapify_up(len(self._heap) - 1)

    def _heapify_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[parent]["cnt"] < self._heap[i]["cnt"]:
                self._heap[parent], self._heap[i] = self._heap[i], self._heap[parent]
                i = parent
            else:
                break

    # ── 최댓값 추출: heapify-down O(log N) ───────────────────────────────────
    def extract_max(self) -> dict | None:
        """
        최댓값(루트) 추출 후 heapify-down으로 힙 속성 복원.
        """
        if not self._heap:
            return None
        max_item = self._heap[0]
        last     = self._heap.pop()
        if self._heap:
            self._heap[0] = last
            self._heapify_down(0)
        return max_item

    def _heapify_down(self, i: int) -> None:
        n = len(self._heap)
        while True:
            largest = i
            l, r    = 2 * i + 1, 2 * i + 2
            if l < n and self._heap[l]["cnt"] > self._heap[largest]["cnt"]:
                largest = l
            if r < n and self._heap[r]["cnt"] > self._heap[largest]["cnt"]:
                largest = r
            if largest == i:
                break
            self._heap[i], self._heap[largest] = self._heap[largest], self._heap[i]
            i = largest

    def __len__(self):
        return len(self._heap)


# ── 알고리즘: 힙 정렬로 Top-K 운동 추출 ────────────────────────────────────
def top_k_exercises(records: list[dict], k: int = 5) -> list[dict]:
    """
    운동 기록에서 Max-Heap을 이용해 Top-K 운동 추출.

    Args:
        records: [{"exercises": [{"name": str, ...}], ...}, ...]
        k:       추출할 상위 운동 수

    Returns:
        [{"name": str, "cnt": int}, ...] (cnt 내림차순)
    """
    # 빈도 카운트 (해시맵)
    count: dict[str, int] = {}
    for rec in records:
        for ex in rec.get("exercises", []):
            name = ex.get("name", "") if isinstance(ex, dict) else str(ex)
            if name:
                count[name] = count.get(name, 0) + 1

    # Max-Heap 구성: O(N log N)
    heap = MaxHeap()
    for name, cnt in count.items():
        heap.insert({"name": name, "cnt": cnt})

    # Top-K 추출: O(K log N)
    result = []
    for _ in range(min(k, len(heap))):
        item = heap.extract_max()
        if item:
            result.append(item)
    return result


# ── 데모 함수 ────────────────────────────────────────────────────────────────
def demo_nam_queue(sep=None) -> None:
    if sep:
        sep("남현욱 — 큐(deque) / FIFO 기구 스케줄링")

    eq = EquipmentQueue("벤치프레스")

    users = [
        User("김동현", sets=4, time_per_set=3),
        User("남현욱", sets=3, time_per_set=3),
        User("박민석", sets=5, time_per_set=2),
    ]

    print(f"\n[FIFO 큐] '{eq.name}' 예약 시뮬레이션")
    for u in users:
        result = eq.reserve(u)
        print(f"  {u.user_id}: {result}")
        print(f"  현재 대기열: {[str(x) for x in eq.queue]}")

    print(f"\n[사용 완료 처리]")
    for _ in range(3):
        result = eq.complete()
        print(f"  → {result}")


def demo_nam_heap(sep=None) -> None:
    if sep:
        sep("남현욱 — Max-Heap / 힙 정렬 Top5 추출")

    # 샘플 운동 기록
    sample_records = [
        {"exercises": [{"name": "벤치프레스"}, {"name": "덤벨 벤치프레스"}, {"name": "플랭크"}]},
        {"exercises": [{"name": "벤치프레스"}, {"name": "스쿼트"}, {"name": "플랭크"}]},
        {"exercises": [{"name": "벤치프레스"}, {"name": "랫풀다운"}, {"name": "바벨 컬"}]},
        {"exercises": [{"name": "스쿼트"},     {"name": "레그 프레스"}, {"name": "플랭크"}]},
        {"exercises": [{"name": "랫풀다운"},   {"name": "덤벨 로우"},   {"name": "바벨 컬"}]},
        {"exercises": [{"name": "오버헤드 프레스"}, {"name": "덤벨 레터럴 레이즈"}]},
    ]

    print(f"\n[Max-Heap] {len(sample_records)}회 운동 기록 기반 Top5")
    top5 = top_k_exercises(sample_records, k=5)
    for i, item in enumerate(top5, 1):
        bar = "█" * item["cnt"]
        print(f"  {i}. {item['name']:25s}  {item['cnt']}회  {bar}")
