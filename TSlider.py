from fltk import Fl_Slider, FL_HORIZONTAL, fl_rgb_color


class TSlider(Fl_Slider):
    def __init__(self, xpos, ypos, width, height, label=None):
        Fl_Slider.__init__(self, xpos, ypos, width, height, label)
        self.type(FL_HORIZONTAL)
        self.precision(0)  # integer values
        self.value(1)  # default value
        self.bounds(1, 27)  # at 27 it rounds up to 100.0%
