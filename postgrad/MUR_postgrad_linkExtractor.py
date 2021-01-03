"""Description:
    * author: Magdy Abdelkader
    * company: Fresh Futures/Seeka Technology
    * position: IT Intern
    * date: 13-11-20
    * description:This script extracts all the courses links and save it in txt file.
"""
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os


option = webdriver.ChromeOptions()
option.add_argument(" - incognito")
option.add_argument("headless")
exec_path = Path(os.getcwd().replace('\\', '/'))
exec_path = exec_path.parent.__str__() + '/Libraries/Google/v86/chromedriver.exe'
browser = webdriver.Chrome(executable_path=exec_path, options=option)

# MAIN ROUTINE
courses_page_url = 'https://search.murdoch.edu.au/s/search.html?collection=mu-course-search&query=&sort=&resultView=Grid&f.Study+level%7CcourseStudyLevel=Postgraduate&f.Study+type%7CstudyType=Course'
list_of_links = []
browser.get(courses_page_url)
the_url = browser.page_source
delay_ = 15  # seconds

# KEEP CLICKING NEXT UNTIL THERE IS NO BUTTON COLLECT THE LINKS
condition = True
while condition:
    result_tag = browser.find_element_by_class_name('list-unstyled.row')
    if result_tag:
        result_elements = result_tag.find_elements_by_tag_name('li')
        for i, element in enumerate(result_elements):
            a_tag = element.find_element_by_tag_name('a')
            url = a_tag.get_attribute('title')
            list_of_links.append(url)
    try:
        browser.execute_script("arguments[0].click();", WebDriverWait(browser, delay_).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[rel="next"]'))))
    except TimeoutException:
        print('timeout')
        condition = False

# SAVE TO FILE
course_links_file_path = os.getcwd().replace('\\', '/') + '/MUR_postgrad_links.txt'
course_links_file = open(course_links_file_path, 'w')
for link in list_of_links:
    if link is not None and link != "" and link != "\n":
        if link == list_of_links[-1]:
            course_links_file.write(link.strip())
        else:
            course_links_file.write(link.strip() + '\n')
course_links_file.close()
