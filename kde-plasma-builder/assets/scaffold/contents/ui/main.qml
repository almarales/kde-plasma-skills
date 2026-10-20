import QtQuick
import QtQuick.Layouts

import org.kde.plasma.plasmoid
import org.kde.plasma.core as PlasmaCore
import org.kde.plasma.extras as PlasmaExtras
import org.kde.kirigami as Kirigami

PlasmoidItem {
    id: root

    Plasmoid.title: i18n("My Widget")
    Plasmoid.icon: "utilities-system-monitor"

    // The theme frame paints the surface: never paint your own.
    Plasmoid.backgroundHints: PlasmaCore.Types.DefaultBackground
                            | PlasmaCore.Types.ConfigurableBackground

    compactRepresentation: Kirigami.Icon {
        source: Plasmoid.icon
        Accessible.name: Plasmoid.title
        Accessible.role: Accessible.Button

        MouseArea {
            anchors.fill: parent
            onClicked: root.expanded = !root.expanded
        }
    }

    fullRepresentation: PlasmaExtras.Representation {
        Layout.minimumWidth: Kirigami.Units.gridUnit * 18
        Layout.minimumHeight: Kirigami.Units.gridUnit * 12

        ColumnLayout {
            spacing: Kirigami.Units.largeSpacing

            Kirigami.Heading {
                level: 2
                text: Plasmoid.configuration.label
            }
        }
    }
}
