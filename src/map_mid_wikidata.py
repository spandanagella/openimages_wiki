import csv
import os
import urllib2
import urllib
import requests
import json
import time
import hashlib
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_wikidata_id(mid):
	query = 'https://query.wikidata.org/sparql?query=SELECT * WHERE {?s wdt:P646 "%s" }&format=json' %(mid)
	#print query
	#query = urllib.quote(query, safe=":/")
	query = query.replace(' ','%20')
	#print query
	response = urllib2.urlopen(query)
	data = json.load(response)
	try:
		values = []
		#print data['results']['bindings']
		for binding in data['results']['bindings']: #[0]['s']['value']
			#print binding
			if binding.has_key('s') and binding['s'].has_key('value'):
				values.append(binding['s']['value'])
		value = '\n'.join(values)
	except Exception as err:
		#print err
		#print 'Exception', mid
		value = ''
	#print data
	return value
	


def get_mid_data(filename):
	out_filename = filename.replace('.csv', '_wikiid.csv')
	print out_filename
	#return 
	#writer = csv.writer(open('../data/dict_wikiid.csv', 'w'))
	writer = csv.writer(open(out_filename, 'w'))
	header = ['mid', 'disc_en', 'wikidata_id']
	writer.writerow(header)
	reader = csv.reader(open(filename, 'r'))
        header= reader.next()
        label_stem = {}
	count = 0
        for row in reader:
		#if '/g' in row[0]:
		#	continue
                #freebase_id, desc
                desc_en = row[1].strip()
		mid = row[0].strip()
		value = get_wikidata_id(mid)
		writer.writerow([row[0], row[1], value])
		count +=1
		print count, mid, value
		if count%100 == 0:
			print 'Finished 100'
			break
		time.sleep(1)


def get_image_name(data):
	image_names = []
	try:
		image_name = data["claims"]["P18"][0]["mainsnak"]["datavalue"]["value"]
	except:
		image_name = None
	return image_name
	
def get_images_for_wikidata(in_filename, out_filename):
	writer = csv.writer(open(out_filename, 'w'))
	wheader = ['mid', 'disc_en', 'wikidata_id', 'image_url']
	writer.writerow(wheader)
	reader = csv.reader(open(in_filename, 'rb'))
        header= reader.next()
	for row in reader:
		nrow = row + []
		if len(row)>=3:
			wiki_id = os.path.basename(row[2])
			query = 'https://www.wikidata.org/w/api.php?action=wbgetclaims&entity=%s&property=P18&format=json' %(wiki_id)
			response = urllib2.urlopen(query)
		        data = json.load(response)
			image_name = get_image_name(data)	
			if image_name is not None:
				#image_url = 'https://commons.wikimedia.org/wiki/File:%s' %(image_name.replace(' ', '_'))
				image_name = image_name.replace(' ', '_')
				#m = hashlib.md5()
				#m.update(image_name)
				#mhex = m.hexdigest()
				#image_url = 'https://upload.wikimedia.org/wikipedia/commons/%s/%s%s/%s' %(mhex[0],mhex[0],mhex[1],image_name)
				#nrow.append(image_url)
				nrow.append(image_name)
				print nrow
				#break
		#else:
		#print nrow
		writer.writerow(nrow)

if __name__ == '__main__':
	#filename = '../data/dict.csv'

	print get_wikidata_id('/m/012047')
	#filename = '../data/class-descriptions.csv'
	#get_mid_data(filename)
