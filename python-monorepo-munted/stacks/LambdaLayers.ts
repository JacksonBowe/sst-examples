import { StackContext } from "sst/constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";

export function LambdaLayers({ app, stack }: StackContext) {
	// aws-lambda-powertools -- always recommended
	const powertools = lambda.LayerVersion.fromLayerVersionArn(
		stack,
		"lambda-powertools",
		`arn:aws:lambda:${stack.region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:60`
	);

	// requests -- optional
	const requests = lambda.LayerVersion.fromLayerVersionArn(
		stack,
		"requests",
		`arn:aws:lambda:${stack.region}:770693421928:layer:Klayers-p312-requests:1`
	);

	// pydandic -- from a local folder
	const pydantic = new lambda.LayerVersion(stack, "pydantic", {
		code: lambda.Code.fromAsset("packages/functions/layers/pydantic"),
	});

	app.addDefaultFunctionLayers([powertools, pydantic]);

	return {
		powertools,
		requests,
		pydantic,
	};
}
