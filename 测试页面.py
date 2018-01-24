import unittest
from selenium import webdriver
import time

class LearnElement(unittest.TestCase):
    #初始化，打开浏览器
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://www.baidu.com')
     #--------元素定位-------------
    #<input id="kw" name="wd" class="s_ipt" value="" maxlength="255" autocomplete="off">
    def testGetElement(self):
        #通过id定位
        element = self.driver.find_element_by_id('kw')

        # 通过class name定位
        #element=self.driver.find_element_by_class_name('s_ipt')
        #通过name定位
        #element = self.driver.find_element_by_name('wd')
        #通过teg name定位
        #element=self.driver.find_element_by_tag_name('input')
        
        element.send_keys('through id')
        submit = self.driver.find_element_by_id('su')
        submit.click()
        time.sleep(1)

        lst=self.driver.find_elements_by_class_name('c-index')
        for ll in lst:
            href = ll.text
            print(href)
        time.sleep(2)
        print("------------------分割线-----------------");
        ele=self.driver.find_element_by_xpath("//a[contains(text(),'精华')]")
        print(ele.text);
        print(ele.get_attribute('href'));
        ele.click()
        print("------------------分割线-----------------");
    #--------关闭浏览器------------
    #def tearDown(self):
     #   self.driver.quit()

if __name__ == '__main__':
    #unittest.main()
    l=LearnElement();
    l.setUp();
    l.testGetElement();