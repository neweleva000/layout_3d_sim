from gen_layout import *


def gen_ex1():
    wavelength = 0.5
    length = wavelength/4
    er = 4
    width = 0.005
    h = 1

    portx = width
    porty = length/5

    layer_gnd = 0
    layer_sub = 1
    layer_sig = 2
    layer_p1 =  3
    layer_p2 = 4

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
    gen_ex1()

if __name__ == '__main__':
    main()
