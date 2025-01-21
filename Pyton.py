import numpy as np
import pandas as pd
import requests
import io

# Download the CSV data
file_id = '11SYH6uH2NCSgA1RH1wzR88YcDz3Yr86I'
download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
response = requests.get(download_url)
csv_data = response.content.decode('utf-8')


data = pd.read_csv(io.StringIO(csv_data))


class PricingEnvironment:
    def __init__(self, data):
        self.data = data
        self.currentIndex = 0
    
    def reset(self):
        self.currentIndex = 0
        return self.data.iloc[self.currentIndex]
    
    def step(self, action):
    
        currentState = self.data.iloc[self.currentIndex]
        nextIndex = self.currentIndex + 1
        nextState = self.data.iloc[nextIndex]
        
        
        reward = (nextState['Total Sales'] - currentState['Total Sales']) + \
                 (nextState['Organic Conversion Percentage'] - currentState['Organic Conversion Percentage'])
        
      
        if nextState['Total Sales'] < currentState['Total Sales']:
            reward -= 10  
        
        self.currentIndex = nextIndex
        
        done = self.currentIndex >= len(self.data) - 1
        
        return nextState, reward, done

#DQN logic
def qLearning(env, episodes=1000, learningRate=0.1, discountFactor=0.95, explorationRate=1.0, explorationDecay=0.995):
  
    qTable = np.zeros((env.data.shape[0], 10))  # 10 possible price actions
    
    for episode in range(episodes):
        state = env.reset()
        
        done = False
        while not done:
          
            if np.random.random() < explorationRate:
                action = np.random.choice(10)  
            else:
                action = np.argmax(qTable[state])
            
            nextState, reward, done = env.step(action)
            
            
            qTable[state, action] = qTable[state, action] + learningRate * \
                                    (reward + discountFactor * np.max(qTable[nextState]) - qTable[state, action])
            
            state = nextState     
        explorationRate *= explorationDeca
    return qTable
env = PricingEnvironment(data)
qTable = qLearning(env)
