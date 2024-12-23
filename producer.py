#!/usr/bin/env python3
import sys
from kafka import KafkaProducer
import json
import math

producer = KafkaProducer(value_serializer = lambda m: json.dumps(m).encode('ascii'))
client1 = sys.argv[1]
client2 = sys.argv[2]
client3 = sys.argv[3]

for line in sys.stdin:
	line=line.strip().split()
	#producer.send(client3,line)
	if line[0]=="problem":
		producer.send(client1,line[3:])
	elif line[0]=="competition":
		producer.send(client2,line[1:])
	#elif line[0] == "solution" :
		#producer.send(client3,line)	
	elif line[0]=="EOF":
		producer.send(client1,"stop")
		producer.send(client2,"stop")
		producer.send(client3,"stop")
		break
	producer.send(client3,line)
producer.flush()

