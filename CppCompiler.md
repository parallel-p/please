# Installing G++ under windows #

1. Go to the http://sourceforge.net/projects/mingw/files/ and download latest version (bold link above the list of files).

2. Run the installer; select "Use pre-packaged repository catalogues"; press Next three times, may be, modifying installation path or start menu data; in the list of optional features select C++ compiler; press Install. Wait until it downloads all the packages and installs it on your computer.

3. In command-line write 'set PATH=%PATH%;`[MinGW installation path]`\bin', where `[MinGW installation path]` is the path you've installed MinGW in 2 step. By default it's C:\MinGW

4. Check that everything's ok by entering 'g++ --version'. If you've done everything correct, it'll show you version of installed compiler.