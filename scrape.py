import os
import re
import time

from selenium.webdriver import Chrome 
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup 

# TODO: replace this by your account info
NAME = ''
PASSWORD = ''
driver = Chrome()

def login(name='', pwd=''):
    login_url = 'https://leetcode.com/accounts/login/'

    if name and pwd:
        driver.get(login_url)
        driver.implicitly_wait(20)
        user = driver.find_element_by_id("username-input")
        pwd = driver.find_element_by_id("password-input")
        user.send_keys(NAME)
        pwd.send_keys(PASSWORD)

        signin = driver.find_element_by_id("sign-in-button")
        flag = True
        #TODO: make this less ugly - we need to wait for the page to 
        #fully load before login can be clicked
        while(flag):
            try:
                time.sleep(0.5)
                signin.click()
                flag = False
            except WebDriverException:
                time.sleep(0.5)
        time.sleep(1)
        if(driver.current_url != login_url):
            print('Login succeeded')
            return True
        else:
            print('Login failed - check username and password')
            return False
    print('Need to provide a username and password!')
    return False

def show_solved_problems():
    statusdropdown = '//*[@id="question-app"]/div/div[2]/div[2]/div[1]/div[2]/div[4]/button'
    solvedoption = '//*[@id="question-app"]/div/div[2]/div[2]/div[1]/div[2]/div[4]/div/div/div/div[2]'
    driver.find_element_by_xpath(statusdropdown).click()
    driver.find_element_by_xpath(solvedoption).click()

def show_all_problems():
    viewall = '//*[@id="question-app"]/div/div[2]/div[2]/div[2]/table/tbody[2]/tr/td/span/select/option[4]'
    driver.find_element_by_xpath(viewall).click()

def get_problem_submission_page_urls():
     table = driver.find_element_by_class_name('reactable-data')
     #collect problem titles and links
     problemPages = {}
     for row in table.find_elements_by_tag_name("tr"):
        
        title = row.find_element_by_tag_name("a").text
        href = row.find_element_by_tag_name("a").get_attribute("href")
        #don't collect the links to solutions presented on leetcode
        if( not "article" in href):
            problemPages[title] = href + "/submissions/"
     return(problemPages)
            
def get_problem_number():
    counter = driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[1]/div/div[1]'
     
                                           '/div/div[2]/div/div/div/div[3]/div/span')
    #we need to wait for the counter to update
    while(counter.text == '-/-'):
        time.sleep(0.05)
    return(counter.text.split("/")[0])
    
def get_submission_urls():
    result = []
    acProblems = driver.find_elements_by_link_text("Accepted")
    for acProblem in acProblems:
        result.append(acProblem.get_attribute("href"))
    return(result)
    
def get_submission_data(submissionUrl):
    driver.get(submissionUrl)
    source = driver.page_source

    soup = BeautifulSoup(source, 'html.parser')
    script = soup.find('script', text=re.compile('submissionCode:'))

    code = re.findall(
        "submissionCode:\s*'(.+)'",
        script.string)[0].encode().decode('unicode-escape')
    language = re.findall("getLangDisplay:\s*'(.+)'",
                                        script.string)[0]
    return (code,language)
        
def get_problem_data(url):
    driver.get(url)
    driver.implicitly_wait(10)
         
    problemNumber = get_problem_number()

    acceptedSubmissionUrls = get_submission_urls()
    data = []
       
    for submissionUrl in acceptedSubmissionUrls:
        data.append ( (get_submission_data(submissionUrl), problemNumber) )
    return data

def write_data_to_file(title, data):    
    for i, ((code, language), number) in enumerate(data):
        ext = language_to_ext(language)
        title = title.replace(" ", "")
        
        folder = './leetcode_solutions/{:04d}_{}'.format(int(number), title) 
        os.makedirs(folder, exist_ok=True)
            
        filename = folder + '/{}_{}.{}'.format(title,i, ext)
        file = open(filename, 'w', encoding='utf-8')
        file.write(code)
        print('Saved solution {} to problem {}'.format(i,title))
        file.close
        
def language_to_ext(language):
    conversion = {'cpp': 'cpp', 'cplusplus': 'cpp', 'c++': 'cpp', 'c': 'c',
          'java': 'java', 'python': 'py', 'python3': 'py', 'py': 'py', 'c#': 'cs',
          'csharp': 'cs', 'javascript': 'js', 'js': 'js', 'ruby': 'rb',
          'rb': 'rb', 'go': 'go', 'golang': 'go', 'swift': 'swift'}
    return conversion[language] if language in conversion else language
    

def scrape_solutions():
   
    driver.get("https://leetcode.com/problemset/algorithms/")
    show_solved_problems()
    show_all_problems()
    
    problemUrls = get_problem_submission_page_urls()
    
    for problem, url in problemUrls.items():
        data = get_problem_data(url)
        print('Found {} solution(s) to {}.'.format(len(data),problem))
        write_data_to_file(problem, data)


if __name__ == '__main__':
    if(login(NAME, PASSWORD)):
        scrape_solutions()
    else:
        print("Login failed!")