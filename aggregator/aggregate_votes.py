import os
import json
from pyspark.sql import SparkSession

# Eenvoudige lokale paths - geen Google API nodig
data_folder = "/data"
output_folder = "/output"

# Spark configuratie
spark = SparkSession.builder \
    .appName("EurovisionVoteAggregator") \
    .master("local[*]") \
    .getOrCreate()

# Zoek alle stembestanden lokaal
vote_files = [f for f in os.listdir(data_folder) if f.endswith("_votes.txt")]

if not vote_files:
    print("No vote files found in /data.")
    exit(1)

all_results = []

for vote_file in vote_files:
    input_file = os.path.join(data_folder, vote_file)
    print(f"Processing {input_file}...")
    
    # Spark RDD verwerking (zoals eerder)
    rdd = spark.sparkContext.textFile(input_file)
    
    mapped = rdd.map(lambda line: line.strip().split(",")) \
                .map(lambda fields: ((fields[0], fields[2]), 1))
    
    reduced = mapped.reduceByKey(lambda a, b: a + b)
    
    grouped = reduced.map(lambda x: (x[0][0], (x[0][1], x[1]))) \
                    .groupByKey() \
                    .mapValues(list)
    
    result = [{
        "country": x[0],
        "votes": [{"song_number": int(song), "count": int(count)} for song, count in x[1]]
    } for x in grouped.collect()]
    
    all_results.extend(result)

# Schrijf naar lokaal output bestand
output_file = os.path.join(output_folder, "italy_votes_reduced.json")
with open(output_file, "w") as f:
    json.dump(all_results, f, indent=4)

print(f"Results saved to {output_file}")
spark.stop()
