import psutil
from please.invoker.invoker import invoke, ExecutionLimits as el

while True:
    res = invoke(psutil.Popen(['svn', 'info', 'ololo']), el(3, 128, 10))
    print(str(res))
    if (res.return_code == 0):
        break
