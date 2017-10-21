// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

    @R0
    D=M
    @counter
    M=D // set counter to the first input

    @R2
    M=0 // initialize sum with 0

(LOOP)
    @counter
    D=M
    @END
    D;JEQ // Finish if counter is zero
    @R1
    D=M
    @R2
    M=M+D // increment sum with the second input
    @counter
    M=M-1 // decrease counter
    @LOOP
    0;JMP // Goto LOOP

(END)
    @END
    0;JMP
