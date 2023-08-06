import os, sys, json, requests, random, datetime as date_time
from .requests_html.requests_html import *
def curnet_directory_script():
    _file = __file__.replace("\\", "/")
    return _file.rsplit("/", 1)[0].split('.')[0]

def argument(arg, search):
	if type(arg) == list or isinstance(arg, list) or type(arg) == dict or isinstance(arg, dict):
		for extract in arg:
			try:
				return arg[search]
			except:
				if any(search.lower() in s for s in extract.split(" ")) == True:
					return arg[search]
				else:
					pass
	return None

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False

def max_min_value(data):
	return min(data), max(data)

def read_config():
	def getLocalFolder():
	    path=str(os.path.dirname(os.path.abspath(__file__))).split(os.sep)
	    return path
	file_names = "{}/external.config".format('/'.join(getLocalFolder()))
	#eval()
	content = open(file_names).read()
	return eval(content)

class Map_Config:
	"""docstring for Map_Config"""
	def __init__(self,):
		super(Map_Config, self).__init__()
		map_config = read_config()
		if map_config['username'] != 'root' and map_config['development'] != 0 \
		and map_config['api_key'] != "5b50f623ddc14b6c91573722222404":
			requests = requests.Session() 
			try:
				r = requests.get("https://api.weatherapi.com/v1/forecast.json?key={}&q=Tulungagung&lang=jv".format(map_config['api_key']))
				if r.status_code != 200 or r.status_code == 401:
					map_config['api_key'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(30))
				else:
					pass
			except:
				pass
		else:
			pass
		self.list = map_config['api_key'], map_config['username']