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

def get_label_mappings(wiki_id_paths, languages):
	#languages = ['de', 'es']
	translations = {}
	for wiki_id_path in wiki_id_paths.split('\n'):
		wiki_id = os.path.basename(wiki_id_path)
		language_translations = {}
		query = 'https://www.wikidata.org/w/api.php?action=wbgetentities&ids=%s&format=json&props=labels' %(wiki_id)
		#print query
		response = urllib2.urlopen(query)
		data = json.load(response)
		#print data['entities'][wiki_id]['labels']['de']
		#print data['entities'][wiki_id]['labels']['es']
		try:
			for language in languages:
				language_translations[language]= []
				if data['entities'][wiki_id]['labels'].has_key(language):
					if data['entities'][wiki_id]['labels'][language].has_key('value'):
						language_translations[language].append(data['entities'][wiki_id]['labels'][language]['value'])
						
		except Exception as err:
			print 'wiki_id', err, wiki_id_paths
		translations[wiki_id_path] = language_translations
	print wiki_id_paths, translations
	return translations	


def get_language_mappings(filename):
	out_filename = filename.replace('.csv', '_trans.csv')
	print out_filename
	
	writer = csv.writer(open(out_filename, 'w'))
	wheader = ['mid', 'disc_en', 'wikidata_id', 'german', 'spanish']
	writer.writerow(wheader)
	reader = csv.reader(open(filename, 'rb'))
        header= reader.next()

	target_languages= ['de', 'es']
	count = 0
	for row in reader:
		#print count, row[2]
		nrow = [row[0], row[1], row[2]]
		count+=1
		if row[2].strip() == '':
			writer.writerow(nrow)
			continue
		id_translations = get_label_mappings(row[2], target_languages)
		print row[0], row[1], id_translations
		for language in target_languages:
			lang_data = []
			for wid in row[2].split('\n'):
				language_translations = id_translations[wid]
				if language_translations.has_key(language):
					trans = ':'.join(language_translations[language])
				else:
					trans = ''
				lang_data.append(trans)
			nrow.append('\n'.join(lang_data))
		writer.writerow(nrow)
		if count%100 == 0:
			print 'Count', count	
		#time.sleep(1)
	return

	
if __name__ == '__main__':
	filename = '../data/dict.csv'

	wiki_id_paths = 'http://www.wikidata.org/entity/Q37859'
	get_label_mappings(wiki_id_paths, ['en', 'de', 'es', 'fr'])

	#wiki_id_filename = filename.replace('.csv', '_wikiid.csv')
	#get_language_mappings(wiki_id_filename)
