from marshmallow import Schema, class_registry
from abc import ABC, abstractmethod


class TiyaroBase(ABC):
    def __init__(self) -> None:
        self.inputSchema = None
        self.outputSchema = None

    def defInputSchema(self, schemaDict):
        self.inputSchema = Schema.from_dict(schemaDict, name="InputSchema")
        class_registry.register("InputSchema", self.inputSchema)

    def defOutputSchema(self, schemaDict):
        self.outputSchema = Schema.from_dict(schemaDict, name="OutputSchema")
        class_registry.register("OutputSchema", self.outputSchema)

    @abstractmethod
    def declareSchema(self):
        pass

    @abstractmethod
    def setup_model(self, pretrained_file_path):
        pass

    @abstractmethod
    def infer(self, json_input):
        pass