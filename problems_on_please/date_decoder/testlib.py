#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Модуль для подготовки соревнований по программированию в стиле ACM ICPC
     Автор: Олег [burunduk3] Давыдов
     Последнее изменение: 4 сентября 2010
     Находится в самом начале разработки, используйте на свой страх и риск.
"""

import sys

class Error(BaseException):
  def ensure( value, message ):
    """Статический метод, проверяющий истинность value и вызывающий исключение, если что-то оно ложно."""
    if not value:
      raise Error(message)
  def new( message ):
    """Статический метод, создающий и вызывающий исключение. Полезен, например в λ-выражениях."""
    raise Error(message)

class Locale:
  """Класс со списком сообщений."""
  FAIL_CANNOT_UNREAD = "fail: cannot unread character"
  FAIL_FLOAT_INTERVAL = "fail: number %s doesn't fit in [%f, %f]"
  FAIL_FORMAT_UNKNOWN = "fail: unknown format character: “%s”"
  FAIL_INTEGER_INTERVAL = "fail: integer %s doesn't fit in [%d, %d]" # LOL: integer %s
  FAIL_LIST = "fail: “%s” isn't a from list %s"
  FAIL_UNEXPECTED = "fail: expected “%s”, found “%s”"
  FAIL_UNEXPECTED_DATA = "fail: expected end of file, found “%s”"
  FAIL_UNEXPECTED_EOF = "fail: unexpected end of file"

class Limit:
  """Класс со списком часто используемых ограничений
     Ограничения на входные данные задаются при помощи функций,
     принимающих один параметр — собственно, значение, которое требуется проверить.
     Функция должна вернуть это значение, если оно подходит под ограничение
     или кинуть исключение testsys.Error в противном случае.
     Функция должна закладываться на то, что передаваемый ей параметр — строка.
  """
  def all():
    """Создание ограничителя, который допускает все строки"""
    return lambda value: value
  def exact( target ):
    """Создание ограничителя, проверяющего, совпадает ли строка с заданной.
       Также может использоваться для проверки одиночных символов.
    """
    target = str(target)
    return lambda value: value if target == value else Error.new(Locale.FAIL_UNEXPECTED % (target, value))
  def list( list ):
    """Создание ограничителя, проверяющего, является ли строка одной из заданного списка строк.
       Также может использоваться для проверки одиночных символов.
    """
    list = set(list)
    return lambda value: value if value in list else Error.new(LOCALE.FAIL_LIST % (value, str(list)))
  def interval( min, max ):
    """Создание ограничителя, проверяющего, лежит ли целое число в заданном диапазоне."""
    min, max = int(min), int(max)
    return lambda value: value if min <= int(value) <= max else Error.new(Locale.FAIL_INTEGER_INTERVAL % (value, min, max))
  def floatInterval( min, max ):
    """Создание ограничителя, проверяющего, лежит ли вещественное число в заданном диапазоне."""
    min, max = float(min), float(max)
    return lambda value: value if min <= float(value) <= max else Error.new(Locale.FAIL_FLOAT_INTERVAL % (value, min, max))

class Tester:
  """Класс со списком часто используемых символьных проверок. Эти проверки
     используются для разделения лексем при чтении входного файла. Технически,
     можно создавать сколь угодно сложные проверки, гарантируется, что при чтении
     одной лексемы функция будет вызвана ровно один раз на каждый символ."""
  blank = lambda ch: ch == ' ' or ch == '\n' or ch == '\r' or ch == '\t'
  digit = lambda ch: '0' <= ch <= '9'
  space = lambda ch: ch == ' '
  nonBlank = lambda ch: not Tester.blank(ch)

class NumberTester:
  def __init__( self ):
    self.minus = None
  def __call__( self, ch ):
    if self.minus is not None: return Tester.digit(ch)
    if ch == '-':
      self.minus = True
      return True
    else:
      self.minus = False
      return Tester.digit(ch)

class Stream:
  """Поток для чтения данных. Имеет встроенный буффер на один символ для упрощения обработки данных."""
  def __init__( self, handle ):
    """Конструктор."""
    self.handle, self.buffer, self.warnings = handle, None, []
  def scanBuffer( self, ensure = False ):
    """Прочитать один символ в буффер (или ничего не делать, если там уже есть). Параметр ensure кидает исключение, если не удалось прочитать."""
    if self.buffer is not None:
      return
    data = self.handle.read(1)
    self.buffer = data if data != '' else None
    Error.ensure(self.buffer != None or not ensure, Locale.FAIL_UNEXPECTED_EOF)
  def scan( self, test ):
    """Прочитать один токен с помощью тестера test: читает по символу, пока тестеру нравится."""
    result = ''
    while True:
      self.scanBuffer()
      if self.buffer is not None and test(self.buffer):
        result += self.buffer
        self.buffer = None
      else:
        break
    return result
  def readChar( self, limit = Limit.all ):
    """Прочитать один символ, проверить его принадлежность ограничению."""
    self.scanBuffer(ensure = True)
    value = self.buffer
    self.buffer = None
    return limit(value)
  def readFloat( self, limit = Limit.all ):
    """Прочитать вещественное число."""
    # TODO: А когда в этом мире будут безлимитные вещественные числа?
    return float(limit(self.scan(lambda ch: '0' <= ch <= '9' or ch in ".+-eE")))
  def readInteger( self, limit = Limit.all ):
    """Прочитать целое число."""
    return int(limit(self.scan(NumberTester())))
  def readToken( self, tester = Tester.nonBlank, limit = Limit.all ):
    """Прочитать один токен с помощью тестера, проверить его на соответствие ограничению."""
    # мой любимый метод =)
    return limit(self.scan(tester))
  def read( self, format, limits ):
    """Прочитать форматированно. Поддерживаются следующие символы формата:
         %% — прочитать символ «%»
         %d — прочитать целое число
         %f — прочитать вещественное число
         %s — прочитать токен (до пробельного символа)
       На каждый символ формата, кроме %% должно быть соответствующее ограничение в списке limits.
       Метод возвращает прочитанные значения, по одному на каждый символ формата."""
    temp, result, li = None, [], 0
    for ch in format:
      if ch != '%' and temp is None:
        self.readChar(Limit.exact(ch))
        continue
      elif temp is None:
        temp = ''
      else:
        temp += ch
        if ch == '%':
          self.readChar(Limit.exact(ch()))
        elif ch == 'd':
          result.append(self.readInteger(limits[li]))
          li += 1
          temp = None
        elif ch == 'f':
          result.append(self.readFloat(limits[li]))
          li += 1
          temp = None
        elif ch == 's':
          result.append(self.readToken(limit = limits[li]))
          li += 1
          temp = None
        else:
          raise Error(Locale.FAIL_FORMAT_UNKNOWN % ch)
    return result
  def readSpace( self ):
    return self.readChar(Limit.exact(' '))
  def readEoln( self ):
    return self.readChar(Limit.exact('\n'))
  def eof( self ):
    self.scanBuffer()
    return self.buffer is None
  def close( self ):
    """Убедиться, что дочитали до конца файла и закрыть поток."""
    self.scanBuffer()
    Error.ensure(self.buffer is None, Locale.FAIL_UNEXPECTED_DATA % self.buffer)
    for warning in self.warnings:
      print(warning)


# До этого был красивый код на питоне, а дальше следует всяческий адский ад.

class TLHStrem:
  """Класс потока, совместимый с testlib.h (http://code.google.com/p/testlib). Не рекомендуется использовать."""
  def __init__( stream ):
    self.s = stream
  def readEof( self ):
    self.s.scanBuffer()
    if self.s.buffer is not None:
      Error.new(Locale.FAIL_UNEXPECTED_DATA % self.buffer)
  def skipBlanks( self ):
    self.s.scan(Tester.blank)
  def curChar( self ):
    self.s.scanBuffer()
    return self.s.buffer
  def skipChar( self ):
    self.s.scanBuffer(ensure = True)
    self.s.buffer = None
  def nextChar( self ):
    self.s.scanBuffer(ensure = True)
    value = self.s.buffer
    self.s.buffer = None
    return value
  def readSpace( self ):
    return self.s.readChar(Limit.exact(' '))
  def readEoln( self ):
    return self.s.readChar(Limit.exact('\n'))
  def unreadChar( self, ch ):
    Error.ensure(self.s.buffer is None, Locale.FAIL_CANNOT_UNREAD)
    self.s.buffer = ch
  def eof( self ):
    self.s.scanBuffer()
    return self.buffer == None
  def seekEof( self ):
    self.s.skipBlanks()
    return self.eof()
  def eoln( self ):
    self.s.scanBuffer()
    return self.s.buffer is not None and self.s.buffer == '\n'
  def seekEoln( self ):
    self.s.scan(lambda ch: ch == ' ' or ch == '\t')
    return eoln()
  def nextLine( self ):
    self.s.scan(lambda ch: ch != '\n')
    self.s.readEoln()
  def readWord( self, limit = Limit.all, name = '' ):
    return self.s.readToken(limit, name)
  def readToken( self, limit = Limit.all, name = '' ):
    # TODO: Я не понимаю пока что, куда воткнуть этот дурацкий name
    return limit(self.s.scan(Tester.nonBlank))
  def readLong( self, limit = Limit.interval(-2**63, 2**63 - 1) ):
    return self.s.readInteger(limit)
  def readInt( self, limit = Limit.interval(-2**31, 2**31 - 1) ):
    return self.s.readInteger(limit)
  def readDouble( self, limit = Limit.all ):
    return self.s.readFloat(limit)
  def readReal( self, limit = Limit.all ):
    return self.s.readFloat(limit)
  def readString( self, limit = Limit.all ):
    return self.s.readLine()
  def readLine( self, limit = Limit.all ):
    value = self.s.scan(lambda ch: ch != '\n')
    if self.s.eoln():
      self.s.nextLine()
    return limit(value)

def validator( validate ):
  validate(Stream(sys.stdin))

