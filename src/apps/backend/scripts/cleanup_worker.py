from modules.cleanup.cleanup_service import CleanupService
from modules.cleanup.types import SearchAccountDeletionRequestParams
from modules.config.config_manager import ConfigManager
from modules.logger.logger import Logger
from modules.logger.logger_manager import LoggerManager


def main() -> None:
    ConfigManager.mount_config()
    LoggerManager.mount_logger()

    account_deletion_requests = CleanupService.get_all_account_deletion_requests()

    if not account_deletion_requests:
        Logger.info(message="No account deletion requests found")
        return

    Logger.info(message=f"Found {len(account_deletion_requests)} account deletion requests")

    cleanup_modules = CleanupService.get_cleanup_modules()

    if not cleanup_modules:
        Logger.info(message="No cleanup modules found")
        return

    Logger.info(message=f"Found {len(cleanup_modules)} cleanup modules")

    main_cleanup_module = next((cleanup_module for cleanup_module in cleanup_modules if cleanup_module.main), None)
    if main_cleanup_module:
        cleanup_modules.remove(main_cleanup_module)
        cleanup_modules.append(main_cleanup_module)

    for account_deletion_request in account_deletion_requests:
        for cleanup_module in cleanup_modules:
            try:
                CleanupService.execute_hook(
                    cleanup_module=cleanup_module, account_deletion_request=account_deletion_request
                )

                Logger.info(
                    message=f"Executed cleanup module: {cleanup_module.module_name} - "
                    f"{cleanup_module.class_name} - {cleanup_module.function_name} "
                    f"for account deletion request: {account_deletion_request.account_id}"
                )

            except Exception as e:
                Logger.error(
                    message=f"Failed to execute cleanup module: {cleanup_module.module_name}."
                    f"{cleanup_module.class_name}.{cleanup_module.function_name} "
                    f"for account deletion request: {account_deletion_request.account_id}"
                    f"\nError: {e}"
                )

            CleanupService.remove_account_deletion_request(
                params=SearchAccountDeletionRequestParams(account_id=account_deletion_request.account_id)
            )
            Logger.info(message=f"Removed account deletion request: {account_deletion_request.account_id}")


if __name__ == "__main__":
    main()
