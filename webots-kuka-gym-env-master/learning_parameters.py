#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np

# Gazebo simulation parameters
time_step = 0.003
update_rate = 2000
solver_iter = 100

# DMP parameters
dmp_num_theta = 10  # number of parameters
dmp_rtime = 20  # number of points to be interpolated
dmp_stime = 100  # number of simulation's timesteps 100 default
dmp_dt = 0.25  # integration time over dmp_rtime
dmp_sigma = 0.05  # standard deviation of each parameters 0.05

# BBO parameters
bbo_lmb = 0.005# softmax temperature
bbo_epochs = 5
bbo_episodes = 20
bbo_num_dmps = 9
bbo_sigma_max = 0.2
bbo_sigma_arm_scale = 0.001
bbo_sigma_joint_scales =  [bbo_sigma_arm_scale,
                           bbo_sigma_arm_scale,
                           bbo_sigma_arm_scale,
                           bbo_sigma_arm_scale,
                           1,1,1,1,1]
bbo_sigma = bbo_sigma_max * np.hstack(
    [
        np.ones(dmp_num_theta + 2) * x
        for x in bbo_sigma_joint_scales
    ]
)  # constant sample variance
bbo_sigma_decay_amp = 0.0  # variable sample variance
bbo_sigma_decay_start = 0
bbo_sigma_decay_period = 0.01
init_gap = 10
continue_learning = True   #Changed

# YOUBOT learning_parameters
dist_dev_alpha = 0.028
dist_dev_beta = 0.1
dist_dev_gamma = 0.012
alpha = 1e4# floor distance
beta = 1        # finger_distance per default a 1
gamma = 1e8# touch * finger_distance
max_rew = 5e5
sigma_moving_average = True
sigma_moving_average_h = 0.2

object_to_grasp = 'otre'
# object

from limits import *


class SimulationManager:
    def __init__(self, env):
        """
        :env: a openai_ros env
        """
        self.env = env
        self.init_gap = init_gap

    def init_trj(self, ro):
        return np.hstack((np.zeros([ro.shape[0], self.init_gap]), ro))

    def __call__(self, rollouts):
        """
        :rollouts: nparray [episode_num, dmp_num, timesteps]
        """

        n_episodes, n_joints, timesteps = rollouts.shape
        rews = np.zeros([n_episodes, timesteps + self.init_gap])

        for episode in range(n_episodes):

            print("episode %d" % episode)

            # simulate with the current joint trajectory to read rewards
            rollout = np.squeeze(rollouts[episode, :, :])
            rollout = self.init_trj(rollout)
            rollout = filter_limits(scale_to_joints(rollout))

            self.env.reset()
            for t in range(timesteps + self.init_gap):
                action = rollout[:, t]
                obs, reward, done, info = self.env.step(action)
                rews[episode, t] = reward

        return rews[:, self.init_gap :]


class ExploreSimulationManager:
    def __init__(self, env):
        """
        :env: a openai_ros env
        """
        self.env = env
        self.init_gap = init_gap

    def init_trj(self, ro):
        return np.hstack((np.zeros([ro.shape[0], self.init_gap]), ro))

    def __call__(self, rollouts):
        """
        :rollouts: nparray [episode_num, dmp_num, timesteps]
        """

        n_episodes, n_joints, timesteps = rollouts.shape
        rews = np.zeros([n_episodes, timesteps + self.init_gap])

        for episode in range(n_episodes):

            print("episode %d" % episode)

            # simulate with the current joint trajectory to read rewards
            rollout = np.squeeze(rollouts[episode, :, :])
            rollout = self.init_trj(rollout)
            rollout = filter_limits(scale_to_joints(rollout))

            self.env.explore_reset()
            for t in range(timesteps + self.init_gap):
                action = rollout[:, t]
                obs, reward, done, info = self.env.step(action)
                rews[episode, t] = reward

        return rews[:, self.init_gap :]


class RunManager(SimulationManager):
    def __call__(self, rollout):
        """
        :rollouts: nparray [dmp_num, timesteps]
        """

        n_joints, timesteps = rollout.shape

        # simulate with the current joint trajectory to read rewards
        rollout = self.init_trj(rollout)
        rollout = filter_limits(scale_to_joints(rollout))

        for t in range(timesteps + self.init_gap):
            action = rollout[:, t]
            obs, reward, done, info = self.env.step(action)


class TestSimulationManager(SimulationManager):
    def __call__(self, rollouts):
        """
        :rollouts: nparray [episode_num, dmp_num, timesteps]
        """

        n_episodes, n_joints, timesteps = rollouts.shape
        rews = np.zeros([n_episodes, timesteps + self.init_gap])

        for episode in range(n_episodes):

            # simulate with the current joint trajectory to read rewards
            rollout = np.squeeze(rollouts[episode, :, :])
            rollout = self.init_trj(rollout)
            rollout = filter_limits(scale_to_joints(rollout))

            reads = np.zeros_like(rollout)

            self.env.reset()
            for t in range(timesteps + self.init_gap):
                action = rollout[:, t]
                obs, reward, done, info = self.env.step(action)
                reads[:, t] = obs["JOINT_POSITIONS"]
                rews[episode, t] = reward

        return rews[:, self.init_gap :], reads
