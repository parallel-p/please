# Устройство валидатора #
  1. Считывать тест валидатор должен со стандартного потока ввода.
  1. Все, что валидатор выводит в stderr и stdout, будет выведено в консоль, в случае завершения его работы с кодом возврата отличным от нуля.

# Как пользоваться #
Чтобы запустить валидацию тестов надо:
  1. Подготовить для этого задачу:
    * Сгенерировать тесты (если этого не сделать, валидатор проверит 0 тестов. Т.е. ничего не проверит и ничего не выдаст)
    * Написать валидатор
    * Поместить валидатор в папку с задачей
    * Добавить валидатор
  1. Запустить валидацию тестов



# Команды #
## 1) Добавление валидатора ##
> ```
please set validator Validator_Path```
> Пример:
> ```
please set validator validator.java```
После чего, если путь правильный, будет выведено
> ```
TestProblem(INFO) [10:54:06]: Validator validator.java was set successfully```
В случае, если файла по заданному пути нет, вы увидите
> ```
TestProblem(ERROR) [11:23:17]: AddSourceError: There is no such file```
А если файл находится вне папки с задачей, будет выведено
> ```
TestProblem(ERROR) [11:26:49]: AddSourceError: Validator isn't in problem folder!```
## 2) Запуск валидатора ##
> ```
please validate tests```
или
> ```
please val tests
please validate```

После чего, если валидатор выходит с кодом возврата 0, вы увидите
> ```
TestProblem(INFO) [11:35:06]: Start validator on test #20
TestProblem(INFO) [11:35:06]: Compiling validator.java
TestProblem(INFO) [11:35:07]: Validator said OK```
а если валидатор выйдет с ненулевым кодом возврата, будет выведено
> ```
TestProblem(ERROR) [11:38:27]: ValidatorError: Validator executions has had RE with exit code: 1
STDERR:
some error
STDOUT:
some info```

# P.S. #
  1. По умолчанию используется валидатор, считающий любой тест корректным.
  1. Также валидацию тестов запускают команды:
    * Создание всей задачи ```
please build all```
    * Генерация тестов```
please generate tests```
    * Генерация условия```
please generate statement```(проверяет sample-тесты)