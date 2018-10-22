import time
import sys
import xlwt
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument("start-maximized")
options.add_argument('--ignore-certificate-errors')
options.add_argument("--disable-notifications")
driver = webdriver.Chrome(chrome_options=options)
driver.get("http://www.facebook.com")
driver.implicitly_wait(30)


def fetch_group_member_details(user, pwd, group_name):

    book = xlwt.Workbook()
    sheet = book.add_sheet('GroupMembersInfo', cell_overwrite_ok=True)
    try:
        sheet.write(0, 0, '#')
        sheet.write(0, 1, 'Name')
        sheet.write(0, 2, 'Profile Link')

        # Enter Email
        email_el = driver.find_element_by_id('email')
        email_el.send_keys(user)

        # Enter Password
        password_el = driver.find_element_by_id('pass')
        password_el.send_keys(pwd)

        # Click on Login Button
        login_button_el = driver.find_element_by_id('loginbutton')
        login_button_el.click()

        driver.get('https://www.facebook.com/groups/{}/members/'.format(group_name))
        members_count = driver.find_element_by_xpath("//div[@id='groupsMemberBrowser']/div/div/div/a/../span")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        members = int(members_count.text.replace(',',''))
        print "Total members: " + str(members)
        x = 0
        print datetime.now()
        for _ in range(14500):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            group_el = driver.find_elements_by_xpath(
                "//div[@data-name='GroupProfileGridItem']/div/div[2]/div/div[2]/div[1]/a")
            y = len(group_el)
            # print "x:"+ str(x),
            # print "y:"+ str(y)

            for index in range(x, y):
                x = y
                print index,
                sheet.write(index, 0, index)

                # print group_el[index].text.encode('utf-8')
                sheet.write(index, 1, group_el[index].text.encode('ascii', 'ignore').decode('ascii'))

                profile_url = group_el[index].get_attribute('href')
                if 'profile.php' in profile_url:
                    sep = '&'
                else:
                    sep = '?'
                # print profile_url.split(sep, 1)[0]
                sheet.write(index, 2, profile_url.split(sep, 1)[0])
                # print "Save data to the workbook"
                book.save('GroupDetails.xls')

    finally:
        print 'End of Script Execution'
        driver.quit()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: scrape.py username password groupname"
    else:
        username = sys.argv[1]
        password = sys.argv[2]
        groupname = sys.argv[3]
        fetch_group_member_details(username, password, groupname)
