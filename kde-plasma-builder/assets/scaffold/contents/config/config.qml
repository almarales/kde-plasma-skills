import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import org.kde.plasma.plasmoid
import org.kde.kirigami as Kirigami

PlasmoidItem {
    id: root

    // The cfg_ alias is what gives the page its Apply / Discard transaction.
    property alias cfg_label: labelField.text

    Kirigami.FormLayout {
        Kirigami.FormData {
            Kirigami.FormData.label: i18n("Label")
            Kirigami.FormData.delegate: TextField {
                id: labelField
                text: Plasmoid.configuration.label
            }
        }
    }
}
