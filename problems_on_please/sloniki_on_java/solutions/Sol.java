import java.io.PrintWriter;
import java.io.File;
import java.util.Scanner;

public class Sol 
{
    public static void main(String[] args) throws Exception
    {
        Scanner in = new Scanner(new File("input.txt"));
        PrintWriter out = new PrintWriter("output.txt");
        out.write(in.nextLine() + "\n");
        out.close();
    }
}

