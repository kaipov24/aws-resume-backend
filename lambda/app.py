import boto3
import json
import hashlib

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("visitor-counter")

def lambda_handler(event, context):
    ip_address = event.get("requestContext", {}).get("http", {}).get("sourceIp", "unknown")
    ip_hash = hashlib.sha256(ip_address.encode()).hexdigest()
    visitor_key = f"visitor-{ip_hash}"

    existing = table.get_item(Key={"pk": visitor_key})
    if "Item" in existing:
        total = table.get_item(Key={"pk": "resume-visits"}).get("Item", {}).get("count", 0)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"visits": int(total)})
        }

    table.put_item(Item={"pk": visitor_key})
    response = table.update_item(
        Key={"pk": "resume-visits"},
        UpdateExpression="ADD #count :inc",
        ExpressionAttributeNames={"#count": "count"},
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW"
    )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        },
        "body": json.dumps({"visits": int(response['Attributes']['count'])})
    }
