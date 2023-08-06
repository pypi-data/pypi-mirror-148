import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.15
import QtWebEngine 1.10
import QtQuick.Window 2.1

Item {

    id: movieItem
    width: 1600
    height: 900
    property var yellow : '#fff436'
    property var blue : '#2d6ba6'
    property var pink : '#e43167'
    property var footerColor: '#380614'
    property var backgroundColor: '#1F1D1E'
    property var headerColor: '#191819'
    property var black: '#110206'
    property var blackblack: '#060102'

    property var title : ''
    property var source : ''
    property var overview : ''
    property var year : ''
    property var vote : ''
    property var duration : ''
    property var genre : ''
    property var stars : ''
    property var posters: ''
    property var trailer: ''
    property var backdrop_path: ''
    property var path: ''



    Connections {
        target: window3
        //(string name, string source, string overview, string year,string  vote, string  duration,string  genre, string  stars )
        function onMovieSignal(name, source, overview, year, vote, duration, genre, stars, posters, characters, trailer, backdrop_path, path) {

            movieItem.title = name
            movieItem.source = source
            movieItem.overview = overview
            movieItem.year = year
            movieItem.vote = vote
            movieItem.duration = duration
            movieItem.genre = genre
            movieItem.stars = stars
            movieItem.posters = posters
            movieItem.trailer = trailer
            movieItem.backdrop_path = backdrop_path
            movieItem.path = path


            var starsList = stars.split(', ')
            var postersList = posters.split(', ')
            var charactersList = characters.split(', ')

            for (var i = 0; i < starsList.length; i++){
                modelCast.append({"castName1":starsList[i], "imageSource1":postersList[i], "characters1":charactersList[i]})

            }

        }
    }

    ListModel {
        id: modelCast
    }

    Rectangle {
        id: watch
        x: 0
        y: 806
        height: 94
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        gradient: Gradient {
            GradientStop {
                position: 0
                color: blackblack
            }

            GradientStop {
                position:0.3
                // color: '#2D0510'
                color: blackblack
            }
            GradientStop {
                position:1
                // color: blackblack
                color: '#2D0510'
            }
        }


        Text {
            id: filterArea
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            wrapMode: Text.WordWrap
            font.bold: true
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors.fill: parent
            text: "WATCH"
            minimumPixelSize: 25
            fontSizeMode: Text.Fit
            font.pixelSize: 35
            color: pink

            MouseArea {
                id: watchButon
                anchors.fill: parent
                hoverEnabled: true
                onEntered: filterArea.color = 'white'
                onExited: filterArea.color = pink
                onClicked: MyApp.watch(path)
                cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
            }


        }

    }


    Rectangle {
        id: innerHeader
        height: 140
        anchors.top: parent.top
        anchors.topMargin: 0
        gradient: Gradient {
            GradientStop {
                position: 0
                //color: "#4d142f"
                color: footerColor
            }

            GradientStop {
                position: 1
                color: "#000000"
            }
        }
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 0


        MouseArea {
            id: mouseArea1
            anchors.fill: parent
            property var geox
            property var geoy
            property var geow
            property var geoh
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

        Text {
            id: title
            width: 624
            height: 110
            color: "#e43167"
            text: movieItem.title
            fontSizeMode: Text.Fit
            font.pixelSize: 45
            minimumPixelSize: 25
            font.bold: true
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 42
            anchors.top: parent.top
            anchors.topMargin: 8
            anchors.left: parent.left
            anchors.leftMargin: 50
        }

        Item {
            id: rating
            x: 0
            width: 200
            anchors.right: parent.right
            anchors.rightMargin: 50

            anchors.top: parent.top
            anchors.topMargin: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0

            Text {
                id: rate
                color: "#e43167"
                font.pixelSize: 40
                minimumPixelSize: 20
                text: qsTr(" Vote "+movieItem.vote)
                visible: true
                anchors.bottomMargin: 42
                anchors.topMargin: 8
                fontSizeMode: Text.Fit
                anchors.fill: parent
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                font.bold: true
            }
        }

        Text {
            id: element2
            width: 489
            height: 36
            color: "#e43167"
            text: qsTr(movieItem.duration+' min' + " | "+movieItem.genre)
            fontSizeMode: Text.Fit
            anchors.top: title.bottom
            anchors.topMargin: 0
            anchors.left: title.left
            anchors.leftMargin: 1
            font.pixelSize: 30
            minimumPixelSize: 10
            verticalAlignment: Text.AlignBottom
            horizontalAlignment: Text.AlignLeft
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 15
        }
    }

}




    Image {
        id: backdrop2
        x: 1762
        y: 900
        visible: false
        source: backdrop_path
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.top: innerHeader.bottom
        anchors.right: parent.right
        anchors.bottom: watch.top
        anchors.left: parent.left
        anchors.topMargin: 0
        opacity: 1
        fillMode: Image.Stretch
    }


    Rectangle {
        id: bodyRect1
        x: 740
        y: 320
        color: 'black'
        anchors.top: innerHeader.bottom
        anchors.right: parent.right
        anchors.bottom: watch.top
        anchors.left: parent.left
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0
        opacity: 0.8
        gradient: Gradient {
            GradientStop {
                position: 0
                color: 'black'

            }
            GradientStop {
                position: 0.3
                color: 'black'


            }

            GradientStop {
                position: 1
                color: footerColor
            }
        }
        visible: false
    }

    Item {
        id: body
        x: 0
        y: 406
        height: 750
        anchors.bottomMargin: 0
        anchors.top: innerHeader.bottom
        anchors.right: parent.right
        anchors.bottom: watch.top
        anchors.left: parent.left
        anchors.topMargin: 0


            Rectangle {
                id: bodyRect
                x: 0
                y: 0
                anchors.fill: parent
                visible: true
                color: 'black'
                anchors.topMargin: 0
                anchors.bottomMargin: 0
                gradient: Gradient {

                    GradientStop {
                        position: 0.7
                        color: "#000000"
                    }

                    GradientStop {
                        position: 1
                        color: footerColor
                    }
                }

                ScrollView{
                    id: scrollView
                    anchors.topMargin: 55
                    clip: true
                    anchors.fill: parent
                    contentHeight: {
                       return gridLayout.height + 400
                    }


                Rectangle {
                    id: imageRect
                    width: 412
                    color: 'transparent'
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 0
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    anchors.top: parent.top
                    anchors.topMargin: 0

                    Image {
                        id: image
                        height: 488
                        anchors.top: parent.top
                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.topMargin: 0
                        anchors.rightMargin: 40
                        anchors.leftMargin: 40
                        antialiasing: true
                        transformOrigin: Item.Center
                        source: movieItem.source
                        fillMode: Image.PreserveAspectFit
                    }

                    Text {
                        id: trailer
                        x: 40
                        y: 700
                        text: movieItem.trailer === 'null' ? '': qsTr("Watch Trailer")
                        anchors.top: image.bottom
                        anchors.topMargin: 15
                        font.bold: true
                        color: pink
                        verticalAlignment: Text.AlignTop
                        horizontalAlignment: Text.AlignHCenter
                        anchors.leftMargin: 0
                        anchors.rightMargin: 0
                        anchors.right: image.right
                        anchors.left: image.left
                        font.pixelSize: 30


                        MouseArea {
                            id: trailerMouseArea
                            x: -50
                            y: -576
                            anchors.topMargin: 0
                            anchors.fill: parent
                            hoverEnabled: true
                            onEntered: true ? trailer.color = 'white' : trailer.color = pink
                            onExited: false ? trailer.color = 'white' : trailer.color = pink
                            cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                            onClicked: {
                                var component = Qt.createComponent("trailerEngine.qml");
                                for (var i=0; i<1; i++) {
                                    var object = component.createObject(rectangle1);
                                    //object.x = (object.width + 10) * i;
                                }


                            }
                        }


                    }

                }



                GridLayout {
                    id: gridLayout
                    columns: 1
                    rowSpacing: 0
                    layoutDirection: Qt.LeftToRight
                    anchors.top: parent.top
                    anchors.topMargin: 0
                    anchors.left: imageRect.right
                    anchors.leftMargin: 0
                    anchors.right: parent.right
                    anchors.rightMargin: 50
                    rows: 1
                    flow: GridLayout.LeftToRight
                    Text {
                        id: overview
                        y: 0
                        width: 500
                        height: 200
                        color: pink
                        text: "<b>Overview: \n</b>"+movieItem.overview
                        font.pixelSize: 25
                        Layout.fillHeight: true
                        Layout.fillWidth: true
                        Layout.rightMargin: 20
                        fontSizeMode: Text.HorizontalFit
                        elide: Text.ElideLeft
                        wrapMode: Text.WordWrap
                        Layout.alignment: Qt.AlignLeft | Qt.AlignTop

                        minimumPixelSize: 25
                        horizontalAlignment: Text.AlignLeft
                    }
                }



                Item {
                    id: listItem
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 0
                    anchors.top: gridLayout.bottom
                    anchors.topMargin: 60
                    anchors.left: gridLayout.left
                    anchors.leftMargin: 0
                    anchors.right: parent.right
                    anchors.rightMargin: 50

                    ListView {
                        ScrollBar.horizontal: ScrollBar {
                            height: 10
                            anchors.bottom: parent.bottom
                            anchors.bottomMargin: 0
                            anchors.right: parent.right
                            anchors.rightMargin: 0
                            anchors.left: parent.left
                                //anchors.leftMargin: -200
                            }
                        id: listView
                        anchors.leftMargin: 0
                        anchors.rightMargin: 0
                        anchors.fill: parent
                        clip: true
                        boundsBehavior: Flickable.StopAtBounds
                        boundsMovement: Flickable.StopAtBounds
                        onMovementEnded:  {
                            if(listView.atXEnd){
                                rightArrow.visible = false
                                leftArrow.visible = true
                            }
                            else if(listView.atXBeginning){
                                rightArrow.visible = true
                                leftArrow.visible = false
                            }

                            else{
                                rightArrow.visible = true
                                leftArrow.visible = true
                            }
                        }

                        orientation: ListView.Horizontal
                        flickableDirection: Flickable.HorizontalFlick
                        model: modelCast
                        delegate: Item {
                            id: cast2
                            //property var castName: 'test'
                            //property var imageSource:'https://image.tmdb.org/t/p/w600_and_h900_bestv2/gjfDl52Kk02MPgUYFjs9bOy33OY.jpg'
                            property var castName: castName1
                            property var imageSource: imageSource1
                            property var characters: characters1
                            x: 5
                            width: 170
                            height: 240

                            Row {
                                id: row1
                                Item{
                                    id: element1
                                    anchors.top: parent.top
                                    anchors.topMargin: 0
                                    Image {
                                        id: image4
                                        x: 1
                                        width: 157
                                        height: 200
                                        anchors.top: parent.top
                                        anchors.topMargin: 0
                                        layer.textureMirroring: ShaderEffectSource.NoMirroring
                                        layer.mipmap: false
                                        layer.enabled: false
                                        opacity: 1
                                        clip: false
                                        source: cast2.imageSource
                                        fillMode: Image.Stretch
                                        sourceSize.width: 157
                                        sourceSize.height: 200
                                        smooth: true
                                        mipmap: true
                                        antialiasing: true

                                        Rectangle {
                                            id: rectangle
                                            anchors.rightMargin: -1
                                            anchors.leftMargin: -1
                                            anchors.fill: parent
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
                                            clip: true
                                            border.width: 0
                                        }

                                    }
                                    Text {
                                        id: realName
                                        width: 130
                                        height: 40
                                        color: "white"
                                        //
                                        text: cast2.castName
                                        anchors.right: image4.right
                                        anchors.rightMargin: 0
                                        anchors.left: image4.left
                                        anchors.leftMargin: 0
                                        font.pointSize: 12
                                        //                                anchors.right: image4.left
                                        //                                anchors.rightMargin: 0
                                        //                                anchors.left: image4.right
                                        //                                anchors.leftMargin: 0
                                        anchors.top: image4.bottom
                                        anchors.topMargin: 0
                                        bottomPadding: 5
                                        style: Text.Outline
                                        fontSizeMode: Text.FixedSize
                                        wrapMode: Text.WordWrap
                                        verticalAlignment: Text.AlignBottom
                                        horizontalAlignment: Text.AlignHCenter

                                    }
                                    Text {
                                        id: movieChar

                                        width: 130
                                        height: 40
                                        color: "white"
                                        //
                                        text: cast2.characters
                                        anchors.right: image4.right
                                        anchors.rightMargin: 15
                                        anchors.left: image4.left
                                        anchors.leftMargin: 15
                                        //anchors.right: image4.left
                                        //anchors.rightMargin: 0
                                        //anchors.left: image4.right
                                        //anchors.leftMargin: 0
                                        font.pointSize: 11
                                        //                                anchors.right: image4.left
                                        //                                anchors.rightMargin: 0
                                        //                                anchors.left: image4.right
                                        //                                anchors.leftMargin: 0
                                        anchors.top: realName.bottom
                                        anchors.topMargin: 5
                                        bottomPadding: 5
                                        style: Text.Outline
                                        fontSizeMode: Text.FixedSize
                                        wrapMode: Text.WordWrap
                                        verticalAlignment: Text.AlignTop
                                        horizontalAlignment: Text.AlignHCenter

                                    }
                                }


                            }
                        }
                    }

                    ToolButton {
                        id: leftArrow
                        height: 36
                        text: qsTr("<")
                        anchors.right: listView.left
                        anchors.rightMargin: -5
                        visible: false

                        contentItem: Text {
                            id: textTool1
                            y: 0
                            height: 36

                            color: leftArrow.hovered ? '#ffffff' : pink
                            text: "<"
                            visible: true
                            anchors.bottom: parent.bottom
                            anchors.bottomMargin: 0
                            anchors.top: parent.top
                            anchors.topMargin: 0
                            anchors.right: parent.right
                            anchors.left: parent.left
                            horizontalAlignment: Text.AlignHCenter
                            opacity: enabled ? 1.0 : 0.3
                            verticalAlignment: Text.AlignVCenter
                            elide: Text.ElideRight
                            font: leftArrow.font
                        }
                        background: Rectangle {
                            color: Qt.darker("#33333333", leftArrow.enabled && (leftArrow.checked || leftArrow.highlighted) ? 1.5 : 1.0)
                            opacity: enabled ? 1 : 0.3
                            visible: false
                            implicitWidth: 40
                            implicitHeight: 40
                        }
                        anchors.topMargin: 100
                        font.bold: true
                        anchors.top: parent.top
                        font.pixelSize: 37


                        MouseArea {
                            cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                            hoverEnabled: true
                            anchors.fill: parent
                            onEntered: textTool1.color = "white"
                            onExited: textTool1.color = pink
                            onClicked:listView.flick(1500,0)
                        }
                    }

                    ToolButton {
                        id: rightArrow
                        x: 0
                        height: 36
                        text: qsTr(">")
                        anchors.leftMargin: 0
                        contentItem: Text {
                            id: textTool2
                            y: 0
                            height: 36

                            color: rightArrow.hovered ? '#ffffff' : pink
                            text: rightArrow.text
                            anchors.bottom: parent.bottom
                            anchors.bottomMargin: 0
                            horizontalAlignment: Text.AlignHCenter
                            opacity: enabled ? 1.0 : 0.3
                            anchors.topMargin: 0
                            verticalAlignment: Text.AlignVCenter
                            anchors.right: parent.right
                            anchors.top: parent.top
                            elide: Text.ElideRight
                            font: rightArrow.font
                            anchors.left: parent.left
                        }
                        background: Rectangle {
                            color: Qt.darker("#33333333", rightArrow.enabled && (rightArrow.checked || rightArrow.highlighted) ? 1.5 : 1.0)
                            opacity: enabled ? 1 : 0.3
                            visible: false
                            implicitWidth: 40
                            implicitHeight: 40
                        }
                        font.bold: true
                        anchors.topMargin: 100
                        anchors.top: parent.top
                        anchors.left: listView.right
                        font.pixelSize: 37
                        MouseArea {
                            cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                            hoverEnabled: true
                            anchors.fill: parent
                            onEntered: textTool2.color = "white"
                            onExited: textTool2.color = pink
                            onClicked:listView.flick(-1500,0)
                        }
                    }
                }




                }




            }

        ToolButton {
            id: back
            width: 131
            height: 36
            text: qsTr("<--")
            background: Rectangle {
                color: Qt.darker("#33333333", back.enabled && (back.checked || back.highlighted) ? 1.5 : 1.0)
                implicitWidth: 40
                visible: false
                implicitHeight: 40
                opacity: enabled ? 1 : 0.3
            }
            font.pixelSize: 37
            anchors.leftMargin: 10
            font.bold: true
            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                onClicked: {
                    ldOutside.source = 'home.qml'
                    MyApp.onComp("Home")
                    header.visible = true
                    titleRect.height = 65
                    console.log('click')
                }
            }
            contentItem: Text {
                id: textTool
                width: 60
                height: 100
                color: back.hovered ? '#ffffff' : pink
                text: back.text
                elide: Text.ElideRight
                anchors.leftMargin: 0
                anchors.top: parent.top
                font: back.font
                verticalAlignment: Text.AlignVCenter
                anchors.left: parent.left
                horizontalAlignment: Text.AlignHCenter
                opacity: enabled ? 1.0 : 0.3
                anchors.topMargin: 0
            }
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.topMargin: 0
        }
    }



    Item {
        id: rectangle1
        anchors.fill: parent
        width: 892
        height: 532
    }
}



/*##^##
Designer {
    D{i:0;formeditorZoom:0.5}D{i:7;anchors_height:100;anchors_width:174;anchors_x:626}
D{i:44;anchors_height:203;anchors_width:150}D{i:51;anchors_width:130}D{i:25;anchors_x:0;anchors_y:0}
}
##^##*/
