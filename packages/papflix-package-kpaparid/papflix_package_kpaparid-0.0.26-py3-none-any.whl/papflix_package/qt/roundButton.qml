import QtQuick 2.14
import QtQuick.Controls 2.14

    Button {

        property var hov :false
        MouseArea {
            id: mA
            cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
            hoverEnabled: true
            anchors.fill: parent
            onClicked: {
                if(!controlSwitch.checked){
                    if(mode === 'genre'){
                        flag = flag === true ? false : true
                        advancedGenre.text = query

                    }
                    else if(mode === 'sort'){

                        advancedSort.text = query

                    }
                }
            }
            onEntered: hov = true
            onExited: hov = false
        }

        id: control
        contentItem: Text {
            id: textID
            font.bold: true

            color: (flag || hov) && !controlSwitch.checked  ? 'white' : window3.pink
            text: name
            font.pointSize: 9


            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }

        background: Rectangle {
            implicitWidth: textID.width
            implicitHeight: textID.height
            color: (flag || hov) && !controlSwitch.checked  ? window3.pink : 'transparent'
            opacity: (flag || hov) && !controlSwitch.checked  ? 1 : 0.2
            //color: pink

            border.color: window3.pink
            //border.width: 1
            radius: 20

        }
    }

/*##^##
Designer {
    D{i:0;formeditorZoom:4}
}
##^##*/
