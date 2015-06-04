#python3
def programe():
    into = open("floyd.in", "r")
    N = int(into.readline().strip())
    out = open("floyd.out", "w")
    matrix = [[] for i in range(N)]
    for i in range(N):
        matrix[i] = list(map(int, into.readline().split()))
    for k in range(N):
        for i in range(N):
            for j in range(N):
                matrix[i][j] = min(matrix[i][k] + matrix[k][j], matrix[i][j])
    for i in range(N):
        for j in range(N):
            out.write(str(matrix[i][j]) + " ")
        out.write("\n")
programe()