#Tested for win7; foe winXP and others - probably another key name/path nedeed
from platform import platform #our platform_detector is not enough


def error_window(hide = False):
    '''Under windows7 turns on (hide = False) or off (hide = True) error windows 
       by changing appropriate key in registry
    '''
    if "Windows-7" in platform():
        from winreg import OpenKey, CreateKey, SetValueEx, CloseKey, HKEY_LOCAL_MACHINE, KEY_ALL_ACCESS, REG_DWORD
        keyVal = r'Software\Microsoft\Windows\Windows Error Reporting'
        key = OpenKey(HKEY_LOCAL_MACHINE, keyVal, 0, KEY_ALL_ACCESS)
        SetValueEx(key, "DontShowUI", 0, REG_DWORD, int(hide))
        CloseKey(key)

