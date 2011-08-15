#Tested for win7; foe winXP and others - probably another key name/path nedeed
from platform import platform #our platform_detector is not enough
if "Windows-7" in platform():
    from winreg import OpenKey, CreateKey, QueryValue, SetValueEx, CloseKey, HKEY_LOCAL_MACHINE, KEY_ALL_ACCESS, REG_DWORD


class PreventErrorWindow:
    '''
    USAGE:  with PreventErrorWindow():
                ...run solution...
    '''

    def __init__(self):
        #for Windows 7
        self.keyVal = r'Software\Microsoft\Windows\Windows Error Reporting'
        self.name = "DontShowUI" 
            
    def __enter__(self):
            self.value = 0 #QueryValue(keyVal, name)
            #print('*', self.value, '*')
            key = OpenKey(HKEY_LOCAL_MACHINE, self.keyVal, 0, KEY_ALL_ACCESS)
            SetValueEx(key, self.name, 0, REG_DWORD, 0)
            CloseKey(key)

    def __exit__(self, type, value, traceback):
            key = OpenKey(HKEY_LOCAL_MACHINE, self.keyVal, 0, KEY_ALL_ACCESS)
            SetValueEx(key, self.name, 0, REG_DWORD, self.value)
            CloseKey(key)


