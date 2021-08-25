from selenium import webdriver
from time import sleep
from scrapy.selector import Selector
from PIL import Image
import os
import datetime
import shutil
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys

# client_image/img, output_images/img, template_with_date/{date}/img, output_not_sent/img

def getting_list(num):
    """ creates list of customer names from inbuilt folder
    """
    if num == 2:
        client_raw_list = os.listdir(r"./client_images/")
    elif num == 1:
        client_raw_list = os.listdir(r"./output_images/")
    client_list = []
    for index in range(len(client_raw_list)):
        client_name = client_raw_list[index].split(".")[0]
        client_list.append(client_name)
    return client_list    
    
def sending_whatsapp():
    """Sends ready images to the customers whatsapp account
    """
    path_output_not_sent = os.getcwd() + "\\output_not_sent"
    try:
        os.mkdir(path_output_not_sent)
    except:
        shutil.rmtree(path_output_not_sent)
        os.mkdir(path_output_not_sent)
    chrome_options = Options()
    chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    driver = webdriver.Chrome("./driver.exe", options=chrome_options)
    #driver = webdriver.Chrome("./driver/driver.exe")
    driver.get("https://web.whatsapp.com/")
    sleep(1)
    signal = input("\n\nPress Any Character Key after successful Login... ")
    success = 0
    fails = 0
    client_list = getting_list(1)
    for client_name in client_list:
        path = r"\\output_images\\{}.jpg".format(client_name)
        path = os.getcwd() + path
        if '- copy' in path:
            client_name = client_name.split('-')[0]
        # Search name on whatsapp
        # changed 26-04-2021 Edited new concept of backspace
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/label/div/div[@class="_13NKt copyable-text selectable-text"]').click()
        sleep(0.5)
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/label/div/div[@class="_13NKt copyable-text selectable-text"]').clear()
        sleep(1)
        # changed 01-03-2021 class="_1awRl copyable-text selectable-text"
        # changed 15-07-2021 class="_2_1wd copyable-text selectable-text" to
        driver.find_element_by_xpath('/html/body/div/div/div/div/div/div/div/label/div/div[@class="_13NKt copyable-text selectable-text"]').send_keys(client_name)
        sleep(3)
        # trying to click and send data
        try:
            # click on name of client from left bar
            driver.find_element_by_xpath("//div/div/div/div/div/div/span/span[@title='{}']".format(client_name)).click()
            sleep(2)
            # click on attach document in messages
            driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[1]/div[2]/div/div[@title="Attach"]').click()
            sleep(1)
            # attaching file to send
            driver.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[1]/div[2]/div/span/div/div/ul/li[1]/button/input').send_keys(path)
            #                             /html/body/div/div/div/div/div/footer/div/div/div/div/span/div/div/ul/li[3]/button/input[@type="file"]').send_keys(path)
            sleep(3)
            # changed xpath on 17 aug 2021
            driver.find_element_by_xpath('//div/div/div/div[@class="_165_h _2HL9j"]').click()
            #                             /html/body/div/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div/span/svg/path
            #                             /html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/span/div/div').click()
            sleep(2)
            print("Successfully Sent to ", client_name)
            success = success + 1
        # if fails, person name not found, then
        except:
            shutil. copy(path, path_output_not_sent)
            print("\n\n\t\t\tERROR : PERSON NOT FOUND : ", client_name, "\n\n")
            fails = fails + 1
        
    print("\n\nImages Successfully Sent : ", success)
    print("\n\nImages Not Sent : ", fails)

def join_images():
    """ joining images and saving file at output_images
    """
    client_list = getting_list(2)
    image3 = Image.open('./contact_image.jpg')
    current_date = datetime.datetime.now()
    date = str(current_date.day) + '-' + str(current_date.month) + '-' + str(current_date.year)
    #Read the two images
    # ===================================== TEST
    # if user wants to make images in prior than uncomment the line below and comment next line to the line below.
    # in such a case we have to make folder with the name of the particular date in which we want to send it to the customer(like ./template_with_date/25-08-2021/image.jpg) and save the "image.jpg" in the date named folder.
    # otherwise simply paste "image.jpg" in the "template_with_date" folder.
    #image1 = Image.open('./template_with_date/{}/image.jpg'.format(date))
    image1 = Image.open('./template_with_date/image.jpg')
    #image1.show()
    for client_name in client_list:
        image2 = Image.open('./client_images/{}.jpg'.format(client_name))
        #image2.show()
        #resize, first image
        image1 = image1.resize((2404, 1660))
        image2 = image2.resize((2404, 1610))
        image1_size = image1.size
        image2_size = image2.size
        new_image = Image.new('RGB', (2404, 3304), (250, 250, 250))
        new_image.paste(image1, (0, 0))
        new_image.paste(image2, (0, image1_size[1]))
        new_image.paste(image3, (0, image1_size[1] + image2_size[1]))
        new_image.save("./output_images/{}.jpg".format(client_name))

def main_method():
    print("          DEVELOPED BY : PARDEEP GREWAL \n\n")
    print('  #####     #     #####  ######   #####  #####  #####')
    print('  #   #    # #    #   #    #   #  #      #      #   #')
    print('  #####   #   #   #####    #   #  ####   ####   #####')
    print('  #      #######  # #      #   #  #      #      # ')
    print('  #     #       # #   #  ######   #####  #####  # \n\n')
    
    print("Creating Images...")
    path = r"\\output_images"
    path = os.getcwd() + "\\output_images"
    try:
        os.mkdir(path)
    except:
        shutil.rmtree(path)
        os.mkdir(path)
    join_images()
    
    sending_whatsapp()
    shutil.rmtree(path)
    f = input("Task completed... PRESS ANY KEY AND THEN RETURN TO CLOSE... ")

main_method()
