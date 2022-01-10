# rpi-gpio-mqtt-on-off-switch
This python script waiting for state change of specified GPIO pin. 
On change, it will verify the signal and send message via MQTT to specified topic.

## build docker image
```sh
docker build . -t rpi-gpio-mqtt-on-off-switch
```

## run docker container
```sh
docker run -it -e GPIO_ID="21" \
                -e BROKER_IP="192.168.1.2" \
                -e BROKER_PORT="1883" \
                -e TOPIC="Home/Livingroom/LightSwitch" \
                -e MESSAGE_HIGH="1" \
                -e MESSAGE_LOW="0" \
                -e USER="mqtt_username" \
                -e PASSWORD="mqtt_password" \
                --device /dev/ttyAMA0:/dev/ttyAMA0 \
                --device /dev/mem:/dev/mem \
                --privileged \
                rpi-gpio-mqtt-on-off-switch
```


##Acknowledgment
Thanks to Angel Castro Martinez, (https://github.com/kronos-cm) for docker multistage 
build recommendations for python projects.