import QtQuick 2.14
import QtQuick.Controls 2.14

Item{

    id: element
    x: 53
    y: 60
    width: 0
    height: 0


    Rectangle {
        id: rectangle3
        x: 0
        y: 0
        width: 317
        height: 357
        color: 'transparent'




        Rectangle {
            id: watch
            x: 0
            y: 283
            height: 37
            visible: false
            anchors.top: mid.bottom
            anchors.topMargin: 0
            gradient: Gradient {
                GradientStop {
                    position: 0
                    color: "#000000"
                }

                GradientStop {
                    position:0.5
                    color: '#2D0510'
                }
                GradientStop {
                    position:1
                    color: window3.black
                }


            }
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 0

            Text {
                id: filterArea
                color: 'transparent'
                text: "WATCH"
                anchors.fill: parent
                wrapMode: Text.WordWrap
                fontSizeMode: Text.Fit
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                minimumPixelSize: 25
                font.pixelSize: 15
                font.bold: true
            }
        }

        Rectangle {
            id: title
            height: 74
            border.width: 0
            gradient: Gradient {
                GradientStop {
                    position: 0
                    color: window3.footerColor

                }

                GradientStop {
                    position: 1
                    color: 'black'
                }
            }
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0
            anchors.top: parent.top
            anchors.topMargin: 0
        }

        Rectangle {

            id: mid
            x: 0

            radius: 0
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0
            anchors.bottom: stars1.bottom
            anchors.bottomMargin: -20
            anchors.top: title.bottom
            anchors.topMargin: -1
            antialiasing:true
            border.width: 0
            //        property var name: movieName
            //        property var imgSource:imageSource
            //        property var ye: year
            //        property var over: overview
            //        property var vot: vote

            gradient: Gradient {
                GradientStop {
                    position: 0
                    color: 'black'

                }
                GradientStop {
                    position: 0.8
                    color: window3.blackblack

                }

                GradientStop {
                    position: 1
                    color: window3.blackblack
                }
            }

        }

        TextArea {
            id: popupTitle
            x: 10
            y: 10
            color: window3.pink
            text: hm.title +" ("+hm.year+")"
            anchors.right: parent.right
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.rightMargin: 10
            anchors.leftMargin: 10
            anchors.topMargin: 10
            leftPadding: 0
            padding: 0
            font.bold: true
            wrapMode: Text.WordWrap
            textFormat: Text.AutoText
            font { pointSize: 15; weight: Font.Normal; capitalization: Font.MixedCase }



            font.wordSpacing: 0
            verticalAlignment: Text.AlignTop
            horizontalAlignment: Text.AlignLeft

        }

        TextArea {
            id: overview
            width: 282
            text: hm.overview
            color: window3.fontColor
            //text :"Last season, House and Cuddy finally decided to take their relationship to the next level, but struggled to find a balance between their professional and personal lives, and ultimately, Cuddy made the very emotional decision to end their relationship. As each of them dealt with the aftermath of the break-up, House got married to an immigrant in need of a Green Card. In the series' milestone 150th episode,"
            font.pointSize: 10
            anchors.top: popupTitle.bottom
            anchors.topMargin: 20
            anchors.right: parent.right
            anchors.rightMargin: 10
            anchors.left: parent.left
            anchors.leftMargin: 10
            verticalAlignment: Text.AlignTop
            horizontalAlignment: Text.AlignLeft
            leftPadding: 0
            padding: 0
            topPadding: 0
            wrapMode: Text.WordWrap

        }

        TextArea {
            id: genre1
            y: 0
            color: window3.fontColor
            height: 34
            text: {
                if(hm.title === 'Mr. Nobody'){
                    print('nobody', hm.genre)

                }

                return "<b>Genre: </b>" + hm.genre
            }
            horizontalAlignment: Text.AlignLeft
            clip: true

            textFormat: TextEdit.RichText
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignBottom
            font.pointSize: 10
            padding: 0
            rightPadding: 0
            topPadding: 0
            leftPadding: 0
            anchors.topMargin: 15
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            anchors.left: overview.left
            anchors.right: overview.right
            anchors.top: overview.bottom
        }

        TextArea {
            id: vote1
            y: 0

            color: window3.fontColor
            text: "<b>Vote: </b>"+ hm.vote
            verticalAlignment: Text.AlignTop
            textFormat: TextEdit.RichText
            wrapMode: Text.WordWrap
            font.pointSize: 10
            leftPadding: 0
            padding: 0
            anchors.top: genre1.bottom
            anchors.topMargin: 0
            anchors.right: overview.right
            anchors.rightMargin: 0
            anchors.left: overview.left
            anchors.leftMargin: 0
        }



        TextArea {
            id: runtime1

            color: window3.fontColor
            text: "<b>Duration: </b>"+ hm.runtime+' min'
            anchors.top: vote1.bottom
            anchors.topMargin: 0
            verticalAlignment: Text.AlignVCenter
            textFormat: TextEdit.RichText
            wrapMode: Text.WordWrap
            font.pointSize: 10
            padding: 0
            topPadding: 0
            leftPadding: 0
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            anchors.left: overview.left
            anchors.right: overview.right
        }

        TextArea {
            id: stars1
            color: window3.fontColor
            text:{
                var stars = ''
                var starsList = hm.stars.split(', ')
                for (var i = 0; i <= 10; i++){
                        stars += starsList[i] + ', '
                }
                return "<b>Stars: </b>"+ stars.substr(0, stars.length-2)

            }


            textFormat: TextEdit.RichText
            wrapMode: Text.WordWrap
            font.pointSize: 10
            leftPadding: 0
            padding: 0
            anchors.topMargin: 0
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            anchors.left: overview.left
            anchors.right: overview.right
            anchors.top: runtime1.bottom

        }









    }



}





/*##^##
Designer {
    D{i:0;formeditorZoom:1.25}D{i:3;anchors_y:0}D{i:7;anchors_x:0;anchors_y:"-20"}D{i:2;anchors_y:0}
D{i:8;anchors_x:0;anchors_y:"-20"}D{i:17;anchors_height:100;anchors_width:100}D{i:18;anchors_height:100;anchors_width:100}
D{i:1;anchors_y:0}
}
##^##*/
