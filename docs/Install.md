## NEW! Установка please с локальным веб-клиентом под Windows 7 ##
Для создания задач в please вам потребуются ТеХ, Delphi, Visual Studio C++, Java.
Мы предполагаем, что эти продукты у вас уже установлены.

  1. скачайте и установите python3.3 x86 с сайта python.org
  1. скачайте дистрибутив please из GitHub командой git clone https://github.com/dubov94/please.git
  1. скачайте и разархивируйте последнюю версию distribute (http://pypi.python.org/pypi/distribute)
  1. установите ее командой c:\python33\python setup.py install
  1. разархивируйте из папки please/third\_party пакет HTML и установите его командой c:\python33\python setup.py install
  1. разархивируйте из папки please/third\_party пакет colorama и установите его командой c:\python33\python setup.py install
  1. разархивируйте из папки please/third\_party пакет psutil и установите его командой c:\python33\python setup.py install
  1. установите пакет please командой c:\python33\python setup.py develop из папки please/trunk (не удаляйте эту папку после установки!)
  1. проверьте, что всё работает, запустив в консоли команду please (она лежит в c:\python33\Scripts)

Для запуска веб-версии:
  1. установите django1.5 (не младше!) с djangoproject.com
  1. установите django-mptt из /third-party/
  1. в папке please/trunk/please/web запустите команду c:\python33\python manage.py syncdb для создания базы данных. В ответ на вопрос о создании пользователя скажите no
  1. в папке please/trunk/web запустите команду c:\python33\python manage.py runserver
  1. откройте браузер и зайдите на страницу http://127.0.0.1:8000

Если что-то не заработало, напишите мне (gurovic@gmail.com).

## Linux ##
  1. скачать из раздела Downloads необходимый архив, распаковать
  1. установить пакеты python3-dev
  1. выполнить sudo python3 setup.py install

## Windows ##
  1. скачать из раздела Downloads необходимый архив, распаковать
  1. скачать и установить psutil (там есть exeшники для инсталляции, или их можно найти, сделав checkout)
  1. выполнить python setup.py install

## Текущая версия ##
  1. сделать clone
  1. установить необходимые библиотеки (см. выше Linux или Windows)
  1. установить pymox (находится в third\_party), распаковав архив и выполнив ...setup.py install
  1. установить mock (easy-install mock; только для python3.2 - в python3.3 она стала стандартной)
  1. выполнить ...setup.py develop