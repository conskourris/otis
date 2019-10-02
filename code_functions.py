from PIL import Image


#create the initial array of the line of pixels to be analysed
def create_array(name, array):
	global height

	image = Image.open(name) # open the image 10k.jpg

	if image.mode in 'RGB':   # check if format is correct

		image = image.convert('RGB')  
		pixels = image.getdata()  # get all pixels of the image and place it in pixels in the form (r, g, b, a)
		width, height = image.size # get the dimentions of the image

		pixel_no = 1

		rows = []

		for pixel in pixels: # iterate through all pixels

			rows.append(pixel)

			if pixel_no % width == 0:
				array.append(rows)
				rows = []

			pixel_no += 1

	else:
		print('image mode incorrect')


# process the line of pixels
def process_array(name, array, processed, fianl_array, all_bands):
	
	pixel_colours = []
	newData = []
	row_num = 1
	start_limit = height/6
	end_limit = 2*height/7

	line_amount = 200

	for row in array:

		for pixel in row:

			if (height == 0):
				print('no height')
				exit()          

			elif (row_num % int(height/line_amount)) == 0:
				if (start_limit <= row_num <= end_limit):
					detect_color(pixel, pixel_colours)
					processed.append(pixel)

		if (row_num % int(height/line_amount)) == 0:
			create_final(pixel_colours, fianl_array)
			all_bands.append(fianl_array)

			pixel_colours = []
			fianl_array = []

		row_num += 1


# creates a text file to store rgb values of each pixel
# only useful for testing
def create_text_file(name):
	file = open(name, 'w') 
	file.truncate(0)

	iteration = 0

	for item in processed_pixels:
		text_item = str(item)
		file.write(text_item + '   ' + pixel_colours[iteration] + '\n')

		iteration += 1


# set the boundaries of different colours
def detect_color(c, array):

	# if (c[0] > 250) & (c[1] > 250) & (c[2] > 250) :
	# 	pixel_colours.append("white")
	if (160 <= c[0] <= 230) & (180 <= c[1] <= 250) & (230 <= c[2]):
		array.append("resistor")
	elif (c[0] <= 114) & (c[1] <= 119) & (c[2] <= 119):
		array.append("black")
	elif ((115 <= c[0] <= 189) & (120 <= c[1] <= 170) & (120 <= c[2] <= 180)) | ((130 <= c[0] <= 189) & (100 <= c[1] <= 130)):
		array.append("brown")
	elif (190 <= c[0] <= 230) & (80 <= c[1] <= 190) & (150 <= c[2] <= 210) | ((180 <= c[0] <= 210) & (70 <= c[1] <= 99) & (110 <= c[2] <= 150)):
		array.append("red")
	elif (110 <= c[0] <= 190) & (200 <= c[1] <= 240) & (150 <= c[2] <= 210):
		array.append("green")
	# elif (95 <= c[0] <= 145) & (70 <= c[1] <= 100) & (50 <= c[2] <= 90):
	# 	pixel_colours.append("orange")
	elif (220 <= c[0] <= 250) & (220 <= c[1] <= 250) & (140 <= c[2] <= 190):
		array.append("yellow")
	else:
		array.append("undetected")



# finite state machine to analyse new pixels
def create_final(datas, fianl_array):

	last = None
	state = 'NO_RESISTOR'
	resistor = False
	orientation = None
	possible_strip = False
	new_strip = False
	
	first_gap = 0
	last_gap = 0
	first_band = 0
	last_band = 0
	
	for data in datas:

		if (len(fianl_array) == 5) & (data == 'resistor'):  # break once all 5 strips are identified
			if first_band > last_band:
				fianl_array.reverse()
			return True

		if state == 'NO_RESISTOR' : # change state once resistor is identified
			if data == 'resistor':
				state == 'RESISTOR_FOUND'
				resistor = True
				new_strip = True


		if resistor is True:

			if data != 'undetected' :  # make sure pixel is detected

				if data == last : # change of state
					state = 'SAME'

				if (data != last): # change of state
					state = 'NEW'


				if state == 'SAME' :

					if data == 'resistor':

						new_strip = True

						if len(fianl_array) == 1: # measure the gap between the first 2 bands
							first_gap += 1

						if len(fianl_array) == 4: # measure the gap between the last 2 bands
							last_gap += 1

					if (len(fianl_array) == 1) & (data != 'resistor'):
						first_band += 1

					if (len(fianl_array) == 5) & (data != 'resistor'):
						last_band += 1

					if (possible_strip is True) & (new_strip is True) & (data != 'resistor') & (len(fianl_array) < 5): # if a seccond occurance of the colour is met, add it to the array
						fianl_array.append(data)
						possible_strip = False
						new_strip = False

				

				if state == 'NEW': # wait for a second occurance of the same colour by setting possible_strip True
					possible_strip = True
					#fianl_array.append(data)

				last = data



def finalise_array(all_bands, complete_bands):
	frequency = [] 

	for band in all_bands:
		if len(band) == 5:
			if band not in complete_bands:
				frequency.append(1)
				complete_bands.append(band)
			else:
				frequency[(complete_bands.index(band))] += 1

	if frequency == []:
		return []
	else:
		array = complete_bands[frequency.index(max(frequency))]
		return array


def get_value(five_bands):
	i = 0
	value = 0
	for band in five_bands:
		if i < 3:
			if band == "black":
				value = int(str(value) + str(0))
			elif band == "brown":
				value = int(str(value) + str(1))
			elif band == "red":
				value = int(str(value) + str(2))
			elif band == "orange":
				value = int(str(value) + str(3))
			elif band == "yellow":
				value = int(str(value) + str(4))
			elif band == "green":
				value = int(str(value) + str(5))
			elif band == "blue":
				value = int(str(value) + str(6))
			elif band == "violet":
				value = int(str(value) + str(7))
			elif band == "grey":
				value = int(str(value) + str(8))
			elif band == "white":
				value = int(str(value) + str(9))

		if i == 3:
			if band == "black":
				pass
			elif band == "brown":
				value = value * 10
			elif band == "red":
				value = value * 100
			elif band == "orange":
				value = value * 1000
			elif band == "yellow":
				value = value * 10000
			elif band == "green":
				value = value * 100000
			elif band == "blue":
				value = value * 1000000
			elif band == "violet":
				value = value * 10000000
			elif band == "grey":
				value = value * 100000000
			elif band == "white":
				value = value * 1000000000


		i += 1


	return value

def


















