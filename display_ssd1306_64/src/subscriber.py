#!/usr/bin/env python
import rospy
from std_msgs.msg import String

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 1
SPI_DEVICE = 0

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
	# 128x64 display with hardware I2C:
	disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

	# Note you can change the I2C address by passing an i2c_address parameter like:
	# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

	# Alternatively you can specify an explicit I2C bus number, for example
	# with the 128x32 display you would use:
	# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

	# 128x32 display with hardware SPI:
	# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

	# 128x64 display with hardware SPI:
	# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

	# Alternatively you can specify a software SPI implementation by providing
	# digital GPIO pin numbers for all the required display pins.  For example
	# on a Raspberry Pi with the 128x32 display you might use:
	# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

	# Initialize library.
	disp.begin()

	# Clear display.
	disp.clear()
	disp.display()

	# Create blank image for drawing.
	# Make sure to create image with mode '1' for 1-bit color.
	width = disp.width
	height = disp.height
	image = Image.new('1', (width, height))

	# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)

	# Draw a black filled box to clear the image.
	draw.rectangle((0,0,width,height), outline=0, fill=0)

	# Draw some shapes.
	# First define some constants to allow easy resizing of shapes.
	padding = 2
	shape_width = 20
	top = padding
	bottom = height-padding
	
	# Load default font.
	font = ImageFont.load_default()

	# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
	# Some other nice fonts to try: http://www.dafont.com/bitmap.php
	#font = ImageFont.truetype('Minecraftia.ttf', 8)

	# Write two lines of text.
	x = padding
	draw.text((x, top),    str(data.data),  font=font, fill=255)
	#draw.text((x, top+20), 'World!', font=font, fill=255)

	# Display image.
	disp.image(image)
	disp.display()

    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('subscriber', anonymous=True)

    rospy.Subscriber("display_text", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
