#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 20:12:35 2020

@author: ece-student
"""
# Import statements
import pytest
from sentiment_analysis import evaluate

class TestUnit:
    
    def test_evaluate_pos(self):
        assert evaluate(0.5) == '+'
    
    def test_evaluate_neutral(self):
        assert evaluate(0) == ' '
        
    def test_evaluate_edge(self):
        assert evaluate(0.2) == ' '
        
    def test_evaluate_neg(self):
        assert evaluate(-3) == 'v'