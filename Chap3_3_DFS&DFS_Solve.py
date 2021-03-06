"""
이것이 코딩 테스트다 2021 강의 몰아보기
2021.04.16

Chapter 3. DFS & BFS

"""



"""
# 음료수 얼려 먹기 : 문제 설명
n * m 크기의 얼음 틀이 있다.
구멍이 뚫려 있는 부분은 0, 칸막이가 존재하는 부분은 1로 표시된다.
구멍이 뚫려 있는 부분끼리 상, 하, 좌, 우로 붙어있는 경우 서로 연결된 것으로 간주한다.
얼음 틀의 모양이 주어졌을 때 생성되는 총 아이스크림의 개수를 구하는 프로그램을 작성하시오.

ex)
0 0 1 1 0
0 0 0 1 1
1 1 1 1 1
0 0 0 0 0
위와 같은 경우에는 아이스크림이 총 3개 생성된다.

** 문제 해결 아이디어
 1. 특정한 지점의 주변 상, 하, 좌, 우를 살펴본 뒤에 주변 지점 중에서 값이 '0'이면서
    아직 방문하지 않은 지점이 있다면 해당 지점을 방문한다.
 2. 방문한 지점에서 다시 상, 하, 좌, 우를 살펴보면서 방문을 진행하는 과정을 반복하면,
    연결된 모든 지점을 방문할 수 있다.
 3. 모든 노드에 대하여 1 ~ 2번의 과정을 반복하며, 방문하지 않은 지점의 수를 카운트한다.


"""



# 음료수 얼려 먹기 _ 답안 예시

# DFS로 특정 노드를 방문하고 연결된 모든 노드들도 방문
def dfs(x, y) :
    # 주어진 범위를 벗어나는 경우에는 즉시 종료
    if x <= -1 or x >= n or y <= -1 or y >= m :
        return False
    # 현재 노드를 아직 방문하지 않았다면
    if graph[x][y] == 0 :
        # 해당 노드 방문 처리
        graph[x][y] = 1
        # 상, 하, 좌, 우의 위치들도 모두 재귀적으로 호출
        dfs(x - 1, y)
        dfs(x, y - 1)
        dfs(x + 1, y)
        dfs(x, y + 1)
        return True
    return False

# n, m을 공백을 기준으로 구분하여 입력 받기
n, m = map(int, input().split())

# 2차원 리스트의 맵 정보 입력 받기
graph = []
for i in range(n) :
    graph.append(list(map(int, input())))

# 모든 노드에 대하여 음료수 채우기
result = 0
for i in range(n) :
    for j in range(m) :
        # 현재 위치에서 DFS 수행
        if dfs(i, j) == True :
            result += 1

print(result)





"""
# 미로 탈출 : 문제 설명

다솔이는 n * m 크기의 직사각형 형태의 미로에 갇혔다.
미로에는 여러 마리의 괴물이 있어 이를 피해 탈출해야 한다.

다솔이의 위치는 (1, 1)이며 미로의 출구는 (n, m)의 위치에 존재하고
한 번에 한 칸씩 이동할 수 있다.
이 때 괴물이 있는 부분은 0으로 괴물이 없는 부분은 1로 표시되어 있다.
미로는 반드시 탈출할 수 있는 형태로 제시된다.

이 때 다솔이가 탈출하기 위해 움직여야 하는 최소 칸의 개수를 구하라.
칸을 셀 때는 시작 칸과 마지막 칸을 모두 포함해서 계산한다.


** 문제 해결 아이디어 :
 1. BFS는 시작 지점에서 가까운 노드부터 차례대로 그래프의 모든 노드를 탐색한다.
 2. 상, 하, 좌, 우로 연결된 모든 노드로의 거리가 1로 동일하다.
    따라서 (1, 1) 지점부터 BFS를 수행하여 모든 노드의 최단 거리 값을 기록하면 된다.
 3. 예시로 다음과 같이 3 * 3 크기의 미로가 있다고 가정해보자.
    
    1 1 0
    0 1 0
    0 1 1
    
    1) (1, 1)의 위치에서 시작한다.
    2) (1, 1) 좌표에서 상, 하, 좌, 우로 탐색을 진행하면 바로 옆 노드인 
       (1, 2) 위치의 노드를 방문하게 되고 방문하는 (1, 2) 노드의 값을 2로 바꾼다.
       
       1 2 0
       0 1 0
       0 1 1
       
    3) 다음으로는 (2, 2)를 방문하여 값을 3으로 바꾼다.
    
       1 2 0
       0 3 0
       0 1 1
       
    4) 다음으로는 (3, 2)를 방문하여 값을 4로 바꾼다.
    
       1 2 0
       0 3 0
       0 4 1
       
    5) 마지막으로 (3, 3)을 방문하여 값을 5로 바꾸고 답을 출력한다.
    
       1 2 0
       0 3 0
       0 4 5

"""



# 미로 탈출 : 답안 예시

from collections import deque
# BFS 소스코드 구현
def bfs(x, y) :
    # 큐 구현을 위해 deque 라이브러리 불러오기
    queue = deque()
    queue.append((x, y))
    # 큐가 빌 때까지 반복하기
    while queue :
        x, y = queue.popleft()
        # 현재 위치에서 4가지 방향으로의 위치 확인
        for i in range(4) :
            nx = x + dx[i]
            ny = y + dy[i]
            # 미로 찾기 공간을 벗어난 경우 무시
            if nx < 0 or nx >= n or ny < 0 or ny >= m :
                continue
            # 벽인 경우 무시
            if graph[nx][ny] == 0 :
                continue
            # 해당 노드를 처음 방문하는 경우에만 최단 거리 기록
            if graph[nx][ny] == 1 :
                graph[nx][ny] = graph[x][y] + 1
                queue.append((nx, ny))
    # 가장 오른쪽 아래까지의 최단 거리 반환
    return graph[n - 1][m - 1]

n, m = map(int, input().split())

graph = []
for i in range(n) :
    graph.append(list(map(int, input())))

# 이동할 네 가지 방향 정의 (상, 하, 좌, 우)
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

# BFS를 수행한 결과 출력
print(bfs(0, 0))




