from dataclasses import dataclass
from typing import Dict

from steamship.base import Client, Request
from steamship.base.response import Response
from steamship.plugin.inputs.training_parameter_plugin_input import TrainingParameterPluginInput
from steamship.plugin.outputs.training_parameter_plugin_output import TrainingParameterPluginOutput


class PluginInstance:
    pass


@dataclass
class CreatePluginInstanceRequest(Request):
    id: str = None
    pluginId: str = None
    pluginHandle: str = None
    pluginVersionId: str = None
    pluginVersionHandle: str = None
    handle: str = None
    upsert: bool = None
    config: Dict[str, any] = None


@dataclass
class DeletePluginInstanceRequest(Request):
    id: str



@dataclass
class PluginInstance:
    client: Client = None
    id: str = None
    handle: str = None
    pluginId: str = None
    pluginVersionId: str = None
    userId: str = None
    config: Dict[str, any] = None
    spaceId: str = None

    @staticmethod
    def from_dict(d: any, client: Client = None) -> "PluginInstance":
        if 'pluginInstance' in d:
            d = d['pluginInstance']

        return PluginInstance(
            client=client,
            id=d.get('id', None),
            handle=d.get('handle', None),
            pluginId=d.get('pluginId', None),
            pluginVersionId=d.get('pluginVersionId', None),
            config=d.get('config', None),
            userId=d.get('userId', None)
        )

    @staticmethod
    def create(
            client: Client,
            pluginId: str = None,
            pluginHandle: str = None,
            pluginVersionId: str = None,
            pluginVersionHandle: str = None,
            handle: str = None,
            upsert: bool = None,
            config: Dict[str, any] = None
    ) -> Response[PluginInstance]:
        req = CreatePluginInstanceRequest(
            handle=handle,
            pluginId=pluginId,
            pluginHandle=pluginHandle,
            pluginVersionId=pluginVersionId,
            pluginVersionHandle=pluginVersionHandle,
            upsert=upsert,
            config=config
        )

        return client.post(
            'plugin/instance/create',
            payload=req,
            expect=PluginInstance
        )

    def delete(self) -> PluginInstance:
        req = DeletePluginInstanceRequest(
            id=self.id
        )
        return self.client.post(
            'plugin/instance/delete',
            payload=req,
            expect=PluginInstance
        )

    def train(self, trainingRequest: TrainingParameterPluginInput) -> PluginInstance:
        return self.client.post(
            'plugin/instance/train',
            payload=trainingRequest,
            expect=PluginInstance
        )

    def getTrainingParameters(self, trainingRequest: TrainingParameterPluginInput) -> PluginInstance:
        return self.client.post(
            'plugin/instance/getTrainingParameters',
            payload=trainingRequest,
            expect=TrainingParameterPluginOutput
        )

@dataclass
class ListPrivatePluginInstancesRequest(Request):
    pass
