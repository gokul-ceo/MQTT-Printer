
# Cloud Print using MQTT Protocol

## What is MQTT Protocol?

MQTT is a standards-based messaging protocol, or set of rules, used for machine-to-machine communication. Smart sensors, wearables, and other Internet of Things (IoT) devices typically have to transmit and receive data over a resource-constrained network with limited bandwidth.

## About this project

This project uses a Raspberry Pi 4 with Ubuntu Server as the client. The Raspberry Pi is connected to a thermal printer via USB cable. The MQTT-broker, which is used to communicate messages, is hosted in HiveMQ Cloud. A server running in Google Cloud publishes restaurant orders to the HiveMQ Cloud Broker. The Raspberry Pi client is subscribed to the topic that the Google Cloud server publishes to. When an order is received, the Raspberry Pi client prints the order details on the thermal printer that is connected to it.

## Tech Stack

**MQTT-Broker:** [Hivemq](https://www.hivemq.com/mqtt-cloud-broker/) 

**Client:** Raspberry pi 4 (ubuntu server os)
