from fltk import *
from rsa import *


def generate_keys_button_cb(button, key_params):
    gen_keys(key_params[0], key_params[1], key_params[2])

def is_power_of_two(x: int):
    return 0 == (x & (x - 1))


def bit_length_input_cb(input):
    global bit_length_is_valid
    value = input.value()
    if 16 > value or not is_power_of_two(int(value)):
        input.textcolor(FL_RED)
    elif FL_RED == input.textcolor():
        input.textcolor(FL_BLACK)
    input.redraw()


def t_slider_cb(slider, box):
    # if t.value() > 511 then "OverflowError: (34, 'Result too large')"
    if slider.value() > 511:
        slider.value(511)
    elif slider.value() < 0:
        slider.value(1)

    # from formula
    chance = 1 - 1 / 4 ** slider.value()

    if chance == 1.0:
        box.label('t={}, (почти) {:.64g}%'.format(int(slider.value()), chance * 100))
    else:
        box.label('t={}, {:.64g}%'.format(int(slider.value()), chance * 100))

    # change text color based on chance of being primary
    box.color(fl_rgb_color(255 - int(slider.value() * 9), int(slider.value() * 9), 0))
    box.redraw()


def open_exponent_button_cb(widget, open_exponent):
    open_exponent = int(widget.label())


def choose_save_path_button_cb(widget, file_chooser):
    global save_path_is_valid
    file_chooser.show()
    while file_chooser.shown():
        Fl.wait()
    if file_chooser.value() is None:
        widget.label('Выбрать путь')
    else:
        widget.label(str(file_chooser.value()))
