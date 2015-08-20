import unittest
import pybald
from pybald.core.controllers import Controller
from pybald.db.models import Model

class TestRegistries(unittest.TestCase):
    def test_controller_registry(self):
        config_obj = dict(env_name="TestFromObject")
        context = pybald.configure(config_object=config_obj)
        class AnotherSampleController(Controller):
            pass
        assert AnotherSampleController in Controller.registry

    def test_model_registry(self):
        config_obj = dict(env_name="TestFromObject")
        context = pybald.configure(config_object=config_obj)
        class AnotherSampleModel(Model):
            pass
        assert AnotherSampleModel in Model.registry

