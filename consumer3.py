#!/usr/bin/env python3

from kafka import KafkaConsumer
import sys
import json
import math 

#New_Elo = Current_Elo + Submission_Points

#Submission_Points = K * (Status_Score * Difficulty_Score) + Runtime_bonus
#K = 32 (constant scaling factor)
#Status_Score = 1 if Passed, 0.2 if TLE, -0.3 if Failed
#Difficulty_Score = 1 if Hard, 0.7 if Medium, 0.3 if Easy
#Runtime_bonus = 10000/runtime
#Initial elo rating for all users = 1200


elo_rate = {}

def SubPoints(diff, runtime, status):
	runtime_bonus = 10000/runtime
	
	diff_score = None
	if diff == "Hard":
		diff_score = 1
	elif diff == "Easy":
		diff_score = 0.3
	else:
		diff_score = 0.7
		
	stat_score = None
	if status == "Passed":
		stat_score = 1
	elif status == "TLE":
		stat_score = 0.2
	else:
		stat_score = -0.3
		
	k = 32
	
	sub_points = k *(stat_score*diff_score) + runtime_bonus
	return sub_points

client1 = sys.argv[3]
consumer=KafkaConsumer(client1, value_deserializer = lambda m: json.loads(m.decode('ascii')))


max_contri = []
max_upvotes = None

for problem in consumer:
	if "stop" in problem.value:
		break
		
	info = problem.value
	#print(info)
	type = info[0]
	if type == "solution":
		user_id = info[1]
		upvotes = int(info[4])
		#print(info)
		#print(f"{upvotes},{user_id}")
		if max_upvotes is None or upvotes > max_upvotes:
			max_contri = [user_id]
			max_upvotes = upvotes
		elif upvotes == max_upvotes:
			max_contri.append(user_id)
			max_upvotes = upvotes
	
	elif type == "problem":
		user_id = info[1]
		status = info[6]
		runtime = int(info[8])
		diff = info[4] 
		#print(info)
		sub_points = SubPoints(diff, runtime, status)
		#print(diff,runtime, status, sub_points)
		
		if user_id not in elo_rate:
			elo_rate[user_id] = 1200 + sub_points
		else:
			elo_rate[user_id] += sub_points
			
	elif type == "competition":
		user_id = info[2]
		status = info[7]
		runtime = int(info[9])
		diff = info[5]
		#print(info)
		sub_points = SubPoints(diff, runtime, status)
		#print(diff,runtime, status, sub_points)
		
		if user_id not in elo_rate:
			elo_rate[user_id] = 1200 + sub_points
		else:
			elo_rate[user_id] += sub_points
		

max_contri.sort()
#print(max_contri)
elo_rate = dict(sorted(elo_rate.items()))
#print(elo_rate)

for key,val in elo_rate.items():
	elo_rate[key] = int(val)

output = dict()

output["best_contributor"] = max_contri
output["user_elo_rating"] = elo_rate
	
print(json.dumps(output, indent = 4))
consumer.close()
