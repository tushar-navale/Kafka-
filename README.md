# Kafka-
Using Kafka streaming for the high density data handling

Reference for the assignment : https://hackmd.io/@pesu-bigdata/ryDbjmTkke#Task-2---Kafka


Run all the consumer that is SUBSCRIBER to get it running to receive the data from the communication infrastructure
Make sure to give all the topic for all the consumers and producers, there are 3 main topic
then run the producer with the same topic writting for all the consumer

Story Background

You are a developer for an online coding platform which hosts various DSA problems and competitions for students, developers and anyone needing interview preparations. There is continuous stream of information generated by the platform and you are tasked with building a producer-consumer pipeline with Kafka to support the various operations and computations needed for the platform.
Dataset Format and Explanation

The rows in the dataset are of 3 types, based on the event that they are describing -

    problem: Describes the event when a user has made a submission for a specific problem with additional fields. The schema for this format is -

    problem user_id problem_id category difficulty submission_id status language runtime

An example row of this format:
problem u_1 p_1 Arrays Medium s_001 Passed Python 300

    competition: Describes the event when a user has made a submission for a problem as a part of the competition with additional fields. The schema for this format is -

    competition comp_id user_id com_problem_id category difficulty comp_submission_id status language runtime time_taken

An example row of this format:
competition c_1 u_1 cp_1 Trees Hard cs_1 Failed C 50 22

    solution: Describes the event when a user has made his correct/passed submission public for other users to see. The schema for this format is -

    solution user_id problem_id submission_id upvotes

An example row of this format:
solution u_1 p_1 s_1 230
Additional Details about the dataset

    The rows will be shuffled, as it is a stream of events.
    The unit of measurement for runtime is millisecond(ms) and for time_taken is minutes.
    The problems and solutions in the competition format are independent/different from those in the problem format.
    If a submission is present in the solution format, it will also be present in the problem format with status Passed.
    In the competition format, the same comp_problem_id can be used for multiple competitions.

Problem Statement

Using the dataset provided to you, generate output files for 3 different clients based on their requirements.
Client 1: Wants to know the most frequently used programming language and the most difficult category to solve.
Client 2: Wants to get the leaderboard for all competitions with the points each user scored in the each competition.
Client 3: Wants to know which user is contributing to the community the most (highest total upvotes), and additionally also wants to calculate every user's elo rating on the platform.
Description

Sample dataset

competition c_0003 u_012 cp_00004 Stacks&Queues Hard cs_00003 Failed Rust 1994 46
problem u_019 p_00006 DP Hard s_00005 Passed C 1408
problem u_016 p_00008 Trees Hard s_00003 Failed Java 1443
problem u_009 p_00015 Graphs Hard s_00004 Passed Go 120
solution u_019 p_00006 s_00005 511
problem u_017 p_00009 Heaps Hard s_00002 Failed Go 821
solution u_009 p_00015 s_00004 180
competition c_0003 u_018 cp_00008 Heaps Easy cs_00005 Passed Go 411 7
competition c_0001 u_005 cp_00004 Stacks&Queues Hard cs_00004 Passed Ruby 756 25
competition c_0002 u_002 cp_00010 Greedy Hard cs_00001 TLE Python 2440 32
competition c_0002 u_003 cp_00010 Greedy Hard cs_00002 TLE Python 2076 18
problem u_020 p_00016 Stacks&Queues Easy s_00001 TLE C++ 2805
EOF

Client 1

Needs information on 2 things -

    Most frequently used programming language, i.e, the language with the most submissions made
    Most difficult category to solve, i.e, the category with the smallest ratio of Passed/Total submissions

Sample output and format after running consumer1.py, for client1: Print the json.dumps of the dictionary in the following format -

{
    "most_used_language": [
        "Go"
    ],
    "most_difficult_category": [
        "Heaps",
        "Stacks&Queues",
        "Trees"
    ]
}

Notes for client 1:

    The client is only interested in the submissions made in the problem format.
    If there is a tie for either part of the question, then return all the results in a list sorted lexicographically(similar to the above output where Heaps and Trees are tied)

Client 2

Needs leaderboard with points for all competitions. You need to compute the points scored in each competition by a user to find the final leaderboard.

Sample output and format after running consumer2.py, for client2: Print the json.dumps of the dictionary in the following format -

{
    "c_0001": {
        "u_005": 2393
    },
    "c_0002": {
        "u_002": 60,
        "u_003": 79
    },
    "c_0003": {
        "u_012": 0,
        "u_018": 2358
    }
}

Notes for client 2:

    Needs the leaderboard in lexicographically sorted order of competition_id.
    Under each competition, there must be key-value pairs of user:points_scored for all the users in the competition.
    The users in each competition must be sorted in lexicographic order of user_id.
    Round down the final points scored to an integer in each competition for each user.
    Formula for points for each submission is given below :point_down:

Submission_Points = Status_Score * Difficulty_Score * Bonus

Status_Score = 100 if Passed | 20 if TLE | 0 if Failed
Difficulty_Score = 3 if Hard | 2 if Medium | 1 if Easy
Bonus = max(1,(1 + Runtime_bonus - Time_taken_penalty))
Runtime_bonus = 10000/runtime
Time_taken_penalty = 0.25*time_spent

Client 3

Needs information on 2 things -

    User with the most contribution to the community, i.e, the user with the most total upvotes.
    Each user's elo rating.

Sample output and format after running consumer3.py, for client3: Print the json.dumps of the dictionary in the following format -

{
    "best_contributor": [
        "u_019"
    ],
    "user_elo_rating": {
        "u_002": 1210,
        "u_003": 1211,
        "u_005": 1245,
        "u_009": 1315,
        "u_012": 1195,
        "u_016": 1197,
        "u_017": 1202,
        "u_018": 1233,
        "u_019": 1239,
        "u_020": 1205
    }
}

Notes for client 3:

    If the best_contributor is tied on upvotes, then list all the user_id's sorted lexicographically.
    The users with elo ratings are sorted by user_id lexicographically.
    Round down the user elo rating to an integer
    Both competition and problem submissions are considered for the elo rating of a user.
    Formula for User Elo Rating -

New_Elo = Current_Elo + Submission_Points

Submission_Points = K * (Status_Score * Difficulty_Score) + Runtime_bonus
K = 32 (constant scaling factor)
Status_Score = 1 if Passed, 0.2 if TLE, -0.3 if Failed
Difficulty_Score = 1 if Hard, 0.7 if Medium, 0.3 if Easy
Runtime_bonus = 10000/runtime


Initial elo rating for all users = 1200

Tips to solve the Task

The logic for the producer and consumer is up to you. The input to the producer file will be streamed through the standard input.

You are required to use the kafka-python library to solve the problem statement. You should have four files, one for the producer and three for the three different consumers. The producer should be named kafka-producer.py and the consumers should be named kafka-consumer1.py, kafka-consumer2.py and kafka-consumer3.py.

It is recommended for you to use three topics to solve the assignment. All three topic names will be passed as command line arguments to all four files, and you may make use of them as required. There is no constraint on how you want to use these 3 topics.

To test your code, run the consumer files first in three seperate terminals and then the producer file in a fourth separate terminal.

./kafka-consumer1.py topicName1 topicName2 topicName3 > output1.json

./kafka-consumer2.py topicName1 topicName2 topicName3 > output2.json

./kafka-consumer3.py topicName1 topicName2 topicName3 > output3.json

cat sample_dataset.txt | ./kafka-producer.py topicName1 topicName2 topicName3
