# Fuzzy Brainfuck
In Fuzzy Brainfuck, instructions are probability distributions over Brainfuck's instruction set. More precisely, program is represented by $PROG^{(t)}$ which is a $P \times 8$ matrix. Timesteps are specified as the program gets shifted (softly) during the execution because only the leftmost part is active. The same principle applies to the memory, input, and output.

A byte is replaced by a probability distribution over all the possible 256 values. This change applies to memory, input, and output. $MEM^{(t)}$, $INP^{(t)}$, and $OUT^{(t)}$ are the memory, input, and output which have the sizes $M \times 256$, $I \times 256$, and $O \times 256$, respectively.

$DIR^{(t)} \in [0, 1]$ tells the direction of the program flow. A value of $1$ corresponds to moving forward, while a value of $0$ corresponds to moving backward.

$HLT^{(t)} \in [0, 1]$ (soft halt flag) tells how hard we weaken instructions. A value of $1$ blocks all instructions and a value of $0$ allows instructions to be executed in full strength.

$LC^{(t)}$ (the soft loop counter) is a probability distribution over the integers $0, 1, 2,..., L_{\max}$ which counts loops and also plays the role of muting instructions whenever we are searching for the matching brace. A non-zero probability for non-zero values causes muting of instructions similar to $HLT^{(t)}$.

$STR^{(t)} = LC^{(t)}(0) \times (1 - HLT^{(t)}) $ refers to how strongly we execute the instruction, taking into account the weakening caused by soft halt flag and soft loop counter.

$HP^{(t)}$ (halting point) is a probability distribution over the integers $1,2,..., P$ (over the program) and it marks the last instruction.

The interpreter applies four transformations over those values: Memory update, IO update, loop-related updates, and program update.


# Memory update

$$MEM^{(t+1)} = STR^{(t)}  (\sum_{I} PROG_{1, I}^{(t)} \times APP(I, MEM^{(t)})) + (1 - STR^{(t)}  \sum_{I} PROG_{1, I}^{(t)}) \times MEM^{(t)}$$

We sum over instructions that has effect on memory: `ADD`, `SUB`, `LFT`, `RGT`, and `INP`.$APP(I, MEM^{(t)})$ denotes the state of memory after applying instruction $I$. `ADD` shifts the probability distribution at the first cell to the right, while sub shifts it to the left. `RGT` shifts the entire memory to the left, while `LFT` shifts it to the right. Finally, input just replaces the value at first cell with the current input.

# IO update

$$INP^{(t+1)} = STR^{(t)} \times PROG_{1, INP}^{(t)} \times L(INP^{(t)}) + (1 - STR^{(t)} \times PROG_{1, INP}^{(t)}) \times INP^{(t)}$$
$$OUT^{(t+1)} = STR^{(t)} \times PROG_{1, OUT}^{(t)} \times R(OUT^{(t)}, MEM^{(t)}) + (1 - STR^{(t)} \times PROG_{1, OUT}^{(t)}) \times OUT^{(t)}$$

$L(A)$ shifts $A$ to the left. $R(A, B)$ takes the $A$, replaces its first row with $B$'s, and then shifts it to the right.

# Loop-related update

This is the most complicated part of the construction. It helps to know the softening of boolean operations: $AND(x, y) = xy$, $OR(x, y) = 1-(1-x)(1-y)$ and $NOT(x) = 1-x$.

Loop counter increments happens when:

1) moving forward, encountered an opening brace, and the active cell holds a value of $0$.

2) moving forward, encountered a closing brace, the active cell, the current cell holds a non-zero value, and the loop counter is $0$

3) moving backward, encountered a closing brace.

(forward/backward talks about the program flow)

Loop counter decrements happens when:

1) Moving backward and encountered an opening brace.

2) moving forward, encountered a closing brace, and the loop counter is non-zero.

Reversal of program flow happens when:

1) Going backward, encountered an opening brace, and the loop counter has value of 1.

2) moving forward, encountered a closing brace, the active cell, the current cell holds a non-zero value, and the loop counter is $0$

With these conditions and the softening of boolean operations, we calculate probabilities $INC^{(t)}$, $DEC^{(t)}$ and $REV^{(t)}$.

$$LC^{(t+1)} = DEC^{(t)} \times L(LC^{(t)}) + INC^{(t)} \times R(LC^{(t)}) + (1-DEC^{(t)}-INC^{(t)}) \times LC^{(t)} $$

$$DIR^{(t+1)} = REV^{(t)} \times (1 - DIR^{(t)}) + (1-REV^{(t)}) \times DIR^{(t)}$$


The halt flag must be true if either it is already true or we have encountered the last instruction (which is marked by $HP^{(t)}$). A reversal of program flow forcefully prevents halting.

$$HLT^{(t+1)} = (1 - REV^{(t)}) \times (1- (1- HLT^{(t)})(1-HP^{(t)}(1)))$$

# Program update


$$PROG^{(t+1)} = (1-DIR^{(t)}) \times B(PROG^{(t)}) + DIR^{(t)} \times F(PROG^{(t)})$$
$$HP^{(t+1)} = (1-DIR^{(t)}) \times B(HP^{(t)}) + DIR^{(t)} \times F(HP^{(t)})$$

$B$ and $F$ shifts backward (right) and forward (left), respectively.
