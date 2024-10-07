import { SSTConfig } from "sst";
import { LambdaLayers } from "./stacks/LambdaLayers";
import { Storage } from "./stacks/Storage";
import { API } from "./stacks/Api";
import { Bus } from "./stacks/Bus";

export default {
	config(_input) {
		return {
			name: "python-showcase",
			region: "ap-southeast-2",
		};
	},
	stacks(app) {
		// TODO: Change this when doing production deploy for realsies
		app.setDefaultRemovalPolicy("destroy");

		app.setDefaultFunctionProps({
			// The copyFiles prop is key here. This is what makes everything work when deployed
			copyFiles: [{ from: "packages/core/src", to: "." }],
			runtime: "python3.12",
			python: {
				noDocker: true,
			},
			environment: {},
		});

		app.stack(LambdaLayers).stack(Storage).stack(Bus).stack(API);
	},
} satisfies SSTConfig;
