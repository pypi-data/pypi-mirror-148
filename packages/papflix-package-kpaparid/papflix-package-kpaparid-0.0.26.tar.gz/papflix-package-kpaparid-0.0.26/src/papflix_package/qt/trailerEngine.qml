import QtQuick 2.14
import QtQuick.Controls 2.14
import QtWebEngine 1.10


Item
{
    id: trailerWindow
    //color: 'black'
    visible: true
    anchors.fill: parent

    MouseArea{
        anchors.fill: parent
        onClicked: trailerWindow.destroy()
    }
    Rectangle{
        id: rectangle
        anchors.fill: parent
        opacity: 0.5
        color: 'black'

    }
    BusyIndicator {
        id: control
        anchors.top: parent.verticalCenter
        anchors.topMargin: -38
        anchors.left: parent.horizontalCenter
        anchors.leftMargin: -38
        running: false

        contentItem: Item {
            implicitWidth: 64
            implicitHeight: 64

            Item {
                id: item2
                x: parent.width / 2 - 32
                y: parent.height / 2 - 32
                width: 64
                height: 64
                opacity: control.running ? 1 : 0

                Behavior on opacity {
                    OpacityAnimator {
                        duration: 250
                    }
                }

                RotationAnimator {
                    target: item2
                    running: control.visible && control.running
                    from: 0
                    to: 360
                    loops: Animation.Infinite
                    duration: 1250
                }

                Repeater {
                    id: repeater
                    model: 6

                    Rectangle {
                        x: item2.width / 2 - width / 2
                        y: item2.height / 2 - height / 2
                        implicitWidth: 15
                        implicitHeight: 15
                        radius: 10
                        color: pink
                        transform: [
                            Translate {
                                y: -Math.min(item2.width, item2.height) * 0.5 + 5
                            },
                            Rotation {
                                angle: index / repeater.count * 360
                                origin.x: 5
                                origin.y: 5
                            }
                        ]
                    }
                }
            }
        }
    }
    //Keys.onEscapePressed: console.log("move left")
    WebEngineView {
        id: engine
        width: 854
        height: 480
        visible: false
        property bool previousS
        focus: true
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        settings.playbackRequiresUserGesture: false
        url: "https://www.youtube.com/embed/" + movieItem.trailer + "?autoplay=1"

        onLoadingChanged: {

            if(loadRequest.status === 2){
                print('url:',url)
                control.running = false
                visible = true

            }
            if(loadRequest.status === 0){
                control.running = true
            }

        }


        onFullScreenRequested: function(request) {
                    if (request.toggleOn){
                        print('ws',window3.visibility)
                        previousS = window3.visibility === 5 ? true:false
                        anchors.fill = trailerWindow
                        focus = true
                        clip = true
                        window3.showFullScreen()
                        titleRect.visible = false

                    }
                    else{

                        if(!previousS) window3.showNormal()
                        focus = false
                        anchors.fill = undefined
                        anchors.horizontalCenter = trailerWindow.horizontalCenter
                        anchors.verticalCenter = trailerWindow.verticalCenter
                        width = 854
                        height = 480
                        titleRect.visible = true
                        print('kleinw re')
                    }
                    request.accept()
        }
        Action {
                shortcut: "Escape"
                onTriggered: {
                    console.log("Escape pressed.");
                    if(!engine.previousS) window3.showNormal()
                    print('ws',window3.visibility)
                    if(engine.isFullScreen){
                        engine.fullScreenCancelled()
                        titleRect.visible = true
                    }
                    else{
                        trailerWindow.destroy()
                    }
                }
            }




    }

    //webEngineID.url = "https://www.youtube.com/embed/" + movieItem.trailer + "?autoplay=1"
    //   eng.url = "https://www.youtube.com/embed/" + movieItem.trailer + "?autoplay=1"
}






/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
