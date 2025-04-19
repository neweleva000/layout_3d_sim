from gen_layout import *

layer_gnd = 0
layer_sub = 1
layer_sig = 2
layer_p1 =  3
layer_p2 = 4

class Stackup:
    def __init__(self, gnd, substrate, p1, p2):
        self.gnd = gnd
        self.substrate = substrate
        self.p1 = p1
        self.p2 = p2

def gen_stackup_adjusted(l, w):
    gnd = Conductor_filter(-w, -l, layer_gnd)
    gnd.add_series(3*l, 3*w, "up")

    substrate = Conductor_filter(-w, -l, layer_sub)
    substrate.add_series(3*l, 3*w, "up")

    p1 = Conductor_filter(0,-0.01, layer_p1)
    p1.add_series(0.01, w, "up")

    p2 = Conductor_filter(0,l, layer_p2)
    p2.add_series(0.01,w, "up")

    s = Stackup(gnd, substrate, p1, p2)
    return s

def gen_stackup(l, w):
    gnd = Conductor_filter(0, 0, layer_gnd)
    gnd.add_series(l, w, "up")

    substrate = Conductor_filter(0, 0, layer_sub)
    substrate.add_series(l, w, "up")

    p1 = Conductor_filter(0,-0.01, layer_p1)
    p1.add_series(0.01, w, "up")

    p2 = Conductor_filter(0,l, layer_p2)
    p2.add_series(0.01,w, "up")

    s = Stackup(gnd, substrate, p1, p2)
    return s

#Microstrip with varying width
def gen_topology1(stackup_w, stackup_l, *args):
    w = float(args[0][0])
    start_x = (stackup_w - w)/2
    start_y = 0

    signal = Conductor_filter(start_x, start_y, layer_sig)
    signal.add_series(stackup_l, w, "up")
    return signal

def gen_topology2(stackup_w, stackup_l, *args):

    num_stubs = int(args[0][0])
    main_w = float(args[0][1])

    start_x = (stackup_w - main_w)/2
    start_y = 0

    stub_w = []
    stub_l = []
    stub_dims = list(args[0][2])
    for stub in range(num_stubs):
        stub_w.append(stub_dims[2*stub+0])
        stub_l.append(stub_dims[2*stub+1])

    stub_spacing = stackup_l / num_stubs


    signal = Conductor_filter(start_x, start_y, layer_sig)
    for s in range(num_stubs):
        signal.add_series(stub_spacing, main_w, "up")
        signal.add_shunt(stub_l[s], stub_w[s], "right")
    return signal
        

def gen_topology3(stackup_w, stackup_l, *args):
    w = args[0][0]
    spacing_l = float(args[0][1])
    overlap_l = float(args[0][2])
    spacing_w = float(args[0][3])
    split_at_l = float(args[0][4])

    l_after_split = stackup_l - spacing_l - split_at_l
    start_x = (stackup_w - w)/2
    start_y = 0

    signal = Conductor_filter(start_x, start_y, layer_sig)
    signal.add_series(split_at_l, w, "up")
    signal.add_series(spacing_w, w, "right")
    signal.add_series(overlap_l+w, w, "up")
    signal.add_series_void(-overlap_l + spacing_l - w, "up")
    signal.add_series_void(-spacing_w -w, "right")
    signal.add_series(l_after_split, w, "up")

    return signal



def gen_full(topology_func, stackup_w, stackup_l, name,\
        *args):
    s = gen_stackup(stackup_w, stackup_l)
    t = topology_func(stackup_w, stackup_l, args)

    rf_objects = [s.gnd, s.substrate, s.p1, s.p2, t]

    generator = Layout_gen(rf_objects, name)  
    generator.build_layout()
    generator.gen_file(name + ".gds")
    generator.display_layout()




def gen_ex1():
    wavelength = 0.5
    length = wavelength/4
    er = 4
    width = 0.005
    h = 1

    portx = width
    porty = length/5


    signal = Conductor_filter(-0.05,0.0, layer_sig)
    #quarterwave transformer at 300M
    signal.add_series(5, 0.1, "up")

    gnd = Conductor_filter(-1, -1, layer_gnd)
    gnd.add_series(7, 2, "up")

    substrate = Conductor_filter(-1, -1, layer_sub)
    substrate.add_series(7, 2, "up")

    p1 = Conductor_filter(-0.05,-0.1, layer_p1)
    p1.add_series(0.1,0.1, "up")

    p2 = Conductor_filter(-0.05,5, layer_p2)
    p2.add_series(0.1,0.1, "up")

    rf_objects = [signal, gnd, substrate, p1, p2]
    generator = Layout_gen(rf_objects, "example")  
    generator.build_layout()
    generator.gen_file('example.gds')
    generator.display_layout()





def main():
    top1_width = 0.01
    #gen_full(gen_topology1, 0.5, 0.5, "top1_ex", \
    #        top1_width)
    #sp_w = (0.5 - wid)/2 - wid - sp_w
    gen_full(gen_topology3, 0.5, 0.5, "top3_ex", 0.1, 0.05, 0.1, 0.1 , 0.1)
    #gen_ex1()

if __name__ == '__main__':
    main()
