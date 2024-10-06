import { SSTConfig } from "sst";
import { LambdaLayers } from "./stacks/LambdaLayers";
import { API } from "./stacks/Api";

export default {
	config(_input) {
		return {
			name: "python-mono",
			region: "ap-southeast-2",
		};
	},
	stacks(app) {
		app.setDefaultFunctionProps({
			copyFiles: [{ from: "packages/core/src", to: "." }],
			runtime: "python3.12",
			python: {
				noDocker: true,
			},
			environment: {},
		});

		app.stack(LambdaLayers).stack(API);
	},
} satisfies SSTConfig;
