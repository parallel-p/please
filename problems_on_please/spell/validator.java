import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashSet;
import java.util.StringTokenizer;



public class validator {
	public static void main(String[] args) throws IOException {
		BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
		String s = in.readLine();
		
		if(s.length() > 1000000){
			System.exit(1); // too many chars
		}
		
		if(s.split(" ").length > 100000){
			System.exit(2); // too many words
		}
		in.close();
	}
}
