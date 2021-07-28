import datetime
import numpy as np
import pandas as pd
import os


class QTable(object):
    stateCount = 0
    stateList = {}

    def __init__(
        self,
        observation_space=1,
        action_space=32, 
        alpha=0.3, 
        gamma=0.9,
        ):
        self.alpha             = alpha
        self.gamma             = gamma
        self.observation_space = observation_space
        self.action_space      = action_space
        self.q               = np.zeros(self.observation_space * self.action_space)\
                                    .reshape((self.observation_space, self.action_space))
    
    
    def addStateList(self, stateName, noActionClickable, noActionTextInput):
        for key, value in self.stateList.items():  
            if (value[0],value[1],value[2]) == (stateName,noActionClickable, noActionTextInput):
                print("key in statelist =" + str(key))
                return key                   
        self.stateList[self.stateCount] = [stateName, noActionClickable, noActionTextInput]
        print(len(self.stateList))
        self.addStateToQ()
        self.stateCount +=1
        return -1

    def eq(self, state=None, action=None):
        if state is None:
            return self.q
        if action is None:
            return self.q[state]
        return self.q[state][action]
    
    def update_q(self, state, action, value,i):
        self.q[state][action] = value
        for element in i :
            self.q[state][element] = value

    def max_q(self, state):
        return np.max(self.q[state])

    def old_value(self, state, action):
        return (1 - self.alpha) * self.eq(state, action)

    def discounted_reward(self, state):
        return self.gamma * self.max_q(state)

    def sarsa_max_update(self, s, a, r, new_s, i):
            new_value = self.old_value(s, a) + (self.alpha * (r + self.discounted_reward(new_s) - self.eq(s, a)))
            self.update_q(s, a, new_value,i)
        
    def saveQ(self, score, name):
        
        df = pd.DataFrame(self.q[:-1, :],dtype=np.float)
       
        if not os.path.exists('result/QValue/' +str(name) +'QValue.csv'):
            df.to_csv('result/QValue/' +str(name) +"QValue.csv")
        else: # else it exists so append without writing the header
            x = 1
            nn = 'result/QValue/' +str(name) + "("+ str(x) +")QValue.csv"
            while os.path.exists(nn):
                x += 1
                nn = 'result/QValue/' +str(name) + "("+ str(x) +")QValue.csv"
            df.to_csv(nn)


    def saveStateList(self,name):
        st = pd.DataFrame.from_dict(self.stateList, orient = "index")
        stateList_str = 'result/Statelist/'
        if not os.path.exists(stateList_str +str(name) +'stateList.csv'):
            st.to_csv(stateList_str +str(name) +"stateList.csv")
        else: # else it exists so append without writing the header
            y = 1
            yy = stateList_str +str(name) + "("+ str(y) +")stateList.csv"
            while os.path.exists(yy):
                y += 1
                yy = stateList_str +str(name) + "("+ str(y) +")stateList.csv"
            st.to_csv(yy)

    def readQ(self,name):
        readFile = pd.read_csv('result/QValue/' +str(name) + 'QValue.csv',header = None).values[1:,1:]
        self.q = readFile
        self.observation_space = np.size(self.q,0)
        self.q.reshape((self.observation_space, self.action_space))
        BB = np.zeros(self.action_space)\
                                        .reshape((1, self.action_space))
            
        CC = np.vstack((self.q,BB))
        self.q = CC
        print ("q = ")
        print (self.q)
        print("readFile = ")
        print (readFile)
    
    def readStateList(self, name):
        rd = pd.read_csv('result/Statelist/' +str(name) + "stateList.csv").iloc[:, 1:]
        d = rd.to_dict("split")
        d = dict(zip(d["index"], d["data"]))
        self.stateList = d
        print ("stateList = ")
        print(self.stateList)
        print ("d = ")
        print(d)

    def addStateToQ(self):
            A = self.q
            B = np.zeros(self.action_space)\
                                        .reshape((1, self.action_space))
            
            C = np.vstack((A,B))
            print("length after add +1 to Q = "+ str(len(C)))
            self.q = C
            self.observation_space = self.observation_space +1 
        


    

    