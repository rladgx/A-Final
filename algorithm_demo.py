# =============================================================================
# GYMlog  —  알고리즘 데모 메인 진입점
# =============================================================================
#
# [과목]  알고리즘
# [팀명]  2팀
# [팀원]  202439731 김동현 / 202439741 남현욱 / 202439742 박민석
#
# [실행 방법]
#   python algorithm_demo.py
#   (exercises.json 없어도 내장 샘플 데이터로 실행됨)
#
# [파일 구조]
#   algorithm_demo.py          ← 메인 진입점 (이 파일)
#   algorithms/
#     __init__.py
#     data_loader.py           ← 공통: exercises.json 로드
#     park_bst.py              ← 박민석: BST + 정렬 배열, DFS + 이진 탐색
#     kim_recommend.py         ← 김동현: 그래프 + 해시맵, 그리디 + 위상정렬
#     nam_queue_heap.py        ← 남현욱: 큐 + Max-Heap, FIFO + 힙 정렬
# =============================================================================

import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from algorithms.data_loader    import load_exercises
from algorithms.park_bst       import demo_park
from algorithms.kim_recommend  import demo_kim
from algorithms.nam_queue_heap import demo_nam_queue, demo_nam_heap


def separator(title=""):
    """섹션 구분선 출력"""
    line = "=" * 70
    print(f"\n{line}")
    if title:
        print(f"  {title}")
        print(line)


def print_summary():
    separator("GYMlog  —  팀원별 알고리즘 요약표")
    rows = [
        ("박민석", "BST",        "정렬 배열",  "DFS",    "이진 탐색"),
        ("김동현", "그래프(DAG)", "해시맵",     "그리디", "위상 정렬"),
        ("남현욱", "큐(deque)",  "Max-Heap",   "FIFO",   "힙 정렬"),
    ]
    print(f"\n  {'이름':8s} | {'자료구조1':12s} | {'자료구조2':10s} | {'알고리즘1':8s} | {'알고리즘2':8s}")
    print("  " + "-" * 64)
    for name, ds1, ds2, al1, al2 in rows:
        print(f"  {name:8s} | {ds1:12s} | {ds2:10s} | {al1:8s} | {al2:8s}")


def main():
    print_summary()

    data = load_exercises()

    demo_park(data,      sep=separator)
    demo_kim(data,       sep=separator)
    demo_nam_queue(      sep=separator)
    demo_nam_heap(       sep=separator)

    separator("전체 데모 완료")


if __name__ == "__main__":
    main()
