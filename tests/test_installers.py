import unittest
from unittest.mock import patch, MagicMock
from app.installers.chrome import install_chrome
from app.installers.waydroid import install_waydroid
from app.installers.qemu import install_qemu

class TestChromeInstaller(unittest.TestCase):
    @patch('app.installers.chrome.subprocess.run')
    @patch('app.installers.chrome.os.path.exists')
    def test_install_chrome_already_installed(self, mock_exists, mock_run):
        mock_exists.return_value = True
        result = install_chrome()
        self.assertEqual(result, "Google Chrome is already installed.")
        mock_run.assert_not_called()

    @patch('app.installers.chrome.subprocess.run')
    @patch('app.installers.chrome.os.path.exists')
    def test_install_chrome_success(self, mock_exists, mock_run):
        mock_exists.return_value = False
        mock_run.return_value = MagicMock()
        result = install_chrome()
        self.assertIn("installed successfully", result)

class TestWaydroidInstaller(unittest.TestCase):
    @patch('app.installers.waydroid.subprocess.run')
    @patch('app.installers.waydroid.os.path.exists')
    def test_install_waydroid_already_installed(self, mock_exists, mock_run):
        mock_exists.return_value = True
        result = install_waydroid()
        self.assertEqual(result, "Waydroid is already installed.")

    @patch('app.installers.waydroid.subprocess.run')
    @patch('app.installers.waydroid.os.path.exists')
    def test_install_waydroid_success(self, mock_exists, mock_run):
        mock_exists.return_value = False
        mock_run.return_value = MagicMock()
        result = install_waydroid()
        self.assertIn("Waydroid installed successfully", result)

class TestQEMUInstaller(unittest.TestCase):
    @patch('app.installers.qemu.subprocess.run')
    @patch('app.installers.qemu.os.path.exists')
    def test_install_qemu_already_installed(self, mock_exists, mock_run):
        mock_exists.return_value = True
        result = install_qemu()
        self.assertEqual(result, "QEMU/KVM is already installed.")

    @patch('app.installers.qemu.subprocess.run')
    @patch('app.installers.qemu.os.path.exists')
    def test_install_qemu_success(self, mock_exists, mock_run):
        mock_exists.return_value = False
        mock_run.return_value = MagicMock()
        result = install_qemu()
        self.assertIn("QEMU/KVM with virt-manager installed successfully", result)

if __name__ == '__main__':
    unittest.main()
