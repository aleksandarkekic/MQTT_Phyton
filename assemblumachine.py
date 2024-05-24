from machine import Machine
from paho.mqtt import client as mqtt_client
from datetime import datetime

import time


class AssemblyMachine(Machine):
    broker = 'localhost'
    port = 1883

    def __init__(self, id, numbOfProducts):
        """
           Initializes a class object with basic information such as broker address, port, client ID, subscribed topic
           Creates an MQTT client using the paho.mqtt.client library
        """
        super().__init__(id)
        self.assembl_machine_working = False
        self.numbOfProducts = numbOfProducts
        self.subscribed_topics = [("control", 1), ("finished/2/3", 1)]
        self.client_id = 3
        self.mess = "default_message"
        self.remote_control = False  # We set this to false when we receive the message STOP or STOPALL from remote control
        self.publish_topic1 = "finished/all"
        self.publish_topic2 = "finished/3"
        self.timeToWork = 3
        self.client = mqtt_client.Client(f"{self.client_id}")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

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
        if msg.topic.__eq__("finished/2/3"):
            self.assembl_machine_working = True
        elif msg.topic.__eq__("control"):
            if message.split("#")[0].__eq__("RUN_TIME") and message.split("#")[1].__eq__(f"{self.client_id}"):
                self.timeToWork = int(message.split("#")[2])
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            elif message.split("#")[0].__eq__("MESSAGE") and message.split("#")[1].__eq__(f"{self.client_id}"):
                self.mess = message.split("#")[2]
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
            elif message.split("#")[0].__eq__("STOP") and message.split("#")[1].__eq__(f"{self.client_id}"):
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
                self.assembl_machine_working = True
                self.remote_control = False
            elif message.split("#")[0].__eq__("STOP") and message.split("#")[1].__eq__("ALL"):
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
                self.assembl_machine_working = True
                self.remote_control = False
            elif message.split("#")[0].__eq__("START") and message.split("#")[1].__eq__(f"{self.client_id}"):
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
                self.assembl_machine_working = True
                self.remote_control = True
            elif message.split("#")[0].__eq__("START") and message.split("#")[1].__eq__("ALL"):
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
                self.assembl_machine_working = True
                self.remote_control = True
            elif message.split("#")[0].__eq__("STOP") and message.split("#")[1].__eq__("APP"):
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
                self.assembl_machine_working = False
                self.remote_control = False
                self.stop()

    def subscribe(self, topic):
        """
        The method used to subscribe to specific topics.
         :param topic:Topics the client wants to subscribe to

        """
        self.client.subscribe(topic)

    def run(self):
        """
        this machine simulates the operation of a assemlby machine
        """
        numOfFinishedProducts = 0
        while numOfFinishedProducts < self.numbOfProducts:
            while self.assembl_machine_working:
                if self.remote_control:
                    print(self.mess)
                    time.sleep(self.timeToWork)
                    numOfFinishedProducts = numOfFinishedProducts + 1
                    trenutno_vreme = datetime.now()
                    formatirano_vreme = trenutno_vreme.strftime("[%d.%m.%Y. %H:%M:%S]")
                    message = f"{formatirano_vreme} Assemblu machine je zavrsila rad na: {numOfFinishedProducts}. materijalu! "
                    self.client.publish(self.publish_topic2, message)
                if numOfFinishedProducts == self.numbOfProducts:
                    self.client.publish(self.publish_topic1, message)
                    self.remote_control = False
                    self.assembl_machine_working = False
                    self.stop()
                # self.assembl_machine_working=False

    def stop(self):
        """
        The method used to stop the client, or log out of the MQTT broker.

        """
        self.client.disconnect()


machine_3 = AssemblyMachine(id=3, numbOfProducts=10)
machine_3.start()
