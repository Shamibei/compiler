# Makefile for assembling and linking x86 NASM code

ASM = nasm
ASM_FLAGS = -f elf32
LD = ld
LD_FLAGS = -m elf_i386

SRC = output1.asm
OBJ = output1.o
EXE = output1

all: $(EXE)

$(OBJ): $(SRC)
	$(ASM) $(ASM_FLAGS) -o $(OBJ) $(SRC)

$(EXE): $(OBJ)
	$(LD) $(LD_FLAGS) -o $(EXE) $(OBJ)

run: all
	./$(EXE)

clean:
	rm -f $(OBJ) $(EXE)
