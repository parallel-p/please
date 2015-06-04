import java.io.*;
import java.math.*;
import java.util.*;

public class dominoes_af3 implements Runnable {
	public static void main(String[] args) {
		new Thread(new dominoes_af3()).start();
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
			
			int ans = maxMatching(g, c[1]);
			
			out.println(a * ans + b * (total - 2 * ans));
		}
	}
	
	ArrayList<Integer>[] g;
	
	int maxMatching(ArrayList<Integer>[] g, int m) {
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
		int ff = 0;
		private int[] d, q, cnt;
		int mask;
		final int INF = Integer.MAX_VALUE;
		
		int maxFlow(int s, int t) {
			int ans = 0;
			while (true) {
				Arrays.fill(d, INF);
				d[s] = 0;
				q[0] = s;
				int head = 0;
				int tail = 1;
				while (head != tail) {
					int x = q[head];
					head = (head + 1) & mask;
					for (Edge e : g[x]) {
						if (e.c == 0) continue;
						if (d[e.j] > d[x] + 1) {
							if (d[e.j] == INF) {
								q[tail] = e.j;
								tail = (tail + 1) & mask;
							}
							d[e.j] = d[x] + 1;
							if (e.j == t) break;
						}
					}
				}
				if (d[t] == INF) break;
				Arrays.fill(cnt, 0);
				
				int re = 0;
				while (true) {
					++re;
					boolean tf = sift(s, t);
					if (!tf) break;
					++ans;
				}
				System.out.println(ff++ + " " + d[t] + " " + re);
			}
			return ans;
		}
		
		boolean sift(int s, int t) {
			if (s == t) return true;
			for (; cnt[s] < g[s].size(); ++cnt[s]) {
				Edge e = g[s].get(cnt[s]);
				int v = e.j;
				if (e.c == 0 || !(d[s] + 1 == d[v] || d[s] == d[v] /*&& s < v*/)) continue;
				boolean tf = sift(v, t);
				if (tf) {
					--e.c;
					++e.r.c;
					return true;
				}
			}
			return false;
		}
		
		public Graph(int n) {
			g = new ArrayList[n];
			for (int i = 0; i < g.length; ++i) {
				g[i] = new ArrayList<Edge>();
			}
			d = new int[n];
			cnt = new int[n];
			int qs = 1;
			while (qs < n) qs <<= 1;
			q = new int[qs];
			mask = qs - 1;
		}

		void addEdge(int a, int b, int c) {
			Edge ea = new Edge(b, c);
			Edge eb = new Edge(a, 0);
			ea.r = eb;
			eb.r = ea;
			g[a].add(ea);
			g[b].add(eb);
		}
		
		class Edge {
			int j;
			int c;
			Edge r;
			
			public Edge(int j_, int c_) {
				j = j_;
				c = c_;
			}
		}
		
	}	
}
