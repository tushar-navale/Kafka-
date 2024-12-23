#!/usr/bin/env python3

from kafka import KafkaConsumer
import sys
import json
import math 

client1 = sys.argv[1]
most_lang = {}
diff_cat = {}


consumer=KafkaConsumer(client1, value_deserializer = lambda m: json.loads(m.decode('ascii')))

for problem in consumer:
	if "stop" in problem.value:
		break
		
	info = problem.value
	#print(info)
	category = info[0]
	stat = info[3]
	lang = info[4]
	
	if lang not in most_lang:
		most_lang[lang] = 1
	else:
		most_lang[lang] += 1
				
	if category not in diff_cat:
		diff_cat[category] = dict()
		diff_cat[category]['passed'] = 0
		if stat == "Passed":
			diff_cat[category]['passed'] = 1
		diff_cat[category]['total'] = 1	
	
	else:
		if stat == "Passed":
			diff_cat[category]['passed'] += 1
		diff_cat[category]['total'] += 1 

max_lang = []
max_value = None
for key, value in most_lang.items():
    if max_value is None or value>max_value:
        max_lang = [key]
        max_value = value
    elif value == max_value:
        max_lang.append(key)
     
max_lang.sort()
#print(max_lang) 

max_cat = []
max_diff = None
ratio = {}

for cat, sub_dict in diff_cat.items():
    pass_val = sub_dict['passed']
    total_val = sub_dict['total']
    pass_ratio = pass_val / total_val
    ratio[cat] = pass_ratio   	

min_pass_cat = []
min_value = None
for key, value in ratio.items():
    if min_value is None or value<min_value:
        min_pass_cat = [key]
        min_value = value
    elif value == min_value:
        min_pass_cat.append(key)

min_pass_cat.sort()
#print(min_pass_cat)

output = {}
output["most_used_language"] = max_lang
output["most_difficult_category"] = min_pass_cat     

print(json.dumps(output, indent = 4))	
consumer.close()
