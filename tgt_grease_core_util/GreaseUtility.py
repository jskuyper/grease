import Logging
import Telemetry


class Grease:
    def __init__(self):
        self._logger = Logging.Logger()

    def __del__(self):
        self._logger.__del__()

    def message(self):
        # type: () -> Logging.Logger
        return self._logger

    @staticmethod
    def run_telemetry(command_obj, run_success, is_daemon=False):
        # type: (tgt_grease_core.GreaseCommand, bool, bool) -> None
        telemetry = Telemetry.Database(command_obj, is_daemon)
        return telemetry.store_result(run_success)

    @staticmethod
    def run_daemon_telemetry(command_obj):
        # type: (tgt_grease_daemon.GreaseDaemonCommand) -> None
        telemetry = Telemetry.DatabaseDaemon(command_obj)
        return telemetry.store_result()
