import math

LOCATIONS = {
	"default": (-2, -1.25, 2.5, 2.5),
	"tendril_bulb": (0.3027640, -0.0234289, 0.0000418, 0.0000418),
	"minibrot": (0.305458, -0.023282, 0.00050, 0.00045),
	"spirals": (0.305959, -0.022734, 0.000012, 0.000012)
}
LOCATION_NAME = "spirals"

LOCATION = LOCATIONS[LOCATION_NAME]
TOP_LEFT_RE = LOCATION[0]
TOP_LEFT_IM = LOCATION[1]
BOTTOM_RIGHT_RE = LOCATION[0] + LOCATION[2]
BOTTOM_RIGHT_IM = LOCATION[1] + LOCATION[3]
NUM_ROWS = 2000  # output height
NUM_COLUMNS = round(NUM_ROWS * (LOCATION[2] / LOCATION[3]))  # output width
NUM_COLOURS = 255
INTERACTIVE = False
MAX_ITERATIONS = 1000

SQUARE_WIDTH = (BOTTOM_RIGHT_RE - TOP_LEFT_RE) / (NUM_COLUMNS - 1)
SQUARE_HEIGHT = (BOTTOM_RIGHT_IM - TOP_LEFT_IM) / (NUM_ROWS - 1)


class ComplexNumber:
	def __init__(self, re, im):
		self.re = re
		self.im = im

	def __repr__(self):
		return f"{self.re}+{self.im}i"

	def set(self, complex_number):
		self.re = complex_number.re
		self.im = complex_number.im

	def add(self, other):
		self.re += other.re
		self.im += other.im

	def mul(self, other):
		new_re = self.re * other.re - self.im * other.im
		new_im = self.re * other.im + self.im * other.re
		self.re = new_re
		self.im = new_im

	def squ(self):
		self.mul(self)


initial_point = ComplexNumber(0, 0)  # reuse these objects so we aren't creating new objects each time
point = ComplexNumber(0, 0)


def check_point(re, im):
	global initial_point, point

	initial_point.re = re
	initial_point.im = im
	point.re = re
	point.im = im

	for i in range(MAX_ITERATIONS):
		point.squ()
		point.add(initial_point)

		# print(point)

		# return false if z diverges
		if not -2 < point.re < 2 or not -2 < point.im < 2:
			return i

	# return true if z fails to diverge after many iterations
	return -1


def output(row, output_file=None):
	if INTERACTIVE:
		print(row)
	else:
		assert output_file is not None, "output_file must not be None if INTERACTIVE is True."
		output_file.write(row + "\n")


def repr_pixel(iterations):
	if INTERACTIVE:
		if iterations == -1:
			return "▉"
		else:
			return " "
	else:
		if iterations == -1:
			return "0 0 0 "
		else:
			colour_value = NUM_COLOURS - round((NUM_COLOURS / math.sqrt(MAX_ITERATIONS)) * math.sqrt(iterations))
			return f"{NUM_COLOURS} {colour_value} {colour_value} "



def main():
	print("Calculation started.")

	if INTERACTIVE:
		output_file = None
	else:
		output_file = open(f"output_{LOCATION_NAME}_{NUM_COLUMNS}x{NUM_ROWS}.ppm", "w")
		output_file.write(f"P3\n{NUM_COLUMNS} {NUM_ROWS}\n{NUM_COLOURS}\n")

	y = TOP_LEFT_IM
	row_i = 0

	while row_i < NUM_ROWS:

		row_str = ""
		x = TOP_LEFT_RE
		column_i = 0

		while column_i < NUM_COLUMNS:
			# print(f"{x}+{y}i")

			iterations = check_point(x, y)
			row_str += repr_pixel(iterations)

			x += SQUARE_WIDTH
			column_i += 1

		if not INTERACTIVE and row_i % 100 == 99:
			print(f"Calculated row {row_i + 1} of {NUM_ROWS}.")

		output(row_str, output_file)

		y += SQUARE_HEIGHT
		row_i += 1

	if not INTERACTIVE:
		output_file.close()

	print("Calculation finished.")


if __name__ == "__main__":
	main()
