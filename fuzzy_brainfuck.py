import tensorflow as tf

ADD = 0
SUB = 1
RGT = 2
LFT= 3
OUT = 4
INP = 5
LOP = 6
LCL = 7
# An instruction in Fuzzy Brainfuck is a probability distribution over Brainfuck's instruction set.
# A byte is replace by a probability distribution over all the 256 possible values. This change applies to input, output, and memory.
# Restricting the space of probabilities to {0, 1} turns Fuzzy Brainfuck into normal Brainfuck.
# for input, output, memory and program, only the leftmost part is active.
# Hence, program is shifted every iterations and > < shifts the entire memory.
class Fuzzy_Brainfuck:
	def __init__(self, program_size = 100, output_size = 50, input_size = 50, memory_size = 200, max_loop_count = 20, raw_program = None, inp = None):
		self.program_size = program_size
		self.input_size = input_size
		self.output_size = output_size
		self.memory_size = memory_size
		if raw_program == None:
			self.raw_program = tf.uniform(shape = (program_size, 8), minval = -2.0, maxval = 2.0)
		else:
			self.raw_program = raw_program
		self.initialize(inp)

	def initialize(self, inp):
		# PROGRAM
		self.program = tf.nn.softmax(self.raw_program)
		self.halt_point = tf.Variable([0.0]*(program_size-1) + [1.0], trainable = False) # marks the very last instruction.
		self.direction = tf.Variable(1.0, trainable = False) # direction of execution. A value of 1 corresponds to shifting the program forward and a value of 0 corresponds to shifting it backwards.
		self.halt = tf.Variable(0.0, trainable = False) # tendency to ignore instruction (simulating halting). Value of 1 completely ignores instructions, while a value of 0 allows instructions to be executed in full strength.
		self.loop_counter = tf.Variable([1.0]+[0.0]*max_loop_count, trainable = False) # counts loops (in fuzzy manner). A non-zero value causes the muting of instructions because we are searching for the matching brace.
		# INPUT
		if inp == None:
			self.input = tf.Variable([[1.0]+[0.0]*255]*input_size, trainable = False)
		self.input = inp
		# OUTPUT
		self.output = tf.Variable([[1.0]+[0.0]*255]*output_size, trainable = False)
		# MEMORY
		self.memory = tf.Variable([[1.0]+[0.0]*255]*memory_size, trainable = False)
		self.time_counter = 0

	def forward(self):
		self.memory_update()
		self.loop_related_update()
		self.io()
		self.program_update()
		self.time_counter += 1


	def io(self):
		# Input
		I = self.program[0, INP] * (1 - self.halt) * (1 - self.loop_counter[0])
		shifted_input = tf.roll(self.input, shift = 1, axis = 0)
		self.input = I * shifted_input + (1 - I) * shifted_input
		# Output
		O = self.program[0, OUT] * (1 - self.halt) * (1 - self.loop_counter[0])
		shifted_output = tf.concat([self.memory[:1], self.output[1:]], axis = 0)
		shifted_output = tf.roll(self.output, shift = 1, axis = 0)
		self.output = O * shifted_output + (1 - O) * shifted_output


	def program_update(self):
		self.program = self.direction * tf.roll(self.program, shift = 1, axis = 0)  + (1-self.direction) * tf.roll(self.program, shift = -1, axis = 0)
		self.halt_point = self.halt_point * tf.roll(self.halt_point, shift = 1, axis = 0)  + (1-self.direction) * tf.roll(self.halt_point, shift = -1, axis = 0)
		self.halt = self.halt_point[0]


	def loop_related_update(self):
		# Increment loop counter if:
		# Going forward + Encounter "[" + Current cell = 0
		# Going backward + Encounter "]" + Current cell != 0
		# Decrement loop counter if:
		# Going backward + Encounter "[" + Current cell != 0
		# Going forward + Encounter "]" + Current cell = 0
		bacc = 1 - self.direction
		noz = 1 - self.memory[0, 0]
		INC = 1 - (1 - self.direction* self.program[0, LOP] * self.memory[0, 0])*(1 - bacc * self.program[0, LCL] * noz)
		DEC = 1 - (1 - bacc * self.program[0, LOP] * noz)*(1 - self.direction * self.program[0, LCL] * self.memory[0, 0])
		self.loop_counter = INC * tf.roll(self.loop_counter, shift = 1, axis = 0) + DEC * tf.roll(self.loop_counter, shift = 1, axis = 0)  + (1-INC-DEC)*self.loop_counter
		# Reverse the direction upon zeroing after a loop counter interaction
		REV = (INC + DEC) * self.loop_counter[0]
		self.direction = REV * (1 - self.direction) + (1 - REV) * self.direction
		

	def memory_update(self):
		updated_memory = tf.zeros(shape = (self.memory_size, 256))
		A = self.program[0, ADD] * (1 - self.halt) * (1 - self.loop_counter[0]) 
		S = self.program[0, SUB] * (1 - self.halt) * (1 - self.loop_counter[0]) 
		R = self.program[0, RGT] * (1 - self.halt) * (1 - self.loop_counter[0]) 
		L = self.program[0, LFT] * (1 - self.halt) * (1 - self.loop_counter[0])
		I = self.program[0, INP] * (1 - self.halt) * (1 - self.loop_counter[0])
		updated_memory += A * tf.concat([tf.roll(self.memory[:1], shift = 1, axis = 1), self.memory[1:]], axis = 0)
		updated_memory +=  S * tf.concat([tf.roll(self.memory[:1], shift = -1, axis = 1), self.memory[1:]], axis = 0)
		updated_memory += R * tf.roll(self.memory, shift = 1, axis = 0)
		updated_memory += L * tf.roll(self.memory, shift = -1, axis = 0)
		updated_memory +=  I * tf.concat([self.input[:1], self.memory[1:]], axis = 0)
		updated_memory += (1-A-S-R-L-I) * self.memory
		self.memory = updated_memory
