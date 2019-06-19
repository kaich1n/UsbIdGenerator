all:
	python3 UsbIdGenerator.py
	gcc -Wall test.c -o test
	./test 0x2c7c

clean:
	@rm -rf test *.o

.PHONY: all clean
