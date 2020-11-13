import csv
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
import os
import copy
from CustomMethods import TemplateData

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/MUR_research_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/MUR_research.csv'

course_data = {'Level_Code': '', 'University': 'Murdoch University', 'City': '', 'Country': '',
               'Course': '', 'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'year',
               'Duration': '', 'Duration_Time': '', 'Full_Time': 'yes', 'Part_Time': 'yes', 'Prerequisite_1': 'IELTS',
               'Prerequisite_2': '', 'Prerequisite_3': '', 'Prerequisite_1_grade': '6.5', 'Prerequisite_2_grade': '',
               'Prerequisite_3_grade': '', 'Website': '', 'Course_Lang': '', 'Availability': '', 'Description': '',
               'Career_Outcomes': '', 'Online': 'no', 'Offline': 'yes', 'Distance': 'no', 'Face_to_Face': 'yes',
               'Blended': 'no', 'Remarks': ''}

possible_cities = {'canberra': 'Canberra', 'bruce': 'Bruce', 'mumbai': 'Mumbai', 'melbourne': 'Melbourne',
                   'brisbane': 'Brisbane', 'sydney': 'Sydney', 'queensland': 'Queensland', 'perth': 'Perth',
                   'shanghai': 'Shanghai', 'bhutan': 'Bhutan', 'online': 'Online', 'hangzhou': 'Hangzhou',
                   'hanoi': 'Hanoi', 'bundoora': 'Bundoora', 'brunswick': 'Brunswick', 'bendigo': 'Victoria'}

possible_languages = {'Japanese': 'Japanese', 'French': 'French', 'Italian': 'Italian', 'Korean': 'Korean',
                      'Indonesian': 'Indonesian', 'Chinese': 'Chinese', 'Spanish': 'Spanish'}

course_data_all = []
level_key = TemplateData.level_key  # dictionary of course levels
faculty_key = TemplateData.faculty_key  # dictionary of course levels

# GET EACH COURSE LINK
for each_url in course_links_file:
    remarks_list = []
    actual_cities = []
    browser.get(each_url)
    pure_url = each_url.strip()
    each_url = browser.page_source

    soup = bs4.BeautifulSoup(each_url, 'lxml')
    time.sleep(1)

    # SAVE COURSE URL
    course_data['Website'] = pure_url

    # COURSE TITLE
    title = soup.find('h1', class_='title')
    if title:
        title_text = title.get_text()
        course_data['Course'] = title_text
        print('COURSE TITLE: ', title_text)
    time.sleep(0.5)

    # DECIDE THE LEVEL CODE
    for i in level_key:
        for j in level_key[i]:
            if j in course_data['Course']:
                course_data['Level_Code'] = i
    print('COURSE LEVEL CODE: ', course_data['Level_Code'])

    # DECIDE THE FACULTY
    for i in faculty_key:
        for j in faculty_key[i]:
            if j.lower() in course_data['Course'].lower():
                course_data['Faculty'] = i
    print('COURSE FACULTY: ', course_data['Faculty'])

    # COURSE LANGUAGE
    for language in possible_languages:
        if language in course_data['Course']:
            course_data['Course_Lang'] = language
        else:
            course_data['Course_Lang'] = 'English'
    print('COURSE LANGUAGE: ', course_data['Course_Lang'])

    # DESCRIPTION
    desc_div = soup.find('div', class_='bigtext')
    if desc_div:
        desc_list = []
        desc_p_list = desc_div.find_all('p')
        if desc_p_list:
            for p in desc_p_list:
                desc_list.append(p.get_text())
            desc_list = ' '.join(desc_list)
            course_data['Description'] = desc_list
            print('COURSE DESCRIPTION: ', desc_list)

    # CITY
    actual_cities.append('perth')

    # STUDY MODE
    study_mode_tag = soup.find('h4', text=re.compile('Study mode', re.IGNORECASE))
    if study_mode_tag:
        study_mode = study_mode_tag.find_next_sibling('span')
        if study_mode:
            s_text = study_mode.get_text().lower()
            if 'part time' in s_text or 'part-time' in s_text:
                course_data['Part_Time'] = 'yes'
            else:
                course_data['Part_Time'] = 'no'
            if 'full time' in s_text or 'full-time' in s_text:
                course_data['Full_Time'] = 'yes'
            else:
                course_data['Full_Time'] = 'no'
            print('PART-TIME/FULL-TIME: ', course_data['Part_Time'] + ' / ' + course_data['Full_Time'])

    # career outcomes
    career_title = soup.find('p', text=re.compile('Your future career', re.IGNORECASE))
    if career_title:
        career_ul = career_title.find_next_sibling('ul')
        if career_ul:
            career_list = []
            career_li_list = career_ul.find_all('li')
            if career_li_list:
                for li in career_li_list:
                    career_list.append(li.get_text())
                career_list = ' / '.join(career_list)
                course_data['Career_Outcomes'] = career_list
    else:
        course_data['Career_Outcomes'] = 'Not Mentioned'
    print('CAREER OUTCOMES: ', course_data['Career_Outcomes'])

    # DURATION
    duration_title = soup.find('h4', text=re.compile(r'Duration \(years\)', re.IGNORECASE))
    if duration_title:
        duration = duration_title.find_next_sibling('span')
        if duration:
            duration_text = duration.get_text()
            duration_ = re.search(r"\d+(?:.\d+)|\d+", duration_text)
            if duration_ is not None:
                if duration_.group() == 1 or '1' in duration_.group():
                    course_data['Duration'] = duration_.group()
                    course_data['Duration_Time'] = 'Year'
                elif '0.5' in duration_.group():
                    course_data['Duration'] = '6'
                    course_data['Duration_Time'] = 'Months'
                else:
                    course_data['Duration'] = duration_.group()
                    course_data['Duration_Time'] = 'Years'
    else:
        course_data['Duration'] = 'Not mentioned'
        course_data['Duration_Time'] = 'Not mentioned'
    print('Duration: ', str(course_data['Duration']) + ' / ' + course_data['Duration_Time'])

    # duplicating entries with multiple cities for each city
    for i in actual_cities:
        course_data['City'] = possible_cities[i]
        course_data_all.append(copy.deepcopy(course_data))
    del actual_cities
    course_data['Remarks'] = remarks_list
    del remarks_list

    # TABULATE THE DATA
    desired_order_list = ['Level_Code', 'University', 'City', 'Course', 'Faculty', 'Int_Fees', 'Local_Fees',
                          'Currency', 'Currency_Time', 'Duration', 'Duration_Time', 'Full_Time', 'Part_Time',
                          'Prerequisite_1', 'Prerequisite_2', 'Prerequisite_3', 'Prerequisite_1_grade',
                          'Prerequisite_2_grade', 'Prerequisite_3_grade', 'Website', 'Course_Lang', 'Availability',
                          'Description', 'Career_Outcomes', 'Country', 'Online', 'Offline', 'Distance',
                          'Face_to_Face',
                          'Blended', 'Remarks']

    course_dict_keys = set().union(*(d.keys() for d in course_data_all))

    with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, course_dict_keys)
        dict_writer.writeheader()
        dict_writer.writerows(course_data_all)

    with open(csv_file, 'r', encoding='utf-8') as infile, open('MUR_research_ordered.csv', 'w', encoding='utf-8',
                                                               newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)

