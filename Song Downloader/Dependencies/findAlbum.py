import urllib2
import sys
def getAlbumLink(albumName):
	searchLink = "http://www.allmusic.com/search/albums/"
	#Seperate the words to make a correct link
	words = albumName.rsplit(" ")
	link = "" #This will hold the link to the actual album
		  #Currently we're looking at a search page
	#Append the album title to where you want to search
	print("Looking up album")
	for word in words:
		searchLink += word
		searchLink += "%2B" #Constant allmusic.com uses
	#Get rid of the extra pesky %2B
	searchLink.rsplit("%2B")
	page = urllib2.urlopen(searchLink) 
	data = page.read()
	#Split up the html code line by line not byte by byte
	lines = data.rsplit("\n")
	#Loop throuh it
	for line in lines:
		if(line.find('href="http://www.allmusic.com/album/') != -1):
			#That means that this line has the link
			firstLetter = line.find('href="') + 6 #Six is length of href="
			while( True ):
				#Keep appending to the link until we reach the end, aka the "
				if(line[firstLetter] != '"'):
					#Append the letters to get the link
					link += line[firstLetter]
					firstLetter += 1
				else:
					break
			break #We got our link
			#print(link)
	findSongsinAlbum(link) #This will write all of the Song names to a tmp file
def findSongsinAlbum(albumLink):
	print("Finding songs in album")
	myfile = "/tmp/songsinalbum.txt" #Tmp file
	f = open(myfile, 'w')
	link = albumLink
	#print(link)
	page = urllib2.urlopen(link)
	data = page.read()
	songs = []
	found = False
	#Split up HTML code line by line
	lines = data.rsplit("\n")
	for line in lines:
            if(line.find('itemprop="url">') != -1):
                #find the end of the first link tag
                firstLetter = line.find('itemprop="url">') + 15 #Add one so you dont get the "<" in the titles name
                lastLetter = line.rfind("<")
                #find the start of the closing. Note, 35 is not random
                #But instead keeps us from getting the starting tag <a>
                title = line[firstLetter:lastLetter] #Get the song name
                #Get every title in the album
                songs.append(title)
                #print(title)
                #primary_link means its a song in the album
		
	for song in songs:
		f.write(song) #Write each song to the file 
		f.write("\n") #Seperate them by a "\n"
#
#
#Part that will be run
albumName = ""
#First arg is the path of this file so we don't want it
for i in range(1, len(sys.argv)):
                albumName+=sys.argv[i] + " "
#otherwise lets look up the album name with its name AND the artist making it
#much more likely to find the right album
getAlbumLink(albumName)
