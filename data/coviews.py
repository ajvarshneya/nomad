from pyspark import SparkContext

def get_item_combinations(pair):
	user, items = pair
	items = sorted(list(items))
	num_items = len(items)
	result = []
	for i in range(num_items):
		for j in range(i+1, num_items):
			result.append( (user, (items[i], items[j])) )
	return result

sc = SparkContext("spark://spark-master:7077", "PopularItems")

# Each worker loads a piece of the data file
data = sc.textFile("/tmp/data/access.log", 2)

# Read data in as pairs of (user_id, item_id clicked on by the user)
pairs = data.map(lambda line: tuple(line.split("\t")))

# Remove duplicate (user_id, item_id) pairs
pairs = pairs.distinct()

# Group data into (user_id, list of item ids they clicked on)
pairs = pairs.groupByKey()

# Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
pairs = pairs.flatMap(get_item_combinations)

# Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
pairs = pairs.map(lambda pair: (pair[1], pair[0]))
pairs = pairs.groupByKey()

# Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
# Distinct handled above
pairs = pairs.map(lambda pair: (pair[0], len(pair[1])))

# Filter out any results where less than 3 users co-clicked the same pair of items
pairs = pairs.filter(lambda pair: pair[1] >= 3)

# Bring the data back to the master node so we can print it out
output = pairs.collect()
for key, val in output:
    print ("key {}\t\tval {}".format(key, val))
print ("Popular items done")

sc.stop()
