from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PyPDF2 import PdfFileMerger
import pyautogui as keyboard
import img2pdf
import subprocess
import time
import os

# TODO need to move to config or env file
final_page = "822" #page_num variable is of type string, can't be changed
image_dir = os.path.join(os.getcwd(), 'images')
pdfs_dir = os.path.join(os.getcwd(), 'pdfs')
book_name = "Elementary_Statistics.pdf"
USER = 'SomeUserName'
PASS = 'SomePassword'

def site_login():
    driver.get("https://canvas.park.edu/login/ldap")
    driver.find_element_by_id('pseudonym_session_unique_id').send_keys(USER)
    driver.find_element_by_id('pseudonym_session_password').send_keys(PASS)
    driver.find_element_by_xpath('//*[@id="login_form"]/div[3]/div[2]/button').click()

def nav_to_book():
    driver.find_element_by_css_selector('.ic-DashboardCard__header_hero').click()
    driver.find_element_by_css_selector('.section a[title="Modules"]').click()
    driver.find_element_by_css_selector('a[title*="Unit 1: MyStatLab Pearson eText"]').click()
    driver.find_element_by_xpath('//*[@id="tool_form"]/div/div[1]/div/button').click()
    time.sleep(13)

def close_warning():
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_id('dontshowme').click()
    driver.find_element_by_xpath('//*[@id="browserCheckerMessage"]/div[2]/div/div[1]/button').click()
    time.sleep(15)

def first_image():
    img = driver.find_element_by_css_selector('img#docViewer_ViewContainer_BG_0')
    img_url = img.get_attribute('src')
    page_num = driver.find_element_by_id('goToPageTextField').get_attribute('value')
    actions.move_to_element(img).context_click().perform()
    time.sleep(1)
    save_img(page_num)
    time.sleep(2)

def nav_book():
    page_count = 1 #one for the first image
    prev_page = 0
    while True:
        driver.find_element_by_id('goToNextPage').click()
        time.sleep(3)
        page_num = driver.find_element_by_id('goToPageTextField').get_attribute('value')
        if page_num == 'index':
            print(f"{prev_page} was the last working page.")
            restart_scrape(prev_page)
        keyboard.click(button='right')
        save_img(page_num)
        page_count += 1
        prev_page = page_num
        if page_num == final_page:
            print(f"{page_count} pages were scraped.")
            return False

def restart_scrape(page):
    driver.find_element_by_id('goToPageTextField').click()
    press_button('backspace', 2)
    keyboard.typewrite(page)
    keyboard.press('enter')
    time.sleep(3)
    nav_book()

def close_sel():
    driver.quit()

def error_handler():
    pass

def img_to_pdf():
    sorted_dir = os.popen('ls -tr {}'.format(image_dir)).read().split('\n')
    for img in sorted_dir:
        print(img)
        if not img:
            continue
        pdf_loc = os.path.join(pdfs_dir, "{}.pdf".format(img.split('.')[0]))
        img_loc = os.path.join(image_dir, img)
        with open(pdf_loc, 'wb') as pdf:
            pdf.write(img2pdf.convert(img_loc))
            time.sleep(1)

def stitch_book():
    pdf_merger = PdfFileMerger()
    sorted_dir = os.popen('ls -tr {}'.format(pdfs_dir)).read().split('\n')
    for pdf in sorted_dir:
        if not pdf:
            continue
        print(pdf)
        pdf_path = os.path.join(pdfs_dir, pdf)
        pdf_merger.append(pdf_path)
    with open(book_name, 'wb') as fileobj:
        pdf_merger.write(fileobj)

def main():
    site_login()
    nav_to_book()
    close_warning()
    first_image()
    nav_book()
    close_sel()
    img_to_pdf()
    stitch_book()

## Helper Functions

def press_button(key_val, mult=1):
    if mult == 1:
        keyboard.press(key_val)
    else:
        for i in range(mult):
            keyboard.press(key_val)

def save_img(page_num):
    press_button('down', 4)
    press_button('enter')
    keyboard.typewrite('page-{}'.format(page_num))
    press_button('enter')

def getmtime(folder, name):
    path = os.path.join(folder, name)
    return os.path.getmtime(path)

if __name__ == '__main__':
    options = Options()
    options.set_preference("browser.download.folderList",2)
    options.set_preference("browser.download.dir", image_dir)
    driver = webdriver.Firefox(firefox_options=options)
    actions = ActionChains(driver)
    main()
