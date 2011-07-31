from .. import globalconfig
import xml.etree.ElementTree as ET
import urllib
from urllib import request
import os

def extract_problems(xml):
    for node in xml.findall("*/problem"):
        yield (node.get("index"),
               node.get("name"),
               node.get("url") + "?type=linux"
               ) 

def read_authorised(url):
    print("Reading %s" % url)
    res = request.urlopen(url, data=bytes(urllib.parse.urlencode(globalconfig.access), encoding="UTF-8"))
    return res.read()

def request_contest_xml(contest_id):
    return ET.XML(read_authorised(
            '%s/c/%s/contest.xml' % (
                globalconfig.polygon_url, contest_id)))

def download_problem(url, name):
    print("downloading from url %s to %s.zip" % (url, name))
    request.urlretrieve (
            url,
            name+".zip",
            data = urllib.parse.urlencode(globalconfig.access))
    
def get_problem(contest_id, problem_letter):
    print("__________________________________")
    print(str(os.getcwd()))
    print(contest_id)
    print(problem_letter)
    print("__________________________________")
    contest_xml = request_contest_xml(contest_id)
    for letter, name, url in extract_problems(contest_xml):
        letter = letter.upper() # in xml letter may be in lower case, but in url it should be in upper case
        if letter == problem_letter:
            download_problem(url, name)
            return(name)