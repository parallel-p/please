import unittest

import mox
import psutil

import please.executors.runner as rn


class RunTest(unittest.TestCase):

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.VerifyAll()
        
    def test_run(self) :
        self.mox.StubOutWithMock(psutil, "Popen")
        process = self.mox.CreateMockAnything()
        process.__enter__()
        process.communicate().AndReturn((b'', b''))
        process.__exit__(None, None, None)

        self.mox.StubOutWithMock(rn.invoker, "invoke")
        res_info = self.mox.CreateMock(rn.invoker.ResultInfo)
        res_info.verdict = "OK"
        rn.invoker.invoke(process, rn.globalconfig.default_limits).AndReturn(res_info)

        Snapshot = rn.Snapshot
        self.mox.StubOutWithMock(rn, "Snapshot")
        self.mox.StubOutWithMock(rn.Snapshot, "get_changes")
        snap1 = self.mox.CreateMock(Snapshot)
        rn.Snapshot().AndReturn(snap1)
        snap2 = self.mox.CreateMock(Snapshot)
        rn.Snapshot().AndReturn(snap2)
        snap1.get_changes(snap2).AndReturn(None)

        m = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(rn, "get_lang_config")
        rn.get_lang_config("a.cpp").AndReturn(m)
        m.run_command = ['a.exe']
        m.is_run_garbage = False
        self.mox.StubOutWithMock(rn.trash_remover, "remove_trash")
        rn.trash_remover.remove_trash(None, False)

        psutil.Popen(m.run_command, stdin = None, shell = False,
                     stdout = mox.IgnoreArg(), stderr = mox.IgnoreArg(),
                     env = None).AndReturn(process)


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



