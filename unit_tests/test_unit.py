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
    
    def test_evaluate(self):
        assert evaluate(0.5) == '+'