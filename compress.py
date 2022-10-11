#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 17:39:10 2022

@author: felixdubicki-piper
"""

import scipy.signal as sg
from numpy import pi
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from signal_data import athena

import tkinter as tk
from tkinter import filedialog
root = tk.Tk()
root.withdraw()


class signal:
    def __init__(self, ascan=None, bscan=None, dataprompt=True):
        if (ascan or bscan) or (not (ascan or bscan) and dataprompt):
            self.load_data(ascan, bscan)

        pass

    def load_data(self, ascan=None, bscan=None):
        if not ascan:
            file_a = filedialog.askopenfilename()
        else:
            file_a = ascan

        if not bscan:
            file_b = filedialog.askopenfilename()
        else:
            file_b = ascan

        self.t_a, self.data_a = athena.ReadAScan(file_a)
        self.t_b, self.x, self.data_b = athena.ReadBScan(file_b)

        self.match()

    def match(self):
        out = np.zeros(self.data_b.shape)
        for i in range(self.data_b.shape[1]):
            out[:, i] = sg.correlate(self.data_b[:, i],
                                     self.data_a,
                                     mode='same')/(0.1*len(self.data_a))
        self.results = out

    def match2d(self):
        out = sg.correlate(self.data_b, self.data_a,
                           mode='same')/(0.1*len(self.data_a))
        self.results = out

    def plot1d(self, data, t=None, i0=None, iend=None):
        fig = plt.figure()
        plt.plot(t[i0:iend], data[i0:iend])
        return fig

    def plot2d(self, data, t=None, x=None,  MIN=None, MAX=None):
        fig = plt.figure()
        plt.pcolormesh(data, vmin=MIN, vmax=MAX)
        return fig

    def save_data(self, data=None, filename=None):
        if not data:
            data = self.results
        filepath = filedialog.asksaveasfilename(initialdir='signal_data/',
                                                defaultextension='.csv')
        np.savetxt(filepath, data, delimiter=",")

    def load_results(self, filepath=None):
        if not filepath:
            filepath = filedialog.askopenfilename()
        results = np.genfromtxt(filepath)
