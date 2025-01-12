import time
import board
import adafruit_bh1750
import subprocess

i2c = board.I2C()
sensor = adafruit_bh1750.BH1750(i2c)

# COLOR settings:
# R: 255
# G: 70
# B: 45

def set_monitor_brightness(brightness):
    # Construct the command
    command = ["ddcutil", "setvcp", "10", str(int(brightness))]
    
    try:
        # Run the command without capturing output to minimize overhead
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def nonlinear_map_lux_to_brightness(lux) -> int:
    """
    Maps ambient light (lux) to brightness percentage using a non-linear approach.
    """
    # Define a non-linear mapping with thresholds
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

while True:
    print("%.2f Lux"%sensor.lux)
    set_monitor_brightness(nonlinear_map_lux_to_brightness(sensor.lux))
    time.sleep(10)