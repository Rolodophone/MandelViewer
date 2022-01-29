

TOP_LEFT_RE = -2
TOP_LEFT_IM = -1
NUM_ROWS = 400  # height
NUM_COLUMNS = 500  # width
BOTTOM_RIGHT_RE = 0.5
BOTTOM_RIGHT_IM = 1
INTERACTIVE = False
MAX_ITERATIONS = 1000
CONVERGENCE_TOLERANCE = 0.00001

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
prev_point = ComplexNumber(0, 0)
point = ComplexNumber(0, 0)


def check_point(re, im):
	global initial_point, prev_point, point

	initial_point.re = re
	initial_point.im = im
	point.re = re
	point.im = im

	for i in range(MAX_ITERATIONS):
		prev_point.set(point)
		point.squ()
		point.add(initial_point)

		# print(point)

		# return false if z diverges
		if not -4 < point.re < 4 or not -4 < point.im < 4:
			return False

		# return true if z converges
		if -CONVERGENCE_TOLERANCE < point.re - prev_point.re < CONVERGENCE_TOLERANCE and \
			-CONVERGENCE_TOLERANCE < point.im - prev_point.im < CONVERGENCE_TOLERANCE:
			return True

	# return true if z fails to diverge after many iterations
	return True


def output(row, output_file=None):
	if INTERACTIVE:
		print(row)
	else:
		assert output_file is not None, "output_file must not be None if INTERACTIVE is True."
		output_file.write(row + "\n")


def repr_pixel(inside_set):
	if INTERACTIVE:
		if inside_set:
			return "▉"
		else:
			return " "
	else:
		if inside_set:
			return "1 "
		else:
			return "0 "


def main():
	print("Calculation started.")

	if INTERACTIVE:
		output_file = None
	else:
		output_file = open(f"output_{NUM_COLUMNS}x{NUM_ROWS}.pbm", "w")
		output_file.write(f"P1\n{NUM_COLUMNS} {NUM_ROWS}\n")

	y = TOP_LEFT_IM
	row_i = 0

	while row_i < NUM_ROWS:

		row_str = ""
		x = TOP_LEFT_RE
		column_i = 0

		while column_i < NUM_COLUMNS:
			# print(f"{x}+{y}i")

			row_str += repr_pixel(check_point(x, y))

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
