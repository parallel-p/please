from .exporter.ejudge_exporter import EjudgeExporter
from .exporter.pcms2_exporter import PCMS2Exporter

servers = {
  'zhuravlev_ejudge' : EjudgeExporter(
    network = {
      'host' : '192.168.16.35',
      'port' : '22',
      'login' : 'ejudge',
      'password' : 'ejudge',
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
