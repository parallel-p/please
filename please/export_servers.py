from .exporter.ejudge_exporter import EjudgeExporter

servers = {
  'zhuravlev_ejudge' : EjudgeExporter(
    network = {
      'host' : '192.168.16.28',
      'port' : '22',
      'login' : 'ejudge',
      'password' : 'ejudge'
    },
    libs = []
  )
}
