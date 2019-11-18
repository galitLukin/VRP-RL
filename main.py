import argparse
import os
import numpy as np
from tqdm import tqdm
import tensorflow as tf
import time

from configs import ParseParams

from evaluation.eval_VRP import eval_google_or,eval_Clarke_Wright
from evaluation.benchmark import benchmark
from model.attention_agent import RLAgent

def load_task_specific_components(task):
    '''
    This function load task-specific libraries
    '''
    if task == 'vrp':
        from VRP.vrp_utils import DataGenerator,Env,reward_func
        from VRP.vrp_attention import AttentionVRPActor,AttentionVRPCritic

        AttentionActor = AttentionVRPActor
        AttentionCritic = AttentionVRPCritic

    else:
        raise Exception('Task is not implemented')

    return DataGenerator, Env, reward_func, AttentionActor, AttentionCritic

def main(args, prt):
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)

    # load task specific classes
    DataGenerator, Env, reward_func, AttentionActor, AttentionCritic = \
        load_task_specific_components(args['task_name'])

    dataGen = DataGenerator(args)
    dataGen.reset()
    env = Env(args)
    # create an RL agent
    agent = RLAgent(args,
                    prt,
                    env,
                    dataGen,
                    reward_func,
                    AttentionActor,
                    AttentionCritic,
                    is_train=args['is_train'])
    agent.Initialize(sess)

    # train or evaluate
    prev_actor_loss, prev_critic_loss = float('Inf'), float('Inf')
    curr_actor_loss, curr_critic_loss = 0, 0
    actor_eps, critic_eps = 1e-2, 1e-2
    start_time = time.time()
    if args['is_train']:
        prt.print_out('Training started ...')
        train_time_beg = time.time()
        for step in range(args['n_train']):
            summary = agent.run_train_step()
            _, _ , actor_loss_val, critic_loss_val, actor_gra_and_var_val, critic_gra_and_var_val,\
                R_val, v_val, logprobs_val,probs_val, actions_val, idxs_val= summary

            curr_actor_loss = np.mean(actor_loss_val)
            curr_critic_loss = np.mean(critic_loss_val)
            if abs(prev_actor_loss - curr_actor_loss) < actor_eps \
                and abs(prev_critic_loss - curr_critic_loss) < critic_eps:
                prt.print_out('Converged at step {}'\
                      .format(step))
                train_time_end = time.time()-train_time_beg
                prt.print_out('Train Step: {} -- Time: {} -- Train reward: {} -- Value: {}'\
                      .format(step,time.strftime("%H:%M:%S", time.gmtime(\
                        train_time_end)),np.mean(R_val),np.mean(v_val)))
                prt.print_out('    actor loss: {} -- critic loss: {}'\
                      .format(curr_actor_loss,curr_critic_loss))
                break

            if step%args['save_interval'] == 0:
                agent.saver.save(sess,args['model_dir']+'/model.ckpt', global_step=step)

            if step%args['log_interval'] == 0:
                train_time_end = time.time()-train_time_beg
                prt.print_out('Train Step: {} -- Time: {} -- Train reward: {} -- Value: {}'\
                      .format(step,time.strftime("%H:%M:%S", time.gmtime(\
                        train_time_end)),np.mean(R_val),np.mean(v_val)))
                prt.print_out('    actor loss: {} -- critic loss: {}'\
                      .format(curr_actor_loss, curr_critic_loss))

                train_time_beg = time.time()
            if step%args['test_interval'] == 0:
                agent.inference(args['infer_type'])
            prev_actor_loss = curr_actor_loss
            prev_critic_loss = curr_critic_loss

        # Save the model at the end of the training
        agent.saver.save(sess,args['model_dir']+'/model.ckpt', global_step="final")

    else: # inference
        prt.print_out('Evaluation started ...')
        agent.inference(args['infer_type'])

        # google_or evals
        google_eval = eval_google_or.EvalGoogleOR(args,env)
        google_eval.perform_routing()

        # Clarke_Wright_savings eval
        CW_eval = eval_Clarke_Wright.EvalClarkeWright(args,env)
        CW_eval.perform_routing()

        benchmark_object = benchmark.Benchmark(args,env,prt)
        benchmark_object.perform_benchmark(list_eval=['beam_search','greedy','or_tools','Clarke_Wright'])


    prt.print_out('Total time is {}'.format(time.strftime("%H:%M:%S", time.gmtime(time.time()-start_time))))


if __name__ == "__main__":
    args, prt = ParseParams()
    args['is_train'] = False
    args['test_size'] = 1000
    args['load_path'] = "/Users/jpoullet/Documents/MIT/Thesis/ML6867_project/VRP-RL/logs/vrp10-2019-11-02_11-55-35/model/"

    # Random
    random_seed = args['random_seed']
    if random_seed is not None and random_seed > 0:
        prt.print_out("# Set random seed to %d" % random_seed)
        np.random.seed(random_seed)
        tf.set_random_seed(random_seed)
    tf.reset_default_graph()

    main(args, prt)
