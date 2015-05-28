import sys
import gzip
import urllib
import StringIO
import xmlrpclib

BLACKLIST = [ 'anal', 'anus', 'arse', 'ass', 'asshole', 'assfucker', 'ballsack', 'balls', 'bastard', 'bitch', 'biatch', 'bloody', 'blowjob', 'bollock', 'bollok', 'boner', 'boob', 'bugger', 'bum', 'butt', 'buttplug', 'clitoris', 'cock', 'coon', 'crap', 'cunt', 'damn', 'dick', 'dildo', 'dyke', 'fag', 'feck', 'fellate', 'fellatio', 'felching', 'fuck', 'fucker', 'fucking', 'fudgepacker', 'flange', 'goddamn', 'hell', 'homo', 'jerk', 'jizz', 'labia', 'muff', 'nigger', 'nigga', 'penis', 'piss', 'poop', 'prick', 'pube', 'pussy', 'queer', 'scrotum', 'sex', 'shit', 'slut', 'tosser', 'turd', 'twat', 'vagina', 'wank', 'whore' ]

def downloadAndRate(movie):
	
	print 'Selected {}, downloading subtitle...'.format(movie['title'])
	
	subsResult = openSubs.SearchSubtitles(token, [{ 'sublanguageid': 'eng', 'imdbid': movie['id'] }])
	
	if subsResult['status'] == '200 OK' and subsResult['data'] != False:
		link = max([(x['SubDownloadsCnt'], x['SubDownloadLink']) for x in subsResult['data']])[1]
	
	else:
		print 'Can\'t find subtitles for the given title.'
		sys.exit(-9)
	
	content = gzip.GzipFile(fileobj = StringIO.StringIO(urllib.urlopen(link).read())).read().lower()
	
	count = { word : content.count(word) for word in BLACKLIST if content.count(word) }
	
	if count:
		for w in count.keys():
			print '{} - {} time(s)'.format(w, count[w])
	
	else:
		print 'Movie is clean...probably. :)'
	
	openSubs.close()
	sys.exit(0)

if len(sys.argv) != 2:
	print "Swear expects exactly one argument. (Movie name)"
	sys.exit(-1)

openSubs = xmlrpclib.Server('https://api.opensubtitles.org/xml-rpc')

try:
	token = openSubs.LogIn('', '', 'en', 'OSTestUserAgent')
	
	if token['status'] == '200 OK':
		token = token['token']
	
	else:
		print 'Please check the UserAgent provided.'
		sys.exit(-2)
	
	movieQueryResult = openSubs.SearchMoviesOnIMDB(token, sys.argv[1])
	
	if movieQueryResult['status'] == '200 OK':
		if movieQueryResult['data'] == False:
			print 'Can\'t find any titles for the given query!'
			sys.exit(-3)
		
		movieQueryResult['data'] = [_ for _ in movieQueryResult['data'] if '(TV Series)' not in _['title'] and '(Video Game)' not in _['title']]
		n = len(movieQueryResult['data'])
		
		if n == 1:
			print movieQueryResult
			print 'Found one title based on the given query.'
			print movieQueryResult['data'][0]['title']
			option = raw_input('Is this the title you are looking for? (Y/N)')
			
			if option == 'Y' or option == 'y':
				downloadAndRate(movieQueryResult['data'][0])
			else:
				print 'Can\'t find any other title. Please change your query'
				sys.exit(-4)
		
		if n > 1:
			print 'Found the following partial matches'
			
			for _ in xrange(0, n):
				print '[{}] {}'.format(_ + 1, movieQueryResult['data'][_]['title'].encode('ascii', 'ignore'))
			
			option = raw_input('Select a title: ')
			
			if option.isdigit():
				option = int(option)
				
				if option > 0 and option < len(movieQueryResult['data']):
					downloadAndRate(movieQueryResult['data'][option - 1])
				else:
					print 'Cannot find any other results. Please change your query.'
					sys.exit(-5)
			else:
				print 'Invalid option, exiting.....'
				sys.exit(-6)
			
	else:
		print 'Movie query failed. Please try again later.'
		sys.exit(-7)
	
except Exception as e:
	if e.strerror == 'Name or service not known':
		print 'Invalid XMLRPC url.'
		sys.exit(-8)
	
	else:
		print 'Something went wrong! Please try again later.'
		sys.exit(-9)