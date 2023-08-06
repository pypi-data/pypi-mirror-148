import QtQuick 2.14
import QtQuick.Controls 2.14



Item {

    id: window
    width: 1600
    height: 900
    visible: true
    ListModel {
        id: suggestionsModel
    }
    Rectangle {
        id: background_body
        x: 0
        width: 0
        clip: false
        visible: true
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.right: parent.right
        anchors.left: parent.left
        gradient: Gradient {

            GradientStop {
                position: 0.8
                color: "black"
            }


            GradientStop {
                position: 1
                color: '#1c030a'
            }
        }
    }




    Flickable {
        id: scrollView
        boundsBehavior: Flickable.StopAtBounds
        interactive: true
        flickableDirection: Flickable.VerticalFlick
        anchors.rightMargin: 5
        anchors.bottomMargin: 0
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.topMargin: 0
        clip: false

        ScrollBar.vertical: ScrollBar {
            anchors.rightMargin: 0
            parent: scrollView.parent
            anchors.top: scrollView.top
            anchors.right: scrollView.right

            anchors.bottom: scrollView.bottom
            //anchors.leftMargin: -200
        }

        contentWidth: parent.width

        onWidthChanged: {
            var ch = gridRect.height + back_drop.height + 50
            //            print('pw',parent.width, 'ph',parent.height)
            back_drop.height =parent.width * 800 / 1920
            if(ch === Infinity){
                //                print('INFrh',gridRect.height,'INFbd',back_drop.height)
                //                print('INFch',contentHeight)
                contentHeight = 1516
            }else{
                contentHeight = gridRect.height + back_drop.height + 100
                //                print('rh',gridRect.height,'bd',back_drop.height)
//                print('ch',contentHeight)
            }



        }

        Component.onCompleted:  {

            contentHeight = 1516
        }

        Item {

            id: back_drop
            x: 0
            y: 0
            width: window3.width
//            onWidthChanged: {
//                print(width)
//            }

            anchors.top: parent.top
            anchors.topMargin: 0
            clip: false
            anchors.left: parent.left
            anchors.leftMargin: 0
            SwipeView {
                id: view
                height: parent.width * 800 / 1920
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.right: parent.right
                anchors.rightMargin: 0
                anchors.left: parent.left
                anchors.leftMargin: 0
                clip: true
                currentIndex: 0

                Repeater {
                    model: SuggestionsModel
                    Loader {
                        active: SwipeView.isCurrentItem || SwipeView.isNextItem || SwipeView.isPreviousItem
                        id: sm
                        source: "swipeSource.qml"
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
            Timer {
                running: true
                repeat: true
                interval: 5500
                onTriggered: {
                    var nextIndex = (view.currentIndex + 1) % view.count
                    view.setCurrentIndex(nextIndex)
                }
            }

            PageIndicator {
                id: indicator
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.right: parent.right
                anchors.rightMargin: 15

                count: view.count
                currentIndex: view.currentIndex

                delegate: Rectangle {
                    implicitWidth: 8
                    implicitHeight: 8

                    radius: width
                    color: pink

                    opacity: index === indicator.currentIndex ? 0.95 : pressed ? 0.7 : 0.45

                    Behavior on opacity {
                        OpacityAnimator {
                            duration: 100
                        }
                    }
                }




            }
        }
        Rectangle {
            Component.onCompleted: {
                print('completed')
                MyApp.onComp("Home")
            }

            id: gridRect
            color: 'transparent'
            visible: true
            property var nCells : 7
            property var cellW: 170

            height: {
                var items_per_row = Math.floor(window.width / cellW) >= 7 ? 7 : Math.floor(window.width / cellW)
                var movieCount = 21
                var h = Math.ceil(movieCount / items_per_row) * 250
//                print(movieCount )
                //print('items',items_per_row,'h',h,'bh',back_drop.height,'=',back_drop.height+h, scrollView.contentHeight)

                return h
            }



            anchors.left: parent.left
            anchors.leftMargin:{
                if((window3.width - (nCells * cellW))/2 >= 0){

                    return (window3.width - (nCells * cellW))/2
                }
                return (window3.width - Math.floor(window3.width/cellW) * cellW)/2
            }
            //color: '#cf1212'
            anchors.top: headerText.bottom
            anchors.topMargin: 15

            clip: false
            width: {
                if((window3.width - (nCells * cellW))/2 >= 0){
                    rightBinding = gridRect.anchors.leftMargin + nCells * cellW
                    return nCells * cellW
                }else{
                    rightBinding = window3.width - gridRect.anchors.leftMargin - 4
                    return window3.width
                }

            }


            GridView {
                id: gridView
                x: 50
                y: -70
                width: gridRect.nCells * gridRect.cellW
                cellWidth: gridRect.cellW
                cellHeight: 250
                height: 0
                interactive: false

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

        Text {
            id: headerText
            width: 340
            color: "#e43167"
            text: qsTr("Random Movies:")
            font.bold: true
            font.pixelSize: 25
            anchors.top: back_drop.bottom
            anchors.topMargin: 0
            anchors.left: gridRect.left
            anchors.leftMargin: 10
        }
    }

    Connections {
        target: MyApp
        function onClearMovies(){
            movieModel.clear()
            suggestionsModel.clear()
        }
        function onCloseFilter(text){
            headerText.text = text
            popup2.close()
        }

    }















}











/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}D{i:5;anchors_height:18}
}
##^##*/
