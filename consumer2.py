#!/usr/bin/env python3

from kafka import KafkaConsumer
import sys
import json
import math 

client1 = sys.argv[2]

#Submission_Points = Status_Score * Difficulty_Score * Bonus
#Status_Score = 100 if Passed | 20 if TLE | 0 if Failed#
#Difficulty_Score = 3 if Hard | 2 if Medium | 1 if Easy
#Bonus = max(1,(1 + Runtime_bonus - Time_taken_penalty))
#Runtime_bonus = 10000/runtime
#Time_taken_penalty = 0.25*time_spent

comp_dict = dict()


def SubPoints(time_taken, runtime, diff, status):
	
	time_penalty = 0.25 * time_taken
	runtime_bonus = 10000/runtime
	
	bonus = max(1, (1 + runtime_bonus - time_penalty))
	
	status_score = None
	if status == "Passed":
		status_score = 100
	elif status == "TLE":
		status_score = 20
	else:
		status_score = 0
		
	diff_score = None
	if diff == "Hard":
		diff_score = 3
	elif diff == "Medium":
		diff_score = 2
	else:
		diff_score = 1
		
	sub_points = diff_score * status_score * bonus
	return sub_points

consumer=KafkaConsumer(client1, value_deserializer = lambda m: json.loads(m.decode('ascii')))

for competition in consumer:
	if "stop" in competition.value:
		break
		
	info = competition.value
	#print(info)
	comp_id = info[0]
	user_id = info[1]
	time_taken = int(info[-1])
	run_time = int(info[-2])
	diff = info[4]
	status = info[6]
	#print(comp_id, user_id, time_taken, run_time,diff, status)
	
	sub_points = int(SubPoints(time_taken, run_time, diff, status))
	#print(comp_id,user_id,sub_points)
	
	if comp_id not in comp_dict:
		comp_dict[comp_id] = {}
		comp_dict[comp_id][user_id] = sub_points
		
	else:
		if user_id not in comp_dict[comp_id]:
			comp_dict[comp_id][user_id] = sub_points
		else:
			comp_dict[comp_id][user_id] += sub_points
		

output = dict()
for key,sub_dict in comp_dict.items():
	#print(sub_dict)
	output[key] = dict(sorted(sub_dict.items()))

output = dict(sorted(output.items()))
print(json.dumps(output, indent = 4))	
consumer.close()
