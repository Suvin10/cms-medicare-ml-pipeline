df = pd.read_csv(data_path)

# Load model
model = joblib.load("/tmp/model.joblib")

# If model not local, download it
s3 = boto3.client("s3")