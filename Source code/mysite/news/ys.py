
import urllib.request
import urllib.parse
import re

def ysearch(keywords):
    query_string = urllib.parse.urlencode({"search_query" : keywords})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_result = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    if len(search_result) > 0:
        return search_result[0]

    return None


