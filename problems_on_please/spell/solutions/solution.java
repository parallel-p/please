import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashSet;
import java.util.StringTokenizer;



public class solution {
	public static void main(String[] args) throws IOException {
		BufferedReader inn = new BufferedReader(new FileReader("spell.in"));
		PrintWriter out = new PrintWriter(new File("spell.out"));
		StringTokenizer in = new StringTokenizer(inn.readLine());
		HashSet<String> differentWords = new HashSet<String>();
		while(in.hasMoreTokens()){
			differentWords.add(in.nextToken());
		}
		
		out.println(differentWords.size());
		out.close();
		inn.close();
	}
}
