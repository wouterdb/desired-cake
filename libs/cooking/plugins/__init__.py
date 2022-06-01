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
from inmanta.plugins import plugin
from inmanta.resources import resource, PurgeableResource
from inmanta.agent.handler import CRUDHandler, ResourcePurged, HandlerContext, provider
import os
import time
from typing import List

@resource(name="cooking::Do", id_attribute="action", agent="agent")
class Bake(PurgeableResource):
    fields = ("action", )

    @staticmethod
    def get_action(exporter, resource):
         return str(resource.idx) + " " + resource.action


@resource(name="cooking::Buy", id_attribute="action", agent="agent")
class Buy(PurgeableResource):
    fields = ("action", )

    @staticmethod
    def get_action(exporter, resource):
        return str(resource.idx) + " Koop " + resource.what


@provider(resource_type="cooking::Do", name="do")
@provider(resource_type="cooking::Buy", name="buy")
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

@plugin
def get_idx(me: "cooking::Step") -> "int":
    def get_idx(val):
        if hasattr(val, "idx"):
            return val.idx
        return 0

    return max((get_idx(i) for i in me.requires), default=0)+1
