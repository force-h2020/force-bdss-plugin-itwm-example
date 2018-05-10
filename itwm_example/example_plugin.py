from force_bdss.api import BaseExtensionPlugin, plugin_id
from itwm_example.csv_writer.csv_writer_factory import CSVWriterFactory
from itwm_example.fixed_value_data_source.fixed_value_data_source_factory \
    import \
    FixedValueDataSourceFactory


class ExamplePlugin(BaseExtensionPlugin):
    id = plugin_id("itwm", "example")

    def _data_source_factories_default(self):
        return [FixedValueDataSourceFactory(self)]

    def _mco_factories_default(self):
        return []

    def _notification_listener_factories_default(self):
        return [CSVWriterFactory(self)]

    def _ui_hooks_factories_default(self):
        return []
