import time
import board
import adafruit_bh1750
import subprocess
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

i2c = board.I2C()
sensor = adafruit_bh1750.BH1750(i2c)

def set_monitor_brightness(brightness):
    """
    Sets the monitor brightness using the ddcutil tool.
    """
    command = ["ddcutil", "setvcp", "10", str(int(brightness))]

    try:
        subprocess.run(command, check=True)
        logging.info(f"Set brightness to {brightness}%")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to set brightness: {e}")

def nonlinear_map_lux_to_brightness(lux) -> int:
    """
    Maps ambient light (lux) to brightness percentage using a non-linear approach.
    """
    if lux < 10:
        return 0
    elif lux < 50:
        return (lux - 10) / 40 * 50  # 10-50 lux maps to 0-50%
    elif lux < 200:
        return 50 + (lux - 50) / 150 * 30  # 50-200 lux maps to 50-80%
    elif lux < 500:
        return 80 + (lux - 200) / 300 * 20  # 200-500 lux maps to 80-100%
    else:
        return 100  # 500 lux and above maps to 100%

def main():
    """
    Main loop that continuously reads light levels and adjusts brightness.
    """
    while True:
        try:
            lux = sensor.lux
            logging.info(f"Current light level: {lux:.2f} Lux")
            brightness = nonlinear_map_lux_to_brightness(lux)
            set_monitor_brightness(brightness)
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

        time.sleep(10)

if __name__ == "__main__":
    main()
