import QtQuick 2.14
import QtQuick.Controls 2.14



Item {
    property var yellow : '#fff436'
    property var blue : '#2d6ba6'
    property var pink : '#e43167'
    property var footerColor: '#380614'
    property var backgroundColor: '#1F1D1E'
    property var headerColor: '#191819'
    property var ocean: '#243B55'
    id: element
    anchors.fill: parent

    Image {
        id: image0
        anchors.right: parent.right
        anchors.left: parent.left
        clip: false
        fillMode: Image.Stretch
        source: sm.backdrop_path
        height: parent.width * 800 / 1920
        anchors.rightMargin: 0
        anchors.leftMargin: 0

        anchors.bottom: parent.bottom
        anchors.bottomMargin: 50


        Rectangle {
            id: background_body1
            anchors.fill: parent
            gradient: Gradient {
                GradientStop {
                    position: 0
                    color: "#00000000"
                }


                GradientStop {
                    position: 0.76
                    color: "#00000000"
                }

                GradientStop {
                    position: 0.9
                    color: "black"
                }

                GradientStop {
                    position: 1
                    color: "black"
                }
            }
        }

        Item {

            id: infoSuggestion
            x: 0
            y: 50
            height: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 20
            width: gridRect.width
            anchors.left: parent.left
            anchors.leftMargin: gridRect.anchors.leftMargin
            property var infocolor: pink
            Rectangle {
                id: rectangle
                color: "#221f1f"
                anchors.leftMargin: 0
                anchors.right: overview.right
                anchors.bottom: parent.bottom
                anchors.left: overview.left
                anchors.top: parent.top
                anchors.rightMargin: 0
            }

            Text {
                id: popupTitle
                x: 10
                color: infoSuggestion.infocolor
                text: "<b>"+sm.title + ' (' + sm.year + ')' + "</b>"
                anchors.bottom: vote1.top
                anchors.bottomMargin: -8
                font.weight: Font.Normal
                anchors.leftMargin: 10
                wrapMode: Text.WordWrap
                font.pixelSize: 35
                verticalAlignment: Text.AlignBottom
                leftPadding: 0
                padding: 0
                anchors.left: parent.left
                font.wordSpacing: 0
                horizontalAlignment: Text.AlignLeft
                textFormat: Text.AutoText
                anchors.rightMargin: 10
                anchors.right: parent.right
                font.bold: true
                font.capitalization: Font.MixedCase
            }


            Text {
                id: genre1
                color: infoSuggestion.infocolor
                text: "Genre: " +"<b>"+sm.genre+"</b>"
                bottomPadding: 0
                anchors.leftMargin: 3
                wrapMode: Text.WordWrap
                font.pixelSize: 15
                verticalAlignment: Text.AlignVCenter
                leftPadding: 0
                padding: 0
                anchors.top: vote1.top
                anchors.left: vote1.right
                horizontalAlignment: Text.AlignLeft
                topPadding: 0
                textFormat: TextEdit.RichText
                rightPadding: 0
                anchors.rightMargin: 0
                anchors.right: parent.right
                anchors.topMargin: 0
                anchors.bottom: vote1.bottom
                anchors.bottomMargin: 0
            }


            Text {
                id: vote1
                width: 93
                height: 28
                color: infoSuggestion.infocolor
                text: "Vote: <b>" +sm.vote+"</b>"
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                leftPadding: 0
                textFormat: TextEdit.RichText
                anchors.left: overview.left
                padding: 0
                horizontalAlignment: Text.AlignLeft
                font.strikeout: false
                wrapMode: Text.WordWrap
                font.pixelSize: 15
                verticalAlignment: Text.AlignVCenter
                anchors.leftMargin: 0
            }

            Text {
                id: overview
                height: 163
                color: infoSuggestion.infocolor
                text: sm.overview
                visible: false
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                anchors.right: parent.right
                anchors.rightMargin: 0
                leftPadding: 0
                anchors.left: parent.left
                topPadding: 0
                padding: 0
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignLeft
                font.pixelSize: 15
                verticalAlignment: Text.AlignBottom
                anchors.leftMargin: 10
            }

            MouseArea {
                id: suggestArea
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                anchors.bottomMargin: 0
                anchors.top: popupTitle.top
                anchors.right: popupTitle.right
                anchors.bottom: popupTitle.bottom
                anchors.left: popupTitle.left
                anchors.topMargin: 0
                hoverEnabled: true
                focus: true
                cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                onEntered: true ? infoSuggestion.infocolor = 'white' : infoSuggestion.infocolor = pink
                onExited: false ? infoSuggestion.infocolor = 'white' : infoSuggestion.infocolor = pink
                onClicked: {
                    print('click suggest')
                    ldOutside.source = 'movie.qml'
                    window3.movieSignal(sm.title, sm.poster, sm.overview, sm.year, sm.vote, sm.runtime, sm.genre, sm.stars, sm.starsPoster, sm.characters, sm.trailer, sm.backdrop_path, sm.path)

                }
            }

        }

    }



}






/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}D{i:10;anchors_height:75}D{i:8;anchors_height:500;anchors_x:0}
}
##^##*/
