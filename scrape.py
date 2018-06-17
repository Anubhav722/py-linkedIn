import csv
import parameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector

def validate_field(field):
    if field:
        pass
    else:
        field = ''
    return field

writer = csv.writer(open(parameters.file_name, 'wb'))
writer.writerow(['Name', 'Job Title', 'School', 'Location', 'Company', 'Url'])

driver = webdriver.Chrome(parameters.chromedriver_path)

driver.get('https://www.linkedin.com')

# Enter username and password
username = driver.find_element_by_class_name('login-email')
password = driver.find_element_by_class_name('login-password')

# Send keys
username.send_keys(parameters.linkedin_username)
sleep(0.5)
password.send_keys(parameters.linkedin_password)
sleep(0.5)

sign_in_button = driver.find_element_by_id('login-submit')
sign_in_button.click()
sleep(5)

driver.get('https://www.google.com')
sleep(3)

search_query = driver.find_element_by_name('q')
search_query.send_keys(parameters.search_query)
sleep(0.5)

search_query.send_keys(Keys.RETURN)
sleep(3)

linkedin_urls = driver.find_elements_by_tag_name('cite')
linkedin_urls = [url.text for url in linkedin_urls if 'linkedin' in url.text]
sleep(0.5)

# print (linkedin_urls)

for linkedin_url in linkedin_urls:
    driver.get(linkedin_url)
    sleep(5)

    sel = Selector(text=driver.page_source)
    name = sel.xpath('//h1/text()').extract_first().strip()
    job_title = sel.xpath('//h2/text()').extract_first().strip()
    if job_title:
        job_title = job_title.strip()

    school = sel.xpath('//*[starts-with(@class, "pv-top-card-section__school")]/text()').extract_first()

    if school:
        school = school.strip()

    location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first()
    if location:
        location = location.strip()

    company = sel.xpath('//*[starts-with(@class, "pv-top-card-sectio__company")]/text()').extract_first()
    if company:
        company = company.strip()

    url = driver.current_url

    name = validate_field(name)
    job_title = validate_field(job_title)
    school = validate_field(school)
    location = validate_field(location)
    company = validate_field(company)
    url = validate_field(url)



    print '\n'
    print 'Name: ' + name
    print 'Job Title: ' + job_title
    print 'School: ' + school
    print 'Location: ' + location
    print 'Company: ' + company
    print 'Url: ' + url
    print '\n'

    writer.writerow([name.encode('utf-8'),
                     job_title.encode('utf-8'),
                     school.encode('utf-8'),
                     location.encode('utf-8'),
                     company.encode('utf-8'),
                     url.encode('utf-8')])


driver.quit()
