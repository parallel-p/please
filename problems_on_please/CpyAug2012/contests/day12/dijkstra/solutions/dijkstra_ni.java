import java.io.*;
import java.util.*;

public class dijkstra_ni {

	MyScanner in;
	PrintWriter out;
	static int INF = 1000000000;
	/**
	 * @param args
	 */
	int n;
	int s, f;
	int ma[][];
	void load() {
		n = in.nextInt();
		s = in.nextInt();
		f = in.nextInt();
		ma = new int[n][n];
		int i, j;
		for (i = 0; i < n; i++)
			for (j = 0; j < n; j++)
				ma[i][j] = in.nextInt();
	}

	void solve() {
		int d[] = new int[n];
		int use[] = new int[n];
		Arrays.fill(d, INF);
		Arrays.fill(use, 0);
		--s;
		--f;
		d[s] = 0;
		int i;
		while (true) {
			int k = -1;
			for (i = 0; i < n; i++)
				if (use[i] == 0 && (k == -1 || d[k] > d[i]))
					k = i;
			if (k == -1) break;
			use[k] = 1;
			for (i = 0; i < n; i++)
				if (ma[k][i] != -1 && d[i] > d[k] + ma[k][i])
					d[i] = d[k] + ma[k][i];
		}
		if (d[f] == INF) out.print("-1");
		else out.print(d[f]);
	}

	public void run() {
		try {
			in = new MyScanner("dijkstra.in");
			out = new PrintWriter("dijkstra.out");
			load();
			solve();
			out.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new dijkstra_ni().run();
	}
	
	class MyScanner {
		BufferedReader br;
		StringTokenizer st;
		
		MyScanner(String file) {
			try {
				br = new BufferedReader(new FileReader(new File(file)));
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		
		String nextToken() {
			while (st == null || (!st.hasMoreTokens())) {
				try {
					st = new StringTokenizer(br.readLine());
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			}
			return st.nextToken();
		}

		int nextInt() {
			return Integer.parseInt(nextToken());
		}

		double nextDouble() {
			return Double.parseDouble(nextToken());
		}

	}

}
