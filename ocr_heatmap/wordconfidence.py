#writes the coordinates and word confidence scores to a text file

from bs4 import BeautifulSoup


infile = open("filename.xml","r")
#change to the name of the ALTO xml file

contents = infile.read()
soup = BeautifulSoup(contents, 'xml')
stringblock = soup.find_all('String')
log = open("coordinates_confidence.txt", "w")
for s in stringblock:
	print(s['HPOS'],",",s['VPOS'],",",s['WC'], sep='', file = log)
