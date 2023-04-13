import paho.mqtt.client as paho
from paho import mqtt
import json
import ssl
from escpos.printer import Usb

VENDOR_ID = 0x0fe6
PRODUCT_ID = 0x811e

# Initialize printer variable
global printer
printer = None


def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected with result code " + str(rc))
    # subscribe to the topic when connected
    client.subscribe("print/orderdetails", qos=1)


def on_message(client, userdata, msg):
    try:
        # decode the incoming message
        data = json.loads(msg.payload.decode("utf-8"))

        # establish printer connection
        printer = Usb(VENDOR_ID, PRODUCT_ID)

        # set up receipt header
        printer.set("center", "a", "b", 1, 1)
        printer.text("SRI SARAVANA\n")
        printer.text("NH SERVICE ROAD\n")
        printer.text("MELMARUVATHUR -603319\n\n")

        # print order number, bill number, time and date
        printer.set("left", "a", "b", 1, 1)
        # printer.text("Order No: "+ data["orderno"] +"\n")
        printer.set("right", "a", "b", 1, 1)
        printer.text("Time: " + data["timestamp"] + "\n")
        printer.text("Date: " + data["date"] + "\n")
        printer.set("left", "a", "b", 1, 1)
        printer.text("Bill No: " + str(data["bill_number"]) + "\n\n")
        printer.set('center', 'a', 'b', 1, 1)

        # set up receipt items
        items = data["items"]

        # print item details and calculate subtotal
        subtotal = 0
        printer.text("{:<20}{:<8}{:<10}\n".format("Item", "Qty", "Price"))
        printer.text("-------------------------------------------\n")
        for item in items:
            printer.text("{:<20}{:<8}{:<10.2f}\n".format(item["name"], item["quantity"], item["price"]))
            subtotal += item["price"] * int(item["quantity"])
        printer.text("-------------------------------------------\n")

        # calculate tax and total

        total = subtotal
        printer.text("{:<20}{:<10.2f}\n".format("Subtotal", subtotal))
        printer.text("{:<20}{:<10.2f}\n".format("Total", total))

        # set up receipt footer
        printer.text("--------------------------------\n")
        printer.text("Thank you for visiting!\n")

        # cut the paper

        printer.cut()  # close printer connection
        printer.close()

    except Exception as e:
        print(f"Failed to print receipt: {e}")
    if printer is not None:
        printer.close()

client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE
client.tls_set_context(ssl_ctx)
client.tls_insecure_set(True)
client.username_pw_set(username="printagent", password="printagent")
client.connect("aef90c8a1e6548278f2e423f0cf14f4c.s1.eu.hivemq.cloud", 8883)
client.on_connect = on_connect
client.on_message = on_message

# continuously check for incoming messages
client.loop_forever()