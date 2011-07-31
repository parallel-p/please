import java.io.*;
import java.math.*;
import java.util.*;

public class dominoes_af4 implements Runnable {
	public static void main(String[] args) {
		new Thread(new dominoes_af4()).start();
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
						if (i < n - 1 && tab[i + 1][j] == '*') {
							g[nm[i][j]].add(nm[i + 1][j]);
						}
						if (j > 0 && tab[i][j - 1] == '*') {
							g[nm[i][j]].add(nm[i][j - 1]);
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
	
	ArrayList<Integer>[] g;
	
	long maxMatching(ArrayList<Integer>[] g, int m) {
		int n = g.length;
		Graph gf = new Graph(1 + n + m + 1);
		for (int i = 0; i < n; ++i) {
			gf.addEdge(0, i + 1, 1);
		}
		for (int i = 0; i < m; ++i) {
			gf.addEdge(n + i + 1, n + m + 1, 1);
		}
		for (int i = 0; i < n; ++i) {
			for (int j : g[i]) {
				gf.addEdge(i + 1, n + j + 1, 1);
			}
		}
		return gf.maxFlow(0, n + m + 1);
	}
	
	class Graph {
		ArrayList<Edge>[] g;

		private int[] d, q, par;
		int mask;
		final int INF = Integer.MAX_VALUE;

		void bfs(int s, int t) {
			Arrays.fill(d, INF);
			d[s] = 0;
			q[0] = s;
			int head = 0;
			int tail = 1;
			while (head != tail) {
				int x = q[head];
				head = (head + 1) & mask;
				for (Edge e : g[x]) {
					if (e.r.c == 0)
						continue;
					int y = e.j;
					if (d[y] > d[x] + 1) {
						if (d[y] == INF) {
							q[tail] = y;
							tail = (tail + 1) & mask;
						}
						d[y] = d[x] + 1;
						if (y == t)
							break;
					}
				}
			}
		}

		long maxFlow(int s, int t) {
			long ans = 0;
			bfs(t, -1);
			while (d[s] < g.length) {
				ans = ans + sift(s, t, INF);
			}
			return ans;
		}

		boolean tryMore = false;

		long sift(int i, int t, long mf) {
			if (i == t) {
				return mf;
			}
			boolean hg = false;
			while (true) {
				for (Edge e : g[i]) {
					if (e.c > 0 && d[i] == d[e.j] + 1) {
						hg = true;
						long fl = sift(e.j, t, e.c < mf ? e.c : mf);
						if (tryMore) {
							break;
						}
						if (fl > 0) {
							// System.out.print((e.j + 1) + " ");
							e.c -= fl;
							e.r.c += fl;
							return fl;
						}
					}
				}
				if (tryMore) {
					tryMore = false;
					continue;
				}
				break;
			}
			if (!hg) {
				tryMore = true;
				d[i] = Integer.MAX_VALUE / 2;
				for (Edge e : g[i]) {
					if (e.c > 0) {
						d[i] = Math.min(d[i], d[e.j] + 1);
					}
				}
			}
			return 0;
		}

		public Graph(int n) {
			g = new ArrayList[n];
			for (int i = 0; i < g.length; ++i) {
				g[i] = new ArrayList<Edge>();
			}
			d = new int[n];
			par = new int[n];
			int qs = 1;
			while (qs < n)
				qs <<= 1;
			q = new int[qs];
			mask = qs - 1;
		}

		void addEdge(int a, int b, long c) {
			Edge ea = new Edge(b, c);
			Edge eb = new Edge(a, 0);
			ea.r = eb;
			eb.r = ea;
			g[a].add(ea);
			g[b].add(eb);
		}

		class Edge {
			int j;
			long c;
			Edge r;

			public Edge(int j_, long c_) {
				j = j_;
				c = c_;
			}
		}

	}
}
