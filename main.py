import sys
import gzip
import urllib
import StringIO
import xmlrpclib

BLACKLIST = [ 'anal', 'anus', 'arse', 'ass', 'asshole', 'assfucker', 'ballsack', 'balls', 'bastard', 'bitch', 'biatch', 'bloody', 'blowjob', 'bollock', 'bollok', 'boner', 'boob', 'bugger', 'bum', 'butt', 'buttplug', 'clitoris', 'cock', 'coon', 'crap', 'cunt', 'damn', 'dick', 'dildo', 'dyke', 'fag', 'feck', 'fellate', 'fellatio', 'felching', 'fuck', 'fucker', 'fucking', 'fudgepacker', 'flange', 'goddamn', 'hell', 'homo', 'jerk', 'jizz', 'labia', 'muff', 'nigger', 'nigga', 'penis', 'piss', 'poop', 'prick', 'pube', 'pussy', 'queer', 'scrotum', 'sex', 'shit', 'slut', 'tit', 'tosser', 'turd', 'twat', 'vagina', 'wank', 'whore' ]

if len(sys.argv) != 2:
	print "Swear expects exactly one argument. (Movie name)"
	sys.exit(-1)

openSubs = xmlrpclib.Server('https://api.opensubtitles.org/xml-rpc')
token = openSubs.LogIn('', '', 'en', 'OSTestUserAgent')

if token['status'] == '200 OK':
	token = token['token']

movieQueryResult = openSubs.SearchMoviesOnIMDB(token, sys.argv[1])

if movieQueryResult['status'] == '200 OK':
	n = len(movieQueryResult['data'])
	
	if n == 1:
		print 'Found one title based on the given query.'
		print movieQueryResult['data'][0]['title']
		option = raw_input('Is this the title you are looking for? (Y/N)')
		
		if option == 'Y' or option == 'y':
			
		else:
			print 'Can\'t find any other title. Please change your query'
			sys.exit(-2)
	
	if n > 1:
		print 'Found the following partial matches'
		
		for _ in xrange(0, len(movieQueryResult['data'])):
			print '{} - {}'.format(_ + 1, movieQueryResult['data'][_]['title'].encode('ascii', 'ignore'))
		
		option = raw_input('Select a title.')
		
		if option.isdigit():
			option = int(option)
			
			if option > 0 and option < len(movieQueryResult['data']):
				print 'Selected {}, downloading subtitles now...'.format(movieQueryResult['data'][option - 1]['title'])
				
				IMDB_ID = movieQueryResult['data'][option - 1]['id']
				
				subsResult = openSubs.SearchSubtitles(token, [{ 'sublanguageid': 'eng', 'imdbid': IMDB_ID }])
				
				if subsResult['status'] == '200 OK':
					link = max([(x['SubDownloadsCnt'], x['SubDownloadLink']) for x in subsResult['data']])[1]
				
				content = gzip.GzipFile(fileobj = StringIO.StringIO(urllib.urlopen(link).read())).read().lower()
				
				for word in BLACKLIST:
					print '{} - {}'.format(word, content.count(" " + word + " "))
			
			else:
				print 'Cannot find any other results. Please change your query.'
				sys.exit()
		else:
			print 'Invalid option, exiting.....'
			sys.exit()
		
else:
	print 'Cannot'
