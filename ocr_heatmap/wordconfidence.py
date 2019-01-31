#requires at least one xml file in the same folder as the python script
#this script will create a text file with the same filename as each xml file in the directory
#and write the HPOS, VPOS and WC values to a .csv type output. 


from bs4 import BeautifulSoup
import glob, os
from tqdm import tqdm
xmllist = []
for file in glob.glob("*.xml"):
    xmllist.append(file)


for d in xmllist:
	infile = open(d, "r", encoding='utf-8')
	contents = infile.read()
	soup = BeautifulSoup(contents, 'xml')
	stringblock = soup.find_all('String')
	f = open(( d.rsplit( ".", 1 )[ 0 ] ) + ".txt", "w")
	for i in tqdm(range(len(xmllist))):	
		for s in stringblock:
		print(s['HPOS'],",",s['VPOS'],",",s['WC'], sep='', file = f)
