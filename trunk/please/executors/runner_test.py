import mox
import psutil
import subprocess
import please.executors.runner as rn
import unittest
import os

import tempfile

class RunTest(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.VerifyAll()
        
    def test_run(self) :
        self.mox.StubOutWithMock(psutil, "Popen")
        process = self.mox.CreateMockAnything()
        psutil.Popen(["a.exe"], stdin = None, shell = False, stdout = mox.IgnoreArg(), stderr = mox.IgnoreArg(), env = None).AndReturn(process)
        process.__enter__()

        self.mox.StubOutWithMock(rn.invoker, "invoke")
        res_info = self.mox.CreateMock(rn.invoker.ResultInfo)
        res_info.verdict = "OK"
        rn.invoker.invoke(process, rn.globalconfig.default_limits).AndReturn(res_info)

        self.mox.StubOutWithMock(rn.snapshot, "Snapshot")
        self.mox.StubOutWithMock(rn.snapshot, "get_changes")
        rn.snapshot.Snapshot().AndReturn([])
        rn.snapshot.Snapshot().AndReturn([])
        rn.snapshot.get_changes([], [])

        m = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(rn, "get_language_configurator")
        rn.get_language_configurator("a.cpp").AndReturn(m)
        m.get_run_command("a.cpp").AndReturn(["a.exe"])
        m.is_compile_garbage = False
        self.mox.StubOutWithMock(rn.trash_remover, "remove_trash")
        rn.trash_remover.remove_trash(None, False)

        #ec = self.mox.CreateMockAnything()
        #self.mox.StubOutWithMock(rn, "ExecutionControl")
        #rn.ExecutionControl(None, mox.IgnoreArg(), mox.IgnoreArg(), process).AndReturn(ec)
        #ec.__enter__()
        #ec.__exit__(None, None, None)


        self.mox.ReplayAll()

        result = rn.run("a.cpp")
        self.assertEqual((result[0].verdict, result[1], result[2]), \
                         ("OK", b'', b''))

if __name__ == '__main__':
    unittest.main()



