import java.io.*;
import java.math.*;
import java.util.*;

public class dominoes_af1 implements Runnable {
	public static void main(String[] args) {
		new Thread(new dominoes_af1()).start();
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
			u = new int[c[0]];
			p = new int[c[1]];
			Arrays.fill(p, -1);
			v = new boolean[c[0]];
			for (int i = 0; i < c[0]; ++i) {
				for (int j : g[i]) {
					if (p[j] == -1) {
						p[j] = i;
						v[i] = true;
						break;
					}
				}
			}
			for (int i = 0; i < c[0]; ++i) {
				++color;
				if (v[i]) continue;
				dfs(i);
			}
			int ans = 0;
			for (int i = 0; i < c[0]; ++i) {
				if (v[i]) ++ans;
			}
			System.out.println(total + " " + ans);
			out.println(a * ans + b * (total - 2 * ans));
		}
	}
	ArrayList<Integer>[] g;
	int[] p;
	boolean[] v;
	int[] u;
	
	int color = 0;
	
	boolean dfs(int i) {
		u[i] = color;
		for (int j : g[i]) {
			if (p[j] == -1 || u[p[j]] != color && dfs(p[j])) {
				p[j] = i;
				v[i] = true;
				return true;
			}
		}
		return false;
	}
}
