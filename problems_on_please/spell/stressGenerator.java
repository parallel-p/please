import java.util.Random;
import java.util.Scanner;


public class stressGenerator {
	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);
		long rSeed = in.nextLong();
		Random r = new Random();
		r.setSeed(rSeed);
		int l = r.nextInt(100000);
		for (int i = 0; i < l; i++) {
			int wordLength = r.nextInt(9)+1;
			String s = "";
			for(int j = 0; j < wordLength; j++){
				char c = (char) (r.nextInt(50) + 'A');
				s+=c;
			}
			System.out.print(s + " ");
		}
		System.out.println();
		in.close();
	}
}
