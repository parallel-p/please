#python3
def programe():
    into = open("distance.in", "r")
    N, M = list(map(int, into.readline().split()))
    S, F = list(map(int, into.readline().split()))
    out = open("distance.out", "w")
    array = [[] for i in range(N)]
    dist = [10 ** 9 for i in range(N)]
    dist[S - 1] = 0
    used = [-1 for i in range(N)]
    prev = [-1 for i in range(N)]
    for i in range(M):
        a, b, c = list(map(int, into.readline().split()))
        array[a - 1] += [(b - 1, c)]
        array[b - 1] += [(a - 1, c)]

    for i in range(N):
        mini = 10 ** 8
        idi = -1
        for j in range(N):
            if mini > dist[j] and used[j] == -1:
                mini = dist[j]
                idi = j
        if idi == -1:
            break
        used[idi] = 1
        dist[idi] = mini
        for v in array[idi]:
            if dist[v[0]] > dist[idi] + v[1]:
                dist[v[0]] = dist[idi] + v[1]
                prev[v[0]] = idi
    if dist[F - 1] != 10 ** 9:
        out.write(str(dist[F - 1]) + "\n")
        i = F - 1
        answer = []
        k = 0
        while prev[i] != -1:
            answer += [i + 1]
            i = prev[i]
            k += 1
        answer += [S]
        for i in range(k, -1, -1):
            out.write(str(answer[i]) + " ")
    else:
        out.write("-1")
programe()