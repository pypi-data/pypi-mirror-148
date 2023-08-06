import os, sys, re, json
from pathlib import Path
from PIL import Image
try:
	import pandas as pd
except:
	pd = ''

try:
	from html2image import Html2Image
except:
	Html2Image = ''

from tabulate import tabulate

tabel_head = ["LINK", "DESCRIPT"]
class Save_My_Data:
	"""docstring for Save_My_Data"""
	def __init__(self, arg):
		super(Save_My_Data, self).__init__()
		self.arg = arg
		def check():
			try:
				data = str(self.arg)
				self.arg = json.loads(data)
				self.types = "json"
			except:
				self.types = "text"
		check()

	def cleanhtml(self):
		CLEANR = re.compile('<.*?>')
		cleantext = re.sub(CLEANR, '', self.arg)
		return cleantext

	def text(self):
		try:
			result = self.cleanhtml()
		except:
			result = []
			for extract in self.arg:
				result.append([extract['link'], extract['Desc']])
			result = "\n\n  ".join(['\n'.join(a) for a in result])
		return result
	"""
		def check_json(self):
			try:
				reads = self.arg
				json.loads(reads)
			except ValueError as err:
				return False
			return True
	"""
	def pdf(self, paths):
		paths = paths.replace("\\", "/")
		paths_split = paths.split("/")
		pathc = ''

		folder = Path(paths)
		if folder.is_dir():
			pathc +=paths_split[0]
			for filepath in paths_split:
				if filepath:
					if paths_split[0] == filepath:
						pass
					else:
						pathc += "/"+filepath
			filename = pathc
			filename = str(filename)

			try:
				self.images(filename)
			except:
				return
			image1 = Image.open(r'{}/images.png'.format(filename))
			im1 = image1.convert('RGB')
			im1.save(r'{}/net_met.pdf'.format(filename))
		else:
			raise Exception("Failed to reading/create file")


	def images(self, paths):
		paths = paths.replace("\\", "/")
		paths_split = paths.split("/")
		pathc = ''

		folder = Path(paths)
		if folder.is_dir():
			hti = Html2Image()
			css = "body{background:white; text-justify: auto; padding:0px; margin:0px; border:none ; text-decoration: none;}"
			pathc +=paths_split[0]
			for filepath in paths_split:
				if filepath:
					if paths_split[0] == filepath:
						pass
					else:
						pathc += "/"+filepath
			filename = pathc
			filename = str(filename)
			hti.output_path = filename
			try:
				hti.screenshot(html_str=str(self.html()), css_str=css , save_as="images.png")
				return "success"
			except:
				return "failed"

	def json(self):
		try:
			data = self.arg
			self.arg = json.loads(data)
			return self.arg
		except:
			em = {
			'code':'error reading'
			}
			if len(self.arg[0].keys())>0:
				return { 'result:': self.arg }
			return em

	def html(self):
		result = []
		for extract in self.arg:
			result.append([extract['link'], extract['Desc']])
		return tabulate(result, tabel_head, tablefmt="html")


