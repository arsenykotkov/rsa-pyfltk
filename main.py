from fltk import *


def slider_t_cb(sl, pp):
    # if t.value() > 511 then "OverflowError: (34, 'Result too large')"
    if sl.value() > 511:
        sl.value(511)
    elif sl.value() < 0:
        sl.value(1)

    probability = 1 - 1 / 4 ** sl.value()

    if probability == 1.0:
        pp.label('(почти) {:.64g}%'.format(probability * 100))
    else:
        pp.label('{:.64g}%'.format(probability * 100))

    # change text color based on probability percent
    pp.color(fl_rgb_color(255 - int(sl.value() * 9), int(sl.value() * 9), 0))
    pp.redraw()


window = Fl_Double_Window(640, 480, "RSA pyFLTK")
primarity_probability = Fl_Box(5, 5, window.w() - 5 * 2, 64,
                               'Двигайте ползунок t для расчёта вероятности получения простого числа (по умолч. 75%)')
primarity_probability.box(FL_DOWN_BOX)
slider_t = Fl_Value_Slider(5, 64 + 5 * 2, window.w() - 5 * 2, 32)
slider_t.type(FL_HORIZONTAL)
slider_t.precision(0)
slider_t.value(1)
slider_t.do_callback()
# at 27 it rounds up to 100.0%
slider_t.bounds(1, 27)
slider_t.callback(slider_t_cb, primarity_probability)

window.end()
window.show()
Fl.run()
