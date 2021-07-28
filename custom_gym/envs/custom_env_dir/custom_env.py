import gym 
from gym import spaces
from gym.utils import seeding
from appium import webdriver
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from subprocess import Popen, PIPE
from dotenv import load_dotenv
import time
import random
import os

max_reward = 10

load_dotenv()

deviceName = os.getenv('deviceName')
appPackage = os.getenv('appPackage')
wait_activity = os.getenv('wait_activity')
automationName = os.getenv('automationName')
version = os.getenv('version')
platformName = os.getenv('platformName')
app_path = os.getenv('app_path_string')


start_time = time.time()
#3-20 char a-zA-Z0-9 
Unique_username = "Sylphsgt098VWE"
# 8-... a-zA-Z0-9 
Unique_password = "u8zvTBYNnnGn"
Email = "randomemail@gmail.com"

Unspecified_text = "YaaKcuMEgEsr"

PhoneNo = "0800000000"
firstname = "firstname"
lastname = "lastname"
Country = "Thailand"
Province = "Bangkok"
DOB = ""
Search = "Mark"


PII = {"email" : Email,
"user" : Unique_username,
"pass" : Unique_password,
"pwd" : Unique_password,
"pword" : Unique_password,
"phoneno" : PhoneNo,
"firstname" : firstname,
"lastname" : lastname,
"country" : Country, 
"province" : Province, 
"dob" : DOB,
"search" : Search
}

class CustomEnv(gym.Env):
    
    app_path_string = app_path
    app_path = os.path.abspath(app_path_string)

    desired_caps = {
            "deviceName" : deviceName,
            "platformName": platformName,
            "udid": deviceName,
            "version": version,
            "appActivity" : wait_activity,
            "appPackage" : appPackage,
            "app" : app_path,
            "autoGrantPermissions" : "true",
            "gpsEnabled" : "true",
            "noReset": "true",
            "fullReset" :"false",
            "automationName": automationName
        }

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    get_current_window_cmd = "dumpsys window windows | grep -E mCurrentFocus"

    # #get app activity
    # p = Popen(["adb","-s",deviceName,"shell",get_current_window_cmd], stdin=PIPE, stdout=PIPE, stderr=PIPE) 
    # output, err = p.communicate() 
    # rc = p.returncode
    # output = output.decode("utf-8").split('/')


    def __init__(self):

        super(CustomEnv,self).__init__()
        self.reward_range = (0,max_reward)
        self.action_space = spaces.Discrete(32)
        self.observation_space = spaces.Discrete(1)
        #self.state_counter = [1,2,3,4]
        self.state_counter = 0
        self.state = []
        self.state_with_activities = {}
        self.action_counter = 0
        self.current_state = -1
        self.performance_width = 0
        self.actions_performed = {}
        self.state.append(self.driver.current_activity)
        self.state_with_activities_current_episode = {}
        self.countOutOfPackage = 0
        self.driver.reset()
        time.sleep(3)
        self.action_count =0
        #for KhunLook only to move through popup page
        window_size = self.driver.get_window_size()
        height = window_size['height']
        width = window_size['width']
        action = TouchAction(self.driver)
         
 

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        #self.state_counter= [1,2,3,4]
        print("RESET APPLICATION!")
        self.current_state = -1
        self.state_counter = 0
        self.driver.close_app()
        self.driver.launch_app()
        self.state_with_activities_current_episode = {}
        self.action_counter = 0
        self.countOutOfPackage = 0
        
        #for KhunLook only to move through popup page
        #action = TouchAction(self.driver)
        #try : action.tap(None,height/2,width/2,2).release().perform()
        #except : print("tapped but crash")
        time.sleep(3) #sleep to wait for splash screen and popup screen in khunlook

        c,tx,total = self.getAction()
        Total_Elements_Expand = ['swipe','swipe','swipe','swipe']
        temp = 0 
        pointer = 0
        if len(total) > 0 : 
            while temp < 28 :
                Total_Elements_Expand.append(total[pointer])
                pointer+=1 
                temp+=1
                if pointer == len(total):
                    pointer = 0
        else : 
            while temp < 28 :
                Total_Elements_Expand.append('swipe')
                temp+=1
        self.current_state,e = self.check_state(c,tx,total,Total_Elements_Expand)

        return self.state, self.current_state, self.state_with_activities

    def getAction(self):
        Clickable_Elements = self.driver.find_elements_by_android_uiautomator("new UiSelector().clickable(true)")
        Textinput_Elements = []
        Total_Elements = Clickable_Elements
        
        for element in Clickable_Elements:
            if element.get_attribute("class") == "android.widget.EditText" and element.get_attribute("focusable") == 'true':
                Textinput_Elements.append(element)
        
        Clickable_Elements = list(set(Clickable_Elements) - set(Textinput_Elements))
    
        return Textinput_Elements,Clickable_Elements,Total_Elements


    def check_state(self,Total_Elements,Clickable_Elements,Textinput_Elements,Total_Elements_Expand):
        current_activity = self.driver.current_activity
        current_state = self.current_state   
        if current_activity not in self.state:
            print("activity not in state, this is a new activity")
            explored = True
            current_state = len(self.state_with_activities)
            self.state.append(current_activity)
            state_key = current_state
            self.state_with_activities_current_episode[state_key] = [len(Total_Elements),len(Clickable_Elements),len(Textinput_Elements),Total_Elements_Expand,current_activity]
            self.state_with_activities[state_key] = [len(Total_Elements),len(Clickable_Elements),len(Textinput_Elements),Total_Elements_Expand,current_activity]
            self.actions_performed[state_key]=[]
        else :   
        # have seen this activity before
           
            explored = True
            count_occurence = 0
            for k,v in self.state_with_activities.items():
                    #have seen this activity in this episode with same number of clickable and text elements
                    if current_activity in v[4]:
                        if v[1] == len(Clickable_Elements) and v[2] == len(Textinput_Elements):
                            print("same activity and same number of actions")
                            explored = False
                            current_state = k
                            self.state_counter+=1
                            break
                        count_occurence +=1
            if explored :
                #have seen this activity in this episode but different buttons
                print("activity is in state, but the number of actions is different")
                current_state = len(self.state_with_activities)
                state_key = current_state
                self.state_with_activities_current_episode[state_key] = [len(Total_Elements),len(Clickable_Elements),len(Textinput_Elements),Total_Elements_Expand,current_activity]
                self.state_with_activities[state_key] = [len(Total_Elements),len(Clickable_Elements),len(Textinput_Elements),Total_Elements_Expand,current_activity]
                self.actions_performed[state_key]=[]
            
        self.current_state = current_state

        return current_state,explored



    def step(self, action):
        reward = 0
        previous_state = self.current_state
        assert self.action_space.contains(action) #try catch
        (Textinput_Elements,Clickable_Elements,Total_Elements) = self.getAction()
        Total_Elements_Expand = ['swipe','swipe','swipe','swipe']
        temp = 0 
        pointer = 0
        if len(Total_Elements) > 0 : 
            while temp < 28 :
                Total_Elements_Expand.append(Total_Elements[pointer])
                pointer+=1 
                temp+=1
                if pointer == len(Total_Elements):
                    pointer = 0
        else : 
            while temp < 28 :
                Total_Elements_Expand.append('swipe')
                temp+=1

       
        element= Total_Elements_Expand[action]

        indices = [i for i, x in enumerate(Total_Elements_Expand) if x == element]
        
        if element == 'swipe':
            #Swipe
            window_size = self.driver.get_window_size()
            height = window_size['height']
            width = window_size['width']
            temp = random.randrange(3)
            #driver.swipe(startX, startY, endX, endY, duration)
        
            action = TouchAction(self.driver)
            if temp == 0:
                try : self.driver.swipe(int(width/2), int(height*3/4), int(width/4), int(height*3/4), 400)                    
                except:
                    print("Can not swipe")                            
            if temp == 1:
                try : self.driver.swipe(int(width*1/4), int(height*3/4), int(width/2), int(height*3/4), 400)                         
                except: 
                    print("Can not swipe")       
            if temp == 2:
                try : self.driver.swipe(int(width/2), int(height/2), int(width/2), int(height*3/4), 400)                              
                except: 
                    print("Can not swipe")        
            if temp == 3:
                try : self.driver.swipe(int(width/2), int(height*3/4), int(width/4), int(height/2), 400)                           
                except: 
                    print("Can not swipe")       


        elif element in Textinput_Elements:
            for text_field_element in Textinput_Elements:
                resource_id = text_field_element.get_attribute
                x = self.actions_performed[self.current_state]
                if action not in x:
                    reward+=30
                    self.performance_width +=1
                    x.append(action)
                    self.actions_performed.update({self.current_state:x})
                else :
                    self.action_counter+=1
                    reward += 30*(1/self.action_counter)

            #fill username with unique value
            # text_field_element.send_keys(Unspecified_text)
                i=1
                for pii in PII: 
                    try:
                        if pii in resource_id.lower():
                            text_field_element.click()
                            text_field_element.send_keys(PII[pii]+"\n")
                            self.driver.hide_keyboard()
                            
                            break
                        else:
                            i= i+1
                            if i > len(PII):
                                text_field_element.click()
                                try:    
                                    text_field_element.send_keys("text"+ "\n")
                                    self.driver.hide_keyboard()
                                except : 
                                    try : 
                                        self.driver.press_keycode(8)
                                        self.driver.press_keycode(7)
                                        self.driver.hide_keyboard()
                                    except : 
                                            print("not a text nor a number")
                                            self.driver.hide_keyboard()


                    except:
                        text_field_element.click()
                        try:
                            text_field_element.send_keys("no resource id this is a random text"+ "\n")
                            self.driver.hide_keyboard()
                            print("no resource ID")
                            break
                        except:
                            self.driver.press_keycode(8)
                            self.driver.press_keycode(7)
                            self.driver.hide_keyboard()
                            print("no resourceID")
                            break
                                
            #ELSE IF ACTION TO PERFORM IS A BUTTON CLICK BUTTON
        elif element in Clickable_Elements:
            x = self.actions_performed[self.current_state]
            if action not in x:
                x.append(action)
                self.performance_width +=1
                self.actions_performed.update({self.current_state:x})
                reward += 30
            else: 
                self.action_counter+=1 
                reward +=-1*(self.action_counter) 
            element.click() 
            
        (current_state,explored) = self.check_state(Total_Elements,Clickable_Elements,Textinput_Elements,Total_Elements_Expand)
    
        (next_click,next_text,next_total) = self.getAction()
        if len(next_total) > len(Total_Elements):
            reward+= 6
        

        if self.action_counter > 3 :
            reward += -10
            done = True
            print("done clicked same action twice")
        else: 
            done = False

        if self.state_counter > 10 : 
            print("done reach same state 10 times")
            #reward += -5
            done = True
        else : 
            done = False
        
        if explored:
            reward += 30
  
        
        if (self.driver.current_package != appPackage):
            self.driver.back()
            self.countOutOfPackage += 1
            reward += -3
        
        if (self.countOutOfPackage == 5):
            self.reset()
        
        self.action_count +=1
        time.sleep(0.5)
        return self.current_state, reward, done, indices,self.state_with_activities,self.action_count
        
    
