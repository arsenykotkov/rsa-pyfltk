from fltk import *
from callbacks import *
from TSlider import *

# define common padding
padding = 5
height = 32
label_height = 24

window = Fl_Double_Window(640, 315, "RSA pyFLTK")
main_pack = Fl_Pack(padding, padding, window.w() - 2 * padding, window.h() - 2 * padding)
main_pack.spacing(padding)

label = Fl_Box(0, 0, 0, label_height, "Длина p, q в битах (не менее 16, степень двойки)")
label.align(FL_ALIGN_INSIDE | FL_ALIGN_LEFT)

# choose bit length
bit_length = None
bit_length_input = Fl_Value_Input(padding, padding, window.w() - 2 * padding, height)
bit_length_input.box(FL_DOWN_BOX)
bit_length_input.value(16)
bit_length_input.callback(bit_length_input_cb)

# choose t parameter
label = Fl_Box(0, 0, 0, label_height, "Количество тестов t")
label.align(FL_ALIGN_INSIDE | FL_ALIGN_LEFT)
chance_being_primary_box = Fl_Box(5, padding, window.w() - 2 * padding, height)
chance_being_primary_box.label('Двигайте ползунок t для расчёта вероятности получения простого числа (по умолч. 75%)')
chance_being_primary_box.box(FL_DOWN_BOX)
t_slider = TSlider(5, 64 + 5 * 2, window.w() - 5 * 2, 32)
t_slider.callback(t_slider_cb, chance_being_primary_box)

# choose open exponent
label = Fl_Box(0, 0, 0, label_height, "Открытая экспонента e")
label.align(FL_ALIGN_INSIDE | FL_ALIGN_LEFT)
open_exponent = None
possible_open_exponents = [3, 5, 17, 257, 65537]
open_exponent_group = Fl_Pack(int(window.w() / 4), 131, window.w(), 32)
open_exponent_group.align(FL_ALIGN_RIGHT)
open_exponent_buttons = []
for i in range(0, 5):
    # Fl_Pack automatically computes position of its children, so x, y and w can be set to zero, but
    # since it's horizontal Fl_Pack, height must be specified
    open_exponent_buttons.append(Fl_Radio_Round_Button(0, 0, 64, 0, str(possible_open_exponents[i])))
    open_exponent_buttons[i].callback(open_exponent_button_cb, open_exponent)
open_exponent_group.type(FL_HORIZONTAL)
open_exponent_group.end()

# name keys and choose where to store them
file_chooser = Fl_File_Chooser('./', '*', 2, '')
choose_save_path_button = Fl_Button(0, 0, 0, height, 'Выбрать путь')
choose_save_path_button.callback(choose_save_path_button_cb, file_chooser)

# generate key pair
generate_keys_button = Fl_Button(0, 0, 0, height, 'Сгенерировать ключи @returnarrow')
open_exponent = 3
key_params = [int(bit_length_input.value()), open_exponent, file_chooser.value()]
generate_keys_button.callback(generate_keys_button_cb, key_params)

main_pack.end()
window.end()
window.show()
Fl.run()
