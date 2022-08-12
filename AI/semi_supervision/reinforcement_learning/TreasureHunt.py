import numpy as np
import pandas as pd
import time
np.random.seed(2)
N_STATES=6
ACTIONS=['Left','Right']
EPSILON=0.9#greedy police
ALPHA=0.1#learning rate
LAMBDA=0.9#discount factor
MAX_EPISODES=13#maximum episodes
FRESH_TIME=0.1#fresh time for one move
def build_q_table(n_states,actions):
    table=pd.DataFrame(
        np.zeros((n_states,len(actions))),
        columns=actions,
    )
    return table
def choose_action(state,q_table):
    #This is how to choose an action
    state_actions=q_table.iloc[state]
    if (np.random.uniform()>EPSILON) or (state_actions.all()==0):
        action_name=np.random.choice(ACTIONS)
    else:
        action_name=ACTIONS[state_actions.argmax()]
    return action_name
def get_env_feedback(state,action):
    #This is how agent will interact with the environment
    if action==ACTIONS[1]:
        if state==N_STATES-1:
            state_next='terminal'
            reward=1
        else:
            state_next=state+1
            reward=0
    else:
        reward=0
        if state==0:
            state_next=state
        else:
            state_next=state-1
    return state_next,reward
def update_env(state,episode,step_counter):
    #This is how the environment be updated
    env_list=['-']*(N_STATES-1)+['T']
    if state=='terminal':
        interaction='Episode %s:total_steps=%s'%(episode+1,step_counter)
        print('\r{}'.format(interaction),end='')
        time.sleep(2)
        print('\r',end='')
    else:
        env_list[state]='o'
        interaction=''.join(env_list)
        print('\r{}'.format(interaction),end='')
        time.sleep(FRESH_TIME)
    return
def main():
    q_table=build_q_table(N_STATES,ACTIONS)
    for episode in range(MAX_EPISODES):
        step_counter=0
        state=0
        is_terminated=False
        update_env(state,episode,step_counter)
        while not is_terminated:
            action=choose_action(state,q_table)
            state_next,reward=get_env_feedback(state,action)
            try:
                q_predict=q_table[action][state]
            except:
                print(action,state)
            if state_next!='terminal':
                q_target=reward+LAMBDA*q_table.iloc[state_next,:].max()
            else:
                q_target=reward
                is_terminated=True
            q_table[action][state]+=ALPHA*(q_target-q_predict)
            state=state_next
            step_counter+=1
            update_env(state,episode,step_counter)
    print(q_table)
main()