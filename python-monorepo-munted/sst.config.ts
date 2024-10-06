import { SSTConfig } from "sst";
import { LambdaLayers } from "./stacks/LambdaLayers";
import { API } from "./stacks/Api";

import path from "path";

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
			environment: {
				// ...(app.local && {
				// 	PYTHONPATH: [path.resolve("./packages")].join(";"),
				// }),
			},
		});

		app.stack(API);
	},
} satisfies SSTConfig;
