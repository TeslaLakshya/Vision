import urllib.request

x = input("Give the mispelled word : ")
url = "http://www.google.com/search?q=" + x
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req)
page_source = response.read()
page_source_str = page_source.decode('utf-8')
#start = page_source_str.find('spellcheck') + len('spellcheck') + 2
#end = page_source_str.find(r'"', start)
#print(page_source_str[start : end])
dym = page_source_str.find('Did you mean')
srf = page_source_str.find('Showing results for')
if dym != -1 :
	start = page_source_str.find('<b><i>', dym) + len('<b><i>')
	end = page_source_str.find('<', start)
	print(page_source_str[start : end])
elif srf != -1 :
	start = page_source_str.find('function(){var q=', srf) + len('function(){var q=') + 1
	end = page_source_str.find(r"'", start)
	print(page_source_str[start : end])
else : 
	print('The word is not mispelled')