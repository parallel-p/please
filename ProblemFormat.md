# О формате #

Философия:
  * `please` работает с задачами только в этом формате;
  * из многих имеющихся форматов в этот легко импортировать;
  * во многие имеющиеся форматы из этого легко экспортировать; (при этом можно экспортировать только в нередактируемый (не удобно редактируемый) вид)

Формат относительно гибкий, охватывает разумно широкий класс задач по информатике.

# Конвенции #

  * .please — кажется, что лучше все сгенерированное и временное класть в одну папочку, чтобы не было много левых папок;
  * названия файлов состоят из латинских букв, цифр, знаков подчеркивания и точек; названия **регистро-независимы** (please громко ругается!! если есть заглавные буквы не на Java и матерится, если есть два файла, которые отличаются только регистром);
  * языки обозначаются их кодами [ISO\_639-1](http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes);
  * в этом тексте <font color='red'>красным цветом</font> выделены обязательные файлы (в каталоге) и строчки (в файле);

Расширения (суффиксы) названий файлов:
  * `*.pas, *.pp` — исходные коды на Free Pascal;
  * `*.dpr` — исходные коды на Free Pascal (delphi???);
  * `*.c` — исходные коды на C;
  * `*.cpp, *.c++` — исходные коды на C++;
  * `*.java` — исходные коды на Java;
  * `*.cs` — исходные коды на C#;
  * `*.py` — исходные коды на Python;

# Структура каталога #
(для задачи стандартного типа)

<font color='gray'><code>.please/</code></font> — генерируемый каталог с временными и сгенерированными файлами;<br />
<font color='red'><code>statements/</code></font><br />
<font color='black'><code>statements/pictures/</code></font><br />
<font color='black'><code>statements/include/</code></font><br />
<font color='red'><code>statements/default.{language}.tex</code></font><br />
<font color='black'><code>statements/{modification}.{language}.tex</code></font><br />
<font color='red'><code>solutions/</code></font><br />
<font color='black'><code>solutions/problemName_author.*</code></font><br />
<font color='black'><code>solutions/problemName_author_description.*</code></font><br />
<font color='red'><code>tests/</code></font><br />
<font color='red'><code>tests/generate.please</code></font><br />
<font color='black'><code>tests/check.*</code></font> (или `Check.java` с заглавной буквы)<br />
<font color='black'><code>tests/validate.*</code></font> (или `Validate.java` с заглавной буквы)<br />
<font color='red'><code>default.package</code></font><br />
<font color='black'><code>{modification}.package</code></font><br />
<font color='red'><code>description.{language}.tex</code></font><br />
<font color='black'><code>description_{modification}.{language}.tex</code></font><br />
<font color='gray'><code>.fingerprint</code></font><br />

# Файл `default.package` #

<font color='red'><code>please_version=0.1</code></font><br />
`tags={tag1}, {tag2}, ..., {tagN}` — смотри [Tags](Tags.md)<br />
`type={|output_only}`<br />
`input={filename.ext|stdin}`<br />
`output={filename.ext|stdout}`<br />
`time_limit={<число>s|<число>ms}`<br />
`memory_limit={<число>Mb|<число>Kb}`<br />
`check={filename.ext|standard (?)}`<br />
`validate={filename.ext|standard (?)}`<br />

# Файл `generate.please` #

```
# comment
[meta1=a,b meta2=c meta3+=d]
    command parameters
    source/executable parameters
    [group]
        command1
        command2 parameters
    [meta4=value]
        another-command parameters
```

## Команды ##
  * `echo param1 param2` - вывести параметры через пробел, результат является тестом
  * `echo "some  string"` - вывести текст в качестве теста
  * `call source/executable parameters` - запустить файл с параметрами (если задан исходник - скомпилировать)
  * `extract src dst` - распаковать файл(ы)
  * `shell script-file parameters` - запустить скрипт (shell/cmd)
  * `split source-file separator` - разделить исходный файл, сгенерировав из него тесты, по умолчанию сепаратор - перевод строки

## Параметры ##
  * `tags=(+=)sample,manual,...`
  * `input={|file mask|stdout|none}`
  * `output={|file mask|stdout|none}`
  * `stdout` - то же что `input=stdout`
  * `group` - сгруппировать

# Файлы `description*.tex` #

<font color='red'>
{описание условия}<br />
{описание решения}<br>
</font>