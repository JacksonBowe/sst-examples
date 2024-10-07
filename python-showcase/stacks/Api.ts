import { StackContext, Api, use } from "sst/constructs";
import { Function } from "sst/constructs";

import { Storage } from "./Storage";
import { Bus } from "./Bus";

export function API({ stack }: StackContext) {
	const { appTable } = use(Storage);
	const { bus } = use(Bus);

	new Function(stack, "MyFunction", {
		handler: "packages/functions/src/functions/scripts/seed_database.handler",
	});

	const api = new Api(stack, "api", {
		defaults: {
			function: {
				bind: [appTable, bus],
				environment: {
					SST_TABLE_TABLENAME_APPTABLE: appTable.tableName,
					SST_EVENTBUS_EVENTBUSNAME_BUS: bus.eventBusName,
				},
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
