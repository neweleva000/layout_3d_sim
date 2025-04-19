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

def num_topology2(num_gen):
    glob_name = "top2_ex"
    for s in range(num_gen):
        name = glob_name + "_" + str(s)
        rand_num_stubs = random.randint(1,8)
        rand_w = random.uniform(0, max_width)
        stub_dims = []
        for stub in range(rand_num_stubs):
            stub_dims.append(random.uniform(0, 0.05))
            stub_dims.append(random.uniform(0, 0.15))

        gen_full(gen_topology2, 0.5, 0.5, name, \
                rand_num_stubs, rand_w, stub_dims)
        os.system("./py_call_3d_sim.sh " + name + ".gds")

def num_topology3(num_gen):
    glob_name = "top3_ex"
    for s in range(num_gen):
        name = glob_name + "_" + str(s)

        
        rand_w = random.uniform(0, max_width)
        rand_spacing_l = random.uniform(0.01, 0.1)
        rand_overlap_l = random.uniform(0.02, 0.15)
        max_sp_w = (0.5 - rand_w)/2 - rand_w - 0.05
        rand_spacing_w = random.uniform(0.03, max_sp_w)
        rand_split_at_l = random.uniform(0.1, 0.28)

        gen_full(gen_topology3, 0.5, 0.5, name, rand_w,\
                rand_spacing_l, rand_overlap_l,\
                rand_spacing_w, rand_split_at_l)
        os.system("./py_call_3d_sim.sh " + name + ".gds")




def main():
    #num_topology1(2)
    #num_topology2(2)
    num_topology3(2)

if __name__ == '__main__':
    main()

