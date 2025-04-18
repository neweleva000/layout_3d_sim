from layout_utilities import *
import os
import random

max_width = 0.15
def num_topology1(num_gen):
    glob_name = "top1_ex"
    for s in range(num_gen):
        name = glob_name + "_" + str(s)
        rand_w = random.uniform(0, max_width)
        gen_full(gen_topology1, 0.5, 0.5, name, \
                rand_w)
        os.system("./py_call_3d_sim.sh " + name + ".gds")


def main():
    num_topology1(2)

if __name__ == '__main__':
    main()

