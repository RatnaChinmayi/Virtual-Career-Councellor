class Config:
    SECRET_KEY = "some_random_secret_key"

    AWS_REGION_NAME = "us-east-1"

    DYNAMODB_TABLE = "VirtualCareerUsers"

    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012:VirtualCareerAlerts"

    UPLOAD_FOLDER = "static/uploads"
