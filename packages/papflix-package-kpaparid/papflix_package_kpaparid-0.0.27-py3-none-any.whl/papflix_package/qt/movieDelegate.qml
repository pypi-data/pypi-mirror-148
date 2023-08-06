import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14


Item {

    height: 200
    id: column
    x: 10
    width: gridView.cellWidth  - 20


    Column {
        id: column1
        anchors.fill: parent


        Item {
            id: element1
            visible: true


            Image {
                id: image
                width: column.width
                height: 200

                layer.textureMirroring: ShaderEffectSource.NoMirroring
                layer.mipmap: false
                layer.enabled: false
                opacity: 1
                clip: false
                source: hm.poster

                fillMode: Image.Stretch
                //sourceSize.width: 129
                //sourceSize.height: 194
                //fillMode: Image.PreserveAspectFit
                smooth: true
                mipmap: true
                antialiasing: true

                Rectangle {
                    id: rectangle
                    anchors.bottomMargin: -2
                    anchors.rightMargin: -2
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.top: parent.top
                    anchors.leftMargin: -2
                    visible: true
                    gradient: Gradient {
                        GradientStop {
                            position: 0
                            color: "#00ffffff"
                        }
                        GradientStop {
                            position: 0.8
                            color: "#00ffffff"
                        }

                        GradientStop {
                            position:0.95
                            color: "#000000"
                        }
                        GradientStop {
                            position: 1
                            color: "#000000"
                        }




                    }
                    clip: false

                    border.width: 0
                }

                MouseArea {

                    id: mouseArea
                    hoverEnabled: true
                    property var iconArea: false
                    anchors.fill: parent
                    cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                    onEntered: {
                        if(containsMouse){
                            if(popup.closed){
                                //console.log('open1 '+hm.movieName)
                                popup.open()
                            }
                        }
                    }
                    onExited: {
                        if(popup.opened){

                                //console.log('close')
                                popup.close()

                    }
                }
            }


            Text {
                font { pointSize: 11; weight: Font.Normal; capitalization: Font.MixedCase }
                id: element
                y: 180
                height: 51
                //color: window.pink
                color: "white"
                text: hm.title
                anchors.left: parent.left
                anchors.leftMargin: 0
                anchors.right: parent.right
                anchors.rightMargin: 0
                font.bold: true
                bottomPadding: 5
                style: Text.Outline
                fontSizeMode: Text.Fit
                wrapMode: Text.WordWrap
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }

    Popup {
        id: popup
        y: -100
        spacing: 0
        rightPadding: 0
        padding: 1
        margins: 0
        bottomPadding: 0
        leftPadding: 0
        topPadding: 0
        rightMargin: 0
        bottomMargin: 0
        leftMargin: 0
        topMargin: 0
        onOpened: {
            var distance = mapFromItem(window, 0, 0)
            // console.log('distance' + distance.x)
            // console.log('window3.width' + window3.width)

            x = window3.width + distance.x
            if(x<=550){
                popup.x = -390
            }
            else{
                popup.x = 150
            }
        }
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent
        Loader{
            id: loader
            active: true
            source: "popupwindow.qml"
            property var exit: true
        }

    }


    Connections {
        target: mouseArea
        function onClicked(){
            print(titleRect.height)
            titleRect.height = 0
            header.visible = false
            ldOutside.source = 'movie.qml'
            window3.movieSignal(hm.title, hm.poster, hm.overview, hm.year, hm.vote, hm.runtime, hm.genre, hm.stars, hm.starsPoster, hm.characters, hm.trailer, hm.backdrop_path, hm.path)
        }
    }



}
}








