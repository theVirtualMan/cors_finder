import sys
import tldextract
import requests
import queue
import concurrent.futures
import logging
from tqdm import tqdm

class CORS:
	def __init__(self, file_name):
		self.urls = self.get_urls(file_name)
		logging.basicConfig(level=logging.INFO,
							filename='logs.txt',
                            filemode='w',
                            format='%(message)s',
                    )
        # format='[%(levelname)s] (%(threadName)-10s) %(message)s',

	def get_urls(self, file_name):
		urls = []
		for url in open(file_name):
			urls.append(url.strip())
		return urls


	"""
		url = 'http://example.com'

		origins considered for testing:
		http://example.com
		http://evil.com
		http://aexample.com
		http://examplea.com
		null
	"""
	# use some libraries that seperates domain name
	def get_origins(self, url):
		origins = []
		protocol = url.split("://")[0]
		# no_cache_extract = tldextract.TLDExtract(cache_dir=False)
		# ext = no_cache_extract(url)
		ext = tldextract.extract(url)
		domain = ext.domain
		suf = url.split(ext.domain)[1]

		origins.append(url)
		origins.append(protocol + '://evil.com')
		origins.append(protocol + '://a' + domain + suf)
		origins.append(protocol + '://' + domain + 'a' + suf)
		origins.append('null')

		return origins


	def log(self, url, origin, req):
		logging.info({
			'url' : url,
			'origin' : origin,
			'ACAO' : req.headers['Access-Control-Allow-Origin'],
			'ACAC' : req.headers['Access-Control-Allow-Credentials']
		})


	def check_cors_implementation(self, url):
		# logging.info({'url': url})
		origins = self.get_origins(url)
		for origin in origins:
			try:
				# logging.info({'origin': origin})
				headers = {}
				headers['Origin'] = origin
				headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0 Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'

				req = requests.get(url, headers=headers, timeout=10)
				# should rewrite the filter condition
				if (req.headers['Access-Control-Allow-Credentials'] == 'true') and (req.headers['Access-Control-Allow-Origin'] == origin):
					if url != origin:
						self.log(url, origin, req)
			except KeyError as e: # should add explicit exception handling
				pass
				# print('Invalid key: {}'.format(e), end='\n\n')
			except Exception as e:
				logging.error('Unhandled exception: {}'.format(e))
			

	def get_buggy_urls(self):
		with concurrent.futures.ThreadPoolExecutor(max_workers=256) as executor:
			results = list(tqdm(executor.map(self.check_cors_implementation, self.urls), total=len(self.urls)))

			# future_to_url = {executor.submit(self.check_cors_implementation, url): url for url in self.urls}

			# for future in tqdm(concurrent.futures.as_completed(future_to_url), total=len(future_to_url)):
			# 	pass


if __name__ == "__main__":
	file_name = sys.argv[1]
	cors = CORS(file_name)
	cors.get_buggy_urls()