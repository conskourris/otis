import code_functions as otis



file = 'example.jpg'


while True:
	pixel_colours = []
	all_data = []
	processed_pixels = []
	fianl_array = []
	all_bands = []
	complete_bands = []
	deduction = []
	resistor_found = False
	
	try:
		otis.vibrate()

		while resistor_found is False:
			sleep(5)
			otis.take_picture(file)
			otis.create_array(file, all_data)
			resistor_found = otis.check_res()

		otis.stop_vibrate()


		pixel_colours = []
		all_data = []
		processed_pixels = []
		fianl_array = []
		all_bands = []
		complete_bands = []
		deduction = []

		otis.take_picture(file)
		otis.create_array(file, all_data)
		otis.process_array(file, all_data, processed_pixels, fianl_array, all_bands)
		deduction = otis.finalise_array(all_bands, complete_bands)

		print(deduction)

		print(otis.get_value(deduction))

		otis.sort(deduction)
		otis.open_flap()

		print('Sorted ', value, ' Ohm resistor')

	except:
		break

print("OTIS")