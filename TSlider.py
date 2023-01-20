from fltk import Fl_Slider


class TSlider(Fl_Slider):
    def __init__(self, xpos, ypos, width, height, label=None):
        Fl_Slider.__init__(self, xpos, ypos, width, height, label)
       