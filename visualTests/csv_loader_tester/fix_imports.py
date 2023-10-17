import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
first_parent = os.path.dirname(current_dir)
second_parent = os.path.dirname(first_parent)
sys.path.append(first_parent)
sys.path.append(second_parent)