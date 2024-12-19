import pandas as pd
from kafka import KafkaProducer
import json

# Konfigurasi Kafka
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'shipping-data'

# Setup Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Baca dataset
data = pd.read_csv('../dataset/train_dataset.csv')

# Kirim data dalam batch
for _, row in data.iterrows():
    producer.send(TOPIC_NAME, value=row.to_dict())
    print(f"Data sent: {row.to_dict()}")
producer.flush()
