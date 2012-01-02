import java.io.PrintWriter;

class NotGen
{
}

public class Gen
{
    class NotGen2
    {
    }

    public static void main(String[] args) throws Exception
    {
        Integer idx = 1;
        for(String s : args) {
            PrintWriter out = new PrintWriter(idx.toString());
            out.write(s + "\n");
            out.close();
            ++idx;
        }
    }
}

