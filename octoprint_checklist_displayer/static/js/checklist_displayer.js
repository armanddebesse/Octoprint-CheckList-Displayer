$(function() {
    function Checklist_displayerViewModel(parameters) {
        var self = this;

        self.onStartup = function() {
            $("#validateButton").click(function() {
                console.log('Confirmed')
                $("#dialog_confirm_before_print").modal("hide")
                $.post("/plugin/checklist_displayer/confirm");
            });
        }

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "checklist_displayer") {
                return;
            }

            if (data.type == "SHOW_CHECKLIST") {
                $("#dialog_confirm_before_print").modal("show");
            }
        };

        // self.confirmPrint = function() {
        //     // Si l'utilisateur confirme, informez le serveur
        //     console.log('Confirmed')
        //     $.post("/plugin/confirmbeforeprint/confirm");
        // };
    }

    // Enregistrez le modèle de vue
    ADDITIONAL_VIEWMODELS.push([
        Checklist_displayerViewModel,
        [],
        "#dialog_confirm_before_print"
    ]);
});
