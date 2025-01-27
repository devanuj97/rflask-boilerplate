from modules.cleanup.internal.cleanup_manager import CleanupManager
from tests.modules.cleanup.base_test_cleanup import BaseTestCleanup


class TestCleanupManager(BaseTestCleanup):
    def setUp(self):
        """Setup for CleanupManager tests."""
        self.cleanup_manager = CleanupManager()

    def test_register_hook(self):
        """Test registering a regular cleanup hook."""

        def dummy_hook(params):
            pass

        self.cleanup_manager.register_hook(dummy_hook)
        self.assertIn(dummy_hook, self.cleanup_manager.cleanup_hooks)

    def test_register_final_hook(self):
        """Test registering a final cleanup hook."""

        def dummy_final_hook(params):
            pass

        self.cleanup_manager.register_hook(dummy_final_hook, final=True)
        self.assertEqual(self.cleanup_manager.final_hook, dummy_final_hook)

    def test_execute_hooks(self):
        """Test executing hooks in parallel."""
        executed_hooks = []

        def dummy_hook_1(params):
            executed_hooks.append("hook_1")

        def dummy_hook_2(params):
            executed_hooks.append("hook_2")

        self.cleanup_manager.register_hook(dummy_hook_1)
        self.cleanup_manager.register_hook(dummy_hook_2)

        self.cleanup_manager.execute_hooks(params=self.params)

        self.assertIn("hook_1", executed_hooks)
        self.assertIn("hook_2", executed_hooks)

    def test_execute_final_hook(self):
        """Test executing the final hook after other hooks."""

        def dummy_final_hook(params):
            pass

        self.cleanup_manager.register_hook(dummy_final_hook, final=True)
        self.cleanup_manager.execute_hooks(params=self.params)

    def test_failing_hook(self):
        """Test a failing cleanup hook."""
        executed_hooks = []

        def dummy_hook_1(params):
            executed_hooks.append("hook_1")

        def dummy_failing_hook(params):
            _ = 1 / 0
            executed_hooks.append("failing_hook")

        def dummy_final_hook(params):
            executed_hooks.append("final_hook")

        self.cleanup_manager.register_hook(dummy_hook_1)
        self.cleanup_manager.register_hook(dummy_failing_hook)
        self.cleanup_manager.register_hook(dummy_final_hook, final=True)

        self.cleanup_manager.execute_hooks(params=self.params)

        self.assertIn("hook_1", executed_hooks)
        self.assertIn("final_hook", executed_hooks)
