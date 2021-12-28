"""! @brief Python Library - Solve for homework: 'Formal Languages, Practice 2, Earley test_algo_module' """

##
# @mainpage Homework: 'Formal Languages, Practice 2, Earley algo'
#
# @section description_main Description
# Task: It is necessary to implement the algorithm in the form of an Algo class, which has the following methods:
# * fit(G: Grammar) ! Algo - preprocessing
# • predict(word: String) ! Boolean - checking whether a word belongs to the language.
# Additionally, it is necessary to implement testing of the built preprocessing.
# Algorithms for implementation
# 1. Earley's algorithm
# 2. LR(1)-algorithm
# Since there is no preprocessing in Earley's algorithm, it is necessary to implement the functions:
# • Scan(conf: Configuration, letter: char) ! Set• Predict(...)
# • Complete(...) - think over the interface in such a way that the result can be read-
# test.
#
# # Copyright (c)2021 Andrey Krotov. All rights reserved.
__author__ = "Krotov Andrey <krotov.ai@phystech.edu>"
__version__ = "1.0"
__date__ = "17 December 2021"

# The algorithm module has an implementation of the Earley algorithm
from early_parser.algo import *
# The grammar module contains the implementation of the Grammar module
from early_parser.grammar import *
# from early_parser.logs import *
# A module that has a minimal set of code for testing all the code in the grammar and Earley algorithm modules
from early_parser.test_module import *
