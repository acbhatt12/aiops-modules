import boto3
import json
import os

# Initialize the Bedrock client
bedrock = boto3.client('bedrock')


def lambda_handler(event, context):
    
    # Get the custom model identifier from the event
    model_identifier = event["model_identifier"]
    
    if not model_identifier:
        return {
            'statusCode': 400,
            'body': json.dumps('model_identifier is required in the event payload')
        }
    
    # Get the desired throughput from the event or use a default value
    modelName = event["provisionedModelName"]
    modelUnits = event["modelUnits"]
    
    try:

        # response = client.create_provisioned_model_throughput(
        #     clientRequestToken='string',
        #     modelUnits=123,
        #     provisionedModelName='string',
        #     modelId='string',
        #     commitmentDuration='OneMonth'|'SixMonths',
        #     tags=[
        #         {
        #             'key': 'string',
        #             'value': 'string'
        #         },
        #     ]
        # )

        # Create or update provisioned throughput for the model
        response = bedrock.create_provisioned_model_throughput(
            modelId = model_identifier,
            provisionedModelName = modelName,
            modelUnits = modelUnits
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'Provisioned throughput for custom model {model_identifier} has been set to {desired_throughput}')
        }
    
    except bedrock.exceptions.ResourceNotFoundException:
        return {
            'statusCode': 404,
            'body': json.dumps(f'Custom model {model_identifier} not found')
        }
    except bedrock.exceptions.ValidationException as ve:
        return {
            'statusCode': 400,
            'body': json.dumps(f'Validation error: {str(ve)}')
        }
    except bedrock.exceptions.AccessDeniedException as ae:
        return {
            'statusCode': 403,
            'body': json.dumps(f'Access denied: {str(ae)}')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }