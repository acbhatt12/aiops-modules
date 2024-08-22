import * as cdk from "aws-cdk-lib";
import { Annotations, Match, Template } from "aws-cdk-lib/assertions";
import { AmazonBedrockFinetuningStack } from "../lib/bedrock-finetuning-stack";

describe("Bedrock Finetuning Stack", () => {
  const app = new cdk.App();

  const projectName = "mlops";
  const deploymentName = "platform";
  const moduleName = "bedrock-finetuning";
  const removalPolicy = "DESTROY";
  const bedrockBaseModelID = "amazon.titan-text-express-v1:0:8k";
  const vpcId = "vpc-123";
  const subnetIds = ["sub1", "sub2"];
  const account = "123456789";
  const region = "us-east-1";

  const stack = new AmazonBedrockFinetuningStack(
    app,
    `${projectName}-${deploymentName}-${moduleName}`,
    {
      bedrockBaseModelID,
      vpcId,
      subnetIds,
      projectName,
      deploymentName,
      moduleName,
      removalPolicy,
      env: { account, region },
    },
  );

  test("Synth stack", () => {
    const template = Template.fromStack(stack);

    template.hasResource("AWS::Lambda::Function", {});
    template.hasResource("AWS::S3::Bucket", {});
    template.hasResource("AWS::StepFunctions::StateMachine", {});
  });

  test("No CDK Nag Errors", () => {
    const errors = Annotations.fromStack(stack).findError(
      "*",
      Match.stringLikeRegexp("AwsSolutions-.*"),
    );
    expect(errors).toHaveLength(0);
  });

  test("Set provisioned throughput lambda", async () => {
    const mockModel = "test-model";
    const mockEvent = {
      model_id: mockModel,
      model_name: "test",
      model_units: 2
    };
    
    const lambda = await import("../src/lambda-functions/setProvisionedThroughputLambda");
    const response = await lambda.handler(mockEvent, null);
    
    expect(response.statusCode).toBe(200);
    expect(response.body).toContain(mockModel);
  });

  test("Set provisioned throughput lambda invalid input", async () => {
    const mockEvent = {
      model_name: "test",
      model_units: 2  
    };

    const lambda = await import("../src/lambda-functions/setProvisionedThroughputLambda");
    const response = await lambda.handler(mockEvent, null);

    expect(response.statusCode).toBe(400);
    expect(response.body).toContain("model_id is required");
  });

    // Add a rule to trigger provisioned throughput state machine
    // after fine-tuning job completes
});
