mv tests/solution* solutions/
please add solution solutions/solution.cpp
please add solution solutions/solution.py
echo "#!/usr/bin/python3" >.tmp
cat solutions/solution.py >>.tmp
mv .tmp solutions/solution.py

please set main solution solutions/solution.py
please set standart checker wcmp.cpp

rm tests.please
touch tests.please

for f in `ls tests/??`
do
    if [ "tests/01" == $f ]
    then
        printf "[sample,tests] tests/01\n" >>tests.please
    else
        printf "[tests] %s\n" $f >>tests.please
    fi
done
