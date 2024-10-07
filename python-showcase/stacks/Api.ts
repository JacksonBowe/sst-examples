import { StackContext, Api, use } from "sst/constructs";
import { Function } from "sst/constructs";

import { Storage } from "./Storage";

export function API({ stack }: StackContext) {
	const { appTable } = use(Storage);

	new Function(stack, "MyFunction", {
		handler: "packages/functions/src/functions/scripts/seed_database.handler",
	});

	const api = new Api(stack, "api", {
		defaults: {
			function: {
				bind: [appTable],
			},
		},
		routes: {
			"ANY /{proxy+}": "packages/functions/src/functions/rest/main.handler",
		},
	});

	stack.addOutputs({
		ApiEndpoint: api.url,
	});
}
