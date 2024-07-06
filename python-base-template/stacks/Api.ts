import { StackContext, Api } from "sst/constructs";

export function API({ stack }: StackContext) {
	const api = new Api(stack, "api", {
		defaults: {
			function: {
				runtime: "python3.12",
			},
		},
		routes: {
			"GET /": "packages/functions/rest/main.handler",
		},
	});

	stack.addOutputs({
		ApiEndpoint: api.url,
	});
}
