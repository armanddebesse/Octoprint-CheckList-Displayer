# coding=utf-8
from __future__ import absolute_import
from flask import jsonify

import octoprint.plugin
import octoprint.events

class Checklist_displayerPlugin(octoprint.plugin.AssetPlugin,
                               octoprint.plugin.TemplatePlugin,
                               octoprint.plugin.BlueprintPlugin,
                               octoprint.plugin.EventHandlerPlugin
):
    # Étape 1 : Intercepter l'événement d'impression
    def on_event(self, event, payload):
        if event == "PrintStarted":
            user = payload.get('user')
            if user != "local":
                self._printer.cancel_print()  # Annuler immédiatement l'impression
                # Envoyer un événement à l'interface utilisateur pour afficher la checklist
                self._plugin_manager.send_plugin_message(self._identifier, dict(type="SHOW_CHECKLIST"))

    # Étape 2 : Gérer la confirmation de l'utilisateur
    @octoprint.plugin.BlueprintPlugin.route("/confirm", methods=["POST"])
    def confirm_print(self):
        # Assurez-vous que l'imprimante est prête à imprimer
        if not self._printer.is_ready():
            return jsonify(success=False, reason="Printer is not ready"), 409
        
        # Récupérez le dernier fichier d'impression utilisé
        current_job = self._printer.get_current_job()
        if current_job["file"]["origin"] and current_job["file"]["path"]:
            file_path = current_job["file"]["path"]
            file_origin = current_job["file"]["origin"]

            # Si l'utilisateur confirme, redémarrer l'impression
            self._printer.start_print(file_path, file_origin)

            return jsonify(success=True)
        else:
            return jsonify(success=False, reason="No file to print"), 404

    # Étape 3 : Fournir le JS pour gérer l'affichage de la checklist
    def get_assets(self):
        return dict(js=["js/checklist_displayer.js"])

    # Étape 4 : Fournir le HTML pour la checklist
    def get_template_configs(self):
        return [dict(type="generic", template="checklist.jinja2")]

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            # put your plugin's default settings here
        }

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/checklist_displayer.js"],
            "css": ["css/checklist_displayer.css"],
            "less": ["less/checklist_displayer.less"]
        }

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/master/bundledplugins/softwareupdate.html
        # for details.
        return {
            "checklist_displayer": {
                "displayName": "Checklist_displayer Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "armanddebesse",
                "repo": "OctoPrint-Checklist_displayer",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/armanddebesse/OctoPrint-Checklist_displayer/archive/{target_version}.zip",
            }
        }



__plugin_name__ = "Checklist_displayer Plugin"


__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Checklist_displayerPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
