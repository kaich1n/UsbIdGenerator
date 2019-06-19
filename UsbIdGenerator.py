import os
import logging
import requests


USBID_URL = "http://www.linux-usb.org/usb.ids"


class UsbDevice(object):
    def __init__(self, vid, did, v_name, d_name):
        self.vid = vid
        self.did = did
        self.v_name = v_name
        self.d_name = d_name

    def __str__(self):
        return "-".join([self.vid, self.did, self.v_name, self.d_name])


class UsbIdGenerator(object):
    def __init__(self):
        self.devices = []
        self.version = ""
        self.date = ""

    def fetch(self):
        r = os.access("usb.ids", mode=os.W_OK)
        if r:
           return

        r = requests.get(USBID_URL)
        if r.status_code == 200:
            with open("usb.ids", mode="w+b") as f:
                f.write(bytearray(r.text, encoding="utf8"))

    def parse(self):
        with open("usb.ids", encoding="utf8") as f:
            for line in f:
                line = line.rstrip()
                if not line:
                    continue
                if line.startswith("C 00  (Defined at Interface level)"):
                    break
                if line.startswith("# Version:"):
                    self.version = line.split()[2].strip()
                    continue
                if line.startswith("# Date:"):
                    self.date = line.split(maxsplit=2)[2].strip()
                    continue
                if line.startswith("#"):
                    continue
                if not line.startswith("\t"):
                    v = line.split(maxsplit=1)
                    vid = v[0]
                    v_name = v[1].replace("\\", "\\\\").replace("\"", "\\\"").replace("?", "")
                else:
                    v = line.split(maxsplit=1)
                    did = v[0]
                    d_name = v[1].replace("\\", "\\\\").replace("\"", "\\\"").replace("?", "")
                    self.devices.append(UsbDevice(vid, did, v_name, d_name))

    def gen(self):
        self.fetch()
        self.parse()
        comments = "#ifndef _USB_IDS_H_\n#define _USB_IDS_H_\n\n//\n// AUTO GENERATED, DON'T EDIT\n// http://www.linux-usb.org/usb.ids\n// Version : {}\n//\n"
        header = \
"""#include <stdint.h>

struct usb_device_id {
    uint16_t vid;
    uint16_t did;
    const char *v_name;
    const char *d_name;
} usb_device_ids[] = {
"""

        end = \
"""};

#endif // _USB_IDS_H_
"""

        with open("usb_ids.h", "w+b") as f:
            f.write(bytearray(comments.format(self.version), encoding="utf8"))
            f.write(bytearray(header, encoding="utf8"))
            for d in self.devices:
                item = "\t{\n" + \
                    f"\t\t.vid = 0x{d.vid},\n" + \
                    f"\t\t.did = 0x{d.did},\n" + \
                    f"\t\t.v_name = \"{d.v_name}\",\n" + \
                    f"\t\t.d_name = \"{d.d_name}\",\n" + \
                    "\t},\n"
                f.write(bytearray(item, encoding="utf8"))
            f.write(bytearray(end, encoding="utf8"))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    UsbIdGenerator().gen()