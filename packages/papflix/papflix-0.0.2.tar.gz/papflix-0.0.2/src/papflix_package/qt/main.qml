import QtQuick 2.14
import QtQuick.Controls 2.14



Item {

    id: window
    //title: qsTr("Hello Kostas")
    width: 1600
    height: 900

    visible: true

    property var yellow : '#fff436'
    property var blue : '#2d6ba6'
    property var pink : '#e43167'
    property var footerColor: '#380614'
    property var backgroundColor: '#1F1D1E'
    property var headerColor: '#191819'
    property var ocean: '#243B55'

    //color: 'transparent'





    ListModel {
        id: movieModel

    }



    //Component.onCompleted: {movieModel.append({"position":"Movie"})}

    



    Rectangle {
        id: rectangle2
        x: 0
        anchors.leftMargin: 0
        gradient: Gradient {
            GradientStop {
                position: 0.7
                color: "black"
            }


            GradientStop {
                position: 1
                color: '#1c030a'
                //color: 'white'
            }
        }
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.topMargin: 0
    }

    Rectangle {
        Component.onCompleted: {
            print('completed')
            MyApp.onComp("main")
        }

        id: gridRect
        color: 'transparent'
        visible: true
        property var nCells : 7
        property var cellW: 170

        anchors.left: parent.left
        anchors.leftMargin:{
            if((window3.width - (nCells * cellW))/2 >= 0){

                return (window3.width - (nCells * cellW))/2
            }

            return (window3.width - Math.floor(window3.width/cellW) * cellW)/2
        }
        //color: '#cf1212'
        anchors.top: headerText.bottom
        anchors.bottom: parent.bottom
        anchors.topMargin: 15
        anchors.bottomMargin: 0

        clip: false

        width: {
            if((window3.width - (nCells * cellW))/2 >= 0){
                window3.rightBinding = gridRect.anchors.leftMargin + nCells * cellW
                //print(window3.rightBinding)
                return nCells * cellW
            }else{
                window3.rightBinding = window3.width - gridRect.anchors.leftMargin - 4
                return window3.width
            }

        }


        GridView {
            id: gridView
            x: 50
            y: -70
            width:    gridRect.nCells * gridRect.cellW
            ScrollBar.vertical: ScrollBar {
                parent: gridView.parent
                anchors.top: gridView.top
                anchors.left: gridView.right
                anchors.bottom: gridView.bottom
                //anchors.leftMargin: -200
            }

            onWidthChanged:  print(contentWidth)

            cellWidth: gridRect.cellW
            cellHeight: 250
            height: 0
            interactive: true
            cacheBuffer: 640

            anchors.top: parent.top
            anchors.topMargin: 0
            visible: true
            clip: true
            boundsMovement: Flickable.StopAtBounds
            flow: GridView.FlowLeftToRight
            highlightRangeMode: GridView.StrictlyEnforceRange
            flickableDirection: Flickable.VerticalFlick
            boundsBehavior: Flickable.StopAtBounds
            contentHeight: 0
            contentWidth: 0
            contentY: 0
            transformOrigin: Item.Center
            keyNavigationWraps: true
            snapMode: GridView.SnapToRow
            layoutDirection: Qt.LeftToRight
            contentX: 0
            rightMargin: 0
            bottomMargin: 0
            leftMargin: 0
            topMargin: 0
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            anchors.left: parent.left
            model: myListModel



            delegate: Component {
                Loader {
                    id: hm
                    source: "movieDelegate.qml"
                    property var title: title1
                    property var year: year1
                    property var overview: overview1
                    property var poster:poster1
                    property var vote: vote1
                    property var runtime: runtime1
                    property var genre: genre1
                    property var stars: stars1
                    property var starsPoster: starsPoster1
                    property var characters: characters1
                    property var trailer: trailer1
                    property var backdrop_path: backdrop_path1
                    property var path: path1
                }

            }

        }

    }


    Connections {
        target: MyApp
        function onClearMovies(){
            movieModel.clear()
        }
        function onCloseFilter(text){
            headerText.text = text
            popup2.close()
        }
    }


    Text {
        id: headerText
        color: window3.fontColor
        text:'Random Movies:'
        font.bold: true
        font.pixelSize: 25
        width: gridView.width


        textFormat: TextEdit.RichText
        wrapMode: Text.WordWrap
        leftPadding: 0
        padding: 0
        anchors.topMargin: 25
        anchors.leftMargin: 0
        anchors.left: gridRect.left
        anchors.top: parent.top
    }

}















/*##^##
Designer {
    D{i:0;formeditorZoom:0.6600000262260437}D{i:4;anchors_y:140}D{i:8;anchors_y:140}D{i:6;anchors_y:140}
}
##^##*/
