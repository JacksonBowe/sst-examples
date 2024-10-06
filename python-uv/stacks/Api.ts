import { StackContext, Api } from "sst/constructs";
import { Function } from "sst/constructs";

export function API({ stack }: StackContext) {
	new Function(stack, "MyFunction", {
		handler: "packages/functions/src/functions/main.handler",
	});

	const api = new Api(stack, "api", {
		defaults: {
			function: {},
		},
		routes: {
			$default: "packages/functions/src/functions/main.handler",
		},
	});

	// stack.addOutputs({
	// 	ApiEndpoint: api.url,
	// });
}
