Импорт задачи из polygon'а

# Introduction #

Основные команды:

please import polygon package @path\_to\_zip\_archive\_with\_problem

please import polygon contest @path\_to\_zip\_archive\_with\_contest

Автору сего труда поныне ~~неизвестно, как работает и работает ли следующая функция, поскольку она связана с http://codecenter.sgu.ru:8080/polygon, а сайт этот не загружается. Макс знает, как это работет, но молчит. Может быть, ты затестишь это, юзер?~~ известно, в текущей версии работает фигово, однако должна быстро фикситься. Может быть, ты пофиксишь это, разработчик?

please import polygon problem @problem\_name from @contest\_id

# Details #

## Импорт задачи из полигона ##

Example:
> please import polygon package olymp/polygon/memory.zip

Создает в текущей директории папку с задачей, имя папки соответствует названию задачи. Если такая папка уже существует, то выводится "Import error: @problem\_name already exists" и работа please завершается.

Импортирует TL, ML, input, output, тэги, тесты ручные, генераторы, мультигенераторы, не импортирует группы тестов, так как они не поддерживаются в please.

Импортирует условия на всех языках, в default.package прописывает русское условие (russian), если оно есть, иначе английское (english), если оно есть, иначе любое другое. Если в задаче _внезапно_ отсутствуют условия, условия берутся по умолчанию и выводится "There is no statements in problem, please used default statements!"

В текущей версии не поддерживает импорт задач с изображениями.

Копирует ресурсы к решению, чекер, валидатор, генераторы в корневую папку задачи.

Импортирует решения с вердиктом Check Failed или Rejuected, но expected\_verdicts и possible\_verdicts не отражают того, что хотел сказать про решения автор. В текущем формате please невозможно задать необходимость хотя бы одного не OK'а. Вердикт тоже CF тоже пока не поддерживается.
| Polygon | expected\_verdicts | possible\_verdicts |
|:--------|:-------------------|:-------------------|
| 'main' | ['OK'] | [.md](.md) |
| 'accepted' | ['OK'] | [.md](.md) |
| 'memory-limit-exceeded' | ['ML'] | ['OK', 'WA', 'TL', 'RE', 'PE'] |
| 'time-limit-exceeded' | ['TL'] | ['OK', 'WA', 'ML', 'RE', 'PE'] |
| 'wrong-answer': (['WA'] | ['OK', 'ML', 'TL', 'RE', 'PE'] |
| 'presentation-error' | ['PE'] | ['OK', 'WA', 'ML', 'TL', 'RE'] |
| 'rejected' | [.md](.md) | ['OK', 'WA', 'ML', 'TL', 'RE', 'PE'] |
| 'failed' | [.md](.md) | ['OK', 'WA', 'ML', 'TL', 'RE', 'PE'] |


~~Неизвестно, как работает программа при количестве ручных тестов или претестов большем или равном 100, но едва ли такая ситуация когда-нибудь случится.~~
Известно, все хорошо работает.

При успешном распаковывании архива выводится "Problem @problem\_name has been being created successfully"

При успешном завершении выводится "Imported polygon package @package\_name"

# Импорт контеста #

Example:
> please import polygon contest home/user/contest-218.zip

В текущей директории создает конфигурационный файл с контестом и папки со всеми задачами. Если задача с именем какой-нибудь из задач контеста уже существует, то она пропускается и подключается к контесту. Импорт задач работает как описано выше. В случае существования контеста работа прерывается и выводится "Import error: @problem\_name already exists"