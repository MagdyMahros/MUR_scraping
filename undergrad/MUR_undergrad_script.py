import csv
import re
import time
from pathlib import Path
from selenium import webdriver
import bs4 as bs4
import os
import copy
from CustomMethods import TemplateData
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException, \
    StaleElementReferenceException, JavascriptException, ElementClickInterceptedException

option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# read the url from each file into a list
course_links_file_path = Path(os.getcwd().replace('\\', '/'))
course_links_file_path = course_links_file_path.__str__() + '/MUR_undergrad_links.txt'
course_links_file = open(course_links_file_path, 'r')

# the csv file we'll be saving the courses to
csv_file_path = Path(os.getcwd().replace('\\', '/'))
csv_file = csv_file_path.__str__() + '/MUR_undergrad.csv'

course_data = {'Level_Code': '', 'University': 'Murdoch University', 'City': '', 'Country': '',
               'Course': '', 'Int_Fees': '', 'Local_Fees': '', 'Currency': 'AUD', 'Currency_Time': 'year',
               'Duration': '', 'Duration_Time': '', 'Full_Time': 'yes', 'Part_Time': 'yes', 'Prerequisite_1': '',
               'Prerequisite_2': 'IELTS', 'Prerequisite_3': '', 'Prerequisite_1_grade': '', 'Prerequisite_2_grade': '6.0',
               'Prerequisite_3_grade': '', 'Website': '', 'Course_Lang': '', 'Availability': '', 'Description': '',
               'Career_Outcomes': '', 'Online': 'no', 'Offline': 'yes', 'Distance': 'no', 'Face_to_Face': 'yes',
               'Blended': 'no', 'Remarks': '',
               'Subject_Description_1': '', 'Subject_or_Unit_2': '', 'Subject_Objective_2': '',
               'Subject_Description_2': '',
               'Subject_or_Unit_3': '', 'Subject_Objective_3': '', 'Subject_Description_3': '',
               'Subject_or_Unit_4': '', 'Subject_Objective_4': '', 'Subject_Description_4': '',
               'Subject_or_Unit_5': '', 'Subject_Objective_5': '', 'Subject_Description_5': '',
               'Subject_or_Unit_6': '', 'Subject_Objective_6': '', 'Subject_Description_6': '',
               'Subject_or_Unit_7': '', 'Subject_Objective_7': '', 'Subject_Description_7': '',
               'Subject_or_Unit_8': '', 'Subject_Objective_8': '', 'Subject_Description_8': '',
               'Subject_or_Unit_9': '', 'Subject_Objective_9': '', 'Subject_Description_9': '',
               'Subject_or_Unit_10': '', 'Subject_Objective_10': '', 'Subject_Description_10': '',
               'Subject_or_Unit_11': '', 'Subject_Objective_11': '', 'Subject_Description_11': '',
               'Subject_or_Unit_12': '', 'Subject_Objective_12': '', 'Subject_Description_12': '',
               'Subject_or_Unit_13': '', 'Subject_Objective_13': '', 'Subject_Description_13': '',
               'Subject_or_Unit_14': '', 'Subject_Objective_14': '', 'Subject_Description_14': '',
               'Subject_or_Unit_15': '', 'Subject_Objective_15': '', 'Subject_Description_15': '',
               'Subject_or_Unit_16': '', 'Subject_Objective_16': '', 'Subject_Description_16': '',
               'Subject_or_Unit_17': '', 'Subject_Objective_17': '', 'Subject_Description_17': '',
               'Subject_or_Unit_18': '', 'Subject_Objective_18': '', 'Subject_Description_18': '',
               'Subject_or_Unit_19': '', 'Subject_Objective_19': '', 'Subject_Description_19': '',
               'Subject_or_Unit_20': '', 'Subject_Objective_20': '', 'Subject_Description_20': '',
               'Subject_or_Unit_21': '', 'Subject_Objective_21': '', 'Subject_Description_21': '',
               'Subject_or_Unit_22': '', 'Subject_Objective_22': '', 'Subject_Description_22': '',
               'Subject_or_Unit_23': '', 'Subject_Objective_23': '', 'Subject_Description_23': '',
               'Subject_or_Unit_24': '', 'Subject_Objective_24': '', 'Subject_Description_24': '',
               'Subject_or_Unit_25': '', 'Subject_Objective_25': '', 'Subject_Description_25': '',
               'Subject_or_Unit_26': '', 'Subject_Objective_26': '', 'Subject_Description_26': '',
               'Subject_or_Unit_27': '', 'Subject_Objective_27': '', 'Subject_Description_27': '',
               'Subject_or_Unit_28': '', 'Subject_Objective_28': '', 'Subject_Description_28': '',
               'Subject_or_Unit_29': '', 'Subject_Objective_29': '', 'Subject_Description_29': '',
               'Subject_or_Unit_30': '', 'Subject_Objective_30': '', 'Subject_Description_30': '',
               'Subject_or_Unit_31': '', 'Subject_Objective_31': '', 'Subject_Description_31': '',
               'Subject_or_Unit_32': '', 'Subject_Objective_32': '', 'Subject_Description_32': '',
               'Subject_or_Unit_33': '', 'Subject_Objective_33': '', 'Subject_Description_33': '',
               'Subject_or_Unit_34': '', 'Subject_Objective_34': '', 'Subject_Description_34': '',
               'Subject_or_Unit_35': '', 'Subject_Objective_35': '', 'Subject_Description_35': '',
               'Subject_or_Unit_36': '', 'Subject_Objective_36': '', 'Subject_Description_36': '',
               'Subject_or_Unit_37': '', 'Subject_Objective_37': '', 'Subject_Description_37': '',
               'Subject_or_Unit_38': '', 'Subject_Objective_38': '', 'Subject_Description_38': '',
               'Subject_or_Unit_39': '', 'Subject_Objective_39': '', 'Subject_Description_39': '',
               'Subject_or_Unit_40': '', 'Subject_Objective_40': '', 'Subject_Description_40': ''}

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

    # PREREQUISITE
    atar_tag = soup.find('div', class_='atar')
    if atar_tag:
        atar = atar_tag.find('span')
        if atar:
            course_data['Prerequisite_1_grade'] = atar.get_text()
            course_data['Prerequisite_1'] = 'year 12'
            print('ATAR: ', atar.get_text())

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
            duration_ = re.search(r'\d+', duration_text)
            if duration_ is not None:
                if duration_ == 1:
                    course_data['Duration'] = duration_.group()
                    course_data['Duration_Time'] = 'Year'
                else:
                    course_data['Duration'] = duration_.group()
                    course_data['Duration_Time'] = 'Years'
    else:
        course_data['Duration'] = 'Not mentioned'
        course_data['Duration_Time'] = 'Not mentioned'
    print('Duration: ', str(course_data['Duration']) + ' / ' + course_data['Duration_Time'])

    # UNITES
    subjects_link = []
    try:
        THE_XPATH = "//h2[contains(text(), 'Structure')]/following-sibling::div/descendant::td/descendant::a"
        units_list = browser.find_elements_by_xpath(f"{THE_XPATH}")
        for i, a in enumerate(units_list):
            if i < 40:
                link = a.get_attribute('href')
                subjects_link.append(link)
            if len(subjects_link) == 40:
                break
        # print('links list: ', subjects_link)
        i = 1
        for s in subjects_link:
            browser.get(s)
            # subject name
            try:
                THE_XPATH = '//*[@id="academic-item-banner"]/div/div/h2'
                WebDriverWait(browser, 3).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, f'{THE_XPATH}'))
                )
                value = browser.find_element_by_xpath(f'{THE_XPATH}').text
                print('UNIT NAME: ', value)
                course_data[f'Subject_or_Unit_{i}'] = value
            except(AttributeError, TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
                print(f'cant extract subject name {i}')
            # subject description
            try:
                THE_XPATH = '//*[@id="Overview"]/div[2]/div[1]/div[2]/p'
                WebDriverWait(browser, 3).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, f'{THE_XPATH}'))
                )
                value = browser.find_element_by_xpath(f'{THE_XPATH}').text
                print('UNIT DESCRIPTION: ', value)
                course_data[f'Subject_Description_{i}'] = value
            except(AttributeError, TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
                print(f'cant extract subject description {i}')
            # subject objectives
            try:
                value = []
                THE_XPATH = "//div[contains(text(), 'Learning outcomes')]/ancestor::h3/ancestor::div/following-sibling::div[@class='AccordionItem css-gq1n00-Box-SAccordionBody e1450wuy0']/descendant::div[@class='css-1smylv8-Box-Flex']/descendant::div[@class='css-1b16hwh-Box-Flex-SListContent e1450wuy3']/descendant::div/descendant::div"
                WebDriverWait(browser, 3).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, f'{THE_XPATH}'))
                )
                values = browser.find_elements_by_xpath(f'{THE_XPATH}')
                for v in values:
                    value.append(v.text)
                value = ' / '.join(value)
                print('UNIT OBJECTIVE: ', value)
                course_data[f'Subject_Objective_{i}'] = value
            except(AttributeError, TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
                print(f'cant extract subject description {i}')
            i += 1

    except (AttributeError, TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f'something went wrong here:  {e}')



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
                          'Face_to_Face', 'Blended', 'Remarks',
                          'Subject_or_Unit_1', 'Subject_Objective_1', 'Subject_Description_1',
                          'Subject_or_Unit_2', 'Subject_Objective_2', 'Subject_Description_2',
                          'Subject_or_Unit_3', 'Subject_Objective_3', 'Subject_Description_3',
                          'Subject_or_Unit_4', 'Subject_Objective_4', 'Subject_Description_4',
                          'Subject_or_Unit_5', 'Subject_Objective_5', 'Subject_Description_5',
                          'Subject_or_Unit_6', 'Subject_Objective_6', 'Subject_Description_6',
                          'Subject_or_Unit_7', 'Subject_Objective_7', 'Subject_Description_7',
                          'Subject_or_Unit_8', 'Subject_Objective_8', 'Subject_Description_8',
                          'Subject_or_Unit_9', 'Subject_Objective_9', 'Subject_Description_9',
                          'Subject_or_Unit_10', 'Subject_Objective_10', 'Subject_Description_10',
                          'Subject_or_Unit_11', 'Subject_Objective_11', 'Subject_Description_11',
                          'Subject_or_Unit_12', 'Subject_Objective_12', 'Subject_Description_12',
                          'Subject_or_Unit_13', 'Subject_Objective_13', 'Subject_Description_13',
                          'Subject_or_Unit_14', 'Subject_Objective_14', 'Subject_Description_14',
                          'Subject_or_Unit_15', 'Subject_Objective_15', 'Subject_Description_15',
                          'Subject_or_Unit_16', 'Subject_Objective_16', 'Subject_Description_16',
                          'Subject_or_Unit_17', 'Subject_Objective_17', 'Subject_Description_17',
                          'Subject_or_Unit_18', 'Subject_Objective_18', 'Subject_Description_18',
                          'Subject_or_Unit_19', 'Subject_Objective_19', 'Subject_Description_19',
                          'Subject_or_Unit_20', 'Subject_Objective_20', 'Subject_Description_20',
                          'Subject_or_Unit_21', 'Subject_Objective_21', 'Subject_Description_21',
                          'Subject_or_Unit_22', 'Subject_Objective_22', 'Subject_Description_22',
                          'Subject_or_Unit_23', 'Subject_Objective_23', 'Subject_Description_23',
                          'Subject_or_Unit_24', 'Subject_Objective_24', 'Subject_Description_24',
                          'Subject_or_Unit_25', 'Subject_Objective_25', 'Subject_Description_25',
                          'Subject_or_Unit_26', 'Subject_Objective_26', 'Subject_Description_26',
                          'Subject_or_Unit_27', 'Subject_Objective_27', 'Subject_Description_27',
                          'Subject_or_Unit_28', 'Subject_Objective_28', 'Subject_Description_28',
                          'Subject_or_Unit_29', 'Subject_Objective_29', 'Subject_Description_29',
                          'Subject_or_Unit_30', 'Subject_Objective_30', 'Subject_Description_30',
                          'Subject_or_Unit_31', 'Subject_Objective_31', 'Subject_Description_31',
                          'Subject_or_Unit_32', 'Subject_Objective_32', 'Subject_Description_32',
                          'Subject_or_Unit_33', 'Subject_Objective_33', 'Subject_Description_33',
                          'Subject_or_Unit_34', 'Subject_Objective_34', 'Subject_Description_34',
                          'Subject_or_Unit_35', 'Subject_Objective_35', 'Subject_Description_35',
                          'Subject_or_Unit_36', 'Subject_Objective_36', 'Subject_Description_36',
                          'Subject_or_Unit_37', 'Subject_Objective_37', 'Subject_Description_37',
                          'Subject_or_Unit_38', 'Subject_Objective_38', 'Subject_Description_38',
                          'Subject_or_Unit_39', 'Subject_Objective_39', 'Subject_Description_39',
                          'Subject_or_Unit_40', 'Subject_Objective_40', 'Subject_Description_40']

    course_dict_keys = set().union(*(d.keys() for d in course_data_all))

    with open(csv_file, 'w', encoding='utf-8', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, course_dict_keys)
        dict_writer.writeheader()
        dict_writer.writerows(course_data_all)

    with open(csv_file, 'r', encoding='utf-8') as infile, open('MUR_undergrad_ordered.csv', 'w', encoding='utf-8',
                                                               newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=desired_order_list)
        # reorder the header first
        writer.writeheader()
        for row in csv.DictReader(infile):
            # writes the reordered rows to the new file
            writer.writerow(row)

