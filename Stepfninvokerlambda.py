create lambda fn-> Stepfninvoker -> existing role-stepfnfullaccess -> paste the step fn arn in below code
python code:
import json
import boto3
import uuid

client = boto3.client('stepfunctions')

def lambda_handler(event, context):
	#INPUT -> { "TransactionId": "foo", "Type": "PURCHASE"}
	transactionId = str(uuid.uuid1()) #90a0fce-sfhj45-fdsfsjh4-f23f

	input = {'TransactionId': transactionId, 'Type': 'PURCHASE'}

	response = client.start_execution(
		stateMachineArn='arn:aws:states:us-east-1:016444685310:stateMachine:StepfnSNSDemo',
		name=transactionId,
		input=json.dumps(input)	
		)
        
Create IAM policy to invoke statemachine from lambda:
IAM > Roles > Stepfunctioninvoker-role-veqb1h2i > add perm > create inline policy > 
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": [
				"states:StartExecution"
			],
			"Resource": [
				"arn:aws:states:us-east-1:016444685310:stateMachine:*"
			]
		}
	]
}