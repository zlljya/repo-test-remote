import boto3

def lambda_handler(event, context):
    # 初始化 EC2 客户端
    ec2 = boto3.client('ec2')
    
    try:
        # 描述所有实例信息
        response = ec2.describe_instances()
        instances = response.get('Reservations', [])
        
        # 用于存储实例状态的列表
        instance_states = []
        
        for reservation in instances:
            for instance in reservation.get('Instances', []):
                instance_id = instance['InstanceId']
                state = instance['State']['Name']  # 获取实例状态
                instance_states.append({
                    "InstanceId": instance_id,
                    "State": state
                })
        
        # 返回所有实例状态
        return {
            "statusCode": 200,
            "body": instance_states
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }
