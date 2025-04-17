#TODO -- generate rectange using new architecture
import gdspy
import pudb

#goal specify filter kind and have it take recquisite parameters and gen layout
#class which has filter object and generates layout
class Layout_gen():

    def __init__ (self, filter_obj, name = "filter"):
        self.lib = gdspy.GdsLibrary()
        self.cell = self.lib.new_cell(name)
        self.filter_obj = filter_obj
    
    #parse filter object polygons, build polygons and add to cell
    def build_layout(self):
        #TODO generalize to multiple filter objects
        for f in self.filter_obj:
            for p in f.polygons:
                self.cell.add(self.build_polygon(p, f))
    
    #Given polygon specification build points and polygons
    def build_polygon(self, rect, obj):
        #TODO figure out generalization
        rect = gdspy.Rectangle(rect.start_point,\
                rect.end_point, obj.layer) 
        return rect

    def display_layout(self):
        gdspy.LayoutViewer(self.lib)

    def gen_file(self, file_name='filter_name'):
        self.lib.write_gds(file_name)

    #Rotate layout
    def rotate_layout(self):
        pass

class Rect_Spec():
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_point = (start_x, start_y)
        self.end_point = (end_x, end_y)

#TODO add rounding and chamfer

class Slot_filter():
    pass

#class which contains filter specifications
class Conductor_filter():

    #Position of end of last polygon chain
    curr_x = None
    curr_y = None

    #These are to prevent overlap on bends
    prev_delta_x = 0
    prev_delta_y = 0

    def __init__ (self, start_x=0, start_y=0, layer=0):
        self.curr_x = start_x
        self.curr_y = start_y
        self.layer = layer
        self.polygons = []

    #Add series transmisiosn line to polygons in specified direction
    #dir_offset is starting point offset from direction normal to direction
    def add_series(self, length, width, direction, dir_offset = 0):
        t_line = None
        new_tline = True
        if direction == "up":
            t_line = Rect_Spec(self.curr_x + dir_offset, self.curr_y + self.prev_delta_y,\
                    self.curr_x + width + dir_offset, self.curr_y + length + self.prev_delta_y)
            self.curr_y += length# + abs(self.prev_delta_y)
            self.curr_x += dir_offset

            self.prev_delta_x = width
            self.prev_delta_y = 0

        if direction == "down":
            self.add_series(-length, width, "up", dir_offset - width)
            new_tline = False

        if direction == "right":
            t_line= Rect_Spec(self.curr_x + self.prev_delta_x, self.curr_y + dir_offset,\
                    self.curr_x + length + self.prev_delta_x, self.curr_y - width + dir_offset)
            self.curr_x += length + self.prev_delta_x
            self.curr_y += dir_offset

            self.prev_delta_y = -width
            self.prev_delta_x = 0

        if direction == "left":
            self.add_series(-length, width, "right", dir_offset + width)
            new_tline = False
            self.curr_y += width
            #self.prev_delta_y *= -1

        if(new_tline):
            self.polygons.append(t_line)

    def add_series_void(self, length, direction):
        if direction == "up":
            self.curr_y += length

        if direction == "down":
            self.curr_y -= length

        if direction == "right":
            self.curr_x += length

        if direction == "left":
            self.curr_x -= length

    #Add shunt transmisiosn line to polygons in specified direction
    def add_shunt(self, length, width, direction, dir_offset=0):
        t_line = None
        new_tline = True
        if direction == "up":
            t_line = Rect_Spec(self.curr_x + dir_offset, self.curr_y,\
                    self.curr_x + width + dir_offset, self.curr_y + length, self.layer)
        if direction == "right":
            self.curr_x += self.prev_delta_x
            t_line= Rect_Spec(self.curr_x, self.curr_y + dir_offset,\
                    self.curr_x + length, self.curr_y -width + dir_offset, self.layer)
            self.curr_x -= self.prev_delta_x

        if direction == "left":
            self.curr_x -= self.prev_delta_x
            self.add_shunt(-length, width, "right", \
                    self.prev_delta_y)
            self.curr_x += self.prev_delta_x
            new_tline = False

        if new_tline:
            self.polygons.append(t_line)

    def add_chamfer_corner():
        pass

    def add_rounded_corner():
        pass

#TODO specify filter topologies
class high_pass_filter():
    pass

#Take specifications from command line
#This is useful for debugging and one-off generation
def command_line_parser():
    pass

#Long term this file will be called elsewhere which will handle the iterative generation
#Short term main will be used to debug specifics
#TODO implement more directions for each
#TODO Clean up whatever things pop up
#TODO clean up todos
#TODO for some reason the example.py puts all layers on every layer
def main():
    layer_gnd = 0
    layer_sub = 1
    layer_sig = 2
    signal = Conductor_filter(0,0, layer_sig)
    signal.add_series(0.2,1.1, "up")

    gnd = Conductor_filter(0, 0, layer_gnd)
    gnd.add_series(5, 5, "up")

    substrate = Conductor_filter(0, 0, layer_sub)
    substrate.add_series(5, 5, "up")

    rf_objects = [signal, gnd, substrate]
    generator = Layout_gen(rf_objects)  
    generator.build_layout()
    generator.gen_file('tline.gds')
    generator.display_layout()

if __name__ == '__main__':
    main()
