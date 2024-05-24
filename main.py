from paho.mqtt import client as mqtt_client
import time


broker = 'localhost'
port = 1883
client_id = 4
publish_topic_1="control"
subscribed_topics = [("finished/all", 1)]
work=True

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        """
        :param client:MQTT client instance
        :param userdata:User data transferred during connection
        :param flags:additional information about the connection
        :param rc:Return code indicating successful connection (0 for success)

        """
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(f"{client_id}")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def printComands():
    time.sleep(1) #With this, we first print information about connecting to the broker, and after that, we print all options
    print("\n")
    print("******* You have following options: *******")
    print("******* RUN_TIME#<ID>#5 *******") #With this command, we set the waiting time in the run() method.
    print("******* MESSAGE#<ID>#Some_message *******") #With this command, we adjust the output displayed on the terminal after processing each material
    print("******* STOP#<ID> *******") #With this message, we stop the operation of the machine with the specified identifier, but we can initiate the operation again.
    print("******* START#<ID> *******") #With this message, we initiate the operation of the machine with the specified identifier
    print("******* STOP#ALL *******")#With this message, we stop the operation of all machines, but we can start it again.
    print("******* START#ALL *******")#With this message, we initiate the operation of all machines
    print("******* STOP#APP *******")#With this message, we stop the whole application

def choose_option(client):
    printComands()
    global work
    while work:
        opcija = input("Input one of options: ")
        if opcija.split("#")[0].__eq__("STOP") and opcija.split("#")[1].__eq__("ALL"):
            client.publish(publish_topic_1, opcija)
        elif opcija.split("#")[0].__eq__("STOP") and opcija.split("#")[1].__eq__("APP"):
            client.publish(publish_topic_1, opcija)
            work=False
        else:
            client.publish(publish_topic_1, opcija)



def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        """
        :param client:client:MQTT client instance
        :param userdata:User data transferred during connection
        :param msg:The received message is an instance of the `MQTTMessage` class

        """
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        if msg.topic.__eq__("finished/all"):
            global work
            work=False


    client.subscribe(subscribed_topics)
    client.on_message = on_message
def run():
    client = connect_mqtt()
    subscribe(client=client)
    client.loop_start()
    choose_option(client=client)

if __name__ == '__main__':
    run()
