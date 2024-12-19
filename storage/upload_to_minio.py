from minio import Minio
import os

# Konfigurasi MinIO
client = Minio(
    'localhost:9000',
    access_key='minioadmin',
    secret_key='minioadmin',
    secure=False
)

bucket_name = 'batch-data'

# Buat bucket jika belum ada
if not client.bucket_exists(bucket_name):
    client.make_bucket(bucket_name)

# Unggah file batch ke MinIO
batch_folder = './batch'
for file_name in os.listdir(batch_folder):
    file_path = os.path.join(batch_folder, file_name)
    client.fput_object(bucket_name, file_name, file_path)
    print(f"Uploaded {file_name} to MinIO")
