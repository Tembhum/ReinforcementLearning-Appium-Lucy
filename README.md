# Lucy
Reinforcement learning based android application testing tool, implementing with Appium which extracts android GUI components and choosing actions based on the QTable.

# Installation
1.  Install the virtalenv and all the required packages/libraries on requirement.txt by using the command pip install -r
    requirements.txt in the virtalenv directory. requirement.txt is in the z folder in the senior directory.
2.  Setup the environment according to the link belowed
    https://medium.com/@apoddar573/making-your-own-custom-environment-in-gym-c3b65ff8cdaa
    *The custom env is the reinforcement learning environement cloned from this repo
3.  Install the appium desktop
4. Install the android studio and the android emulator in case you don't have an android device
    
# Parts
1. Environment

    OVERVIEW : The appium environment which performed actions available on the connected device.
    
    DIRECTORY FOR ENVIRONMENT : senior/custom_gym/envs/custom_env_dir/custom_env.py

    CONFIG FOR ENVIRONMENT: 
    - Application Path => app_path_string = '../senior/apps/duolingo.apk'
    - Landing Page => wait_activity = 'com.duolingo.app.LoginActivity'
    - Package Name => appPackage = 'com.duolingo'
    - DeviceName => deviceName = "emulator-5554"

    METHODS :
    - init : initialize the environment (open the application configured in app path on the connected device and get the available      actions on the home page)
    - reset : reset the environment at the beginning of a new episode (reset the parameters)
    - getAction : get a numpy list of  clickable, text_inputs, and total (clickable + textinput) actions
    - check_state : return current state and check whether it is already explored in the current episode
    - step : performed action and get state after performing the action, reward, and check for episode ends.

2. Agent

    OVERVIEW: The agent used to store Q Table, choose action to be performed, and walk through the environment.
    
    DIRECTORY FOR AGENT : senior/custom_gym/z/agent

    CONFIG FOR AGENT
    - observation_space = no. of possible states (in our case, we started from 1 and increment after a new state is found)
    - action_space = no. of possible actions (we 32 as max no. of actions)
    - alpha = learning rate
    - gamma = discount factor
    - epsilon = rate of exploration
    - epsilon_decay = rate of decay on the epsilon after each episodes

    METHODS:
    - update epsilon : update the epsilon using epsilon decay
    - epsilon_greedy : choose action from Q Table
    - select_action : given a state, select an action with greedy approach
    - step : update q after the step in environment using rewards from the action performed in the last step
    - addState : add a state and observation space if new state is discovered

3. Q Table

    OVERVIEW: q table
    
    DIRECTORY FOR Q TABLE : senior/custom_gym/z/QTable

    CONFIG for Q TABLE:
    -  same as Agent

    METHODS:
    - addStateList : state list is a table showing the name of the state with the state id used in Q table, addStateList add new row to the stateList
    - eq : get q value
    - update_q: update q value
    - max_q: find max q in the given state(row)
    - old_value: store old q value before updated
    - discounted_reward: gamma multiplied to the new q value
    - sarsa_max_update: use update_q to update q value
    - saveQ: print Q Table to csv
    - saveStateList: save state list to csv
    - readQ: read Q value from the saved csv file
    - readStateList: read stateList from the saved csv file
    - addStateToQ: add new row to Q Table

4. Monitor

    OVERVIEW: a medium between environment and agent, control episodes 
    
    DIRECTORY FOR MONITOR : senior/custom_gym/z/monitor

    CONFIG FOR MONITOR:
    - appName = 'duolingoShow' => name used in the prefix for saving QTable in csv
    - num_episodes = 30 (set number of episodes for your implementation)

    METHODS:
    - interact : perform a session with setted no. of episodes, print QTable and State List at the end of the whole session


5. Main

    OVERVIEW: run the code
    
    DIRECTORY FOR MAIN : senior/custom_gym/z/main


# How to run
1. Config all the parameters following the above
2. Open terminal
3. Run Appium Desktop, set Host to 0.0.0.0 and port to 4723 
4. Run android studio, run android emulator
5. Run the main file in the terminal by typing python main.py in MAIN DIRECTORY
6. Choose in the terminal between LoadQTable from previous session or not
7. If yes then type the name of session, and the session will start
8. If no then the session started 
9. Session starts
