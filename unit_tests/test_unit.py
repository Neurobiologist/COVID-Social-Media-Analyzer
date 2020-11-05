#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 20:12:35 2020

@author: ece-student
"""
# Import statements
import pytest
import unittest
from sentiment_analysis import evaluate
from sentiment_analysis import mkr
import tkinter as tk
from tkinter import ttk

class TestUnit:
    
    # Expected Behavior
    
    def test_evaluate_pos(self):
        assert evaluate(0.5) == '+'
    
    def test_evaluate_neutral(self):
        assert evaluate(0) == ' '
        
    def test_evaluate_edge(self):
        assert evaluate(0.2) == ' '
        
    def test_evaluate_neg(self):
        assert evaluate(-3) == 'v'
        
    def test_mkr_pos(self):
        assert mkr('+') == 'b'
        
    def test_mkr_neutral(self):
        assert mkr(' ') == 'k'
        
    def test_mkr_neg(self):
        assert mkr('v') == 'r'
        
class TestTKinter(unittest.TestCase):
    
    def setUp(self):
        self.app = ttk.Combobox()

    def tearDown(self):
        self.app.destroy()
        
    #def 

    #def test_button(self):
       # self.app.children['Analyze'].invoke()
    
    
        
    