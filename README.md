# GYMlog - 스마트 운동 플래너
## 알고리즘이 적용된 헬스 서비스 프로토타입

| 항목 | 내용 |
|------|------|
| 과목 | 알고리즘 |
| 팀명 | 2팀 |
| 팀원 | 202439731 김동현 / 202439741 남현욱 / 202439742 박민석 |
| 제출일 | 2026-06-12 |

---

## 실행 방법

**GitHub Pages**: https://rladgx.github.io/A-Final
**로컬**: `index.html`을 Live Server로 실행 (파일 직접 열기 시 Firebase CORS 오류 발생)

---

## 1. 프로토타입 설명

| 항목 | 내용 |
|------|------|
| **What** | 운동 기록 · 루틴 자동 추천 · 기구 실시간 예약 · 식단 분석을 하나의 앱으로 통합한 헬스 관리 서비스 |
| **Who** | 헬스장을 정기적으로 이용하는 일반 사용자 (초급~고급) |
| **When** | 헬스장 방문 전(루틴 계획) · 운동 중(기록·타이머·기구 예약) · 운동 후(분석·식단) |
| **Why** | 운동 계획·기록·분석이 여러 앱에 분산되어 불편하고, 기구 대기 정보를 실시간으로 알 수 없는 문제를 해결하기 위해 알고리즘 기반 통합 서비스로 구현 |

---

## 2. 업무 분장표

| 팀원 | 담당 기능 | 사용 자료구조 | 사용 알고리즘 | 핵심 함수 |
|------|----------|-------------|-------------|---------|
| 202439731 김동현 | 루틴 추천 모듈 설계 및 구현, Firebase 연동, 전체 UI | 그래프(인접리스트), 해시맵 | 그리디(Greedy), 위상 정렬(Kahn's) | `runRecommend()` |
| 202439741 남현욱 | 기구 예약 모듈, 실시간 대기열 관리 | 큐(Queue), 배열 | 큐 스케줄링(FIFO), 힙 정렬(Top5 추출) | `makeReservation()`, `completeUse()`, `heapInsert()`, `heapExtractMax()`, `renderTop5()` |
| 202439742 박민석 | 운동 찾아보기 모듈, exercises.json 데이터 수집 | BST(이진탐색트리), 배열 | DFS(깊이우선탐색), 이진 탐색 | `buildExerciseBST()`, `searchExercise()`, `filterByPart()`, `class ExerciseBST` |

---

## 3. Input 데이터

### exercises.json (운동 데이터)

- **출처**: 번핏(Burnfit) 라이브러리 기반 직접 수집
- **규모**: 110개 운동 (헬스 5부위 + 맨몸)
- **필드 구조**:

```json
{
  "헬스": {
    "하체": [
      {
        "name": "바벨 백스쿼트",
        "level": "중급",
        "time_per_set": 3,
        "muscle": "대퇴사두",
        "equipment": "바벨",
        "youtube": "https://...",
        "playlist": {
          "다이어트": "https://...",
          "근성장": "https://...",
          "유지": "https://..."
        },
        "url": "https://burnfit.io/library/..."
      }
    ]
  }
}
```

### FOOD_DB (식품 영양성분 데이터)

- **출처**: 식품안전처 식품영양성분 DB (공공데이터포털 data.go.kr)
- **규모**: 77개 주요 식품 내장 + 실시간 OpenAPI 검색 병행
- **필드 구조**:

```json
{
  "닭가슴살": { "cal": 165, "carb": 0, "protein": 31, "fat": 3.6 }
}
```

### Firebase Realtime Database

- **출처**: 자체 Firebase 프로젝트 (a-final-f8b6f)
- **users/{phone}**: 사용자 정보 (name, goal, level, joinedAt)
- **records/{id}**: 운동 기록 (userId, date, exercises, duration, totalVolume)
- **queues/{equipment}**: 기구별 대기열 상태 (currentUser, queue[], status)

---

## 4. 사용한 자료구조 & 알고리즘

### 모듈별 요약

| 모듈 | 자료구조 | 알고리즘 | 담당 |
|------|---------|---------|------|
| 루틴 추천 | 그래프(인접리스트), 해시맵 | 위상 정렬(Kahn's), 그리디 | 김동현 |
| 기구 예약 | 큐(Queue), 배열 | 큐 스케줄링(FIFO), 힙 정렬 | 남현욱 |
| 운동 찾아보기 | BST, 배열 | DFS, 이진 탐색 | 박민석 |
| 운동 기록 분석 | 배열, 해시맵 | 힙 정렬(Top5), 선형 탐색 | 남현욱 |

### 알고리즘 선택 이유

| 알고리즘 | 선택 이유 |
|---------|---------|
| **그리디** | 제한된 운동 시간 내 효율(점수/시간) 최대화 - 최적 부분 구조 만족 |
| **위상 정렬** | 운동 간 선행 관계(스쿼트→레그컬 등)를 DAG로 표현, 올바른 순서 보장 |
| **FIFO 큐** | 선착순 공정성 보장 - 헬스장 대기열의 현실 규칙과 일치 |
| **Max-Heap** | 빈도수 기반 Top K 추출을 O(N log N)으로 처리, 전체 정렬보다 효율적 |
| **BST** | 운동 이름 가나다순 자동 정렬 저장, 이진 탐색으로 O(log N) 검색 |
| **DFS** | 키워드 포함 운동 전체 탐색 - 부분 일치 검색에 적합, 재귀 구현 간결 |

---

## 5. 설계/구현 방법

### Architecture

```
┌──────────────────────────────────────────────────────┐
│                   index.html (단일 파일)               │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  홈 / 캘린더 │  │  루틴 추천    │  │  기구 예약    │  │
│  │  운동 일지   │  │  그리디+위상정렬│  │  큐+힙       │  │
│  └────────────┘  └──────────────┘  └──────────────┘  │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ 운동 찾아보기│  │  성장 분석    │  │   식단 관리   │  │
│  │ BST+DFS    │  │  힙 정렬 Top5 │  │  OpenAPI     │  │
│  └────────────┘  └──────────────┘  └──────────────┘  │
└──────────────┬───────────────────────────┬───────────┘
               │                           │
    ┌──────────▼───────────┐   ┌───────────▼──────────┐
    │  Firebase Realtime DB │   │  식품안전처 OpenAPI   │
    │  - users             │   │  (data.go.kr)        │
    │  - records           │   │  실시간 식품 검색      │
    │  - queues (대기열)    │   └──────────────────────┘
    └──────────────────────┘
```

### 동작 방식

1. **로그인**: 전화번호 입력 → Firebase에서 사용자 조회 → 신규면 회원가입
2. **운동 일지**: 루틴 선택 → 타이머 시작 → 세트/중량/횟수 입력 → Firebase 저장
3. **루틴 추천**: 목표·부위·시간·수준 선택 → 그리디로 최적 운동 선발 → 위상정렬로 순서 결정
4. **기구 예약**: 기구 선택 → 큐에 enqueue → Firebase 실시간 동기화 → 완료 시 dequeue
5. **운동 찾기**: BST 구축(앱 시작 시 1회) → 검색어 입력 → 정확 일치는 이진 탐색, 부분 일치는 DFS
6. **성장 분석**: Firebase 기록 로드 → 해시맵으로 빈도 집계 → Max-Heap으로 Top5 추출

### 핵심코드

#### [1] 그리디 + 위상 정렬 (루틴 추천) — `runRecommend()`

```javascript
// ① 그리디: 효율(목표점수 / 소요시간) 기준 내림차순 정렬 후 시간 예산 내 최대 선택
const scored = candidates.map(ex => {
  const sets = levelSets[ex.level] || 3;
  const tot  = ex.time_per_set * sets;
  const score = (goalScore[goal] || {})[ex.muscle] || 1;
  return { eff: score / tot, tot, sets, ex };
}).sort((a, b) => b.eff - a.eff);

let rem = time, selected = [];
for (const { tot, sets, ex } of scored) {
  if (rem >= tot) { selected.push({...ex, recSets: sets, recTime: tot}); rem -= tot; }
}

// ② 위상 정렬(Kahn's): 운동 선행관계 DAG → 진입차수 0부터 큐에 넣어 순서 결정
const inDeg = {};
names.forEach(n => inDeg[n] = 0);
names.forEach(n => (deps[n] || []).forEach(nb => { if (inDeg[nb] !== undefined) inDeg[nb]++; }));
const q = names.filter(n => inDeg[n] === 0);
while (q.length) {
  const cur = q.shift();
  if (map[cur]) sorted.push(map[cur]);
  (deps[cur] || []).forEach(nb => { if (--inDeg[nb] === 0) q.push(nb); });
}
```

#### [2] Max-Heap 구현 + 힙 정렬 Top5 (운동 기록 분석) — `heapInsert()`, `renderTop5()`

```javascript
// Max-Heap 삽입: heapify-up O(log N)
function heapInsert(heap, item) {
  heap.push(item);
  let i = heap.length - 1;
  while (i > 0) {
    const parent = Math.floor((i - 1) / 2);
    if (heap[parent].cnt < heap[i].cnt) {
      [heap[parent], heap[i]] = [heap[i], heap[parent]];
      i = parent;
    } else break;
  }
}

// Max-Heap 추출: heapify-down O(log N)
function heapExtractMax(heap) {
  const max = heap[0];
  heap[0] = heap.pop();
  let i = 0;
  while (true) {
    let largest = i;
    const l = 2*i+1, r = 2*i+2;
    if (l < heap.length && heap[l].cnt > heap[largest].cnt) largest = l;
    if (r < heap.length && heap[r].cnt > heap[largest].cnt) largest = r;
    if (largest === i) break;
    [heap[i], heap[largest]] = [heap[largest], heap[i]];
    i = largest;
  }
  return max;
}

// Top5 추출: 전체 삽입 O(N log N) + 5번 추출 O(5 log N)
const maxHeap = [];
Object.entries(exCount).forEach(([name, cnt]) => heapInsert(maxHeap, { name, cnt }));
const top5 = [];
for (let k = 0; k < 5 && maxHeap.length > 0; k++) top5.push(heapExtractMax(maxHeap));
```

#### [3] BST + DFS + 이진탐색 (운동 찾아보기) — `class ExerciseBST`

```javascript
class ExerciseBST {
  // 삽입: 가나다순 비교 O(log N) 평균
  _insert(node, key, data) {
    if (!node) return new BSTNode(key, data);
    if (key < node.key) node.left  = this._insert(node.left,  key, data);
    else if (key > node.key) node.right = this._insert(node.right, key, data);
    return node;
  }

  // 이진 탐색: 정확한 이름 검색 O(log N)
  _search(node, key) {
    if (!node) return null;
    if (key === node.key) return node.data;
    return key < node.key ? this._search(node.left, key) : this._search(node.right, key);
  }

  // DFS (전위 순회): 키워드 포함 전체 탐색 O(N)
  _dfs(node, keyword, results) {
    if (!node) return;
    if (node.key.toLowerCase().includes(keyword) ||
        (node.data.muscle || '').toLowerCase().includes(keyword))
      results.push(node.data);
    this._dfs(node.left,  keyword, results);
    this._dfs(node.right, keyword, results);
  }
}

// 검색 로직: 정확 일치 → 이진탐색, 부분 일치 → DFS
const exact      = exerciseBST.search(q);        // 이진 탐색
const dfsResults = exerciseBST.dfsSearch(q);     // DFS
```

#### [4] FIFO 큐 스케줄링 (기구 예약) — `makeReservation()`, `completeUse()`

```javascript
// Enqueue: 대기열 끝에 추가
function makeReservation() {
  const entry = { userId: MY_ID, name: currentUser.name, sets, est, at };
  if (!d.currentUser) {
    queueState[eq].currentUser = entry;   // 빈 기구면 즉시 배정
    queueState[eq].status = 'in_use';
  } else {
    queueState[eq].queue.push(entry);     // 대기열 끝에 enqueue (FIFO)
  }
  saveQueue(eq);
}

// Dequeue: 선착순으로 다음 대기자 처리
function completeUse(eq) {
  if (queueState[eq].queue.length > 0) {
    const next = queueState[eq].queue.shift();   // FIFO: 가장 먼저 기다린 사람
    queueState[eq].currentUser = next;
  } else {
    queueState[eq].currentUser = null;
    queueState[eq].status = 'available';
  }
  saveQueue(eq);
}
```

---

## 6. 최종 완성 결과 (화면 캡처)

> 실행: https://rladgx.github.io/A-Final

### 홈 화면 · 캘린더
![홈](screenshots/home.png)

### 루틴 추천 (그리디 + 위상정렬)
![루틴추천](screenshots/recommend.png)

### 기구 예약 (FIFO 큐)
![기구예약](screenshots/reservation.png)

### 운동 찾아보기 (BST + DFS)
![운동찾기](screenshots/find.png)

### 성장 분석 (힙 정렬 Top5)
![분석](screenshots/stats.png)

---

## 7. Lessons Learned

### 202439731 김동현 (루틴 추천 · 전체 UI)

| | |
|--|--|
| **Plus** | 그리디와 위상정렬을 단순히 이론으로만 알던 것을 실제 "제한된 시간에 어떤 운동을 골라야 하는가"와 "어떤 운동을 먼저 해야 하는가"라는 현실 문제와 직접 연결해 구현해보면서 알고리즘이 단순한 코딩 문제가 아닌 실생활 문제 해결 도구임을 체감할 수 있었다. |
| **Minus** | 위상정렬의 선행관계(deps) 그래프를 하드코딩으로 작성해야 했는데, 운동 전문가 지식 없이 의존 관계를 직접 정의하는 데 한계가 있었다. 실제 서비스라면 운동 전문가와 협업하거나 데이터 기반으로 관계를 학습하는 방식이 필요할 것이다. |
| **Interesting** | 그리디로 선발된 운동 집합이 위상정렬 후 완전히 다른 순서로 재배열되는 것을 보며, "최적 선택"과 "올바른 순서"는 별개의 문제임을 깨달았다. 두 알고리즘이 서로 다른 차원의 문제를 해결한다는 점이 흥미로웠다. |

---

### 202439741 남현욱 (기구 예약 · 힙 정렬)

| | |
|--|--|
| **Plus** | Firebase 실시간 데이터베이스와 FIFO 큐를 결합해 여러 사용자가 동시에 접속해도 대기 순서가 정확히 유지되는 실시간 대기열 시스템을 구현할 수 있었다. 강의에서 배운 큐 자료구조가 실제 헬스장 대기 문제와 이렇게 자연스럽게 맞아떨어진다는 점이 만족스러웠다. |
| **Minus** | Max-Heap을 직접 구현하는 과정에서 `heapify-down` 로직(왼쪽·오른쪽 자식 중 더 큰 쪽과 교환)의 인덱스 계산에서 버그가 생겨 디버깅에 예상보다 많은 시간을 소비했다. 개념을 아는 것과 직접 구현하는 것 사이에 큰 간극이 있음을 느꼈다. |
| **Interesting** | 큐(선착순 공정성)와 힙(우선순위 기반 효율성)이 모두 "대기" 문제를 다루지만 접근 방식이 정반대라는 점이 흥미로웠다. 기구 예약에는 공정성이 중요해 FIFO 큐가 적합하고, 운동 빈도 Top5 추출에는 효율적인 최대값 추출이 중요해 힙이 적합하다는 것을 직접 적용하며 알고리즘 선택의 중요성을 배웠다. |

---

### 202439742 박민석 (운동 찾아보기 · 데이터 수집)

| | |
|--|--|
| **Plus** | BST에 운동 데이터를 삽입하면 중위 순회만으로 가나다순 정렬된 결과를 얻을 수 있어, 별도의 정렬 함수 없이 자동 정렬 목록을 구현할 수 있었다. 자료구조 자체가 정렬 속성을 내포한다는 점에서 설계의 우아함을 느꼈다. |
| **Minus** | 한국어 문자열을 키로 사용하는 BST는 데이터 삽입 순서에 따라 트리가 편향될 수 있어 최악의 경우 O(N) 검색이 발생한다. AVL 트리나 Red-Black 트리 같은 자가 균형 BST를 적용했으면 더 완성도 있는 구현이 됐을 것이다. |
| **Interesting** | 같은 "검색"이라는 목적에 대해 이진 탐색(정확히 아는 이름)과 DFS(키워드로 탐색)를 상황에 따라 다르게 적용했는데, 사용자가 검색어를 입력했을 때 두 알고리즘이 순차적으로 실행되며 서로를 보완하는 구조가 실제 검색 엔진의 동작 방식과 유사하다는 것을 깨달았다. |

---

## 외부 연동

- **Firebase Realtime Database** (a-final-f8b6f): 실시간 대기열 동기화, 운동 기록 저장
- **식품안전처 식품영양성분 OpenAPI** (data.go.kr): 식품 실시간 검색
- **GitHub Pages**: 모바일 웹 배포
