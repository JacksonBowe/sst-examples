import { StackContext, Api } from "sst/constructs";
import { Function } from "sst/constructs";

export function API({ stack }: StackContext) {
	new Function(stack, "MyFunction", {
		handler: "packages/functions/src/functions/scripts/seed_database.handler",
	});

	const api = new Api(stack, "api", {
		defaults: {
			function: {},
		},
		routes: {
			"ANY /{proxy+}": "packages/functions/src/functions/rest/main.handler",
		},
	});

	stack.addOutputs({
		ApiEndpoint: api.url,
	});
}
