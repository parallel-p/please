import java.io.*;
import java.util.*;

public class TestsGen {
    static int testcount = 0;

    static Random random = new Random(36498732);

    static void write(int[][] tab) throws IOException {
        PrintWriter out = new PrintWriter(String.format("%d", ++testcount));
        System.out.println("Generating test #" + testcount);
        int n = tab.length;
        out.println(n);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                out.print(tab[i][j]);
                if (j < n - 1) {
                    out.print(" ");
                }
            }
            out.println();
        }
        out.close();
    }

    static void writeRand(int n, int m) throws IOException {
        int[][] tab = new int[n][n];
        for (int i = 0; i < m; i++) {
            int x = random.nextInt(n);
            int y = random.nextInt(n);
            while (x == y || tab[x][y] == 1) {
                x = random.nextInt(n);
                y = random.nextInt(n);
            }
            tab[x][y] = 1;
            tab[y][x] = 1;
        }
        write(tab);
    }

    static void writeAnti(int n, int m) throws IOException {
        int[][] tab = new int[n][n];
        for (int i = 0; i < n; i++) {
            Arrays.fill(tab[i], 1);
            tab[i][i] = 0;
        }
        for (int i = 0; i < m; i++) {
            int x = random.nextInt(n);
            int y = random.nextInt(n);
            while (x == y || tab[x][y] == 0) {
                x = random.nextInt(n);
                y = random.nextInt(n);
            }
            tab[x][y] = 0;
            tab[y][x] = 0;
        }
        write(tab);
    }

    static void writeTree(int n) throws IOException {
        int[] par = new int[n];
        ArrayList<Integer> al = new ArrayList<Integer>();
        al.add(0);
        for (int i = 1; i < n; i++) {
            par[i] = random.nextInt(i);
            al.add(i);
        }
        Collections.shuffle(al, random);
        int[][] tab = new int[n][n];
        for (int i = 1; i < n; i++) {
            int x = al.get(i);
            int y = al.get(par[i]);
            tab[x][y] = 1;
            tab[y][x] = 1;
        }
        write(tab);
    }

    static void writeCycle(int n) throws IOException {
        int[] par = new int[n];
        ArrayList<Integer> al = new ArrayList<Integer>();
        al.add(0);
        par[0] = n - 1;
        for (int i = 1; i < n; i++) {
            par[i] = i - 1;
            al.add(i);
        }
        Collections.shuffle(al, random);
        int[][] tab = new int[n][n];
        for (int i = 0; i < n; i++) {
            int x = al.get(i);
            int y = al.get(par[i]);
            tab[x][y] = 1;
            tab[y][x] = 1;
        }
        write(tab);
    }

    static void writeCyclePlus(int n) throws IOException {
        int[] par = new int[n];
        ArrayList<Integer> al = new ArrayList<Integer>();
        al.add(0);
        par[0] = n - 2;
        for (int i = 1; i < n - 1; i++) {
            par[i] = i - 1;
            al.add(i);
        }
        Collections.shuffle(al, random);
        int[][] tab = new int[n][n];
        for (int i = 0; i < n - 1; i++) {
            int x = al.get(i);
            int y = al.get(par[i]);
            tab[x][y] = 1;
            tab[y][x] = 1;
        }
        write(tab);
    }

    static void writeLine(int n) throws IOException {
        ArrayList<Integer> al = new ArrayList<Integer>();
        al.add(0);
        for (int i = 1; i < n; i++) {
            al.add(i);
        }
        Collections.shuffle(al, random);
        int[][] tab = new int[n][n];
        for (int i = 1; i < n; i++) {
            int x = al.get(i);
            int y = al.get(i - 1);
            tab[x][y] = 1;
            tab[y][x] = 1;
        }
        write(tab);
    }

    public static void main(String[] args) throws IOException {
        testcount = Integer.parseInt(args[0]);
        writeLine(1);
        writeRand(2, 0);
        writeTree(2);
        writeTree(3);
        writeAnti(3, 0);
        writeAnti(5, 0);
        writeCycle(5);
        writeCyclePlus(5);
        writeTree(5);
        writeTree(10);
        writeLine(10);
        writeCycle(10);
        writeCyclePlus(10);
        writeAnti(10, 0);
        writeRand(4, 2);
        writeRand(4, 3);
        writeRand(4, 5);
        writeLine(50);
        writeCycle(50);
        writeCyclePlus(50);
        writeLine(100);
        writeRand(100, 100);
        writeRand(100, 99);
        writeRand(100, 500);
        writeRand(100, 1000);
        writeRand(100, 2000);
        writeAnti(100, 0);
        writeAnti(100, 10);
        writeAnti(100, 100);
        writeAnti(100, 500);
        writeAnti(100, 1000);
        writeAnti(100, 2000);
        writeCycle(100);
        writeCyclePlus(100);
        writeTree(50);
        writeTree(75);
        writeTree(100);
        writeTree(100);
        writeTree(100);
    }

}
