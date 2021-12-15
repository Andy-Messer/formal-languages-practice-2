"""! @brief Python Library - Solve for homework: 'Formal Languages, Practice 2, Earley test_algo_module' """

##
# @mainpage Homework: 'Formal Languages, Practice 2, Earley algo'
#
# @section description_main Description
# Task: Необходимо реализовать алгоритм в виде класса Algo, в котором есть следующие методы:
# • fit(G: Grammar) ! Algo - препроцессинг
# • predict(word: String) ! Boolean - проверка принадлежности слова языку.
# Дополнительно необходимо реализовать тестирование построенной предобработки.
# Алгоритмы для реализации
# 1. Алгоритм Эрли
# 2. LR(1)-алгоритм
# Поскольку в алгоритме Эрли нет предобработки, то необходимо реализовать функции:
# • Scan(conf: Configuration, letter: char) ! Set• Predict(...)
# • Complete(...) - продумайте интерфейс таким образом, чтобы результат можно было про-
# тестировать.
#
# Copyright (c)2021 Andrey Krotov. All rights reserved.
__author__ = "Krotov Andrey <krotov.ai@phystech.edu>"
__version__ = "0.1"
__date__ = "13 December 2021"

from early_parser.algo import *
from early_parser.grammar import *
