import sys
import urllib2
import math
def getSongLink(name, song):
        searchLink = "http://www.allmusic.com/search/songs/"
        #Seperate the words to make a correct link
   	words = song.rsplit(" ")
	allWords = name.rsplit(" ")
        link = "http://allmusic.com" #This will hold the link to the actual album
                  #Currently we're looking at a search page
        #Append the album title to where you want to search
        #print("Looking up album")
        for word in words:
                searchLink += word
                searchLink += "%2B" #Constant allmusic.com uses
        #Get rid of the extra pesky %2B
        #searchLink = searchLink.rsplit("%2B")
        #print(searchLink)
	page = urllib2.urlopen(searchLink)
        data = page.read()
        #Split up the html code line by line not byte by byte
        lines = data.rsplit("\n")
        #Loop throuh it
        artists = []
        links = []
        lastLine = "" #Holds value of last line
        for line in lines:
                #print(line)
                if(line.find('href="/song/') != -1):
			#print(line)
			#That means that this line has the link
                        firstLetter = line.find('href="') + 6 #Six is length of href="
                        #Here we get the Artist name (we want the right version of the song lol)
                        firstChar = lastLine.find("by ") + 3
                        lastChar = lastLine.find('"', firstChar)
			artists.append(lastLine[firstChar:lastChar].upper())
                        #Now its added to the array which will be searched!
                        while( True ):
                                #Keep appending to the link until we reach the end, aka the "
                                if(line[firstLetter] != '"'):
                                        #Append the letters to get the link
                                        link += line[firstLetter]
                                        firstLetter += 1
                                else:
                                        links.append(link)
                                        link = "http://allmusic.com"
                                        break
                lastLine = line
        #Here lets find the right link to the right song
        index = 0
        ratios = []
        for artist in artists:
                name = name.upper()
                artistWords = artist.rsplit(" ")
                numRight = 0
                numWords = 0
                for word in artistWords:
                        numWords += 1
                        if(name.find(word) != -1):
                                numRight += 1
                if(numWords == numRight):
       			val = findTimeForSong(links[index])
			try:
				a = int(val)
				return val
			except:
				ratios.append(0)
				index += 1
		        #return findTimeForSong(links[index])
                        #We've got the perfect one
                #print("ME")
		else:
			ratios.append(numRight / numWords)
                	index += 1
	order = []
	while( True ):
		index = 0
		max = 0
		maxIndex = 0
		#Here we will fill out order
		for i in ratios:
			if(i > max):
				if(findInOrder(order, index)):
					pass
				else:
					maxIndex = index
					max = i
			index += 1
		if(max == 0):
			 break
		else:
			order.append(maxIndex)
	time = "" 
	for i in range(0, len(order) - 1):
		time = findTimeForSong(links[order[i]])
			#If we got a good value for time :)
		print(i)
		print(time)
		try:
			tmp = int(time)
			break
		except:
			#We have a bad value for time
			continue
	
	try:
		tmp = int(time)
	except:
		time = 10000000	
	return time
def findInOrder(order, num):
	for i in order:
		if(i == num):
			return True
	return False

def findTimeForSong(link):
	#Finds the actual length of a song
        page = urllib2.urlopen(link)
        data = page.read()
        lines = data.rsplit("\n")
        for line in lines:
             #print(line)   
	     if(line.find('class="time"') != -1):
		        firstLetter = line.find("data-sort-value") + 17
                        lastLetter = firstLetter + 4
                        time = line[firstLetter] + line[firstLetter + 2:lastLetter]
                        #print(time)
			return time

#This will pick the best youtube video to download
def compareTitles(possibleTitles, titles, string, times, song):     
  	#First lets get the length of the song running the whole findTime sequence 
	actualTime = int(getSongLink(string, song))
	actualTime = (actualTime % 100) + ((actualTime // 100) * 60)
	#print("AC")
	#print(actualTime)
	#
       	numWords = 0
	#split up the words input by word to be put in the search form
	#properly
        words = string.rsplit(" ")
        for word in words:
                numWords = numWords + 1
        #Allows us to see how many words are in the title
        #which will be used when seeing how good a video option each is
	currVid = 0 #Will help us find which video we want by storing the best
        for vid in titles:
                numWordsRight = 0 #Will hold the number of words from our searchthat are in the video title
                vid = vid.upper()
		string = string.upper()
		for word in words:
                        #Uppercase comparisons to make uncase sensitive
                        #vid = vid.upper()
                        word = word.upper()
                        #Look for search word in video title
                        if(vid.find(word) != -1):
                                numWordsRight = numWordsRight + 1
                #See if the song were looking for is a remix
                if(string.find("REMIX") == -1):
                        #If it isnt, make sure that the video isnt a remix either
                        if(vid.find("REMIX") != -1):
                                numWordsRight = numWordsRight - 3 
				#If it is a remix we'll reduce its value arbitraily
                #We don't really want live versions either since they're annoying
		if(string.find("LIVE") == -1):
                        #If it isnt wanted, make sure that the video isnt live either
                        if(vid.find("LIVE") != -1):
                                numWordsRight = numWordsRight - 3
		if(string.find("CLEAN") == -1):
                        #If it isnt wanted, make sure that the video isnt clean either
                        if(vid.find("CLEAN") != -1):
                                numWordsRight = numWordsRight - 2 
				#No one wants a clean version...
		#Decrease the want of videos that have bad times
		#This is to say no to videos with talking, pauses, etc
		#One extra case below sometimes, better save the error
		try:
			timeDiff = math.fabs(actualTime - times[currVid])
		except:
			timeDiff = 21
		if(timeDiff > 100000):
			pass
			#This means that the length of the video couldn't be found
			#Thus we won't do anything
			#Unless theres a youtube video thats over 1000 minutes long in which case, oops
		elif(timeDiff > 15):
			numWordsRight -= 3
		elif(timeDiff > 5):
			numWordsRight -= 2
		elif(timeDiff > 3):
			numWordsRight -= 1
		#Now we compare
		if(numWordsRight == numWords):
                        #All of the search words are in the video title
                        return currVid #This could not be the best if there are extra words
				       #Not an issue worth dealing with as this works fine
                #If you dont break immeadiatly, save your options so you can later choose the best one
                possibleTitles.append(numWordsRight) #Its index will be used to refer to the title
                currVid = currVid + 1
        #If no option is perfect, find the best option
        max = 0
        maxIndex = 0
        index = 0
        for i in possibleTitles:
                if(i > max):
                        maxIndex = index
                        max = i
                index = index + 1
	#store the best index and then we return
	
        #Give a warning on bad performance
        if( max < numWords * 1 / 4):
                print("This title was hard to find and might be downloading the wrong song")
                print("Check your spelling")
                print("Downloading anyways")
        return maxIndex

def lookupYoutube(string, song, pick = True):
	#Make it a proper search link
        words = string.rsplit(" ")
        link = "http://www.youtube.com/results?client=safari&rls=en&q="
        for each in words:
         	link += each + "+"
        link = link.rstrip('+') #Get rid of the pesky extra +
        link += "&oe=UTF-8&um=1&ie=UTF-8&sa=N&tab=w1" #Add the ending part
        page = urllib2.urlopen(link)
	data = page.read()
        currLine = "" #will hold the current tag line
        inTag = False
        inVideo = False
        vidLink = ""
        num = 1
        links = []
        titles = []
	times = []
	#NOTE: Read through in a byte by byte manner
	currTime = ""
 	inTime = False
        for line in data:
		if(inTime):
			currTime += line	
                if(line == "<"):
			if(inTime == True):
				currTime = currTime.rstrip("<")
				currTime = currTime.replace(":", "")
				#print(currTime)
				try:
					Time = int(currTime)
				#	print(Time)
					Time = (Time % 100) + ((Time // 100) * 60) #In seconds
				except:
					Time = 0
				#print(Time)
				times.append(Time)
				currTime = ""
				inTime = False
                        inTag = True
                if(inTag):
                        currLine += line
                if(inVideo):
                        vidLink += line
                if(line == ">"):
                        if(inVideo):
                                watch = "youtube.com"+vidLink[vidLink.find('/watch'):]
                                watch = watch.rstrip('">')
                                title = vidLink[vidLink.find("title=") + 7:vidLink.find("data-sessionlink") - 2]
                      		
				links.append(watch)
                                titles.append(title)
                                inVideo = False
                                vidLink = ""
                                num += 1
			#Once we reach the end of the line we look to see if it was a vid link
                        if(currLine.find('h3 class="yt-lockup2-title"') != -1):
				#if it is!
                                inVideo = True
			if(currLine.find('class="video-time"') != -1):
				inTime = True
                        currLine = ""
                        inTag = False
        input = 2 #Will be used to choose which vid to return
		  #Titled input because for a long time this wasn't automatic!
        if(pick):
		#THIS IS THE -noauto ARGUMENT IN FRUITION, started out as an -auto option interestingly enough
                num = 0
                for title in titles:
                        num = num + 1
                        print(str(num) + " " + title)
                #Give a nice output if they are picking
                while(True):
                        input = raw_input("Pick a video: ")
                        try:
                                input = int(input)
                                if(input <= num):
                                        input = input - 1
                                        break
                        except:
                                pass
                        #Empty except statement
        else:
                possibleVideos = []
                #compare titles returns the most matching of videos
		bestVid = compareTitles(possibleVideos, titles, string, times, song)
                print("Downloading Video: "+titles[bestVid])
                input = bestVid
	#Will be returned and written to a tmp for use by getmemusic 
        return links[input]
#Figure out the inputs to go into lookupYoutube
myfile = "/tmp/youtubelink.txt"
f = open(myfile, 'w')
line = ""
song = ""
index = 0
middleIndex = 0
for a in range(1, len(sys.argv)):
	#print(sys.argv[a])
	if( sys.argv[a] == ":" ):
		middleIndex = index	
	index += 1 
for a in range(middleIndex + 2, len(sys.argv)):
	song += sys.argv[a] + " "
song = song.rstrip(" ")
#print(sys.argv[middleIndex])
if(sys.argv[middleIndex] == "-auto"):
	#print("auto")
	for i in range(1, middleIndex):
		line+=sys.argv[i] + " "
	link = lookupYoutube(line, song, False)
else:
	for i in range(1, middleIndex + 1):
		line+=sys.argv[i] + " "
	link = lookupYoutube(line, song, True)
f.write(link)
