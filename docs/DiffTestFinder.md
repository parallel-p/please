Находить тесты, сгенерированные генератором по диффу

# Introduction #

См. subj

# Details #

Класс для определения по диффу папки с задачей, что является тестами

```
class DiffTestFinder:
    def __init__(self, execute_dir, mask=None, exclude=None)
    #mask and exclude is a string, execute_dir - string, directory, in which generator worked
    def tests(self, diff, stdout=None):
        #diff is a list of files, stdout - file of redirected stdout of generator, returns names of test files
        if exclude defined:
	    diff = diff / <set of files, which matchs exclude>
        if mask defined:
            diff = diff / <set of files, which not matchs mask>
        if diff is empty and stdout is not None:
            return [stdout]
        else:
            return diff
```


Перевод с псевдопитона на русский:

Конструктор принимает опционально маску файлов, являющихся тестами (mask), маску файлов, не являющихся тестами (exclude, исключение) и директорию, в которой запускался генератор (execute\_dir). Все имена файлов для сравнения с масками переводятся в относительные для execute\_dir пути. Если файл соответствует сразу двум маскам, то исключение приоритетно.

tests принимает diff и stdout (файл с перенаправденным стандартным выводом генератора), исключает оттуда исключения.

Если есть маска тестов, исключает файлы, ей не подходящие.

Если в результате файлов не осталось и задан stdout, возвращает список из одного элемента: stdout, иначе возвращет оставшиеся файлы.