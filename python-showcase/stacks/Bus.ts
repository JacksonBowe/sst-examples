import { StackContext, use, EventBus } from "sst/constructs";

export function Bus({ stack }: StackContext) {
	const bus = new EventBus(stack, "Bus", {});

	bus.subscribe("note.created", {
		handler: "packages/functions/src/functions/events/note_created.handler",
	});

	return {
		bus,
	};
}
