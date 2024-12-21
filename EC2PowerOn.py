import boto3

def lambda_handler(event, context):
    # 直接指定 EC2 实例 ID
    instance_id = "i-08a18c4efc432f811"
    
    # 初始化 EC2 客户端
    ec2 = boto3.client("ec2")
    
    try:
        # 检查实例是否存在并获取状态
        response = ec2.describe_instances(InstanceIds=[instance_id])
        instances = response.get("Reservations", [])
        
        if not instances:
            return {
                "statusCode": 404,
                "body": f"Error: EC2 instance with ID {instance_id} not found."
            }
        
        # 获取实例状态
        state = instances[0]["Instances"][0]["State"]["Name"]
        if state == "running":
            return {
                "statusCode": 200,
                "body": f"Instance {instance_id} is already running."
            }
        
        # 启动实例
        ec2.start_instances(InstanceIds=[instance_id])
        return {
            "statusCode": 200,
            "body": f"Successfully started EC2 instance {instance_id}."
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
