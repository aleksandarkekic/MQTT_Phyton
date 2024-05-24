from paho.mqtt import client as mqtt_client
import time
from datetime import datetime


class Client:
    def __init__(self):
        """
        Initializes a class object with basic information such as broker address, port, client ID, subscribed topics
        Creates an MQTT client using the paho.mqtt.client library
        """
        self.broker = 'localhost'
        self.port = 1883
        self.client_id = 6
        self.subscribed_topics = [("finished/all", 1), ("control", 1), ("finished/2/3", 1), ("finished/1/2", 1),
                                  ("finished/3", 1)]
        self.client = mqtt_client.Client(f"{self.client_id}")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        """
        :param client:MQTT client instance
        :param userdata:User data transferred during connection
        :param flags:additional information about the connection
        :param rc:Return code indicating successful connection (0 for success)

        """
        if rc == 0:
            print("Connected to MQTT Broker!")
            self.subscribe(self.subscribed_topics)
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_message(self, client, userdata, msg):
        """
        :param client:client:MQTT client instance
        :param userdata:User data transferred during connection
        :param msg:The received message is an instance of the `MQTTMessage` class

        """
        message = msg.payload.decode()
        trenutno_vreme = datetime.now()

        if msg.topic.__eq__("control"):
            if message.split("#")[0].__eq__("STOP") and message.split("#")[1].__eq__("APP"):
                formatirano_vreme = trenutno_vreme.strftime("[%d.%m.%Y. %H:%M:%S]")
                print(f"{formatirano_vreme} Received `{msg.payload.decode()}` from `{msg.topic}` topic")
                self.stop()
            else:
                formatirano_vreme = trenutno_vreme.strftime("[%d.%m.%Y. %H:%M:%S]")
                print(f"{formatirano_vreme} Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        else:
            formatirano_vreme = trenutno_vreme.strftime("[%d.%m.%Y. %H:%M:%S]")
            print(f"{formatirano_vreme} Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    def subscribe(self, topic):
        """
        The method used to subscribe to specific topics.
        :param topic:Topics the client wants to subscribe to

        """
        self.client.subscribe(topic)

    def stop(self):
        """
        The method used to stop the client, or log out of the MQTT broker.

        """
        self.client.disconnect()

if __name__ == '__main__':
    client = Client()
