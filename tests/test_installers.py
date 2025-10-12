import unittest
from unittest.mock import patch, MagicMock
from app.installers.chrome import install_chrome

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

if __name__ == '__main__':
    unittest.main()
