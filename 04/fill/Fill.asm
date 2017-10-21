// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

    @8192   // total bytes of pixels
    D=A
    @pixels
    M=D

(LOOP)
    @index // point at screen to write at
    M=0

    @KBD
    D=M
    @keypressed // store pressed key to save check in each iteration
    M=D

(RENDER)
    @index
    D=M
    @SCREEN
    D=A+D
    @screenaddress // calculated address of screen register to write to
    M=D

    @keypressed
    D=M
    @WHITE
    D;JEQ


(BLACK)
    @currentcolor
    M=-1
    @WRITEPIXEL
    0;JMP

(WHITE)
    @currentcolor
    M=0

(WRITEPIXEL)
    @currentcolor
    D=M
    @screenaddress
    A=M
    M=D

(END)
    @index
    MD=M+1  // Increment index
    @pixels
    D=D-M
    @LOOP
    D;JEQ   // Reset loop and read key again if all pixels rendered
    @RENDER
    0;JMP   // else, continue rendering

