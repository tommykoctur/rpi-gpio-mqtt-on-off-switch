import subprocess
import RPi.GPIO as GPIO
import time
import click


@click.command()
@click.option('--gpio', required=True, help='RaspberryPi GPIO number', type=int)
@click.option('--broker_ip', required=True, help='MQTT broker ip', type=str)
@click.option('--broker_port', required=True, default="1883", help='MQTT broker port', type=str)
@click.option('--topic', required=True, help='MQTT topic', type=str)
@click.option('--message_high', required=True, help='MQTT message on GPIO HIGH', type=str)
@click.option('--message_low', required=True, help='MQTT message on GPIO LOW', type=str)
@click.option('--user', required=True, help='MQTT user name', type=str)
@click.option('--password', required=True, help='MQTT password', type=str)
def switch(gpio, broker_ip, broker_port, topic, message_high, message_low, user, password):

    # configure variables
    gpio_id = gpio
    broker_ip = broker_ip
    broker_port = broker_port
    mqtt_topic = topic
    message_high = message_high
    message_low = message_low
    mqtt_user = user
    mqtt_password = password

    interference_burst_protect = 0.1


    # Setup GPIO - pull up to reduce interference
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_id, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # load gpio state on startup
    if GPIO.input(gpio_id):
        prev_state = 1
    else:
        prev_state = 0

    while True:
        GPIO.wait_for_edge(gpio_id, GPIO.BOTH, bouncetime=200)
        # a little delay to check if we received interference signal (short peak).
        # 100uF parallel capacitor should reduce interference, but it in rare cases
        # gpio can get short signal burst when long wires to switch are used.
        time.sleep(interference_burst_protect)
        if GPIO.input(gpio_id) == GPIO.HIGH and prev_state == 0:
            subprocess.call(["mosquitto_pub",
                             "-h", broker_ip,
                             "-p", broker_port,
                             "-t", mqtt_topic,
                             "-m", message_high,
                             "-u", mqtt_user,
                             "-P", mqtt_password])
            prev_state = 1

        if GPIO.input(gpio_id) == GPIO.LOW and prev_state == 1:
            subprocess.call(["mosquitto_pub",
                             "-h", broker_ip,
                             "-p", broker_port,
                             "-t", mqtt_topic,
                             "-m", message_low,
                             "-u", mqtt_user,
                             "-P", mqtt_password])
            prev_state = 0

    # clean up GPIO on normal exit:
    GPIO.cleanup()


if __name__ == '__main__':
    switch()