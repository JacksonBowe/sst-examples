import { SSTConfig } from "sst";
import { API } from "./stacks/Api";

export default {
	config(_input) {
		return {
			name: "python-uv",
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
