import { StackContext, Table } from "sst/constructs";

export function Storage({ stack }: StackContext) {
	// Create a DynamoDB table to hold our entities

	const appTable = new Table(stack, "AppTable", {
		fields: {
			PK: "string",
			SK: "string",
			entityType: "string",
		},
		primaryIndex: { partitionKey: "PK", sortKey: "SK" },
		globalIndexes: {
			itemsByType: {
				partitionKey: "entityType",
				sortKey: "PK",
			},
		},
	});

	stack.addOutputs({
		AppTable: appTable.tableName,
	});

	return {
		appTable,
	};
}
