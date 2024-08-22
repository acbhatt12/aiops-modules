import boto3
import json

bedrock = boto3.client('bedrock')

def handler(event, context):
    model_id = event.get('model_id')
    if not model_id:
        return {
            'statusCode': 400,
            'body': json.dumps('model_id is required')
        }
    
    model_name = event.get('model_name', 'my-provisioned-model')
    model_units = event.get('model_units', 1)
    
    try:
        response = bedrock.create_provisioned_model_throughput(
            ModelId=model_id,
            ProvisionedModelName=model_name,
            ModelUnits=model_units
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Provisioned {model_units} units for {model_name} ({model_id})')
        }
        
    except bedrock.exceptions.ResourceNotFoundException:
        return {
            'statusCode': 404,
            'body': json.dumps(f'Model {model_id} not found')
        }
        
    except bedrock.exceptions.ValidationException as e:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Validation error: {e}')
        }
        
    except bedrock.exceptions.AccessDeniedException as e:
        return {
            'statusCode': 403, 
            'body': json.dumps(f'Access denied: {e}')
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
