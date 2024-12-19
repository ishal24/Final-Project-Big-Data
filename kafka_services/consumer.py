from kafka import KafkaConsumer
import json
import os
import pandas as pd

# Konfigurasi Kafka
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'shipping-data'
BATCH_FOLDER = '../storage/batch'

# Setup Kafka Consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

batch = []
batch_size = 100

# Proses data dari Kafka
for message in consumer:
    batch.append(message.value)
    if len(batch) >= batch_size:
        # Simpan batch ke file
        batch_df = pd.DataFrame(batch)
        batch_file = os.path.join(BATCH_FOLDER, f'batch_{len(os.listdir(BATCH_FOLDER)) + 1}.json')
        batch_df.to_json(batch_file, orient='records')
        print(f"Batch saved: {batch_file}")
        batch = []
