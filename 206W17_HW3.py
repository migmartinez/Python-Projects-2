import unittest
import re

## SI 206 - W17 - HW3
## Miguel Martinez


#####################



##Regex Exercise

def parse_counted_words(string):
    pattern1 = "\\b(\d+)\\s(.[A-Za-z]+)"
    answer = re.findall(pattern1, string)
    if answer:
        return answer[-1]
    return None


infile2a = open("./computer_paths.txt", "r")
pattern2a = r"\d*[.]"
file_lst = []
for aline in infile2a:
    aline = aline.rstrip()
    if re.findall(pattern2a, aline):
        file_lst.append(aline)
file_paths_num = len(file_lst)
infile2a.close()

infile2b = open('./computer_paths.txt', 'r')
pattern2b = r'^[/~]'
full_lst = []
for bline in infile2b:
    bline = bline.rstrip()
    if re.findall(pattern2b, bline):
        full_lst.append(bline)
full_paths_num = len(full_lst)
infile2b.close()

infile2c = open('./computer_paths.txt', 'r')
pattern2c = r'[SI][206]\S+[.][py]'
py_lst = []
for cline in infile2c:
    cline = cline.rstrip()
    if re.findall(pattern2c, cline):
        py_lst.append(cline)
python_course_paths = len(py_lst)
infile2c.close()

infile2d = open('./computer_paths.txt', 'r')
pattern2d = r'\d[.][xlsd]'
micro_lst = []
for dline in infile2d:
    dline = dline.rstrip()
    if re.findall(pattern2d, dline):
        micro_lst.append(dline)
microsoft_files_num = len(micro_lst)        
infile2d.close()


####### UNIT TESTING BELOW #######

class Part1_HW3(unittest.TestCase):
    def test_pcw_1(self):
        self.assertEqual(parse_counted_words('5 watermelons, 13 pineapples, and 1 papaya.'),('1','papaya'))
    def test_pcw_2(self):
        self.assertEqual(parse_counted_words('101 dalmations!'),('101','dalmations'))
    def test_pcw_3(self):
        self.assertEqual(parse_counted_words('snow white and the 7 #littledwarves'),('7','#littledwarves'))
    def test_pcw_4(self):
        self.assertEqual(parse_counted_words('goldilocks and the 3 little pigs'),('3','little'))
    def test_pcw_5(self): 
        self.assertEqual(parse_counted_words('678 1234567 890  '),None)
    def test_pcw_6(self):
        self.assertEqual(parse_counted_words("hellllo 5000"), None)
    def test_pcw_7(self):
        self.assertEqual(parse_counted_words("!!!! 6"), None)
    def test_pcw_8(self):
        self.assertEqual(parse_counted_words("!!!!! 72 and 76 calendars"),('76',"calendars"))

class Part2_HW3(unittest.TestCase):
    def test_cpaths_1(self):
        self.assertEqual(file_paths_num,16)
    def test_cpaths_2(self):
        self.assertEqual(full_paths_num,16)
    def test_cpaths_3(self):
        self.assertEqual(python_course_paths,3)
    def test_cpaths_4(self):
        self.assertEqual(microsoft_files_num,3)


if __name__ == "__main__":
    unittest.main(verbosity=2)

