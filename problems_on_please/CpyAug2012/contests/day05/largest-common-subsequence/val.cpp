#include "testlib.h"

/*
� ������ ������ �������� ����� �������� ����� $N$~--- ����� ������ ������������������ ($1 \le N \le 1000$).

�� ������ ������ �������� ����� ������ ������������������ (����� ������)~--- ����� �����, ��
������������� 10\,000 �� ������.

� ������� ������ �������� ����� $M$~--- ����� ������ ������������������ ($1 \le M \le 1000$).

� ��������� ������ ��������
����� ������ ������������������ (����� ������)~--- ����� �����, �� ������������� 10\,000 �� ������.
*/
using namespace std;

int main()
{
    registerValidation();

    for (int j = 0; j < 2; ++j) {
        int n = inf.readInt(1, 1000);
        inf.readEoln();

        for (int i = 0; i < n; ++i)
        {
            inf.readInt(-10000, 10000);
            if (i < n - 1) {
                inf.readSpace();
            } else {
                inf.readEoln();
            }
        }
    }

    inf.readEof();
    return 0;
}
