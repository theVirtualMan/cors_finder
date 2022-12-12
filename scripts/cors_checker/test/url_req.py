import sys
import tldextract
import requests
import queue
import concurrent.futures
import logging
from tqdm import tqdm

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
def get_origins(url):
	origins = []
	protocol = url.split("://")[0]
	ext = tldextract.extract(url)
	domain = ext.domain
	suf = url.split(ext.domain)[1]
	
	origins.append(url)
	origins.append(protocol + '://evil.com')
	origins.append(protocol + '://a' + domain + suf)
	origins.append(protocol + '://' + domain + 'a' + suf)
	origins.append('null')

	return origins



def check_cors_implementation(url):
	print('url: {}'.format(url))
	origins = get_origins(url)
	for origin in origins:
		try:
			print('origin: {}'.format(origin))
			headers = {}
			headers['Origin'] = origin
			headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0 Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'

			req = requests.get(url, headers=headers, timeout=10)
			# should rewrite the filter condition
			if (req.headers['Access-Control-Allow-Credentials'] == 'true') and (req.headers['Access-Control-Allow-Origin'] == origin):
				print('response: {}'.format({'ACAC': req.headers['Access-Control-Allow-Credentials'], 'ACAO': req.headers['Access-Control-Allow-Origin']}), end='\n\n')
		except KeyError as e: # should add explicit exception handling
			print('Invalid key: {}'.format(e), end='\n\n')
		except Exception as e:
			print('unhandled exception: {}'.format(e), end='\n\n')
			



if __name__ == "__main__":
	file_name = sys.argv[1]
	with open(file_name) as f:
		for url in f:
			check_cors_implementation(url.strip())
