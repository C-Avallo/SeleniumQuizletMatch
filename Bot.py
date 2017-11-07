
from selenium import webdriver
import time
import pickle
import sys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pymsgbox

class Bot:

    pathtoQuizletAnswers = ""

    driver = webdriver.Chrome()
    driver.set_window_position(0,0)
    driver.set_window_size(600, 1000)

    def Login_With_Google(self, username, password):

        time_sleep = 4

        self.driver.get("https://quizlet.com/login")
        print("Opened Quizlet")
        time.sleep(time_sleep)
        self.driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/div/div[1]/div/a/span/div').click()
        time.sleep(time_sleep)
        self.driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(str(username))
        time.sleep(time_sleep)
        print("Entered Username")
        self.driver.find_element_by_xpath('//*[@id="identifierNext"]/content/span').click()
        time.sleep(time_sleep)
        self.driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(str(password))
        time.sleep(time_sleep)
        print("Entered Password")
        self.driver.find_element_by_xpath('//*[@id="passwordNext"]/content').click()
        time.sleep(time_sleep)
        print("Proceeding")

    def Login(self, username, password):

        self.driver.get("https://quizlet.com/login")
        print("Opened Quizlet")
        time.sleep(4)
        self.driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/form/div[1]/div/label[1]/div/input').send_keys(str(username))
        print("Entered Username")
        self.driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/form/div[1]/div/label[2]/div/input').send_keys(str(password))
        print("Entered Password")
        self.driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div[2]/form/button').click()
        time.sleep(4)
        print("Proceeding")

    def playLearn(self, gameId):
        self.driver.get("https://quizlet.com/{}/write".format(str(gameId)))
        Quizlet_Txt = open(pathtoQuizletAnswers, "r")
        quizlet_text = Quizlet_Txt.readlines()
        time.sleep(2)
        question_num = self.driver.find_element_by_xpath('//*[@id="LearnModeTarget"]/div/div/div/div[1]/div/div/div/div[2]/div[1]/div/div[1]').text
        question_num_final = str(question_num).replace(" REMAINING", "")

        for i in range(int(question_num_final)):
            question = self.driver.find_element_by_xpath(
                '//*[@id="js-learnModeInner"]/div/div/div[1]/div/div/div/div/span').text

            for p in range(len(quizlet_text)):

                if(quizlet_text[p] in question):
                    q_split = quizlet_text[p].split(":")
                    self.driver.find_element_by_xpath('//*[@id="user-answer"]').send_keys(str(q_split[1]))
                    self.driver.find_element_by_xpath('//*[@id="js-learnModeAnswerButton"]').click()




    def playMatch(self, gameName, gameId, Length, speed):

        time_to_wait = float(speed)
        Quizlet_Txt = open(pathtoQuizletAnswers, "r")
        quizlet_text = Quizlet_Txt.readlines()

        self.matchConfig(gameId)

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        answers = []
        questions = []

        questions.append(0)

        for x in range(len(quizlet_text)):
            try_line = quizlet_text[x].split(":")
            answers.append(try_line[0])

        for y in numbers:
            questions.append(self.driver.find_element_by_xpath('//*[@id="MatchModeTarget"]/div/div/div/div[2]/div/div/div[{}]/div/div/div/div'.format(str(y))).text)

        for j in numbers:
            try:
                question = questions[j]
            except:
                print("-")

            if(question in answers):

                try:
                    self.driver.find_element_by_xpath('//*[@id="MatchModeTarget"]/div/div/div/div[2]/div/div/div[{}]'.format(str(j))).click()
                    time.sleep(time_to_wait)

                except:
                    print("-")

                for p in range(len(quizlet_text)):

                    if question in quizlet_text[p]:
                        current_line = quizlet_text[p].split(":")
                        print("Question: " + question + ". Solved with answer: " + str(current_line[1]))

                        for o in numbers:
                            try:
                                answer_o = self.driver.find_element_by_xpath('//*[@id="MatchModeTarget"]/div/div/div/div[2]/div/div/div[{}]/div/div/div/div'.format(str(o))).text
                            except:
                                print("-")

                            if(answer_o in current_line[1]):
                                try:
                                    self.driver.find_element_by_xpath('//*[@id="MatchModeTarget"]/div/div/div/div[2]/div/div/div[{}]'.format(str(o))).click()
                                    time.sleep(time_to_wait)
                                except:
                                    print("-")

        time_test = 0
        while True:
            try:
                self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div/div/div[1]/button")
                break
            except:
                time.sleep(.01)
                time_test+=1
                if(time_test > 500):
                    print("Error - went to fast, quizlet could not recognize clicks")
                    pymsgbox.alert("Error - Quizlet Failure: Use a better computer next time/change wait time", "Lazy-Quizlet", "Ok", root=None, timeout=None)
                    break
        path = "screen.png"
        self.driver.save_screenshot(path)
        self.showImage(path)
        self.driver.quit()

    def matchConfig(self, gameID):
        time.sleep(1)
        self.driver.get("https://quizlet.com/" + str(gameID) + "/match")
        time.sleep(3)
        try:
            self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div/div/div/div[2]/button').click()
        except:
            self.driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/div/div/div/div[2]/button').click()

    def showImage(self, path):
        img = Image.open(path)
        img.show()


