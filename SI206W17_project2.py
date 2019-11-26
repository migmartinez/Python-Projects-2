## SI 206 W17 - Project 2 

## 
##  Miguel Martinez
## This program will grab five tweets using the Tweepy API using certain keywords.



## Import statements
import unittest
import json
import requests
import tweepy
import twitter_info # Requires you to have a twitter_info file in this directory
import re
import codecs
from bs4 import BeautifulSoup

## Tweepy authentication setup
## Fill these in in the twitter_info.py file
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up to be able grab stuff from twitter with your authentication using Tweepy methods, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())




CACHE_FNAME = "206project2_caching.json"
try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}



def find_urls(url_string):
	pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))*"
	urls = re.findall(pattern, url_string)
	return urls

 
def get_umsi_data():
	unique_identifier = "umsi_directory_data"
	if unique_identifier in CACHE_DICTION:
		print('retreiving UMSI directory data from local disk')
		print('\n')
		umsi = CACHE_DICTION[unique_identifier]
		return umsi
	else:
		umsi_directory_data = []
		print('retreiving UMSI directory data from the web')
		for i in range(12):
			page = "https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All&page={}".format(i)
			results = requests.get(page, headers = {'User-Agent': 'SI_CLASS'})
			umsi_directory_data.append(results.text)
			CACHE_DICTION[unique_identifier] = umsi_directory_data
			f = open(CACHE_FNAME,'w')
			f.write(json.dumps(CACHE_DICTION))
			f.close()
		return umsi_directory_data



 of Information"...
umsi_titles = {}
for i in get_umsi_data():
	soup = BeautifulSoup(i,"html.parser")
	people = soup.find_all("div",{"class":"views-row"})
	for x in people:
		names = x.find("div",{"class":"field-item even", "property":"dc:title"})
		titles = x.find("div",{"class":"field field-name-field-person-titles field-type-text field-label-hidden"})
		umsi_titles[names.text] = titles.text


def get_five_tweets(search):
	unique_identifier = "twitter_{}".format(search)
	if unique_identifier in CACHE_DICTION:
		print('retreiving search term for cache: ', search)
		print('\n')
		twitter_results = CACHE_DICTION[unique_identifier]
	else:
		print('getting new data for search term: ', search)
		print('\n')
		twitter_results = api.search(q=search)
		CACHE_DICTION[unique_identifier] = twitter_results
		f = codecs.open(CACHE_FNAME, 'w', encoding = 'utf-8')
		f.write(json.dumps(CACHE_DICTION))
		f.close()
	tweets = []
	for tweet in twitter_results['statuses']:
		tweets.append(tweet['text'])
	return tweets[0:5]




five_tweets = get_five_tweets("University of Michigan")




tweet_urls_found = ()
for tweet in five_tweets:
	link = (find_urls(tweet))
	if link:
		tweet_urls_found = tweet_urls_found + tuple(link)	

########### TESTS; DO NOT CHANGE ANY CODE BELOW THIS LINE! ###########

class CachingTests(unittest.TestCase):
	def test_cache_diction(self):
		self.assertEqual(type(CACHE_DICTION),type({}),"Testing whether you have a CACHE_DICTION dictionary")
	def test_cache_file(self):
		f = open("206project2_caching.json","r")
		s = f.read()
		f.close()
		self.assertEqual(type(s),type(""),"Doesn't look like you have a cache file with the right name / with content in it")
	def test_cache_data(self):
		f = open("206project2_caching.json","r")
		s = f.read()
		f.close()
		jv = json.loads(s)
		self.assertTrue("umsi_directory_data" in jv, "Checking whether the UMSI data identifier is in the data in the cache file, formatted properly")
	def test_cache_data2(self):
		f = open("206project2_caching.json","r")
		s = f.read()
		f.close()
		jv = json.loads(s)
		self.assertTrue("twitter_University of Michigan" in jv, "Checking whether the Twitter University of Michigan identifier is correctly in the cache")

class PartOne(unittest.TestCase):
	def test_findurls_oneurl(self):
		self.assertEqual(find_urls("http://www.google.com is a great site"),["http://www.google.com"])
	def test_findurls_multurls(self):
		self.assertEqual(find_urls("I love looking at websites like http://etsy.com and http://instagram.com and lol.com and stuff"),["http://etsy.com","http://instagram.com"])
	def test_findurls_multurls_all(self):
		self.assertEqual(find_urls("I love looking at websites like http://etsy.com and http://instagram.com and https://www.bbc.co.uk and stuff"),["http://etsy.com","http://instagram.com","https://www.bbc.co.uk"])
	def test_findurls_none(self):
		self.assertEqual(find_urls("the internet is awesome #worldwideweb"),[])

class PartTwo(unittest.TestCase):
	def test_list_len(self):
		self.assertEqual(len(get_umsi_data()),12,"Testing the length of the list returned from get_umsi_data")
	def test_list_type(self):
		self.assertEqual(type(get_umsi_data()),type([]))
	def test_begin_of_list(self):
		self.assertEqual(get_umsi_data()[0][:100],"""<!DOCTYPE html>
<!--[if IEMobile 7]><html class="iem7"  lang="en" dir="ltr"><![endif]-->
<!--[if lte""", "Testing the beginning of the first element of the return value of get_umsi_data")
	def test_part_of_list(self):
		self.assertEqual(get_umsi_data()[4][500:512],"""c: http://pu""")
	def test_umsi_titles_len(self):
		self.assertEqual(len(umsi_titles.keys()),235)
	def test_umsi_titles_content(self):
		self.assertEqual(sorted(umsi_titles.keys()),['Adrienne Nwachukwu', "Alaina O'Connor", 'Alexandra Haller', 'Alicia Baker', 'Alissa Centivany', 'Alissa Talley-Pixley', 'Allan Martell', 'Allen Flynn', 'Allison Sweet', 'Allison Tyler', 'Amanda Ciacelli', 'Andrea Barbarin', 'Andrea Daly', 'Andy Wright', 'Anna Thompson', 'Annie Knill', 'Aprille McKay', 'Ayse Buyuktur', 'Barbara Smith', 'Barry Fishman', 'Ben Armes', 'Bradley Iott', 'Caitlin Holman', 'Carl Haynes', 'Carl Lagoze', 'Carol Moser', 'Carolyn Frost', 'Carolyn Gregurich', 'Casey Pierce', 'Catherine Robinson', 'Celia Riecker', 'Ceren Budak', 'Chanda Phelan', 'Charles Friedman', 'Charles Severance', 'Chen Wang', 'Cheng Li', 'Chris Teplovs', 'Christian Sandvig', 'Christopher Brooks', 'Chuan-Che Huang', 'Cindy Kaiying Lin', 'Claudia Leo', 'Clifford Lampe', 'Colleen Van Lent', 'Corey Turner', 'Craig Johnson', 'D TenBrink', 'Danaja Maldeniya', 'Daniel Atkins III', 'Daniel Klyn', 'Daniel Romero', 'Daphne Chang', 'David Hanauer', 'David Hessler', 'David Wallace', 'David Young', 'Deborah Apsley', 'Desmond Patton', 'Devon Keen', 'Douglas Van Houweling', 'Dragomir Radev', 'Earnest Wheeler', 'Edward Happ', 'Edward Platt', 'Elena Godin', 'Elizabeth Kaziunas', 'Elizabeth Whittaker', 'Elizabeth Yakel', 'Elliot Soloway', 'Erik Hofer', 'Erin Krupka', 'Evan Hoye', 'Eytan Adar', 'Fangzhou Zhang', 'Florian Schaub', 'Francis Blouin Jr', 'Gary Olson', 'Gaurav Paruthi', 'George Furnas', 'George Sprague', 'Glenda Bullock', 'Grace YoungJoo Jeon', 'Hariharan Subramonyam', 'Harmanpreet Kaur', 'Heather Newman', 'Heeryung Choi', 'Heidi Skrzypek', 'Helen Severino', 'Iman Yeckehzaare', 'Iris Gomez-Lopez', 'Jaclyn Cohen', 'Jacques Chestnut', 'James Duderstadt', 'James Hilton', 'Jasmine Jones', 'Jean Hardy', 'Jeff Stern', 'Jeffrey MacKie-Mason', 'Jeremy York', 'Jessica Litman', 'Jiaqi Ma', 'Jo Angela Oehrli', 'Joan Durrance', 'Joanna Kroll', 'Jocelyn Webber', 'Jodee Jernigan', 'Joey Hsiao', 'John Leslie King', 'John Lockard', 'Jonathan Brier', 'Joyojeet Pal', 'Judith Olson', 'Judy Lawson', 'Julia Adler-Milstein', 'Jumanah Saadeh', 'Kanda Fletcher', 'Karen Markey', 'Katherine Lawrence', 'Kathryn Ross', 'Katie Dunn', 'Kelly Iott', 'Kelly Kowatch', 'Kentaro Toyama', 'Kevyn Collins-Thompson', 'Kristin Fontichiaro', 'Kyle Swanson', 'Laura Elgas', 'Laurence Kirchmeier', 'Leah Brand', 'Lia Bozarth', 'Lija Hogan', 'Lindsay Blackwell', 'Linfeng Li', 'Linh Huynh', 'Lionel Robert', 'Lorraine Buis', 'Lynn Johnson', 'Margaret Hedstrom', 'Margaret Levenstein', 'Mark Ackerman', 'Mark Newman', 'Mark Thompson-Kolar', 'Markus Mobius', 'Marsha Antal', 'Martha Pollack', 'Matthew Kay', 'Maurita Holland', 'Megh Marathe', 'Melissa Chalmers', 'Melissa Levine', 'Michael Hess', 'Michael Nebeling', 'Michael Shallcross', 'Michael Williams', 'Mohamed Abbadi', 'Nancy Benovich Gilby', 'Nayiri Mullinix', 'Nickie Rowsey', 'Nicole Ellison', 'Padma Chirumamilla', 'Paige Nong', 'Patricia Garcia', 'Paul Conway', 'Paul Courant', 'Paul Edwards', 'Paul Resnick', 'Pei-Yao Hung', 'Penny Trieu', 'Perry Samson', 'Predrag Klasnja', 'Priyank Chandra', 'Qiaozhu Mei', 'Rachael Wiener', 'Rasha Alahmad', 'Rayoung Yang', 'Rebecca Frank', "Rebecca O'Brien", 'Rebecca Pagels', 'Reginald Beasley', 'Ridley Jones', 'Rohail Syed', 'Ryan Burton', 'Samone Williams', 'Samuel Carton', 'Sangseok You', 'Sarah Argiero', 'Sarita Yardi Schoenebeck', 'Scott Staelgraeve', 'Seyram Avle', 'Shannon Zachary', 'Sheryl Smith', 'Shevon Desai', 'Shiqing (Licia) He', 'Shiyan Yan', 'Shriti Raj', "Sile O'Modhrain", 'Silvia Lindtner', 'Sonia Raheja', 'Soo Young Rieh', 'Sophia Brueckner', 'Stacy Callahan', 'Stephanie Teasley', 'Steve Oney', 'Sun Young Park', 'Sungjin Nam', 'T Charles Yun', 'Tamy Guberek', 'Tanya Rosenblat', 'Tawanna Dillahunt', 'Tawfiq Ammari', 'Teng Ye', 'Theodore Hanss Jr', 'Thomas Finholt', 'Thomas Slavens', 'Tiffany Veinot', 'Todd Ayotte', 'Todd Stuart', 'Tonya McCarley', 'Tsuyoshi Kano', 'VG Vinod Vydiswaran', 'Vadim Besprozvany', 'Veronica Falandino', 'Victor Rosenberg', 'Walt Borland', 'Walter Lasecki', 'Wei Ai', 'Xin Rong', 'Xuan Zhao', 'Yan Chen', 'Yingzhi Liang', 'Youyang Hou', 'Yu-Jen Lin', 'Yusuf Masatlioglu', 'Zhewei Song'],"Testing the dictionary keys")
	def test_dict_values(self):
		self.assertEqual(sorted(umsi_titles.values()),[' ', ' ', ' ', ' ', ' ', 'Academic Advisor', 'Academic Advisor', 'Academic Programs Coordinator', 'Accountant Senior', 'Adjunct Associate Professor of Information, School of Information', 'Adjunct Clinical Associate Professor of Information and iDream Program Manager, School of Information', 'Adjunct Professor of Business Economics and Public Policy, Stephen M Ross School of Business, Research Professor, Survey Research Center and ISR Center Director, Institute for Social Research', 'Administrative Assistant', 'Administrative Assistant Inter', 'Administrative Assistant Senior', 'Administrative Assistant and Events Coordinator', 'Administrative Director', 'Admissions Associate Dir Unit', 'Admissions and Student Affairs Assistant', 'Arthur F Thurnau Professor, Professor of Climate and Space Sciences and Engineering, College of Engineering and Professor of Information, School of Information', 'Arthur F Thurnau Professor, Professor of Education, School of Education and Professor of Information, School of Information', 'Arthur F Thurnau Professor, Professor of Electrical Engineering and Computer Science, College of Engr, Professor of Education, School of Education and Professor of Information, School of Information', 'Arthur F Thurnau Professor, Vice Provost for Academic Innovation, Office of the Provost and Executive Vice President for Academic Affairs, Dean of Libraries, University Library, Professor of Information, School of Information and Faculty Associate, Resear', 'Assistant Dean for Diversity, Equity, and Inclusion, School of Information', 'Assistant Director of Human Resources and Support Services', 'Assistant Director of Recruiting and Admissions, School of Information and Intermittent Lecturer in Social Work, School of Social Work', 'Assistant Director, Health Informatics Program', 'Assistant Professor of Art and Design, Penny W Stamps School of Art and Design and Assistant Professor of Information, School of Information', 'Assistant Professor of Art and Design, Penny W Stamps School of Art and Design and Assistant Professor of Information, School of Information', 'Assistant Professor of Electrical Engineering and Computer Science, College of Engineering and Assistant Professor of Information, School of Information', 'Assistant Professor of Family Medicine, Medical School and Assistant Professor of Information, School of Information', 'Assistant Professor of Information, School of Information', 'Assistant Professor of Information, School of Information', 'Assistant Professor of Information, School of Information', 'Assistant Professor of Information, School of Information', 'Assistant Professor of Information, School of Information', 'Assistant Professor of Information, School of Information and Assistant Professor of Art and Design. Penny W Stamps School of Art and Design', 'Assistant Professor of Information, School of Information and Assistant Professor of Electrical Engineering and Computer Science, College of Engineering', 'Assistant Professor of Information, School of Information and Assistant Professor of Electrical Engineering and Computer Science, College of Engineering', 'Assistant Professor of Information, School of Information and Assistant Professor of Electrical Engineering and Computer Science, College of Engineering', 'Assistant Professor of Information, School of Information and Assistant Professor of Electrical Engineering and Computer Science, College of Engineering', 'Assistant Professor of Information, School of Information and Assistant Professor of Electrical Engineering and Computer Science, College of Engineering', 'Assistant Professor of Information, School of Information and Assistant Professor of Electrical Engineering and Computer Science, College of Engineering', 'Assistant Professor of Information, School of Information and Assistant Professor of Health Behavior and Health Education, School of Public Health', 'Assistant Professor of Information, School of Information, Assistant Professor of Electrical Engineering and Computer Science, College of Engineering and Assistant Professor of Complex Systems, College of Literature, Science, and the Arts', 'Assistant Professor of Learning Health Sciences, Medical School and Assistant Professor of Information, School of Information', 'Assistant Professor of Social Work, School of Social Work and Assistant Professor of Information, School of Information', 'Associate Archivist and Assistant Director, Bentley Historical Library and Adjunct Lecturer in Information, School of Information', 'Associate Archivist, Bentley Historical Library and Assistant Director, Bentley Historical Library and Adjunct Lecturer in Information, School of Information', 'Associate Director UMSI Computing', 'Associate Director of Development & Alumni Relations', 'Associate Librarian, University of Michigan Library', 'Associate Professor Emerita of Information, School of Information', 'Associate Professor Emeritus of Information, School of Information', 'Associate Professor of  Pediatrics and Communicable Diseases, Medical School and Clinical Associate Professor of Information, School of Information', 'Associate Professor of Electrical Engineering and Computer Science, College of Engineering and Associate Professor of Information, School of Information', 'Associate Professor of Information, School of Information', 'Associate Professor of Information, School of Information', 'Associate Professor of Information, School of Information', 'Associate Professor of Information, School of Information', 'Associate Professor of Information, School of Information and Associate Professor of Economics, College of Literature, Science, and the Arts', 'Associate Professor of Information, School of Information and Associate Professor of Electrical Engineering and Computer Science, College of Engineering', 'Associate Professor of Information, School of Information and Associate Professor of Electrical Engineering and Computer Science, College of Engineering', 'Associate Professor of Information, School of Information and Associate Professor of Electrical Engineering and Computer Science, College of Engineering', 'Associate Professor of Information, School of Information and Associate Professor of Health Behavior and Health Education, School of Public Health', 'Associate Professor of Information, School of Information and Associate Professor of Health Management and Policy, School of Public Health', 'Associate Professor of Music, School of Music, Theatre & Dance and Associate Professor of Information, School of Information', 'Business Systems Analyst Assoc', 'Career Development & Engaged Learning Coordinator', 'Career Services Counselor and Internship Coordinator and Adjunct Lecturer in Information, School of Information', 'Chief Information Officer and Clinical Assistant Professor of Information, School of Information', 'Citizen Experience Design Community Development Liaison and Adjunct Lecturer in Information, School of Information', 'Clinical Associate Professor of  Information, School of Information', 'Clinical Associate Professor of Information, School of Information', 'Clinical Associate Professor of Information, School of Information', 'Communications Specialist', 'Community Engagement & Exchange Coordinator', 'Dean Emeritus, Arthur W Burks Collegiate Professor Emeritus of Information and Computer Science, Professor Emeritus of Information, School of Information, Professor Emeritus of Economics, College of Literature, Science, and the Arts and Professor Emeritus', 'Dean and Professor of Information, School of Information', 'Director Admissions and Student Affairs', 'Director of Career Development', 'Director of Development and Alumni Relations', 'Director of Development, Bentley Historical Library', 'Director of Engaged Learning Programs', 'Director of Finance', 'Director of Human Resources and Support Services', 'Director of Marketing and Communications', 'Director of Research Administration', 'Ehrenberg Director of Entrepreneurship, Adjunct Clinical Associate Professor of Information and Research Investigator, School of Information', 'Employer Relations Coordinator', 'Engagement Manager', 'Events Manager', 'Facilities Coordinator', 'Financial Specialist Senior', 'George Herbert Mead Collegiate Professor of Human-Computer Interaction, Professor of Information, School of Information and Professor of Electrical Engineering and Computer Science, College of Engineering', 'Graduate Programs Coordinator', 'Graphic Designer', 'HR Generalist Intermediate', 'Harold T Shapiro Collegiate Professor of Public Policy, Arthur F Thurnau Professor, Interim Provost and Executive Vice President for Academic Affairs, Office of the Provost  and Executive Vice President for Academic Affairs, Presidential Bicentennial Prof', 'Intermittent Lecturer I in Information, School of Information', 'Intermittent Lecturer in Information, School of Information', 'Intermittent Lecturer in Information, School of Information', 'Intermittent Lecturer in Information, School of Information', 'John F Nickoll Professor of Law, Professor of Law, Law School and Professor of Information, School of Information', 'Josiah Macy, Jr Professor of Medical Education, Chair, Department of Learning Health Sciences, Professor of Learning Health Sciences, Medical School, Professor of Information, School of Information and Professor of Health Management and Policy, School of ', 'Large-Scale Research Program Manager', 'Lead Developer, Digital Innovation Greenhouse and Adjunct Lecturer in Information, School of Information', 'Lecturer III in Information, School of Information', 'Lecturer III in Information, School of Information', 'Lecturer III in Information, School of Information and Intermittent Lecturer in Residential College, College of Literature, Science, and the Arts', 'Lecturer IV in Information and Research Investigator, School of Information', 'Lecturer IV in Information, School of Information', 'Librarian, Library Budget and Planning - Copyright, University Library', 'Librarian, Library Collection, University Library and Adjunct Lecturer in Information, School of Information', 'MHI Recruitment and Admissions Coordinator', 'Marketing Assistant Associate', 'Marketing Project Manager', 'Michael D Cohen Collegiate Professor of Information, Associate Dean for Research and Faculty Affairs, Professor of Information and Interim Director of Health Informatics, School of Information', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'PhD student', 'President Emeritus and University Professor of Science and Engineering', 'Professor Emerita of Information, School of Information', 'Professor Emerita of Information, School of Information', 'Professor Emerita of Information, School of Information, Professor Emerita of Computation and Information Systems, Stephen M Ross School of Business and Professor Emerita of Psychology, College of Literature, Science, and the Arts', 'Professor Emeritus of Information, School of Information', 'Professor Emeritus of Information, School of Information', 'Professor Emeritus of Information, School of Information and Professor Emeritus of Electrical Engineering and Computer Science, College of Engineering', 'Professor Emeritus of Information, School of Information and Professor Emeritus of Psychology, College of Literature, Science, and the Arts', 'Professor of Dentistry, Department of Periodontics and Oral Medicine, Associate Dean for Faculty Affairs and Institutional Effectiveness, School of Dentistry and Clinical Professor of Information, School of Information', 'Professor of Information, School of Information', 'Professor of Information, School of Information', 'Professor of Information, School of Information', 'Professor of Information, School of Information and Professor of History, College of Literature, Science, and the Arts', 'Professor of Information, School of Information and Professor of History, College of Literature, Science, and the Arts', 'Professor of Information, School of Information, Faculty Associate, Center for Political Studies, Institute for Social Research and Professor of Communication Studies, College of Literature, Science, and the Arts', 'Professor of Information, School of Information, Professor of Electrical Engineering and Computer Science, College of Engineering and Prof of Psychology, College of Literature, Science and the Arts', 'Professor of Information, School of Information, Professor of Electrical Engineering and Computer Science, College of Engineering and Professor of Linguistics, College of Literature, Science, and the Arts', 'Professor of Information, School of Information, Professor of Electrical Engineering and Computer Science, College of Engineering and Provost and Executive Vice President for Academic Affairs, Office of the Provost and Executive Vice President for Academi', 'Program Manager and Research Coordinator', 'Project Manager', 'Research Area Specialist , School of Information', 'Research Area Specialist Lead and Research Investigator, School of Information', 'Research Assistant Professor, School of Information', 'Research Fellow, Information, Research Investigator, Information and Lecturer III in Information, School of Information', 'Research Fellow, Information, School of Information', 'Research Fellow, Information, School of Information', 'Research Investigator, Information and Research Fellow, School of Information', 'Research Process Coordinator', 'Research Process Coordinator Senior', 'Research Process Manager', 'Research Professor, School of Information', 'Research and HR Administrative Assistant', 'Robert M Warner Collegiate Professor of Information, Professor of Information, School of Information and Faculty Associate, Institute for Social Research', 'School Registrar', 'School of Information Intern', 'Senior Assistant to the Dean', 'Senior Associate Dean for Academic Affairs and Professor of Information, School of Information', 'Senior Associate Librarian, Graduate Library, University Library and Intermittent Lecturer in Information, School of Information', 'Senior Associate Librarian, Learning and Teaching, University Library and Adjunct Lecturer in Curriculum Support, College of Literature, Science, and the Arts', 'Social Media Specialist', 'Solution Architect Lead and Adjunct Lecturer in Information, Sch of Information, Director of Infrastructure ActiveStep, App Programmer/Analyst Ld, Family Medicine, Medical School', 'Student Services Assistant', 'Systems Programmer Analyst', 'Systems Programmer/Analyst Lead', 'Undergraduate Program Manager', 'Unix and IT Security Administrator', 'Videographer', 'Visiting Associate Professor of Economics, College of Literature, Science, and the Arts and Adjunct Associate Professor of Information, School of Information', 'W K Kellogg Professor of Community Information, Associate Professor of Information, School of Information', 'Web Software Developer', 'William Warner Bishop Collegiate Professor of Information and Professor of Information, School of Information'])
class PartThree(unittest.TestCase):
	def test_get_tweets(self):
		self.assertEqual(len(get_five_tweets("University of Michigan")),5,"Testing that get_five_tweets returns a sequence of 5 things")
	def test_get_tweets_type(self):
		self.assertEqual(type(get_five_tweets("McGill University")),type([]),"Testing that get_five_tweets returns a list")
	def test_get_tweets_element_type(self):
		self.assertEqual(type(get_five_tweets("University of Michigan")[1]),type(u""), "Testing that an element of the return val of get_tweets is a Unicode string")
	def test_five_tweets(self):
		self.assertEqual(type(five_tweets),type([]))
	def test_five_tweets_len(self):
		self.assertEqual(len(five_tweets),5)
	def test_tweet_urls_found(self):
		self.assertEqual(set([x[:4] for x in tweet_urls_found]),set(["http"]),"Testing that each element in tweet_urls_found list is a URL begin. with HTTP")

if __name__ == "__main__":
	unittest.main(verbosity=2)
