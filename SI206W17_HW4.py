import unittest
import requests
from bs4 import BeautifulSoup


## SI 206 - W17 - HW4
## Miguel Martinez


#####################


#get HTML data
html_data = requests.get('http://www.nytimes.com').text
infile = open('nytimes_data.html', 'w', encoding='utf-8')
infile.write(html_data)
infile.close()
#####################


infile2 = open('nytimes_data.html', 'r', encoding='utf-8')
soup = BeautifulSoup(infile2, 'html.parser')
nytimes_long_headlines = []
for link in soup.find_all('h2',{'class':'story-heading'}):
	nytimes_long_headlines.append(link.text)
nytimes_headlines = nytimes_long_headlines[0:10]


#####################



response = requests.get("https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All")
htmldoc = response.text

soup = BeautifulSoup(htmldoc,"html.parser")
people = soup.find_all("div",{"class":"views-row"})
umsi_titles = {}
#print(people)

response = requests.get("https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All")
htmldoc = response.text

soup = BeautifulSoup(htmldoc,"html.parser")
people = soup.find_all("div",{"class":"views-row"})
umsi_titles = {}
for i in people:
	for title in i.find_all('div',{"class":"field field-name-field-person-titles field-type-text field-label-hidden"}):
		for elem in i.find_all('div',{"class":"field-item even", "property":"dc:title"},'h2'):
			umsi_titles[elem.text] = title.text
print(umsi_titles)









######### UNIT TESTS ######### 


class HW4_Part2(unittest.TestCase):
	def test_first_last_elem(self):
		self.assertEqual(type(nytimes_headlines[0]),type(""), "Testing that the first type in the nytimes_headlines list is a string")
		self.assertEqual(type(nytimes_headlines[-1]),type(""), "Testing that the last type in the nytimes_headlines list is a string")
	def length_of_ten(self):
		self.assertEqual(len(nytimes_headlines),10, "Testing that there are ten headlines in the list")

class HW4_Part3(unittest.TestCase):
	def test_key_value(self):
		self.assertEqual(umsi_titles["Eytan Adar"],"Associate Professor of Electrical Engineering and Computer Science, College of Engineering and Associate Professor of Information, School of Information", "Testing one key-value pair that should be in your umsi_titles diction")
	def test_key_value2(self):
		self.assertEqual(umsi_titles["Ben Armes"],"Videographer", "Testing another key-value pair that should be in your umsi_titles diction")
	def test_len_items(self):
		self.assertEqual(len(umsi_titles.keys()),20, "Testing that there are 20 keys in the dictionary umsi_titles")
	def test_full_dict_items(self): 
		self.assertEqual(sorted(umsi_titles.items()),[('Alicia Baker', 'Administrative Assistant'), ('Andrea Barbarin', 'PhD student'), ('Ben Armes', 'Videographer'), ('Daniel Atkins III', 'Professor Emeritus of Information, School of Information and Professor Emeritus of Electrical Engineering and Computer Science, College of Engineering'), ('Deborah Apsley', 'Director of Human Resources and Support Services'), ('Eytan Adar', 'Associate Professor of Electrical Engineering and Computer Science, College of Engineering and Associate Professor of Information, School of Information'), ('Julia Adler-Milstein', 'Associate Professor of Information, School of Information and Associate Professor of Health Management and Policy, School of Public Health'), ('Lindsay Blackwell', 'PhD student'), ('Mark Ackerman', 'George Herbert Mead Collegiate Professor of Human-Computer Interaction, Professor of Information, School of Information and Professor of Electrical Engineering and Computer Science, College of Engineering'), ('Marsha Antal', 'School Registrar'), ('Mohamed Abbadi', 'PhD student'), ('Nancy Benovich Gilby', 'Ehrenberg Director of Entrepreneurship, Adjunct Clinical Associate Professor of Information and Research Investigator, School of Information'), ('Rasha Alahmad', 'PhD student'), ('Reginald Beasley', 'Admissions and Student Affairs Assistant'), ('Sarah Argiero', 'Academic Advisor'), ('Seyram Avle', 'Research Investigator, Information and Research Fellow, School of Information'), ('Tawfiq Ammari', 'PhD student'), ('Todd Ayotte', 'Director of Finance'), ('Vadim Besprozvany', 'Lecturer III in Information, School of Information and Intermittent Lecturer in Residential College, College of Literature, Science, and the Arts'), ('Wei Ai', 'PhD student')], "Testing the entire dictionary contents")

if __name__ == "__main__":
	unittest.main(verbosity=2)
