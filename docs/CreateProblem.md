## Создание задачи ##
# Автоопределитель ошибок #
Если написать какую-либо команду с одной ошибкой, программа самостоятельно догадается, что за команду пытались ввести.
# Напоминание #
Прежде чем запускать:
  * generate answers
  * validate tests
  * compute TL
  * check solutions
и т.п., нужно убедиться, что тесты **_уже сгенерированы_**!


**Все действия с задачей выполняются из корня папки с задачей!**
# Создание #
Переместимся в директорию, в которой хотим создать задачу. Теперь создадим пустой макет для нашей задачи с помощью команды **please create problem PROBLEM\_NAME**.
```
~$ please create problem cubes
Untitle(INFO) [12:34:13]: Problem cubes has been being created successfully
```
Зайдём в папку с задачей и посмотрим, что внутри.
```
~$ cd cubes
~/test$ ll
drwxrwxr-x 6 dubov94 dubov94  4096 2012-01-03 12:34 ./
drwxrwxr-x 7 dubov94 dubov94  4096 2012-01-03 12:34 ../
-rw-r--r-- 1 dubov94 dubov94   133 2012-01-03 12:34 checker.cpp
-rw-rw-r-- 1 dubov94 dubov94   589 2012-01-03 12:34 default.package
drwxrwxr-x 2 dubov94 dubov94  4096 2012-01-03 12:34 .please/
drwxrwxr-x 2 dubov94 dubov94  4096 2012-01-03 12:34 solutions/
drwxrwxr-x 2 dubov94 dubov94  4096 2012-01-03 12:34 statements/
-rw-r--r-- 1 dubov94 dubov94 56061 2012-01-03 12:34 testlib.h
-rw-r--r-- 1 dubov94 dubov94 12114 2012-01-03 12:34 testlib.pas
drwxrwxr-x 2 dubov94 dubov94  4096 2012-01-03 12:34 tests/
-rw-rw-r-- 1 dubov94 dubov94     0 2012-01-03 12:34 tests.please
-rw-r--r-- 1 dubov94 dubov94    99 2012-01-03 12:34 validator.cpp
```
  * tests - папка с ручными тестами
  * solutions - папка со всеми решениями, лежит заготовка на cpp
  * statements - папка со всеми условиями, лежат три заготовки, для описания (description.ru.tex), непосредственно условий (default.ru.tex) и разбора (analysis.ru.tex). В перспективе развития please - много условий на разных языках, но пока этой возможности нет, поэтому не обращаем внимания на `*`.ru.tex
  * checker.cpp, validator.cpp - заготовки соответственно чекера и валидатора
  * .please - папка с файлом md5.config, в котором хранятся md5-суммы созданных файлов (системный файл)
  * testlib.h, testlib.pas - библиотеки, необходимые для написания чекеров, валидаторов, и т.п., см. [testlib](http://code.google.com/p/testlib/)
  * default.package - см. [конфигурирование параметров](ProblemConfig.md)
  * tests.please - см. [конфигурирование тестов](TestsConfig.md)
# После конфигурирования #
Предварительно необходимо сгенерировать тесты. Генерируются они командой **please generate tests**:
```
~/cubes$ please generate tests
cubes(INFO) [10:28:18]: Generating 19 tests series
cubes(INFO) [10:28:18]: Test #1 'tests/1' is generated
cubes(INFO) [10:28:18]: Test #2 'tests/2' is generated
cubes(INFO) [10:28:18]: Test series #1 generated
cubes(INFO) [10:28:18]: Test #3 'tests/3' is generated
cubes(INFO) [10:28:18]: Test #4 'tests/4' is generated
cubes(INFO) [10:28:18]: Test series #2 generated
cubes(INFO) [10:28:18]: Compiling generator_random.cpp
cubes(INFO) [10:28:19]: Test #5 'stdout of generator_random.cpp' is generated
cubes(INFO) [10:28:19]: Test series #3 generated
cubes(INFO) [10:28:19]: Test #6 'stdout of generator_random.cpp' is generated
cubes(INFO) [10:28:19]: Test series #4 generated
...
cubes(INFO) [10:28:21]: Test #19 'stdout of generator_random.cpp' is generated
cubes(INFO) [10:28:21]: Test series #17 generated
cubes(INFO) [10:28:21]: Compiling generator_max.cpp
cubes(INFO) [10:28:21]: Test #20 'stdout of generator_max.cpp' is generated
cubes(INFO) [10:28:21]: Test series #18 generated
cubes(INFO) [10:28:22]: Test #21 'stdout of generator_max.cpp' is generated
cubes(INFO) [10:28:22]: Test series #19 generated
cubes(INFO) [10:28:22]: Start validator on test #1
cubes(INFO) [10:28:22]: Compiling validator.cpp
cubes(INFO) [10:28:24]: Validator said OK
cubes(INFO) [10:28:24]: Start validator on test #2
cubes(INFO) [10:28:24]: Validator said OK
...
cubes(INFO) [10:28:25]: Start validator on test #20
cubes(INFO) [10:28:25]: Validator said OK
cubes(INFO) [10:28:25]: Start validator on test #21
cubes(INFO) [10:28:26]: Validator said OK
cubes(INFO) [10:28:26]: Generating answer for test #1 by solutions/solution.py
cubes(INFO) [10:28:26]: Generating answer for test #2 by solutions/solution.py
...
cubes(INFO) [10:28:35]: Generating answer for test #20 by solutions/solution.py
cubes(INFO) [10:28:36]: Generating answer for test #21 by solutions/solution.py
```
Заметим, что они заодно провалидировались и ответы к ним (по main solution) составились.
Ещё можно задать теги (**please generate tests with tag`[s]` ...**), тогда будут браться тесты только с заданными тегами. Смотрите please help.
<br><br>
Теперь у нас есть некий набор тестов, который хранится в новой папке .tests. Допустим, что мы заметили ошибку в валидаторе, и хотим заново провалидировать уже готовые тесты. Это можно сделать командой <b>please validate tests</b>:<br>
<pre><code>~/cubes$ please validate tests<br>
</code></pre>
Если что-то пойдёт не так, нас ждёт сюрприз:<br>
<pre><code>cubes(ERROR) [10:33:21]: ValidatorError: Validator executions has had RE with exit code: 3<br>
                STDOUT:<br>
FAIL Expected EOLN (stdin)<br>
</code></pre>
Также можно перегенерировать ответы с помощью <b>please generate answers</b>.<br>
<h1>Проверка решений</h1>
Допустим, что мы уже прописали в конфиге все решения, и сгенерировали все тесты. Тогда мы можем проверять различные решения, например, главное командой <b>please check main solution</b>:<br>
<pre><code>~/cubes$ please check main solution<br>
cubes(INFO) [00:47:15]: Testing solutions/solution.py on test #1<br>
cubes(INFO) [00:47:15]: Compiling checker.cpp<br>
cubes(INFO) [00:47:15]: Testing solutions/solution.py on test #2<br>
...<br>
cubes(INFO) [00:47:29]: Testing solutions/solution.py on test #21<br>
<br>
----------------------------------<br>
| Test # | solutions/solution.py |<br>
----------------------------------<br>
|      1 | OK T=0.09s RT=0.10s   |<br>
----------------------------------<br>
|      2 | OK T=0.09s RT=0.10s   |<br>
----------------------------------<br>
...<br>
----------------------------------<br>
|     21 | OK T=1.11s RT=1.12s   |<br>
----------------------------------<br>
<br>
Total:  21<br>
Failed: 0<br>
Passed: 21<br>
cubes(INFO) [00:47:29]: HTML report is generated and saved as 'report.html' in the root directory of current problem<br>
</code></pre>
Заметим, что заодно создался HTML отчёт по проведённому тестированию, включающий в себя отчёт о соответствии ожидаемым и возможным вердиктам, прописанным в соответствующем конфиге (default.package).<br>
Можно протестировать какое-нибудь конкретное командой <b>please check solution SOLUTION_PATH</b>:<br>
<pre><code>~/cubes$ please check solution solutions/solution_wrong.cpp<br>
cubes(INFO) [10:36:53]: Testing solutions/solution_wrong.cpp on test #1<br>
cubes(INFO) [10:36:53]: Compiling solutions/solution_wrong.cpp<br>
cubes(INFO) [10:36:54]: Testing solutions/solution_wrong.cpp on test #2<br>
...<br>
cubes(INFO) [10:36:57]: Testing solutions/solution_wrong.cpp on test #21<br>
cubes(ERROR) [10:36:57]: Solution has had RE with exit code: 11<br>
<br>
-----------------------------------------<br>
| Test # | solutions/solution_wrong.cpp |<br>
-----------------------------------------<br>
|      1 | OK T=0.00s RT=0.00s          |<br>
-----------------------------------------<br>
|      2 | OK T=0.00s RT=0.00s          |<br>
-----------------------------------------<br>
...<br>
-----------------------------------------<br>
|     21 | RE T=0.00s RT=0.00s          |<br>
-----------------------------------------<br>
<br>
Total:  21<br>
Failed: 5<br>
Passed: 16<br>
cubes(INFO) [10:36:58]: HTML report is generated and saved as 'report.html' in the root directory of current problem<br>
</code></pre>
Или же все вместе командой <b>please check solutions</b>.<br>
<h1>Автоконфигурирование TL</h1>
Также можно автоматически выставлять TL в конфиг: будет протестировано главное решение и прописано удвоенное максимальное время выполнения. Вывод команды <b>please compute TL</b>:<br>
<pre><code>~/cubes$ please compute TL<br>
cubes(WARNING) [10:39:08]: Remember: TL is setting by execution results of main solution, so it should be the slowest solution<br>
cubes(INFO) [10:39:08]: Testing solutions/solution.py on test #1<br>
cubes(INFO) [10:39:08]: Testing solutions/solution.py on test #2<br>
...<br>
cubes(INFO) [10:39:21]: Testing solutions/solution.py on test #21<br>
cubes(WARNING) [10:39:22]: Maximal execution time: 1.15, now TL in default.package is: 2.3<br>
<br>
</code></pre>
А в default.package теперь записано:<br>
<pre><code>...<br>
output = stdout<br>
time_limit = 2.3<br>
memory_limit = 256<br>
...<br>
</code></pre>
Ещё есть возможность записать то же самое число, но округлённое вверх. Делается это командой <b>please compute integer TL</b>. Содержимое default.package после этого:<br>
<pre><code>...<br>
output = stdout<br>
time_limit = 3<br>
memory_limit = 256<br>
...<br>
</code></pre>
<h1>Стресс-тестирование</h1>
Для того, чтобы провести стресс-тестирование, нужно выполнить следующий алгоритм.<br>
</li></ul>  1. Написать генератор, который создаёт различные тесты в зависимости от первого переданного в main значения
  1. Написать верное решение
  1. Написать любое другое решение
  1. Выполнить команду **`please stress SOLUTION [CORRECT_SOLUTION] GENERATOR`**, полагаю, переменные ясны. Если верное решение прописано как главное в конфиге задачи, параметр CORRECT\_SOLUTION можно опустить.

Пример:
```
~/cubes$ please stress solutions/solution_wrong.cpp solutions/solution.cpp generator_random.cpp
cubes(WARNING) [10:43:27]: Random number for generator is: 753588
cubes(INFO) [10:43:27]: Generating 1 tests series
cubes(INFO) [10:43:27]: Test #1 'standard generator output' is generated
cubes(INFO) [10:43:27]: Test series #1 generated
cubes(INFO) [10:43:27]: Compiling solutions/solution.cpp
cubes(INFO) [10:43:28]: Test passed
cubes(WARNING) [10:43:28]: Random number for generator is: 469681
cubes(INFO) [10:43:28]: Generating 1 tests series
cubes(INFO) [10:43:28]: Test #1 'standard generator output' is generated
cubes(INFO) [10:43:28]: Test series #1 generated
cubes(INFO) [10:43:28]: Test passed
cubes(WARNING) [10:43:34]: Random number for generator is: 951171
cubes(INFO) [10:43:34]: Generating 1 tests series
cubes(INFO) [10:43:34]: Test #1 'standard generator output' is generated
cubes(INFO) [10:43:34]: Test series #1 generated
cubes(ERROR) [10:43:34]: Run exception: solutions/solution_wrong.cpp is not OK, invoker returned RE, return code 11
cubes(ERROR) [10:43:34]: Solution solutions/solution_wrong.cpp failed to run
cubes(ERROR) [10:43:34]: Test failed
```
# Условия #
**please generate statement** создаст pdf на основе tex'овского файла условий, указанного в default.package, и тестов, помеченных тегом sample в tests.please.
# Всё сразу #
please build all <=>
  * please generate tests
  * please generate statement
  * please check solutions
# Очистить от мусора #
**please clean** удалит логи исполняемые файлы, прописанные в default.package и tests.please и pdf.