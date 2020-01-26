# -*-coding:Utf-8 -*
from bs4 import BeautifulSoup 
import urllib.request

#### A   P R O P O S ####################################################################################################################
# Suite à un echec d'implémentation d'une interface plus sexy, voilà la dernière version fonctionelle de mon code et son habillage cheap.
#
# Il dispose de plusieurs modes de jeu : 
#
#	EASY : où un petit résumé des pages de départ et d'arriver est affiché pour aider le joueur à avancer
#
#   REGULAR : où le joueur ne dispose que du nom de la page de départ et de la page cible pour s'en sortir avec les liens
#
#   HARD (HIDDEN) : mode caché qui se déclenchera si le joueur fait preuve d'insubordination dans son choix de mode de jeu. 
#					Dans celui-ci,  le joueur ne dispose que de cinq liens pour naviguer de page en page.
#
##########################################################################################################################################


### getContent
# Filtering all the content to get only the body of the page
###
def getContent(soup):
	for anchor in soup.find_all(True,{'class':'infobox_v3'}):
		anchor.decompose()
	for anchor in soup.find_all(True,{'class':'infobox_v2'}):
		anchor.decompose()
	for anchor in soup.find_all(True,{'class':'mw-editsection'}):
		anchor.decompose()
	for anchor in soup.find_all(True,{'class':'noprint'}):
		anchor.decompose()
	for anchor in soup.find_all(True,{'class':'references-small'}):
		anchor.decompose()
	for anchor in soup.find_all(True,{'class':'reference'}):
		anchor.decompose()
	for anchor in soup.find_all(True,{'class':'extiw'}):
		anchor.decompose()
	for anchor in soup.find_all(True,{'class':'external text'}):
		anchor.decompose()
	for anchor in soup.find_all(True,{'class':'wd_identifiers'}):
		anchor.decompose()
	for anchor in soup.find_all(True,{'class':'incomplet'}):
		anchor.decompose()
	for anchor in soup.find_all(True,{'class':'bandeau-article'}):
		anchor.decompose()
	for anchor in soup.find_all(True,{'class':'bandeau-article'}):
		anchor.decompose()
	for anchor in soup.find_all(True,{'class':'bandeau-article'}):
		anchor.decompose()
	for anchor in soup.find_all('small'):
		anchor.decompose()
	for anchor in soup.find_all('table'):
		anchor.decompose()
	for anchor in soup.find_all('li'):
		anchor.decompose()
	for anchor in soup.find_all(True,{'id':['toc']}):
		anchor.decompose()
	for anchor in soup.find_all(True,{'class':'mw-parser-output'}):
		filteredSoup = anchor
	return filteredSoup

### getTopic
# prints the first paragraph of the page
###
def getTopic(soup):
	topic = soup.p
	return str(topic.get_text())

### printLinks
# Print all links after filtering
# sets the list 'tag_list' from which we will navigate
###
def printLinks(i, cucurbitace):
	#HIDDEN HARD MODE
	if selectMode == 666:
		for anchor in cucurbitace.find_all('a', limit=5):
			if anchor.get_text():
				tag_list.append(str(anchor.get_text()))
				print(str(i)+" - "+str(anchor.get_text()))
				i += 1
	else:
		for anchor in cucurbitace.find_all('a'):
			if anchor.get_text():
				tag_list.append(str(anchor.get_text()))
				print(str(i)+" - "+str(anchor.get_text()))
				i += 1
	print("999 - GO BACK")

### getNextLink
# generates the link the user will be forwarded to using the index of the link 
# this link is first put to a temporary variable to format it before the redirection
###
def getNextLink(userChoice, tag_list):
	nextTemp = tag_list[userChoice]
	print(nextTemp)
	urlTemp = "https://fr.wikipedia.org/wiki/"+ str(nextTemp)
	return urlTemp

### formatURL
# formats the URL
# appends the next page to our history
###
def formatURL(urlTemp, histo_list):
	nextUrl = urlTemp.replace(' ','_').replace('é', 'e').replace('è', 'e').replace('à', 'a').replace('ó', 'o')
	print(nextUrl)
	histo_list.append(str(nextUrl))
	#print(histo_list)
	return nextUrl

### fwdSurf
# checks if the next URL is the goal URL, in which case the gameover will be launched
# navigate from page A to page B
###
def fwdSurf(nextUrl, urlGoal, numTour):
	if nextUrl == urlGoal:
		thanosSnapped(numTour)
		endGame = True
	else:
		webpage = urllib.request.urlopen(nextUrl).read()
		soup = BeautifulSoup(webpage, 'html.parser')
		return soup

### bwdSurf
# surfs from page B to page A using history's last entry
###
def bwdSurf(histo_list):
	lastVisit = histo_list[-1]
	print(lastVisit)
	return lastVisit

### thanosSnapped
# stops the game in case of gameover
###
def thanosSnapped(numTour):
	print("You won in "+str(numTour)+" turns !")

###################################
############# MAIN GAME ###########
###################################
urlStart = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
urlGoal = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"
nextUrl = "null"
tag_list = []
histo_list = []
i = 0
numTour = 0
endGame = False
#WEBPAGES
webpageStart = urllib.request.urlopen(urlStart).read()
webpageGoal = urllib.request.urlopen(urlGoal).read()
#SOUPS
soupGoal = BeautifulSoup(webpageGoal, 'html.parser')
soupStart = BeautifulSoup(webpageStart, 'html.parser')
soupTopicS = BeautifulSoup(webpageStart, 'html.parser')
soupTopicG = BeautifulSoup(webpageGoal, 'html.parser')

#TITLES
start = soupStart.find('h1',{'class':'firstHeading'})
goal = soupGoal.find('h1',{'class':'firstHeading'})

#FIRST SOUPS
selectMode = int(input("Enter 0 to play on easy mode (with topics displayed), enter 1 to play regular (without)"))
#HANDLING WRONT INPUT
try: 
	testMode = int(selectMode)
except ValueError:
	print("Thanks for choosing either 0 or 1")
if selectMode == 0:
	cucurbitace=getContent(soupStart)
	aubergine=getTopic(soupStart)
	chou=getTopic(soupGoal)
elif selectMode == 1:
	cucurbitace=getContent(soupStart)
	aubergine="REGULAR MODE"
	chou="REGULAR MODE"
else:
	print("For your insubordination, you get hard mode. You only have 5 links to navigate. Good luck.")
	cucurbitace=getContent(soupStart)
	aubergine = "HARD MODE"
	chou="HARD MODE"
	selectMode=666

#MAIN LOOP
while endGame == False:
	#LOUSY ATTEMPT AT DUMMY STYLE PRETTIFICATION
	print(" - - - - - - - - - - - - - - - - - - - - - - - -  ")
	print(" - - - - - - - - - - - - - - - - - - - - - - - -  ")
	print(" W i k i G a m e / the lousy edition")
	print(" - - - - - - - - - - - - - - - - - - - - - - - -  ")
	print(" - - - - - - - - - - - - - - - - - - - - - - - -  ")
	#DISPLAYS LAPS
	print("Lap number : "+ str(numTour))
	#ANOTHER LOUSY ATTEMPT AT DUMMY STYLE PRETTIFICATION
	print(" - - - - - - - - - - - - - - - - - - - - - - - -  ")
	#DISPLAYS START URL
	print("Start : "+str(start.get_text()))
	#DISPLAYS START TOPIC / OR MODE IF REGULAR
	print(" -> "+str(aubergine))
	#AND ANOTHER LOUSY ATTEMPT AT DUMMY STYLE PRETTIFICATION
	print(" - - - - - - - - - - - - - - - - - - - - - - - -  ")
	#DISPLAYS GOAL URL
	print("Goal : "+str(goal.get_text()))
	#DISPLAYS GOAL TOPIC / OR MODE IF REGULAR
	print(" ->  "+str(chou))
	#DO I NEED TO SAY IT AGAIN
	print(" - - - - - - - - - - - - - - - - - - - - - - - -  ")

	#GETS THE LINKS
	poireau = printLinks(i, cucurbitace)

	#PRINTS THE LINKS
	print(poireau)

	#USER INPUT FOR NEXT LINK
	userChoice=int(input("Next page?"))

	#REDIRECTS FORWARDS
	if userChoice != 999:
	#HANDLING OUT OF RANGE INPUT
		try:
			fraise = tag_list[userChoice]
		except IndexError:
			fraise = 'null'
			userChoice=int(input("Please enter a valid index"))
		carotte = getNextLink(userChoice, tag_list)
		print(carotte)
		tag_list.clear()
		i=0
		perruche = formatURL(carotte, histo_list)

	#REDIRECTS BACKWARDS 
	elif userChoice == 999:
		carotte = bwdSurf(histo_list)
		perruche = formatURL(carotte, histo_list)

	#REDIRECTS TO NEW PAGE
	jimbo = fwdSurf(perruche,urlGoal, numTour)

	#INCREMENTS LAP COUNT
	numTour += 1

	#GETTING NEW CONTENT
	if selectMode == 0:
		cucurbitace=getContent(jimbo)
		aubergine=getTopic(jimbo)
		chou=getTopic(jimbo)
	elif selectMode == 1:
		cucurbitace=getContent(jimbo)
		aubergine="REGULAR MODE"
		chou="REGULAR MODE"
	else:
		cucurbitace=getContent(jimbo)
		aubergine = "HARD MODE"
		chou="HARD MODE"
		selectMode=666