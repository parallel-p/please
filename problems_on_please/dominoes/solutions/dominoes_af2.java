import java.io.*;
import java.math.*;
import java.util.*;

public class dominoes_af2 implements Runnable {
	public static void main(String[] args) {
		new Thread(new dominoes_af2()).start();
	}

	BufferedReader br;
	StringTokenizer st;
	PrintWriter out;

	public void run() {
		try {
			br = new BufferedReader(new FileReader("dominoes.in"));
			out = new PrintWriter("dominoes.out");
			solve();
			out.close();
		} catch (Throwable e) {
			e.printStackTrace();
			System.exit(-1);
		}
	}

	String nextToken() {
		while (st == null || !st.hasMoreElements()) {
			try {
				st = new StringTokenizer(br.readLine());
			} catch (Exception e) {
				throw new Error("Enexpected end of file");
			}
		}
		return st.nextToken();
	}

	void myAssert(boolean e, String msg) {
		if (!e) {
			throw new Error(msg);
		}
	}

	int nextInt() {
		return Integer.parseInt(nextToken());
	}

	long nextLong() {
		return Long.parseLong(nextToken());
	}

	double nextDouble() {
		return Double.parseDouble(nextToken());
	}

	void solve() throws IOException {
		int n = nextInt();
		int m = nextInt();
		int a = nextInt();
		int b = nextInt();
		char[][] tab = new char[n][];
		for (int i = 0; i < n; ++i) {
			tab[i] = nextToken().toCharArray();
		}
		int total = 0;
		for (int i = 0; i < n; ++i) {
			for (int j = 0; j < m; ++j) {
				if (tab[i][j] == '*') ++total;
			}
		}
		if (2 * b <= a) {
			out.println(total * b);
		} else {
			int[][] nm = new int[n][m];
			int[] c = {0, 0};
			for (int i = 0; i < n; ++i) {
				for (int j = 0; j < m; ++j) {
					if (tab[i][j] == '*') {
						nm[i][j] = c[(i + j) % 2]++; 
					}
				}
			}
			g = new ArrayList[c[0]];
			for (int i = 0; i < g.length; ++i) g[i] = new ArrayList<Integer>();
			for (int i = 0; i < n; ++i) {
				for (int j = 0; j < m; ++j) {
					if (((i + j) % 2 == 0) && tab[i][j] == '*') {
						if (i > 0 && tab[i - 1][j] == '*') {
							g[nm[i][j]].add(nm[i - 1][j]);
						}
						if (j > 0 && tab[i][j - 1] == '*') {
							g[nm[i][j]].add(nm[i][j - 1]);
						}
						if (i < n - 1 && tab[i + 1][j] == '*') {
							g[nm[i][j]].add(nm[i + 1][j]);
						}
						if (j < m - 1 && tab[i][j + 1] == '*') {
							g[nm[i][j]].add(nm[i][j + 1]);
						}
					}
				}
			}
			
			long ans = maxMatching(g, c[1]);
			
			out.println(a * ans + b * (total - 2 * ans));
		}
	}
	
	ArrayList<Edge>[] G;
	ArrayList<Integer>[] g;
	
	long maxMatching(ArrayList<Integer>[] g, int m) {
		int n = g.length;
		G = new ArrayList[1 + n + m + 1];
		for (int i = 0; i < G.length; ++i) G[i] = new ArrayList<Edge>();
		for (int i = 0; i < n; ++i) {
			addEdge(0, i + 1);
		}
		for (int i = 0; i < m; ++i) {
			addEdge(i + n + 1, G.length - 1);
		}
		for (int i = 0; i < n; ++i) {
			for (int j : g[i]) {
				addEdge(i + 1, j + 1 + n);
			}
		}
		return maxFlow(0, G.length - 1);
	}
	
	void addEdge(int a, int b) {
		Edge ea = new Edge(b, 1);
		Edge eb = new Edge(a, 0);
		ea.r = eb;
		eb.r = ea;
		G[a].add(ea);
		G[b].add(eb);
	}
	
	long maxFlow(int s, int t) {
		long ans = 0;
		int[] rp = new int[G.length];
		while (true) {
			Arrays.fill(rp, -1);
			ArrayList<Edge>[] bG = bfs(s, t);
			if (bG == null) break;
			int[] cnt = new int[bG.length];
			while (true) {
				long fl = sift(bG, cnt, 0, T, INF);
				ans += fl;
				if (fl == 0) break;
			}
		}
		return ans;
	}

	long sift(ArrayList<Edge>[] G, int[] cnt, int s, int t, long mf) {
		if (s == t)	return mf;
		for (; cnt[s] < G[s].size(); ++cnt[s]) {
			Edge e = G[s].get(cnt[s]);
			if (e.c == 0) continue;
			long f = sift(G, cnt, e.j, t, Math.min(mf, e.c));
			if (f > 0) {
				e.c -= f;
				e.f += f;
				e.r.c -= f;
				e.r.f += f;
				e.r.r.c += f;
				e.r.r.f -= f;
				return f;
			}
		}
		return 0;
	}

	final long INF = Long.MAX_VALUE / 4;

	int T = 0;
	boolean[] u;
	int[] Q, num;
	
	ArrayList<Edge>[] bfs(int s, int t) {
		int p = 1;
		while (p <= G.length) p <<= 1;
		if (Q == null) {
			Q = new int[p];
		}
		int m = p - 1;
		if (u == null) {
			u = new boolean[p];
		} else {
			Arrays.fill(u, false);
		}
		int head = 0;
		int tail = 1;
		Q[0] = s;
		u[0] = true;
		if (num == null) {
			num = new int[G.length];
		}
		
		Arrays.fill(num, -1);
		num[s] = 0;
		ArrayList<Edge>[] ans =	new ArrayList[G.length];
		int tn = 1;
		bfs:
		while (head != tail) {
			int x = Q[head];
			ArrayList<Edge> c = ans[num[x]] = new ArrayList<Edge>();
			head = (head + 1) & m;
			for (Edge e : G[x]) {
				if (e.c > 0 && !u[e.j]) {
					Q[tail] = e.j;
					u[e.j] = true;
					tail = (tail + 1) & m;
					Edge te = new Edge(tn, e.c);
					te.r = e;
					c.add(te);
					num[e.j] = tn++;
					//if (e.j == t) break bfs;
				}
			}
		}
		if (num[t] < 0)	return null;
		T = num[t];
		return Arrays.copyOf(ans, tn);
	}

	public class Edge {
		int j;
		long c, f;
		Edge r;

		public Edge(int j, long c) {
			this.j = j;
			this.c = c;
			this.f = 0;
		}

		public String toString() {
			return "j = " + j + " c = " + c + " f = " + f;
		}

	}
	
}
