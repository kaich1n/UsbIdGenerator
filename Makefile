all: usb_ids.h
	@gcc -Wall test.c -o test
	./test 0x2c7c

usb_ids.h:
	@pip install --user -r requirements.txt > /dev/null
	@python3 UsbIdGenerator.py

clean:
	@rm -rf test *.o usb_ids.h

distclean:
	@rm -rf test *.o usb.ids  usb_ids.h

.PHONY: all clean distclean
