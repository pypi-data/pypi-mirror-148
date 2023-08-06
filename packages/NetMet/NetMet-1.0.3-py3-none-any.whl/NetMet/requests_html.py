import requests, re
try:
    from bs4 import BeautifulSoup
except:
    from BeautifulSoup import BeautifulSoup

import re
#Github: https://github.com/sujitmandal
#This programe is create by Sujit Mandal
"""
Github: https://github.com/sujitmandal
Pypi : https://pypi.org/user/sujitmandal/
LinkedIn : https://www.linkedin.com/in/sujit-mandal-91215013a/
"""
def find_Anchor(data, relsrch):
    r = requests.get(data)
    if r.status_code == 200 or r.status_code == 410:
        soup = BeautifulSoup(r.text, "html.parser")
        s = soup.findAll("a")
        for x in s:
            data = x.get("href")
            if any(relsrch in v for v in data.split(" ")):
                return data
    return

#search on google "my user agent"
# userAgent = ('') #my user agent
# search = ('') #Enter Anything for Search

httpResponseStatusCodes = {
    100 : 'Continue',
    101 : 'Switching Protocol',
    102 : 'Processing (WebDAV)',
    103 : 'Early Hints',
    201 : 'Created',
    202 : 'Accepted',
    203 : 'Non-Authoritative Information',
    204 : ' No Content',
    205 : 'Reset Content',
    206 : 'Partial Content',
    207 : 'Multi-Status (WebDAV)',
    208 : 'Already Reported (WebDAV)',
    226 : 'IM Used (HTTP Delta encoding)',
    300 : 'Multiple Choice',
    301 : 'Moved Permanently',
    203 : 'Found',
    303 : 'See Other',
    304 : 'Not Modified',
    305 : 'Use Proxy',
    306 : 'unused',
    307 : 'Temporary Redirect',
    308 : 'Permanent Redirect',
    400 : 'Bad Request',
    401 : 'Unauthorized',
    402 : 'Payment Required',
    403 : 'Forbidden',
    404 : 'Not Found',
    405 : 'Method Not Allowed',
    406 : 'Not Acceptable',
    407 : 'Proxy Authentication Required',
    408 : 'Request Timeout',
    409 : 'Conflict',
    410 : 'Gone',
    411 : 'Length Required',
    412 : 'Precondition Failed',
    413 : 'Payload Too Large',
    414 : 'URI Too Long',
    415 : 'Unsupported Media Type',
    416 : 'Range Not Satisfiable',
    417 : 'Expectation Failed',
    418 : 'I am a teapot',
    421 : 'Misdirected Request',
    422 : 'Unprocessable Entity (WebDAV)',
    423 : 'Locked (WebDAV)',
    424 : 'Failed Dependency (WebDAV)',
    425 : 'Too Early',
    426 : 'Upgrade Required',
    428 : 'Precondition Required',
    429 : 'Too Many Requests',
    431 : 'Request Header Fields Too Large',
    451 : 'Unavailable For Legal Reasons',
    500 : 'Internal Server Error',
    501 : 'Not Implemented',
    502 : 'Bad Gateway',
    503 : 'Service Unavailable',
    504 : 'Gateway Timeout',
    505 : 'HTTP Version Not Supported',
    506 : 'Variant Also Negotiates',
    507 : 'Insufficient Storage (WebDAV)',
    508 : 'Loop Detected (WebDAV)',
    510 : 'Not Extended',
    511 : 'Network Authentication Required'
}

def AllowedRedirect(data):
    if any('http' in s for s in [data.split('//')[0]]):
        data = "{}".format(data)
    else:
        data = "https:{}".format(data)
    regex=r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
    s = requests.get(data)
    matches = re.findall(regex, s.text)
    for urlvalid in matches:
        if any('http' in s for s in [urlvalid] ):
            return urlvalid
    return 

def header(html, types):
    soup = BeautifulSoup(html, "html.parser")
    if type(types) == str or isinstance(types, str):
        types = types.split(" ")

        if len(types)==1:
            data = [x.extract() for x in soup.findAll(types[0])]

        elif len(types)==2:

            if any('.' in s for s in types[1].split(' ')):
                data = [x.extract() for x in soup.findAll(types[0], {"class":types[1].replace(".", "")})]
            else:
                data = [x.extract() for x in soup.findAll(types[0], id=types[1].replace("#", ""))]
        if len(data)==1:
            data = str(data[0])
        elif len(data)>1:
            data = ["{}".format(str(x)) for x in data]
            data = " ".join(data)
        else:
            raise "SSS"
        return BeautifulSoup(data, "html.parser")
    return soup

def clean_Bing(data):
    soup = BeautifulSoup(data, "html.parser")
    li_headers = soup.find_all("li")
    for header in li_headers:
        header.name = "div"
    out = [str(x) for x in li_headers]
    out = "".join(out)
    return out













#'tF2Cxc'
def from_Google(data, header):
    saved = []
    soup = BeautifulSoup(data, "html.parser")
    text = soup.findAll("div", {'class': header})

    for cite in soup.find_all("cite", {'class':'iUh30'}):
        cite.decompose()

    for li in soup.find_all("li", {'class':'action-menu-item'}):
        li.decompose()

    "cite:iUh30 li:action-menu-item"
    for out in text:
        saved.append({
            'link':out.a["href"],
            'Desc':out.text
            })

    return saved


#li .b_algo b_attribution

#head all page ol :id #b_results , h2 .b_topTitle remove div .b_attribution

#b_algo
def from_Bing(data, header):
    saved = []
    clean = clean_Bing(data)
    if clean or clean!="":
            data = clean

    soup = BeautifulSoup(data, "html.parser")
    s = soup.findAll("div", {'class': header})
    for div in soup.find_all("div", {'class':'b_attribution'}):
        div.decompose()

    for out in s:
        saved.append({
            'link':out.h2.a["href"],
            'Desc':out.text
            })
    return saved




#head div .results_links 

#rm div .result__extras


#title h2 .result__title
#decript div .result__body
def from_Duck(data, header):
    saved = []
    soup = BeautifulSoup(data, "html.parser")
    s = soup.findAll("div", {'class': header})
    for div in soup.find_all("div", {'class':'result__extras'}):
        div.decompose()

    for out in s:
        saved.append({
            'link':AllowedRedirect(out.h2.a["href"]),
            'Desc':out.text
            })
    return saved

#'relsrch'
def from_Yahoo(data, header, linkname):
    saved = []
    soup = BeautifulSoup(data, "html.parser")
    s = soup.findAll("div", {'class': header})
    
    for spans in soup.find_all("span", {'class':'fc-obsidian'}):
        spans.decompose()

    for spanclass in soup.find_all("span", {'class':'txt'}):
        spanclass.decompose()
    
    for div in soup.find_all("div", {'class':'fc-obsidian'}):
        div.decompose()
    
    for out in s:
        saved.append({
            'link': AllowedRedirect(out.a["href"]), #find_Anchor(out.a["href"], linkname),
            'Desc':out.text
            })
    return saved













def Remove_by_tag(html, types):
    soup = BeautifulSoup(html, "html.parser")
    if type(types) == str or isinstance(types, str):
        types = types.split(" ")

        if len(types)==1:
            data = soup.find_all(types[0])
            print(0)

        elif len(types)==2:

            if any('.' in s for s in types[1].split(' ')):
                data = soup.findAll(types[0], {"class":types[1].replace(".", "")})
                print(1)
            else:
                data = soup.findAll(types[0], id=types[1].replace("#", ""))
                print(2)
        else:
            raise "SSS"

        return data

    return 


def Remove_tags_js_css(html, types):
  
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    try:
        soup.script
    except:
        pass
    try:
        soup.link
    except:
        pass
    try:
        soup.form
    except:
        pass

    try:
        for value in soup.find_all("input", type=types):
            x = value.get('value')
            class_s = value.get('class')
            #print(class_s)
            if x:
                clean = x.split("intext")
                if clean[1]: 
                    break
        #print(class_s, clean[1].split(":")[1])
        client = clean[1].split(":")[1]
        cc = client.split(" ")
        clean_pa = cc[len(cc)-1:]

        #print(1, class_s, x)
        if class_s:
            soup.find("input",{"class":str(class_s[0])})["value"] = client.replace(clean_pa[0], "")
        else:
            findtoure = soup.find_all(text = re.compile(x))
            for comment in findtoure:
                fixed_text = comment.replace(x, client.replace(clean_pa[0], ""))
                comment.replace_with(fixed_text)

    except:
        pass
        #soup.find_all('input', type="text")["value"] = ''

    data = [x.extract() for x in soup.findAll('body')]
    return data

def Remove_All_Tags(html):
  
    # parse html content
    soup = BeautifulSoup(html, "html.parser")
  
    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
  
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

def Google(search):
    results = []
    texts = []
    soup = BeautifulSoup(search, 'html.parser')
    for i in soup.find_all('div', {'class' : 'kCrYT'}):
        for x in i.find_all('a'):
            results.append({"link": x['href'], "desc" : x.text})
    return results

def Duckduckgo(search , userAgent):
    URL = ('https://duckduckgo.com/html/?q=' + search)
    headers = {'user-agent' : userAgent}
    request = requests.get(URL, headers=headers)

    results = []
    texts = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')

        for i in soup.find_all('a', attrs={'class':'result__a'}):
            links = i['href']
            results.append(links)
            texts.append(i.text)
    else:
        results.append('HTTP Status : {}'.format(httpResponseStatusCodes.get(request.status_code)))
        texts.append('HTTP Status : {}'.format(httpResponseStatusCodes.get(request.status_code)))

    return(texts, results)

def Bing(search, userAgent):
    URL = ('https://www.bing.com/search?q='+search)
    headers = {'user-agent' : userAgent}
    request = requests.get(URL, headers=headers)

    results = []
    texts = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, "html.parser")

        for i in soup.find_all('li', {'class' : 'b_algo'}):
            link = i.find_all('a')
            link_text = i.find('a')
            links = link[0]['href']
            results.append(links)
            texts.append(link_text.text)
    else:
        results.append('HTTP Status : {}'.format(httpResponseStatusCodes.get(request.status_code)))
        texts.append('HTTP Status : {}'.format(httpResponseStatusCodes.get(request.status_code)))
 
    return(texts, results)


def Yahoo(search, userAgent):
    URL = ('https://search.yahoo.com/search?q=' + search)
    request = requests.get(URL)

    results = []
    texts = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')

        for i in soup.find_all(attrs={"class": "d-ib ls-05 fz-20 lh-26 td-hu tc va-bot mxw-100p"}):
            results.append(i.get('href'))
            texts.append(i.text)
    else:
        results.append('HTTP Status : {}'.format(httpResponseStatusCodes.get(request.status_code)))
        texts.append('HTTP Status : {}'.format(httpResponseStatusCodes.get(request.status_code)))

    return(texts, results)


def Ecosia(search, userAgent):
    URL = ('https://www.ecosia.org/search?q='+search)
    headers = {'user-agent' : userAgent}
    request = requests.get(URL, headers=headers)

    results = []
    texts = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')
        text = []

        for i in soup.find_all('div', {'class' : 'result-firstline-container'}):
            link = i.find_all('a')
            link_text = i.find('a')
            links = link[0]['href']
            results.append(links)
            text.append(link_text.text)

        for j in text:
            a = j.strip()
            texts.append(a)
    else:
        results.append('HTTP Status : {}'.format(httpResponseStatusCodes.get(request.status_code)))
        texts.append('HTTP Status : {}'.format(httpResponseStatusCodes.get(request.status_code)))
    
    return(texts, results)

def Givewater(search, userAgent):
    URL = ('https://search.givewater.com/serp?q='+search)
    headers = {'user-agent' : userAgent}
    request = requests.get(URL, headers=headers)

    results = []
    texts = []
    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')

        for i in soup.find_all('div', {'class' : 'web-bing__result'}):
            link = i.find_all('a')
            link_text = i.find('a')
            links = link[0]['href']
            results.append(links)
            texts.append(link_text.text)
    else:
        results.append('HTTP Status : {}'.format(httpResponseStatusCodes.get(request.status_code)))
        texts.append('HTTP Status : {}'.format(httpResponseStatusCodes.get(request.status_code)))

    return(texts, results)