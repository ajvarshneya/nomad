import random
import sys

MIN_ID = 1
MAX_ID = 100
NUM_PAIRS = 10
MAX_CLICKS = 20

if __name__ == "__main__":
	# Use a seed for consistent random generation
	random.seed(777)

	# Generate a dictionary of item pairs and click counts
	pairs = {}
	results = {}
	for i in xrange(NUM_PAIRS):
		# Get two item ids
		item_1 = str(random.randint(MIN_ID, MAX_ID))

		item_2 = item_1
		while item_2 == item_1:
			item_2 = str(random.randint(MIN_ID, MAX_ID))

		min_item = min(item_1, item_2)
		max_item = max(item_1, item_2)

		# Set the number of clicks for that item
		clicks = random.randint(1, MAX_CLICKS)
		pairs[(min_item, max_item)] = clicks
		results[(min_item, max_item)] = clicks

	# Map item pairs to list of distinct users who clicked
	user_id = 1
	for key in pairs:
		user_list = []
		for i in range(pairs[key]):
			user_list.append("user" + str(user_id))
			user_id += 1
		pairs[key] = user_list

	lines = []
	for key in pairs:
		item_1, item_2 = key
		user_list = pairs[key]

		for user in user_list:
			lines.append("{}\t{}".format(user, item_1))
			lines.append("{}\t{}".format(user, item_2))

			# Randomly insert duplicate lines (10% chance)
			if random.random() < 0.1:
				lines.append("{}\t{}".format(user, item_1))

	random.shuffle(lines)

	print ("Results:")
	for key in sorted(results):
		if results[key] >= 3:
			print ("{}\t{}".format(key, results[key]))
	print

	print ("File:")
	for line in lines:
		print (line)