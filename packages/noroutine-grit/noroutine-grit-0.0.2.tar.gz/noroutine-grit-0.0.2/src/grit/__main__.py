import pkgutil
import importlib
from typing import Optional

from itertools import product

from pydantic import Field

import yaml
import os

from grit import *
from grit.config import Folder
from grit.variation import Variation
from pydantic_argparse import *


class InspectCommand(BaseModel):
    module: str

    def run(self: str) -> None:
        grit_module = importlib.import_module(self.module)

        print(yaml.dump({
            "name": grit_module.__name__,
            "folders": list(map(lambda m: m.name, pkgutil.iter_modules(grit_module.__path__))),
            "variations": Variation.find_variations_simple(grit_module)
        }, sort_keys=False, indent=2, explicit_start=True))


class PublishCommand(BaseModel):
    module: str
    env: str = Field(description=".env file", default=".env")
    var: Optional[list[str]] = Field(description="variations")

    def run(self) -> None:
        grafana = Grafana(_env_file=self.env)

        grit_module = importlib.import_module(self.module)

        resolutions = {}

        if self.var:
            for var_arg in self.var:
                [k, v] = var_arg.split('=')
                if v == "*":
                    print(f"Wildcard resolutions are not supported with publish command")
                resolutions[k] = v

        Variation.resolve_variations(
            grit_module,
            resolutions=resolutions
        )

        for module in pkgutil.iter_modules(grit_module.__path__):
            folder_module = importlib.import_module(
                f"{grit_module.__name__}.{module.name}")

            # TODO: do we want to place in General folder??, it's a special api
            # if its in root folder, then it makes sense to create it in general folder

            grafana.publish_folder(module.name, module.name)

            for _obj_name in folder_module.__dict__:
                _obj = folder_module.__dict__[_obj_name]
                if isinstance(_obj, Folder):
                    grafana.publish_folder(module.name, _obj.title)

                if isinstance(_obj, Dashboard):
                    grafana.publish_dashboard(folder_uid=module.name, d=_obj)


class GenerateCommand(BaseModel):
    module: str
    var: Optional[list[str]] = Field(description="variations")
    out: str

    def run(self):
        grit_module = importlib.import_module(self.module)

        module_variations = Variation.find_variations_simple(grit_module)
        requested_dict = dict((v, []) for v in module_variations.keys() )
        if self.var:
            for var_arg in self.var:
                [k, v] = var_arg.split('=')
                if k in module_variations:
                    if v == "*":
                        requested_dict[k] = copy.deepcopy(module_variations[k])
                    else:
                        requested_dict[k].append(v)
                else:
                    print(f"Ignoring unknown variation {k}")

        # Remove empty
        requested_dict = {k: v for k, v in requested_dict.items() if len(v) > 0}

        requested_sets = []
        for k, v in requested_dict.items():
            requested_sets.append(list(map(lambda r: (k, r), v)))

        # Here we have finally the desired requested combinations
        requested_combinations = list(map(lambda t: dict(t), list(product(*requested_sets))))

        # Let's roll
        for resolution_combination in requested_combinations:
            # print(resolution_combination)
            resolved_variations = Variation.resolve_variations(
                grit_module,
                resolutions=resolution_combination,
                ignore_missing=True
            )

            resolved_variations_subst = {v.__name__.lower(): r.name for v, r in resolved_variations.items()}

            out_base_dir = self.out.format(module=self.module, **resolved_variations_subst)
            print(f"Generating {out_base_dir}")

            for module in pkgutil.iter_modules(grit_module.__path__):
                folder_module = importlib.import_module(
                    f"{grit_module.__name__}.{module.name}")

                # TODO: do we want to place in General folder??, it's a special api
                # if its in root folder, then it makes sense to create it in general folder

                os.makedirs(f"{out_base_dir}/{module.name}", exist_ok=True)

                for _obj_name in folder_module.__dict__:
                    _obj = folder_module.__dict__[_obj_name]

                    if isinstance(_obj, Dashboard):
                        with open(f"{out_base_dir}/{module.name}/{_obj.uid}.json", "w") as file:
                            file.write(json.dumps(
                                _obj.to_json_data(), sort_keys=True, indent=2, cls=DashboardEncoder))


class Arguments(BaseModel):
    debug: bool = False
    inspect: Optional[InspectCommand] = Field(description="inspect module")
    publish: Optional[PublishCommand] = Field(description="publish to grafana")
    generate: Optional[GenerateCommand] = Field(
        description="generate dashboard json into a folder")


# print(sys.argv[1])
# print(sys.argv[2:])
arg_parser = ArgumentParser(
    model=Arguments,
    prog="Grit",
    description="Grid Toolkit",
    version="0.0.1",
)

# first pass
args = arg_parser.parse_typed_args()

# print(args)
if args.inspect:
    args.inspect.run()

if args.publish:
    args.publish.run()

if args.generate:
    args.generate.run()
