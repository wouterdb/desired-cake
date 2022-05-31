"""
    Copyright 2022 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""
from inmanta.resources import resource, PurgeableResource
from inmanta.agent.handler import CRUDHandler, ResourcePurged, HandlerContext, provider
import os
from typing import List

@resource(name="cooking::Bake", id_attribute="action", agent="agent")
class Bake(PurgeableResource):
    fields = ("action",)

@resource(name="cooking::Merge", id_attribute="action", agent="agent")
class Bake(PurgeableResource):
    fields = ("action",)

@resource(name="cooking::Buy", id_attribute="action", agent="agent")
class Bake(PurgeableResource):
    fields = ("action",)

    @staticmethod
    def get_action(exporter, resource):
        return "Koop " + resource.what


@provider(resource_type="cooking::Merge", name="merge")
@provider(resource_type="cooking::Buy", name="buy")
@provider(resource_type="cooking::Bake", name="bake")
class CookHandler(CRUDHandler):

    def read(self) -> List[str]:
        if not os.path.exists("/tmp/recept"):
            return []
        with open("/tmp/recept", "r") as fh:
            return [line.strip() for line in fh.readlines()]

    def write(self, content: List[str]) -> None:
        with open("/tmp/recept", "w") as fh:
            return fh.write("\n".join(content))

    def read_resource(self, ctx: HandlerContext, resource: PurgeableResource) -> None:
        content = self.read()
        if resource.action not in content:
            raise ResourcePurged()

    def create_resource(self, ctx: HandlerContext, resource: PurgeableResource) -> None:
        content = self.read()
        content.append(resource.action.strip())
        self.write(content)

    def delete_resource(self, ctx: HandlerContext, resource: PurgeableResource) -> None:
        content = self.read()
        content.remove(resource.action.strip())
        self.write(content)
