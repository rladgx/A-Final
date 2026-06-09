# =============================================================================
# GYMlog — 박민석: BST + 정렬 배열, DFS + 이진 탐색
# =============================================================================
# [팀명]  GYMlog (2팀)
# [담당]  202439742 박민석
#
# [자료구조]
#   - BST (Binary Search Tree): 운동 이름 기준 삽입·탐색·순회
#   - 정렬 배열: 이진 탐색을 위한 가나다순 정렬 배열
#
# [알고리즘]
#   - DFS (깊이 우선 탐색): BST 전체를 재귀 탐색해 키워드 포함 운동 수집
#   - 이진 탐색 (Binary Search): 정렬 배열에서 O(log N) 탐색
#
# [시간복잡도]
#   BST 삽입/탐색: 평균 O(log N), 최악 O(N)
#   DFS 탐색:      O(N)
#   이진 탐색:     O(log N)
# =============================================================================


# ── 자료구조 1: BST 노드 ────────────────────────────────────────────────────
class BSTNode:
    __slots__ = ('key', 'data', 'left', 'right')  # 메모리 최적화

    def __init__(self, key: str, data: dict):
        self.key   = key    # 운동 이름 (정렬 기준)
        self.data  = data   # 운동 전체 정보
        self.left  = None
        self.right = None


# ── 자료구조 1: 이진 탐색 트리 (BST) ───────────────────────────────────────
class ExerciseBST:
    """운동 데이터를 가나다순으로 저장하는 이진 탐색 트리."""

    def __init__(self):
        self.root = None
        self.size = 0

    # ── BST 삽입: O(log N) 평균 ─────────────────────────────────────────────
    def insert(self, key: str, data: dict) -> None:
        self.root = self._insert(self.root, key, data)
        self.size += 1

    def _insert(self, node, key, data):
        if node is None:
            return BSTNode(key, data)
        if key < node.key:
            node.left  = self._insert(node.left,  key, data)
        elif key > node.key:
            node.right = self._insert(node.right, key, data)
        return node

    # ── 알고리즘 1: 이진 탐색 — 정확한 이름 탐색: O(log N) ─────────────────
    def search(self, key: str) -> dict | None:
        """정확한 운동 이름으로 O(log N) 탐색."""
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node.data
        if key < node.key:
            return self._search(node.left,  key)
        return self._search(node.right, key)

    # ── 알고리즘 2: DFS — 키워드 포함 운동 전체 탐색: O(N) ──────────────────
    def dfs_search(self, keyword: str) -> list[dict]:
        """
        깊이 우선 탐색(전위순회)으로 keyword를 포함하는 운동 수집.
        재귀 스택 사용, 시간복잡도 O(N).
        """
        keyword = keyword.lower()
        results = []
        self._dfs(self.root, keyword, results)
        return results

    def _dfs(self, node, keyword, results):
        if node is None:
            return
        # 전위 순회: 현재 노드 먼저 확인
        name   = node.key.lower()
        muscle = (node.data.get("muscle") or "").lower()
        if keyword in name or keyword in muscle:
            results.append(node.data)
        self._dfs(node.left,  keyword, results)   # 왼쪽 서브트리
        self._dfs(node.right, keyword, results)   # 오른쪽 서브트리

    # ── 중위 순회: 가나다순 전체 출력 ───────────────────────────────────────
    def inorder(self) -> list[dict]:
        results = []
        self._inorder(self.root, results)
        return results

    def _inorder(self, node, results):
        if node is None:
            return
        self._inorder(node.left, results)
        results.append(node.data)
        self._inorder(node.right, results)


# ── 자료구조 2: 정렬 배열 + 이진 탐색 ─────────────────────────────────────
def build_sorted_array(data: dict) -> list[dict]:
    """exercises.json에서 운동을 수집해 이름 기준 정렬 배열 생성."""
    exercises = [
        ex
        for parts in data.values()
        for exs in parts.values()
        for ex in exs
    ]
    exercises.sort(key=lambda e: e["name"])
    return exercises


def binary_search(arr: list[dict], target: str) -> dict | None:
    """
    정렬 배열에서 운동 이름으로 이진 탐색.
    시간복잡도: O(log N)
    """
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid]["name"] == target:
            return arr[mid]
        elif arr[mid]["name"] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return None


# ── 데모 함수 ───────────────────────────────────────────────────────────────
def demo_park(data: dict, sep=None) -> None:
    if sep:
        sep("박민석 — BST + 정렬 배열 / DFS + 이진 탐색")

    # BST 구축
    bst = ExerciseBST()
    seen = set()
    for parts in data.values():
        for exs in parts.values():
            for ex in exs:
                if ex["name"] not in seen:
                    seen.add(ex["name"])
                    bst.insert(ex["name"], ex)

    print(f"\n[BST] 총 {bst.size}개 운동 삽입 완료")

    # 중위 순회 (가나다순)
    ordered = bst.inorder()
    print(f"\n[중위순회] 가나다순 상위 5개:")
    for ex in ordered[:5]:
        print(f"  {ex['name']:20s}  {ex['muscle']:10s}  {ex['level']}")

    # DFS 키워드 탐색
    keyword = "스쿼트"
    dfs_result = bst.dfs_search(keyword)
    print(f"\n[DFS] '{keyword}' 포함 운동 {len(dfs_result)}개:")
    for ex in dfs_result[:5]:
        print(f"  {ex['name']:25s}  {ex['muscle']}")

    # 정렬 배열 + 이진 탐색
    sorted_arr = build_sorted_array(data)
    print(f"\n[정렬 배열] {len(sorted_arr)}개 운동 정렬 완료")

    targets = ["벤치프레스", "레그 프레스", "존재하지않는운동"]
    print("\n[이진 탐색] 탐색 결과:")
    for t in targets:
        found = binary_search(sorted_arr, t)
        if found:
            print(f"  ✅ '{t}' → 근육: {found['muscle']}, 난이도: {found['level']}")
        else:
            print(f"  ❌ '{t}' → 없음")
