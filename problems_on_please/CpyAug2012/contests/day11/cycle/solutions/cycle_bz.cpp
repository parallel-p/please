#include <cstdio>
#include <cstdlib>
#include <vector>

typedef std::vector <int> vi;
typedef vi::iterator viit;

enum colors {
	WHITE, BLACK, GRAY
};

const int MAXN = 100000;

vi path;
vi v[MAXN];
colors color[MAXN];

void die(int last) {
	printf("YES\n");
        int i = path.size() - 1;
        int len = 1;
        while (path[i] != last)
        {
            --i;
            ++len;
        }
        printf("%d\n", len);
        for (; i < path.size(); ++i)
            printf("%d ", path[i] + 1);
        printf("\n");
	exit(0);
}

void dfs(int k) {
	color[k] = GRAY;

	for (viit it = v[k].begin(); it != v[k].end(); it ++) 
		if (color[*it] == GRAY)
			die(*it);
		else if (color[*it] == WHITE)
                {
                        path.push_back(*it);
			dfs(*it);
                        path.pop_back();
                }

	color[k] = BLACK;
}

int main () {
	freopen("cycle.in", "r", stdin);
	freopen("cycle.out", "w", stdout);

	int n, m, x, y;

	scanf("%d%d", &n, &m);

	for (int i = 0; i < n; i ++)
		color[i] = WHITE;

	for (int i = 0; i < m; i ++) {
		scanf("%d%d", &x, &y);
		v[x - 1].push_back(y - 1);
	}

	for (int i = 0; i < n; i ++)
        {
		if (color[i] == WHITE) 
                {
                        path.clear();
                        path.push_back(i);
			dfs(i);
                }
        }

	printf("NO\n");
	return 0;
}
