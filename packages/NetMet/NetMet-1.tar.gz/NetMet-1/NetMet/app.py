import os, sys, json, requests, random, datetime as date_time
try:
	from NetMet.py_fakes_ip import ClassA as IPCall_A, ClassB as IPCall_B, Topologhy
	from NetMet.encrypt import Encrypt
	from NetMet.requests_html.requests_html import *
	from NetMet.multi_enginer import from_Google as Google, from_Yahoo as Yahoo, from_Bing as Bing, from_Duck as Duckduckgo, Remove_tags_js_css as Remove_tags, header as select_header
	from NetMet.config import curnet_directory_script, argument, uri_validator, max_min_value, read_config, Map_Config
	from NetMet._savdata import Save_My_Data
except:
	from .py_fakes_ip import ClassA as IPCall_A, ClassB as IPCall_B, Topologhy
	from .encrypt import Encrypt
	from .requests_html.requests_html import *
	from .multi_enginer import from_Google as Google, from_Yahoo as Yahoo, from_Bing as Bing, from_Duck as Duckduckgo, Remove_tags_js_css as Remove_tags, header as select_header
	from .config import curnet_directory_script, argument, uri_validator, max_min_value, read_config, Map_Config
	from ._savdata import Save_My_Data

import html


___VERSION___ = 1.0

print("Welcome to Calculator IP, Net Topology, PyNews, PyWeathers.\nVersion:", ___VERSION___)
def pprints(module):
	print("{} its active!".format(module))
"""
from_Google
from_Bing
from_Duck
from_Yahoo
"""
try:# python2
	from urlparse import urlparse
	from urllib import quote_plus as prams_plus
except:# python3
	from urllib.parse import urlparse, quote_plus as prams_plus



class PyWeathers:

	"""docstring for PyWeathers"""
	def __init__(self, arg=None):
		super(PyWeathers, self).__init__()
		pprints(self.__class__.__name__)
		self.parama = arg
		self.Map_Config = Map_Config().list
		self.params = []
		self.json_output = None

	def ___create___(self, map_config):
		_map = read_config()
		if map_config == _map['api_key']:
			map_config = self.Map_Config[0] 
			self.params.append("key={}".format(map_config))

	@classmethod
	def urls(cls, method):
		req_method = ["current.json", "forecast.json"]
		choice = None
		for value in req_method:
			if any(method.lower() in s for s in req_method):
				choice = value
		return "https://api.weatherapi.com/v1/{}".format(choice)

	def _requests(self, req):
		if req and "https://api.weatherapi.com" in req:
			try:
				r = requests.get("{}?{}".format(req, "&".join(self.params)))
				if r.status_code == 200:
					self.output = r.json()
					return self.output
			except:
				pass
		return


	def q_parameter(self, city_or_lat):
		if city_or_lat and len(self.params)==1:
			if self.check_empity(self.params[0], 'q') == False: 
				self.params.append('q={}'.format(city_or_lat))

	def check_empity(self, x, params):
		try:
			PyWeathers.get_param_from_url(x, params)
			return True
		except:
			return False

	def unix_times(self, longtime):
		if type(longtime) == int:
			if len(self.params)==2:
				if self.check_empity("&".join(self.params), "days") == False or self.check_empity("&".join(self.params), "dt") == False:
					self.params.append("unixdt={}".format(longtime))

	def days(self, langdays):
		if langdays<=8:
			lenght_days= str(langdays)
		else:
			lenght_days= "1"

		if len(self.params)==2:
			if self.check_empity("&".join(self.params), "dt") == False or self.check_empity("&".join(self.params), "unixdt") == False:
				self.params.append("days={}".format(lenght_days))

	def date_history(self, datetime):
		if datetime and len(self.params)==2:
			if self.check_empity("&".join(self.params), "days") == False or self.check_empity("&".join(self.params), "unixdt") == False:
				self.params.append("dt={}".format(datetime))

	@classmethod
	def get_param_from_url(cls, url, param_name):
		return [i.split("=")[-1] for i in url.split("?", 1)[-1].split("&") if i.startswith(param_name + "=")][0]

	@property
	def lang(self):
		self.Languages = [
		"arabic ar",
		"bengali bn",
		"bulgarian bg",
		"chinese zh",
		"czech cs",
		"danish da",
		"french fr",
		"german de",
		"greek el",
		"hindi hi",
		"italian it",
		"japanese jp",
		"javanese jv",
		"korean ko",
		"mandarin zh_cmn",
		"portuguese pt",
		"romanian ro",
		"russian ru",
		"spanish es",
		"swedish sv",
		"tamil ta",
		"turkish tr",
		"ukrainian uk",
		"vietnamese vi",
		"wu zh_wuu",
		"zulu zu"
		]

	@lang.setter
	def lang(self, choice):
		for x in self.Languages:
			if any(choice.lower() in s for s in x.split(" "))==True:
				if len(self.params)>=2 and self.check_empity("&".join(self.params), 'lang') == False:
					self.params.append("lang={}".format(x.split(" ")[1]))

	@classmethod
	def key_json(cls, data_json):
		save = []
		for x in data_json:
			save.append(x)
		return save

class PyNews:
	"""docstring for My_IP"""
	def __init__(self, arg=None, **arguments):
		super(PyNews, self).__init__()
		pprints(self.__class__.__name__)
		api_key = Map_Config().list
		if api_key[0] is None:
			raise TypeError("Opps!!. Token its wrong")
		self.keywords = arg
		self.output = []
		self.dorkmethod = [] #q semua
		self.requestpost = []
		self.json_result = ''
		self.country
		if self.keywords:
			error = None
		else:
			if argument(arguments, "params"):
				tags = ''
				keywords = ''
				by_datex = ''
				sites = ''
				for argxx in arguments['params']:
					if 'tags' in argxx:
						tags =  "meta:{}".format(arguments['params']['tags'])
						#nggak penting
					if 'key' in argxx or 'q' in argxx:
						try:
							keywords = "intext:{}".format(arguments['params']['key'])
							self.keywords = arguments['params']['key']
						except:
							keywords = "intext:{}".format(arguments['params']['q'])
							self.keywords = arguments['params']['q']

					if 'by_date' in argxx:
						by_datex =  by_date(arguments['params']['by_date'], 'daterange')
						#nggak penting

					if 'country' in argxx:
						self.country = arguments['params']['country']
					if 'sites' in argxx:

						self.official = arguments['params']['sites']
					
					if 'dork' in argxx:
						self.dork(arguments['params']['dork'])

					#if self.keywords == None or self.keywords == "" or self.keywords== " ":
					if tags and by_datex:
							self.output = [tags, keywords, by_datex]
					elif tags:
							self.output = [tags, keywords]
					elif by_datex:
							self.output = [keywords, by_datex]
					else:
							self.output = [keywords]


					

	def user_agents(self, requests):
		browser_agent=["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15", "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0", 
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
			"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36", requests.utils.default_headers()
			]
		return random.choice(browser_agent)

	def __procxy__(self, code, randoms=0):
		url_procx = "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&country={}&speed=medium&protocols=http%2Chttps".format(code)
		r = requests.get(url_procx)
		list_procxy = []
		json_x = r.json()
		for x in range(0, len(json_x['data'])):
			c = json_x['data'][x]['protocols'][0]+":/", json_x['data'][x]['ip'], json_x['data'][x]['port'], json_x['data'][x]['isp'], json_x['data'][x]['city'] , json_x['data'][x]['speed']
			list_procxy.append(c)
		if type(randoms) == int or isinstance(randoms, int):
			return list_procxy[randoms]
		else:
			if type(randoms) == str or isinstance(randoms, str): 
				try:
					randoms = int(randoms)
					return list_procxy[randoms]
				except:
					return None
			else:
				if type(randoms) == bool or isinstance(randoms, bool):
					return list_procxy[random.randint(0, len(list_procxy)-1)]
				return None

	def dork(self, dork="google"):
		#Google, Yahoo, Bing, Duckduckgo
		switcher={
                'google': ["https://google.com/search", Google],
                'bing': ["https://www.bing.com/search", Bing],
                'duck': ["https://duckduckgo.com/", Duckduckgo],
                'yahoo': ["https://search.yahoo.com/search", Yahoo]
                }
		def search_mount(month):
					for x in switcher:
						if any(dork.lower() in s for s in x.split(" "))==True:
							return x
						else:
							if any(x.lower() in s for s in dork.lower().split(" "))==True:
								return x

					return 'google'
		self.dorkmethod = switcher.get(dork, switcher[search_mount(dork)])

	def params(self, params=None, **args):
		search = ['']
		meta_search = self.google_dork()
		if argument(args, "tags"):
			self.tags = args['tags']
			search.append("{}:{}".format(meta_search[3], self.tags))

		intext = meta_search[1]
		if self.keywords and params:
			#intext = meta_search[1] 
			search.append("{}:{} {}".format(intext, self.keywords, params))

		elif self.keywords:
			search.append("{}:{}".format(intext, self.keywords))

		elif params:
			#intext = meta_search[1] 
			search.append("{}:{}".format(intext, params))

		else:
			pass

		if argument(args, "country"):
			self.country = args['country']

		if argument(args, "by_date"):
			self.daterange = args['by_date']
			if any("daterange".lower() in s for s in self.daterange.split(" "))==True or any("(".lower() in s for s in self.daterange.split(" "))==True:
				search.append(self.daterange)
		try:
			search.remove('')
		except:
			del search[0]

		self.output = search
		#if argument(args, "site"):
		#	self.site = args['site']
		#	search.append("{}:{}".format(meta_search[2], self.site))
		return search

	def get(self, sites="randoms", page=1):

		limit = 100

		if sites.lower()=="randoms" or sites.lower() == "random":
			sites = random.choice(self.official)
		elif sites.lower()=="all" or sites.lower()=="alls":
			sites = self.official
		elif sites:
			if any(sites.lower() in s for s in self.official):
				sites = sites.lower()
			else:
				raise TypeError("Oops!!, not in the dictionary")

		if any('meta' in s for s in self.output[0].split(' ')) and any('intext' in s for s in self.output[1].split(' ')):
				self.output[0] = self.output[0]+" OR"

		self.output = " ".join(self.output)
		session = requests

		if "https://google.com/search" == self.dorkmethod[0]:

			#if type(sites) == str or isinstance(sites, str):
			PARAMS = {'q':"{} site:{}".format(self.output, sites)}

		elif "https://www.bing.com/search"== self.dorkmethod[0]:

			PARAMS = "{} {}:{}".format(self.output, 'site', self.official)
			PARAMS = "{}?q={}".format(self.dorkmethod[0], prams_plus(PARAMS) ) 

		elif "https://duckduckgo.com/" == self.dorkmethod[0]:

			PARAMS = "{} {}:{}".format(self.output, 'site', self.official)
			PARAMS = "{}html/?q={}".format(self.dorkmethod[0], prams_plus(PARAMS) )

		elif "https://search.yahoo.com/search"  == self.dorkmethod[0]:
			
			PARAMS = "{} {}:{}".format(self.output, 'site', self.official)
			PARAMS = "{}?q={}".format(self.dorkmethod[0], prams_plus(PARAMS) )
		
		else:
			raise TypeError("Oops!, please choose one of the links from the list ['google', 'bing', 'duck', 'yahoo']")

		for x in range(0, limit):
			if type(PARAMS) == dict or isinstance(PARAMS, dict):
				r = requests.get(self.dorkmethod[0], params=PARAMS , headers=user_agents)
			else:
				pass


		
	def post(self, **args):
		map_link = []
		text = []
		self.output = self.output

		session = requests
		if argument(args, "params") or argument(args, "param"):
			self.output = args

		if argument(args, "proxies") or argument(args, "prox"):
			try:
				proxies = self.__procxy__(code=args["proxies"].upper(), randoms=1)
			except:
				proxies = self.__procxy__(code=args["prox"].upper(), randoms=1)

			proxies_output = []
			numb = 0
			for x in proxies:
				if numb==3:
					proxies_output.append(x)
					break
				numb +=1

			proxies = proxies_output[0]+"/"+proxies_output[1]+":"+proxies_output[2]
			try:
				session.proxies.update({'http':proxies, 'https':proxies})
			except:
				session.proxies = {'http':proxies, 'https':proxies}

		user_agents = ''
		if argument(args, "user_agent"):
			try:
				user_agents = { 'User-Agent': str(self.user_agents(session)) }
			except:
				user_agents = { 'User-Agent': str(args["user_agent"]) }


			#print(user_agents)#.update({'User-Agent':user_agents})

		if user_agents==None or user_agents == '':
			user_agents =  { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36' } #session.utils.default_headers()

		if self.keywords:
			


			if any('meta' in s for s in self.output[0].split(' ')) and any('intext' in s for s in self.output[1].split(' ')):
				self.output[0] = self.output[0]+" OR"

			self.output = " ".join(self.output)

			if argument(args, "link") or argument(args, "site"):
				try:
					sites = args['link']
				except:
					sites = args['site']
				for website_name in self.official:
					if any(sites.lower() in s for s in website_name.split(' ')):
						self.official = website_name
						break

			if any('http' in s for s in self.keywords.split(' ')):
				links = []
				for url in self.keywords.split(' '):
					if uri_validator(url) == True:
						links.append(url)
						self.output = self.output.replace(url, '')
					else:
						text.append(url)
				map_link = links

			if type(map_link) == list or isinstance(map_link, list):
				try:
					if self.official:
						self.official = "{} | site:{}".format(self.official, urlparse(map_link[0]).netloc)
					else:
						self.official = map_link[0]
				except:
					for x in self.official:
						if any(x in s for s in map_link):
							if self.official:
								self.official = "{} | site:{}".format(self.official, urlparse(map_link[0]).netloc)
							else:
								self.official = map_link[0]
							break

			if type(self.official) == str or isinstance(self.official, str):
				#print("{} {}:{}".format(self.output, 'site', self.official))

				if "https://google.com/search" == self.dorkmethod[0]:
					PARAMS = {'q':"{} {}:{}".format(self.output, 'site', self.official)}
					r = session.get(self.dorkmethod[0], params=PARAMS , headers=user_agents)

					selec_tag_byatrith = "div .v7W49e"


					select_tag_class = "tF2Cxc"
					types = "text"

				elif "https://www.bing.com/search"== self.dorkmethod[0]:
					PARAMS = "{} {}:{}".format(self.output, 'site', self.official)
					r = session.get( "{}?q={}".format(self.dorkmethod[0], prams_plus(PARAMS) )  , headers=user_agents)
					selec_tag_byatrith = "ol #b_results"

					select_tag_class = "b_algo"
					types = "search"

				elif "https://duckduckgo.com/" == self.dorkmethod[0]:
					PARAMS = "{} {}:{}".format(self.output, 'site', self.official)
					url =  "{}html/?q={}".format(self.dorkmethod[0], prams_plus(PARAMS) )
					r = session.get(url, headers=user_agents) #bug

					selec_tag_byatrith = "div .serp__results"

					select_tag_class = "results_links"
					types = "text"

				elif "https://search.yahoo.com/search" ==  self.dorkmethod[0]:
					PARAMS = "{} {}:{}".format(self.output, 'site', self.official)
					r = session.get( "{}?q={}".format(self.dorkmethod[0], prams_plus(PARAMS) )  , headers=user_agents)

					selec_tag_byatrith = "ol .searchCenterMiddle"

					select_tag_class = "relsrch"
					types = "text"

				else:
					raise TypeError("Oops!, please choose one of the links from the list ['google', 'bing', 'duck', 'yahoo']")
				#soup = BeautifulSoup(r.content, 'html.parser')

				style_js_clean = Remove_tags(r.content, types)
				style_js_clean = str(style_js_clean[0])
				style_js_clean = select_header(style_js_clean, selec_tag_byatrith)
				style_js_clean = str(style_js_clean)
				#return style_js_clean[0]

				
				try:
					self.json_result =  self.dorkmethod[1](style_js_clean, select_tag_class)
				except:
					self.json_result =  self.dorkmethod[1](style_js_clean, select_tag_class, self.official)

				#with open(curnet_directory_script()+'/index.html', 'w+', encoding='utf8') as fp:
				#	fp.write(style_js_clean)

				#soup.prettify()
				#session.get(self.dorkmethod, params=payload, allow_redirects=False)
			else:
				raise TypeError("Oops!, please choose one of the links from the list {}".format(self.official))
				#for link_site in self.official:
				#	payload = { 'q' : "{} {}:{}".format(self.output, 'site', link_site)}
				#	print(payload)
		else:
			raise TypeError("Oops!, reset active or arg is none")

	@property
	def result(self):
		return Save_My_Data(self.json_result)

	@property
	def country(self):
		self.internaional = ['edition.cnn.com', "news.google.com", "news.yahoo.com"]
		self.arabic = ["arabic-media.com", "www.arabnews.com"] 
		self.usa = ["www.usnews.com", "washingtonpost.com", "cnbc.com", "nypost.com", "nbcnews.com", "usnews.com", "foxnews.com", "nytimes.com"]
		self.indian = ["indiatimes.com", "news18.com", "www.ndtv.com", "indiatoday.in", "dnaindia.com", "oneindia.com", "www.informalnewz.com", "www.sinceindependence.com"]
		self.philippine = ["www.inquirer.net", "www.techpinas.com", "www.pna.gov.ph", "philnews.ph", "tonite.abante.com.ph"]
		self.chinese = ["www.ecns.cn", "supchina.com", "chinamil.com.cn", "www.bbc.com/news/world/asia/china", "list.juwai.com"]
		self.indonesian = ["www.merdeka.com", "www.tribunnews.com", "www.kompas.com", "sindonews.com", "www.tempo.co", "www.liputan6.com"]
		self.malaysian = ["malaysiakini.com", "thestar.com.my", "hmetro.com.my", "www.malaysianews.net"]
		self.singapore = ["channelnewsasia.com", "straitstimes.com", "www.citynews.sg"]
		self.japanese = ["www.japantimes.co.jp", "japantoday.com", "newsonjapan.com"]
		self.koresoult = ["en.yna.co.kr", "www.koreaherald.com", "www.donga.com", "www.mediatoday.co.kr", "segye.com", "www.hankooki.com"]
		self.koresnort = ["www.nknews.org", "www.northkoreatimes.com"]
		self.russian = ["www.themoscowtimes.com", "tass.com", "lenta.ru", "russia-insider.com"]
		self.german = ["www.t-online.de", "munichnow.com"]
		self.official = {
						"inter"	: self.internaional, 
						"ar"	: self.arabic, 
						"as"	: self.usa, 
						"in"	: self.indian, 
						"ph"	: self.philippine,
						"cn"	: self.chinese, 
						"id"	: self.indonesian, 
						"my"	: self.malaysian, 
						"sg"	: self.singapore, 
						"jp"	: self.japanese,
						"ks"	: self.koresoult, 
						"kn"	: self.koresnort,
						"ru"	: self.russian,
						"de"	: self.german
						}

	@country.setter
	def country(self, code):
		for x in self.official:
			if any(code.lower() in s for s in x.split(" "))==True:
				self.official = self.official[x]


	def by_date(self, datetime, cur="default"):
		months = ''
		today = date_time.date.today()
		daynow, monthnow, yearnow = today.strftime("%d/%m/%Y").split("/")


		def trunc_div(a, b):
		    """Implement 'truncated division' in Python."""
		    return (a // b) if a >= 0 else -(-a // b)

		def formula1(year, month, day):
		    """Convert Gregorian date to julian day number."""
		    return 367 * year - trunc_div(7 * (year + trunc_div(month + 9, 12)), 4) - trunc_div(3 * (trunc_div(year + trunc_div(month - 9, 7), 100) + 1), 4) + trunc_div(275 * month, 9) + day + 1721029

		def formula2(year, month, day):
		    """Convert Gregorian date to julian day number (simplified); only valid for dates from March 1900 and beyond."""
		    return 367 * year - trunc_div(7 * (year + trunc_div(month + 9, 12)), 4) + trunc_div(275 * month, 9) + day + 1721014

		datenow = formula2(int(yearnow), int(monthnow), int(daynow))
		try:
			datetime = int(datetime)
			month = datetime

			minx , maxx = max_min_value([datenow, datetime])
			datebytime = "daterange:{}-{}".format(minx , maxx)
		except:
			if "-" in datetime:
				splitby = "-"
			elif "/" in datetime:
				splitby = "/"
			elif "\\" in datetime:
				splitby = "\\"
			elif "," in datetime:
				datetime = datetime.replace(" ", "")
				splitby = ","
			elif "." in datetime:
				splitby = "."
			else:
				splitby = " "

			year, month, day = datetime.split(splitby)
			try:
				if int(month)>0 and int(month)<=12:
					month = int(month)
				else:
					raise TypeError("Opps!!, {} is not in the calendar".format(month))
			except:
				switcher={
                'january': 1,
                'february': 2,
                'march': 3,
                'april': 4,
                'may': 5,
                'june': 6,
                'july': 7,
                'august': 8,
                'september': 9,
                'october': 10,
                'november': 11,
                'december': 12
                }
				def search_mount(month):
					for x in switcher:
						if any(month.lower() in s for s in x.split(" "))==True:
							return x
					return 'january'
				month = switcher.get(month, switcher[search_mount(month)])
			if any('create' in s for s in cur.split(' ')) or any('default' in s for s in cur.split(' ')):
				datebytime = "(\"{} * {}\" | \"{}/{}\" | {}/{} |{}/*/{})".format(month, year, month, year, month, day, month, day)
			elif any('jul' in s for s in cur.split(' ')) or any('daterange' in s for s in cur.split(' ')):
				datetime = formula2(int(year), int(month), int(day))
				minx , maxx = max_min_value([datenow, datetime])
				datebytime = "daterange:{}-{}".format(minx, maxx)
			else:
				datebytime = "(\"{} * {}\" | \"{}/{}\")".format(month, year, month, year)

		return datebytime



	def google_dork(self):
		self.google_dork = [
		'intitle', #get title
		'intext', #search text web
		'site', #site
		'meta' #tag
		]
		return self.google_dork
		#"(\"May * 2013\" | \"May 2013\" | 05/03 | 05/*/03)"#by create konten
		#"daterange:"

	def reset(self):
		dic = vars(self)
		for i in dic.keys():
			print(i)
			if type(dic[i]) == list or isinstance(dic[i], list):
				dic[i] = []
			elif type(dic[i]) == dict or isinstance(dic[i], dict):
				dic[i] = ()
			elif type(dic[i]) == str or isinstance(dic[i], str):
				dic[i] = ''
			elif type(dic[i]) == int or isinstance(dic[i], int):
				dic[i] = None
			else:
				pass
            