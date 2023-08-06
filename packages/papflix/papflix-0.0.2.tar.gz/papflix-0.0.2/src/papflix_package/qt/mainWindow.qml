import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14
import QtQuick.Controls.Material 2.1

ApplicationWindow {
    id: window3

    title: qsTr("Hello Kostas")


    width: 1600
    height: 900
    property var ratioW: width / 1600
    color: 'black'
    property var maxed: false
    property var yellow : '#fff436'
    property var blue : '#2d6ba6'
    property var pink : '#e43167'
    property var footerColor: '#380614'
    property var backgroundColor: '#1F1D1E'
    property var headerColor: '#191819'
    property var ocean: '#243B55'

    property var fontColor: pink
    property var black: '#110206'
    property var blackblack: '#060102'

    property var rightBinding
    //    visibility: "FullScreen"

//    minimumWidth: 1370
    minimumWidth: 1050
    minimumHeight: 850
    visible: true
    visibility: "Windowed"
    onVisibilityChanged: {
//        print('height ', window3.screen.height)
//        print('height wi ', window3.height)
//        print('visibility after ', window3.visibility)

    }




    flags:  Qt.FramelessWindowHint |
            Qt.WindowMinimizeButtonHint |
            Qt.Window
    property int previousX
    property int previousY
    property int previousW
    property int previousH


    Loader{
        id:ldOutside;
        clip: false
        anchors.top: titleRect.bottom
        anchors.topMargin: 0
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        source: 'home.qml'

    }

    Rectangle {
        id: titleRect
        width: parent.width
        height: 65
        color: "transparent"
        anchors.topMargin: 0
        border.width: 0
        visible: true

        anchors.top: parent.top

        Rectangle {
            id: header
            color: "#000000"
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            clip: false
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0
            anchors.top: parent.top
            anchors.topMargin: 0
            gradient: Gradient {
                GradientStop {
                    position: 0
                    color: footerColor            }
                GradientStop {
                    position: 0.2
                    color: footerColor            }

                GradientStop {
                    position: 1
                    color: 'black'
                }

                GradientStop {
                    position: 1
                    color: 'black'
                }
            }
            MouseArea {
                id: mouseArea1
                anchors.fill: parent

                onPressed: {
                    if (window3.visibility !== 4 & window3.visibility !== 5){
                        previousX = mouseX
                        previousY = mouseY
                    }
                }

                onMouseXChanged: {
                    if (window3.visibility !== 4 & window3.visibility !== 5){
                    var dx = mouseX - previousX
                    window3.setX(window3.x + dx)}
                }

                onMouseYChanged: {
                    if (window3.visibility !== 4 & window3.visibility !== 5){
                    var dy = mouseY - previousY
                    window3.setY(window3.y + dy)}
                }
                onDoubleClicked: {
                    if (window3.visibility === 4 || window3.visibility === 5) {

                        window3.showNormal()
                        previousX = mouseX - (screen.width - window3.width)/2
                        previousY = mouseY - (screen.height - window3.height)/2
                    }
                    else {
                        window3.showMaximized()
                        window3.setGeometry(screen.virtualX, 0,screen.width, screen.desktopAvailableHeight)
                    }
                }

                Rectangle {
                    id: logo
                    x: 5
                    width: 340
                    color: pink
                    anchors.top: parent.top
                    anchors.topMargin: 10
                    clip: false
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 10
                    anchors.left: parent.left
                    anchors.leftMargin:   window3.width - window3.rightBinding+5
                    MouseArea
                    {
                        cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                        hoverEnabled: true
                        anchors.fill: parent
                        onClicked: {
                            ldOutside.source = 'home.qml'
                            MyApp.onComp("Home")
                            console.log('click')
                        }
                    }

                    Text {
                        id: element1
                        text: qsTr("PAPFLIX")
                        anchors.topMargin: 5
                        anchors.bottomMargin: 5
                        anchors.fill: parent
                        font.bold: true
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        font.pixelSize: 45
                    }


                }

                Item{
                    id: element
                    width: 0
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 10
                    anchors.top: logo.top
                    anchors.topMargin: 0
                    anchors.left: parent.left
                    anchors.leftMargin: {
                        if(rightBinding > rectmini.x){
                            return window3.rightBinding - width - rectmini.width - rextmax.width - xclose.width - 40
                        }

                        return window3.rightBinding - width
                    }

                    Rectangle {
                        id: search
                        x: 0
                        y: 15
                        width: 200
                        height: 30
                        color: "#00000000"
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        anchors.rightMargin: 0
                        border.color: pink
                        border.width: 0


                        TextField {
                            id: textField
                            color: pink
                            font.pointSize: 10
                            onHoveredChanged: hovered ? search.border.width = 2 : search.border.width = 0
                            placeholderText: qsTr("Enter keywords here")
                            font.bold: true
                            anchors.fill: parent
                            placeholderTextColor: pink
                            onAccepted: {
                                ldOutside.source = 'main.qml'
                                print('search with enter')
                                MyApp.onSearch(text)
                            }

                            background: Rectangle {
                                color: pink
                                opacity: 0.2
                                implicitWidth: 200
                                implicitHeight: 40
                            }
                        }


                        Image {
                            id: searchImage
                            x: 165
                            width: 16
                            source: "../resources/search.png"
                            anchors.topMargin: 7
                            sourceSize.width: 25
                            anchors.top: parent.top
                            fillMode: Image.Stretch
                            anchors.bottomMargin: 7
                            anchors.rightMargin: 5
                            anchors.bottom: parent.bottom
                            anchors.right: parent.right
                            sourceSize.height: 25
                        }
                        MouseArea {
                            id: mouseAreaInput
                            anchors.rightMargin: 0
                            anchors.leftMargin: 0
                            anchors.bottomMargin: 0
                            anchors.top: searchImage.top
                            anchors.right: searchImage.right
                            anchors.bottom: searchImage.bottom
                            anchors.left: searchImage.left
                            anchors.topMargin: 0
                            hoverEnabled: true
                            onEntered: print('enter')
                            onExited: print('exit')
                            onClicked: {
                                ldOutside.source = 'main.qml'
                                MyApp.onSearch(textField.text)
                            }
                            cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                        }
                    }

                    Button {
                        id: tvbtn
                        width: 0
                        height: 30
                        text: qsTr("Tv-Series")
                        visible: false
                        anchors.right: filterbtn.left
                        anchors.rightMargin: 0
                        anchors.top: search.top
                        anchors.topMargin: 0
                        anchors.bottom: search.bottom
                        anchors.bottomMargin: 0
                        MouseArea {
                            cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                            hoverEnabled: true
                            anchors.fill: parent
                            onEntered: {
                                tvbtntext.color = 'white'
                                tvbtnrect.opacity = 1
                            }
                            onExited :{
                                tvbtntext.color = pink
                                tvbtnrect.opacity = 0.2

                            }
                            onClicked:popup2.open()
                        }

                        contentItem: Text {
                            id: tvbtntext
                            text: tvbtn.text
                            font.bold: true
                            font.pixelSize: 11
                            opacity: enabled ? 1.0 : 0.2
                            color: tvbtn.down ? "white" : pink
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            elide: Text.ElideRight

                        }

                        background: Rectangle {
                            id: tvbtnrect
                            implicitWidth: 100
                            implicitHeight: 40
                            color: pink
                            opacity: tvbtn.down ? 1 : 0.2
                            border.color: pink
                            border.width: 1
                            radius: 2

                        }

                    }

                    Button {
                        id: genrebtn
                        width: 0
                        height: 30
                        text: qsTr("Genres")
                        visible: false
                        enabled: true
                        anchors.bottom: search.bottom
                        anchors.right: moviebtn.left
                        anchors.top: search.top
                        MouseArea {
                            cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                            hoverEnabled: true
                            anchors.fill: parent
                            onEntered: {
                                genretext.color = 'white'
                                genrerect.opacity = 1
                            }
                            onExited :{
                                genretext.color = pink
                                genrerect.opacity = 0.2

                            }
                            onClicked:popup2.open()
                        }

                        background: Rectangle {
                            id: genrerect
                            color: pink
                            radius: 2
                            implicitWidth: 100
                            implicitHeight: 40
                            border.width: 1
                            border.color: pink
                            opacity: genrebtn.down ? 1 : 0.2
                        }
                        contentItem: Text {
                            id: genretext
                            color: genrebtn.down ? "white" : pink
                            text: genrebtn.text
                            verticalAlignment: Text.AlignVCenter
                            elide: Text.ElideRight
                            font.pixelSize: 11
                            horizontalAlignment: Text.AlignHCenter
                            font.bold: true
                            opacity: enabled ? 1.0 : 0.2
                        }
                        anchors.topMargin: 0
                        anchors.rightMargin: 0
                        anchors.bottomMargin: 0
                    }

                    Button {
                        id: moviebtn
                        text: qsTr("Movies")
                        anchors.bottom: search.bottom
                        anchors.right: tvbtn.left
                        anchors.top: search.top

                        MouseArea
                        {
                            cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                            id: mouseArea
                            hoverEnabled: true
                            anchors.fill: parent
                            onEntered: {
                                movietext.color = 'white'
                                movierect.opacity = 1
                            }
                            onExited :{
                                movietext.color = pink
                                movierect.opacity = 0.2

                            }
                            onClicked: {
                                ldOutside.source = 'main.qml'
                                MyApp.onComp("Main")
                                console.log('click')
                            }
                        }

                        background: Rectangle {
                            id: movierect
                            color: pink
                            radius: 2
                            implicitWidth: 100
                            implicitHeight: 40
                            border.width: 1
                            border.color: pink
                            opacity: moviebtn.down ? 1 : 0.2
                        }
                        contentItem: Text {
                            id: movietext
                            color: moviebtn.down ? "white" : pink
                            text: moviebtn.text
                            font.pointSize: 10
                            verticalAlignment: Text.AlignVCenter
                            elide: Text.ElideRight
                            horizontalAlignment: Text.AlignHCenter
                            font.bold: true
                            opacity: enabled ? 1.0 : 0.2
                        }
                        anchors.topMargin: 0
                        anchors.rightMargin: 10
                        anchors.bottomMargin: 0
                    }


                    Button {
                        id: homebtn
                        text: qsTr("Home")
                        anchors.bottom: search.bottom
                        anchors.right: genrebtn.left
                        anchors.top: search.top

                        MouseArea {
                            cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                            hoverEnabled: true
                            anchors.fill: parent
                            onEntered: {
                                hometext.color = 'white'
                                homerect.opacity = 1
                            }
                            onExited :{
                                hometext.color = pink
                                homerect.opacity = 0.2

                            }
                            onClicked: {
                                ldOutside.source = 'home.qml'
                                MyApp.onComp("Home")
                                console.log('click')
                            }
                        }


                        background: Rectangle {
                            id: homerect
                            color: pink
                            radius: 2
                            implicitWidth: 100
                            implicitHeight: 40
                            border.width: 1
                            border.color: pink
                            opacity: homebtn.down ? 1 : 0.2
                        }
                        contentItem: Text {
                            id: hometext
                            color: homebtn.down ? "white" : pink
                            text: homebtn.text
                            font.pointSize: 10
                            verticalAlignment: Text.AlignVCenter
                            elide: Text.ElideRight
                            horizontalAlignment: Text.AlignHCenter
                            font.bold: true
                            opacity: enabled ? 1.0 : 0.2
                        }
                        anchors.topMargin: 0
                        anchors.rightMargin: 10
                        anchors.bottomMargin: 0
                    }
                    Button {
                        id: filterbtn
                        text: qsTr("Filter")
                        anchors.bottom: search.bottom
                        anchors.right: search.left
                        anchors.top: search.top
                        MouseArea {
                            cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                            hoverEnabled: true
                            anchors.fill: parent
                            onEntered: {
                                filtertext.color = 'white'
                                filterrect.opacity = 1
                                filterIcon.opacity = 0
                            }
                            onExited :{
                                filtertext.color = pink
                                filterrect.opacity = 0.2
                                filterIcon.opacity = 1

                            }
                            onClicked:

                                popup2.open()
                        }


                        Image {
                            id: filterIcon
                            width: 18
                            anchors.bottom: filterrect.bottom
                            anchors.bottomMargin: 7
                            anchors.top: filterrect.top
                            anchors.topMargin: 7
                            anchors.left: filtertext.left
                            anchors.leftMargin: 3
                            source: "../resources/filter.png"
                        }
                        background: Rectangle {
                            id: filterrect
                            color: pink
                            radius: 2
                            implicitWidth: 100
                            implicitHeight: 40
                            border.width: 1
                            border.color: pink
                            opacity: homebtn.down ? 1 : 0.2
                        }
                        contentItem:

                            Text {
                            id: filtertext
                            color: filterbtn.down ? "white" : pink
                            text: filterbtn.text
                            font.pointSize: 10
                            verticalAlignment: Text.AlignVCenter
                            elide: Text.ElideRight
                            horizontalAlignment: Text.AlignHCenter
                            font.bold: true
                            opacity: enabled ? 1.0 : 0.2
                        }
                        anchors.topMargin: 0
                        anchors.rightMargin: 10
                        anchors.bottomMargin: 0
                    }

                    //            Button {
                    //                id: filter
                    //                x: -130
                    //                y: 85
                    //                width: 130
                    //                height: 40
                    //                text: qsTr("FILTER")
                    //                anchors.bottom: search.bottom
                    //                anchors.bottomMargin: 0
                    //                anchors.top: search.top
                    //                anchors.topMargin: 0
                    //                anchors.right: parent.right
                    //                anchors.rightMargin: 0
                    //                onClicked: popup2.open()
                    //            }
                }

            }
        }

        Rectangle{
            id: rectclose
            width: 30
            height: 30
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.topMargin: 5
            anchors.rightMargin: 5
            opacity: 0.7
            color: 'transparent'
            Image {
                id: xclose
                width: 13
                height: 13
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                fillMode: Image.PreserveAspectCrop
                source: "../resources/close.png"
            }
            MouseArea{
                anchors.fill: parent
                hoverEnabled: true
                onEntered: {xclose.source = "../resources/xclose white.png"
                            rectclose.color = pink
                            xclose.width= 15
                            xclose.height= 15
                            rectclose.opacity= 1
                }
                onExited: {xclose.source = "../resources/close.png"
                           rectclose.color = 'transparent'
                            xclose.width= 13
                            xclose.height= 13
                    rectclose.opacity= 0.7

                }
                onClicked: {

                    Qt.quit()
                }
            }
        }

        Rectangle{
            color: 'transparent'
            id: rextmax
            width: 30
            height: 30
            anchors.top: parent.top
            anchors.right: rectclose.left
            anchors.topMargin: 5
            anchors.rightMargin: 5
            opacity: 0.7
            Image {
                id: xmax
                width: 13
                height: 13
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                fillMode: Image.PreserveAspectCrop
                source: "../resources/maximize.png"
            }
            MouseArea{
                anchors.fill: parent
                hoverEnabled: true
                onEntered: {
                    rextmax.opacity = 1
                    xmax.width= 15
                    xmax.height= 15}
                onExited: {
                    rextmax.opacity = 0.7
                    xmax.width= 13
                    xmax.height= 13}
                onClicked: {
                    if(window3.width === Screen.width) {
                        window3.showNormal()   
                        xmax.source= "../resources/maximize.png"
                    }
                    else{
                        xmax.source= "../resources/unmaximize.png"
                        window3.showMaximized()
                        window3.setGeometry(screen.virtualX, 0,screen.width, screen.desktopAvailableHeight)
                    }

                }
            }

        }

        Rectangle{
            color: 'transparent'
            id: rectmini
            width: 30
            height: 30
            anchors.top: parent.top
            anchors.right: rextmax.left
            anchors.topMargin: 5
            anchors.rightMargin: 5
            opacity: 0.7
            Image {
                id: xmini
                width: 13
                height: 13
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                fillMode: Image.PreserveAspectCrop
                source: "../resources/minimize.png"
            }
            MouseArea{
                anchors.fill: parent
                hoverEnabled: true
                onEntered: {

                    rectmini.opacity = 1
                    xmini.width= 15
                    xmini.height= 15}
                onExited: {xmini.width= 13
                    xmini.height= 13
                    rectmini.opacity = 0.7
                }
                onClicked: {
                    window3.visibility = 'Minimized'
                }
            }
        }



    }

    MouseArea {
        id: rightResize
        width: 5
        anchors.rightMargin: 0
        enabled: true
        anchors {
            right: parent.right
            top: parent.top
            bottom: parent.bottom
        }

        cursorShape: Qt.SizeHorCursor
        onPressed: previousX = mouseX
        onMouseXChanged: {
            if(window3.width === Screen.width) {
                                window3.showNormal()
                            }
            var dx = mouseX - previousX
            if(parent.width + dx>window3.minimumWidth){
                window3.setWidth(parent.width + dx)
            }
            if(parent.width + dx <= window3.minimumWidth & dx>=0){
                window3.setWidth(parent.width + dx)
            }
        }

    }
    MouseArea {
            id: leftResize
            width: 5
            enabled: true
            cursorShape: Qt.SizeHorCursor

            anchors {
                left: parent.left
                top: parent.top
                bottom: parent.bottom
            }

            onPressed: previousX = mouseX



            onMouseXChanged: {
                if(window3.width === Screen.width) {
                                    window3.showNormal()
                                }
                var dx = mouseX - previousX


                if(window3.width - dx>window3.minimumWidth){
                    window3.setX(window3.x + dx)
                    window3.setWidth(window3.width - dx)
                }

            }

        }

    MouseArea {
        id: topResize
        enabled: true
        height: 5
        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
        }

        cursorShape: Qt.SizeVerCursor

        onPressed: previousY = mouseY

        onMouseYChanged: {
            if(window3.width === Screen.width) {
                                window3.showNormal()
                            }
            var dy = mouseY - previousY


            if(window3.height - dy >window3.minimumHeight){
                window3.setY(window3.y + dy)
                window3.setHeight(window3.height - dy)
            }


        }
    }

    MouseArea {
        id: botResize
        enabled: true
        height: 5
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.bottomMargin: 0

        anchors {
            bottom: parent.bottom
            right: parent.right
        }

        cursorShape: Qt.SizeVerCursor

        onPressed: previousY = mouseY

        onMouseYChanged: {
            if(window3.width === Screen.width) {
                                window3.showNormal()
                            }
            var dy = mouseY - previousY

            if(window3.height + dy >window3.minimumHeight){
                window3.setHeight(window3.height + dy)
            }
            if(window3.height + dy <= window3.minimumHeight & dy>=0){
                window3.setHeight(parent.width + dx)
            }
        }

    }

    Popup {
        id: popup2
        x: window3.width - popup2.width - 80
        y: 80
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
        Loader{
            id: loader
            active: true
            source: "filter.qml"
            focus: true
        }
    }

    //signal movieSignal(string name, string source, string overview, string year,string  vote, string  duration,string  genre, string  stars )
    signal movieSignal(string name, string source, string overview, string year, string  vote, string  duration, string  genre, string  stars, string posters, string characters, string youtube, string backdrop_path, string path)
    //signal movie()
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}D{i:10;anchors_height:60;anchors_y:5}D{i:9;anchors_height:60;anchors_y:5}
D{i:3;anchors_height:55}
}
##^##*/
