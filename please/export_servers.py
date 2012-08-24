from .exporter.ejudge_exporter import EjudgeExporter
from .exporter.pcms2_exporter import PCMS2Exporter

servers = {
  'ejudge' : EjudgeExporter(
    network = {
      'host' : 'ejudge.lksh.ru',
      'port' : '22',
      'login' : 'ejudge',
      'password' : 'axeiraod',
      'destination' : '/home/judges/'
    },
    libs = []
  ),
  'informatics' : EjudgeExporter(
    network = {
      'host' : 'informatics.mccme.ru',
      'port' : '22',
      'login' : 'ejudge',
      'password' : '1QaZsE4',
      'destination' : '/home/judges/'
    },
    libs = []
  ),
  'mingalev_pcms2' : PCMS2Exporter(
    network = {
      'host' : r'Z:\problems'
    },
    libs = []
  )
}
