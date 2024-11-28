# Fuzzy Brainfuck
Fuzzy Brainfuck is a superset of Brainfuck whose program space is continous and its interpreter is differentiable, allowing you to train programs. Instructions in Fuzzy Brainfuck are probability distribution over Brainfuck's instruction set. A byte is replace by a probability distribution over all of the 256 possible values and this change applies to memory, input and output. At any given time, only the leftmost part of memory, input, output and program are active, hence the need for "shifting" them. 

You can create an instance of Fuzzy Brainfuck by creating an instance of the class `Fuzzy_Brainfuck`. The parameters are program_size = 100, output_size = 50, memory_size = 200, max_loop_count = 20, raw_program = None, and inp = None.

Raw program holds the trainable parameters of the program. It is turned into the actual program by applying softmax. The actual program, unlike the raw program, gets modified because of shifting. The rest of parameters are pretty self explanatory.

The methods of the class `Fuzzy_Brainfuck` are `initiate`, `forward`, `memory_update`, `loop_related_update`, and `program_update`.


`initiate` resets the state of the program, memory, and output, and takes the new input.

`forward` forwards the execution by 1 instruction.
