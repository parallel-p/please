import java.util.Random;


public class maxTestGeneratorDifferent4 {
	public static void main(String[] args) {
		Random r = new Random();
		r.setSeed(23489007);
		for (int i = 0; i < 100000; i++) {
			int wordLength = r.nextInt(9)+1;
			String s = "";
			for(int j = 0; j < wordLength; j++){
				char c = (char) (r.nextInt(50) + 'A');
				s+=c;
			}
			System.out.print(s + " ");
		}
		System.out.println();
	}
}
