# Fuzzy Brainfuck
Fuzzy Brainfuck is a superset of Brainfuck whose program space is continuous and its interpreter is differentiable, allowing you to train programs with Gradient-based methods. An instruction in Fuzzy Brainfuck is a probability distribution over Brainfuck's instruction set. A byte is replaced by a probability distribution over all of the 256 possible values and this change applies to memory, input and output.

You can create an instance of Fuzzy Brainfuck by creating an instance of the class `Fuzzy_Brainfuck`. The parameters are program_size = 100, output_size = 50, memory_size = 200, max_loop_count = 20, raw_program = None, and inp = None.

Raw program holds the trainable parameters of the program. It is turned into the actual program by applying softmax. The actual program, unlike the raw program, gets modified during execution because of shifting, which is necessary as, internally, only the leftmost instruction is active. The rest of parameters are pretty self-explanatory.

The two most important methods of the class `Fuzzy_Brainfuck` are `initiate`, `forward`:


`initiate` resets the state of the program, memory, and output, and takes the new input.

`forward` forwards the execution by 1 instruction.

# Training-related information

Fuzzy Brainfuck uses Tensorflow and you should use Tensorflow to train Fuzzy Brainfuck programs.

Training could incentivize convergence to meaningful normal Brainfuck program. One way this could be done is by penalizing ambiguity. The method `program_ambiguity` measures the ambiguity in the program giving a score of 0 for programs whose instructions are pure, and a score of 1 for programs whose instructions are just an equal mix of all Brainfuck instructions.
