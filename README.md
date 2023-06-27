# ConfirmBeforePrintPlugin for OctoPrint

This is a plugin for OctoPrint that adds a feature to show a checklist that the user must accept before they can print. The print operation will be canceled and the checklist will be shown whenever a print job is started, but only for non-local users.

## Requirements

* Python 3.6+
* OctoPrint 1.4.0+

## Installation

To install this plugin, follow these steps:

1. Clone this repository or download the ZIP file and extract it.
2. Navigate to the plugin directory in the terminal.
3. Run the following command to package the plugin:

    ```bash
    python setup.py sdist
    ```

    This will create a .tar.gz file in a new `dist/` directory.

4. Now, go to your OctoPrint interface. Click the wrench icon in the top right to open the settings, and then navigate to the Plugin Manager.
5. In the Plugin Manager, click on the "Get More..." button, then click on "From File". Navigate to your .tar.gz file and install it.
6. After the plugin has been installed, restart your OctoPrint instance. The new plugin should now be active.

## Usage

Once the plugin has been installed, it should work automatically. Whenever a print job is started by a non-local user, the print operation will be immediately canceled and a checklist will appear that the user must accept before the print job can continue.

## Testing

To test the plugin:

1. Start a print job as a non-local user.
2. The print job should be immediately canceled and a checklist should appear.
3. Accept the checklist.
4. The print job should restart.

If you encounter any issues, please check the OctoPrint logs in the "Logging" section under "Settings". You may also want to enable "Safe Mode" under "Settings" > "Server" > "Enable safe mode" to ensure that only essential plugins and your test plugin are enabled.

## Development

For development, you can clone this repository and install the plugin in your local OctoPrint environment:

```bash
source venv/bin/activate
pip install .
```

Then, you can start OctoPrint with the command `octoprint serve`. Any changes made to the plugin files will require a restart of OctoPrint.