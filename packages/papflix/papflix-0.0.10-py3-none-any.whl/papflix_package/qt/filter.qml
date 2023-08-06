import QtQuick 2.14
import QtQuick.Controls 2.14


Rectangle {
    id: filter
    width: 700

    property var count: 0
    
    property var grey: '#bdbebf'

    height: controlSwitch.checked ? 110 + sort.anchors.topMargin + sort.height + filterButton.height +145: 110 + sort.height + filterButton.height + sort.anchors.topMargin
    gradient: Gradient {
        GradientStop {
            position: 0
            color: 'black'
        }


        GradientStop {
            position: 1
            color: footerColor
        }
    }

    
    Item {
        id: advanced
        x: 182
        visible: controlSwitch.checked ? true : false
        anchors.bottom: filterButton.top
        clip: true
        anchors.top: sort.bottom
        anchors.right: parent.right
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.topMargin: 40
        anchors.bottomMargin: 20

        TextArea {
            id: advancedSort
            x: 100
            y: 10
            height: 26
            color: pink
            anchors.top: parent.top
            background: Rectangle {
                anchors.leftMargin: 0
                anchors.rightMargin: 0
                border.color: window3.pink
                color: pink
                opacity: 0.2
                //border.width: 2
                anchors.left: parent.left
                anchors.right: parent.right
            }
            font.bold: true
            anchors.leftMargin: 100
            anchors.rightMargin: 100
            wrapMode: Text.WordWrap
            font.pointSize: 9
            opacity: controlSwitch.checked ? 1 : 0.3
            horizontalAlignment: Text.AlignLeft
            anchors.topMargin: 20
            anchors.left: parent.left
            anchors.right: parent.right
            font.letterSpacing: 1
            leftPadding: 6
            placeholderTextColor: window3.pink
            placeholderText: qsTr("Example: Sort By: Name")
        }

        TextArea {
            id: advancedYear
            x: 100
            y: 10
            height: 26
            opacity: controlSwitch.checked ? 1 : 0.3


            color: window3.pink
            wrapMode: Text.WordWrap
            leftPadding: 6
            font.letterSpacing: 1
            anchors.top: advancedSort.bottom
            anchors.topMargin: 10
            anchors.right: parent.right
            anchors.rightMargin: 100
            anchors.left: parent.left
            anchors.leftMargin: 100
            font.pointSize: 9

            horizontalAlignment: Text.AlignLeft

            font.bold: true
            placeholderText: qsTr("Example: Year >= 1995 AND Year <= 2005")
            background: Rectangle {
                anchors.right: parent.right
                anchors.rightMargin: 0
                anchors.left: parent.left
                anchors.leftMargin: 0
                border.color: window3.pink
                color: pink
                opacity: 0.2
            }
            placeholderTextColor: window3.pink



        }

        TextArea {
            id: advancedRating
            x: 100
            y: 10
            height: 26
            color: window3.pink
            anchors.top: advancedYear.bottom
            background: Rectangle {
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                border.width: 2
                anchors.right: parent.right
                anchors.left: parent.left
                border.color: pink
                color: pink
                opacity: 0.2
            }
            anchors.rightMargin: 100
            anchors.leftMargin: 100
            font.bold: true
            wrapMode: Text.WordWrap
            font.pointSize: 9
            opacity: controlSwitch.checked ? 1 : 0.3
            horizontalAlignment: Text.AlignLeft
            anchors.topMargin: 10
            anchors.right: parent.right
            anchors.left: parent.left
            font.letterSpacing: 1
            leftPadding: 6
            placeholderText: qsTr("Example: Rating >= 0 AND Rating <= 9")
            placeholderTextColor: window3.pink
        }

        TextArea {
            id: advancedGenre
            x: 100
            y: 10
            height: 40
            color: window3.pink
            font.pointSize: 9
            anchors.top: advancedRating.bottom
            background: Rectangle {
                anchors.leftMargin: 0
                anchors.rightMargin: 0
                border.color: pink
                border.width: 1
                color: pink
                opacity: 0.2
                anchors.left: parent.left
                anchors.right: parent.right
            }
            font.bold: true
            anchors.leftMargin: 100
            anchors.rightMargin: 100
            wrapMode: Text.WordWrap
            opacity: controlSwitch.checked ? 1 : 0.3
            horizontalAlignment: Text.AlignLeft
            anchors.topMargin: 10
            anchors.left: parent.left
            anchors.right: parent.right
            font.letterSpacing: 1
            leftPadding: 6
            placeholderTextColor: window3.pink
            placeholderText: qsTr("Example: Western OR Thriller")
        }






    }

    Rectangle {
        id: sort
        x: 27
        width: 180
        color: 'transparent'
        anchors.right: parent.right
        anchors.rightMargin: 18
        anchors.bottom: genreContainer.bottom
        anchors.bottomMargin: 0
        anchors.top: parent.top
        anchors.topMargin: 20


        Column {
            id: row
            width: 180
            height: 151
            bottomPadding: 0
            topPadding: 0
            anchors.top: sortTitle.bottom
            anchors.right: parent.right
            anchors.left: parent.left
            anchors.topMargin: 20
            padding: 0
            antialiasing: true
            spacing: 15
            opacity: controlSwitch.checked ? 0.3 : 1

            Repeater {
                Loader{
                    property var mode: 'sort'
                    property var flag: false
                    property var name: nameL
                    property var query: {

                        if(advancedSort.text === 'Sort By: '+name){
                            flag = true
                            return ''
                        }
                        flag = false
                        return 'Sort By: ' + name

                    }

                    property var weight: 0



                    id: loaderFilter2
                    source: "roundButton.qml"
                    focus: true
                    width: 180

                }

                model: ListModel {
                    ListElement {
                        nameL: "Name"
                    }
                    ListElement {
                        nameL: "Year"
                    }
                    ListElement {
                        nameL: "Vote"
                    }


                }
            }



        }

        Text {

            opacity: controlSwitch.checked ? 0.3 : 1
            id: sortTitle
            x: 0
            height: 39
            color: window3.pink
            text: qsTr("Sort By")
            anchors.top: parent.top
            anchors.topMargin: 6
            font.kerning: true
            font.preferShaping: true
            textFormat: Text.RichText
            fontSizeMode: Text.Fit
            elide: Text.ElideLeft
            anchors.leftMargin: 0
            font.bold: true
            horizontalAlignment: Text.AlignRight
            wrapMode: Text.WordWrap
            anchors.right: parent.right
            font.underline: true
            verticalAlignment: Text.AlignVCenter
            anchors.left: parent.left
            anchors.rightMargin: 0
            font.pixelSize: 20
        }

        Item {
            id: switchItem
            y: 241
            height: 86
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 26
            anchors.left: parent.left
            anchors.leftMargin: 0
            anchors.right: parent.right
            anchors.rightMargin: 0


            Switch {
                id: controlSwitch
                text: qsTr("Switch")
                anchors.fill: parent
                checked: advaMA.clickt


                indicator: Rectangle {
                    id: rectSwitchid
                    x: 66
                    y: 0
                    width: 50
                    implicitWidth: 48
                    implicitHeight: 26
                    color: controlSwitch.checked ? window3.pink : "#bdbebf"
                    radius: 13
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 0

                    //border.color: window3.pink
                    MouseArea {
                        id: advaMA

                        cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
                        hoverEnabled: true
                        anchors.fill: parent

                        property var clickt: false
                        property var flag: false
                        property var preYear:''
                        property var preRating:''
                        property var preGenre:''
                        property var preSort:''
                        onClicked: {

                            clickt = clickt ? false : true

                            var previousYear = advancedYear.text
                            advancedYear.text = controlSwitch.checked ? '' : preYear
                            preYear = !controlSwitch.checked ? advancedYear.text: previousYear

                            var previousRating = advancedRating.text
                            advancedRating.text = controlSwitch.checked ? '' : preRating
                            preRating = !controlSwitch.checked ? advancedRating.text: previousRating

                            var previousGenre = advancedGenre.text
                            advancedGenre.text = controlSwitch.checked ? '' : preGenre
                            preGenre = !controlSwitch.checked ? advancedGenre.text: previousGenre

                            var previousSort = advancedSort.text
                            advancedSort.text = controlSwitch.checked ? '' : preSort
                            preSort = !controlSwitch.checked ? advancedSort.text: previousSort
                        }
                    }
                    Rectangle {
                        x: controlSwitch.checked ? parent.width - width : 0
                        width: 26
                        height: 26
                        color: '#ffffff'
                        radius: 13

                        //border.color: window3.pink
                    }
                }

                contentItem: Text {
                    y: 0
                    height: 31

                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    horizontalAlignment: Text.AlignHCenter
                    font.pixelSize: 12
                    //font: controlSwitch.font
                    font.bold: true

                    opacity: enabled ? 1.0 : 0.3
                    color: window3.pink
                    text: "Advanced Filter"
                    anchors.bottom: rectSwitchid.top
                    anchors.bottomMargin: 20
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    verticalAlignment: Text.AlignBottom
                    //leftPadding: controlSwitch.indicator.width + controlSwitch.spacing
                }
            }
        }


    }
    

    Rectangle {
        id: genreContainer
        width: 180
        height: 346
        color: 'transparent'
        anchors.left: parent.left
        anchors.leftMargin: 18
        anchors.top: parent.top
        anchors.topMargin: 20
        opacity: controlSwitch.checked ? 0.3 : 1
        
        Flow {
            id: element
            width: 152
            anchors.top: sortTitle2.bottom
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            layoutDirection: Qt.LeftToRight
            flow: Flow.LeftToRight
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            anchors.bottomMargin: 20
            anchors.topMargin: 20
            spacing: 6
            padding: 0

            //width: 50
            
            Repeater {
                Loader{


                    property var weight: 1
                    property var name: nameL
                    property var mode: 'genre'
                    property var flag: false
                    property var query: {

                        if (flag === false){
                            if(advancedGenre.text.indexOf(' OR ' + name) !== -1){
                                console.log('mpika1')
                                return advancedGenre.text.replace(' OR '+name, '')
                            }
                            else if(advancedGenre.text.indexOf(name + ' OR ') !== -1){
                                console.log('mpika2')
                                return advancedGenre.text.replace(name + ' OR ', '')

                            }
                            else if(advancedGenre.text.indexOf(name) !== -1){
                                console.log('mpika3')
                                return advancedGenre.text.replace(name, '')

                            }
                        }
                        else{
                            if(advancedGenre.text.length === 0){

                                return name
                            }
                            else{
                                return advancedGenre.text + ' OR ' + name
                            }


                        }

                    }
                    id: loaderFilter
                    source: "roundButton.qml"
                    focus: true
                }
                model: ListModel {
                    ListElement {
                        nameL: "Action"

                    }
                    ListElement {
                        nameL: "Animation"

                    }
                    ListElement {
                        nameL: "Adventure"

                    }
                    ListElement {
                        nameL: "Comedy"
                    }
                    ListElement {
                        nameL: "Crime"
                    }
                    ListElement {
                        nameL: "Documentary"
                    }
                    ListElement {
                        nameL: "Drama"
                    }
                    ListElement {
                        nameL: "Family"

                    }
                    ListElement {
                        nameL: "Fantasy"

                    }
                    ListElement {
                        nameL: "History"

                    }
                    ListElement {
                        nameL: "Horror"

                    }
                    ListElement {
                        nameL: "Music"

                    }
                    ListElement {
                        nameL: "Mystery"

                    }
                    ListElement {
                        nameL: "Romance"

                    }
                    ListElement {
                        nameL: "Science Fiction"

                    }
                    ListElement {
                        nameL: "TV Movie"

                    }
                    ListElement {
                        nameL: "Thriller"

                    }
                    ListElement {
                        nameL: "War"

                    }
                    ListElement {
                        nameL: "Western"

                    }
                }
            }

        }

        Text {
            id: sortTitle2
            x: 0
            y: 6
            height: 39
            color: window3.pink
            text: qsTr("Genre")
            anchors.rightMargin: 0
            font.preferShaping: true
            font.kerning: true
            textFormat: Text.RichText
            font.underline: true
            anchors.leftMargin: 0
            elide: Text.ElideLeft
            fontSizeMode: Text.Fit
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft
            font.pixelSize: 20
            anchors.left: parent.left
            font.bold: true
            wrapMode: Text.WordWrap
            anchors.right: parent.right
        }

    }
    
    

    Item {
        id: mid
        anchors.right: sort.left
        anchors.rightMargin: 0
        anchors.left: genreContainer.right
        anchors.leftMargin: 0
        anchors.bottom: genreContainer.bottom
        anchors.bottomMargin: 0
        anchors.top: genreContainer.top
        anchors.topMargin: 0
        opacity: controlSwitch.checked ? 0.3 : 1

        Rectangle {
            id: keyword
            x: 32
            height: 30
            color: 'transparent'
            visible: false
            anchors.top: sortTitle1.bottom
            anchors.topMargin: 20
            anchors.right: parent.right
            anchors.rightMargin: 20
            border.color: window3.pink
            MouseArea {
                id: mouseAreaInput
                anchors.fill: parent
            }

            TextField {
                id: hiddenText
                color: window3.pink
                font.pointSize: 9

                horizontalAlignment: Text.AlignHCenter
                anchors.fill: parent
                font.bold: true
                placeholderText: qsTr("Enter keywords here")
                background: Rectangle {
                    color: "transparent"
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    implicitWidth: 200
                    implicitHeight: 40
                }
                placeholderTextColor: window3.pink
            }
            border.width: 2
            anchors.left: parent.left
            anchors.leftMargin: 20
        }

        Rectangle {
            id: year
            height: 85
            color: "transparent"
            anchors.top: keyword.bottom
            anchors.topMargin: -50
            anchors.right: parent.right
            anchors.rightMargin: 20
            anchors.left: parent.left
            anchors.leftMargin: 20


            RangeSlider {
                id: control
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                orientation: RangeSlider.SnapAlways
                stepSize: 100
                to: 2022
                from: 1950
                first.value: 1950
                second.value: 2022
                property var val1: Math.round(first.value)
                property var val2: Math.round(second.value)
                enabled: !controlSwitch.checked



                background: Rectangle {
                    x: control.leftPadding
                    y: control.topPadding + control.availableHeight / 2 - height / 2
                    implicitWidth: 200
                    implicitHeight: 4
                    width: control.availableWidth
                    height: implicitHeight
                    radius: 2
                    color: "#bdbebf"

                    Rectangle {
                        x: control.first.visualPosition * parent.width
                        width: control.second.visualPosition * parent.width - x
                        height: parent.height
                        color: window3.pink
                        radius: 2
                    }
                }
                first.handle: Rectangle {
                    id: h1
                    x:  control.leftPadding + control.first.visualPosition * (control.availableWidth - width)
                    y: control.topPadding + control.availableHeight / 2 - height / 2
                    color: control.first.pressed ? window3.pink : "#f6f6f6"
                    implicitWidth: 26
                    implicitHeight: 26
                    radius: 13
                    border.width: 0
                    Text {
                        y:24
                        width: 26
                        id: year1
                        height: 24
                        text: Math.round(control.first.value)
                        font.pointSize: 9
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        color :window3.pink
                        font.bold: true
                    }

                }
                first.onVisualPositionChanged: {
                    var x1 = Math.round(first.value)
                    var x2 = Math.round(second.value)
                    if(Math.abs(x2 - x1)<=7){
                        year1.y = -24

                    }
                    else {
                        year1.y = 24
                    }


                    if(advancedYear.text.length !== 0){
                        advancedYear.text = advancedYear.text.replace('Year >= ' + Math.round(val1), 'Year >= ' + Math.round(first.value))
                    }
                    else{
                        advancedYear.text = 'Year >= ' + Math.round(first.value) + ' AND Year <= ' + Math.round(second.value)
                    }
                    val1 = Math.round(first.value)
                }
                second.handle: Rectangle {
                    id: h2
                    x: control.leftPadding + control.second.visualPosition * (control.availableWidth - width)
                    y: control.topPadding + control.availableHeight / 2 - height / 2
                    color: control.second.pressed ? window3.pink : "#f6f6f6"
                    implicitWidth: 26
                    implicitHeight: 26
                    radius: 13
                    border.width: 0
                    Text {
                        y:24
                        width: 26
                        id: year2
                        height: 24
                        color: window3.pink
                        text: Math.round(control.second.value)
                        font.bold: true
                        font.pointSize: 9
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                second.onVisualPositionChanged: {
                    var x1 = Math.round(first.value)
                    var x2 = Math.round(second.value)
                    if(Math.abs(x2 - x1)<=7){
                        year2.y = -24

                    }
                    else {
                        year2.y = 24
                    }


                    if(advancedYear.text.length !== 0){
                        advancedYear.text = advancedYear.text.replace(' AND Year <= ' + Math.round(val2),' AND Year <= ' + Math.round(second.value))
                    }
                    else{
                        advancedYear.text = 'Year >= ' + Math.round(first.value) + ' AND Year <= ' + Math.round(second.value)
                    }

                    val2 = Math.round(second.value)
                }


                Text {
                    id: element1
                    x: 0
                    height: 31
                    color: window3.pink
                    text: qsTr("Year")
                    anchors.bottom: h1.top
                    anchors.bottomMargin: 20
                    font.bold: true
                    verticalAlignment: Text.AlignBottom
                    horizontalAlignment: Text.AlignHCenter
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    font.pixelSize: 12
                }
            }


        }

        Rectangle {
            id: rating
            height: 114
            color: "#00000000"
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 50
            anchors.rightMargin: 20
            RangeSlider {
                id: control1
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                orientation: RangeSlider.SnapAlways
                first.value: 0
                second.value: 9
                property var val1: Math.round(first.value)
                property var val2: Math.round(second.value)
                enabled: !controlSwitch.checked

                Text {
                    id: element2
                    x: 0
                    y: 0
                    height: 31
                    color: window3.pink
                    text: qsTr("Rating")
                    anchors.bottom: r1.top
                    anchors.bottomMargin: 20
                    anchors.rightMargin: 0
                    verticalAlignment: Text.AlignBottom
                    horizontalAlignment: Text.AlignHCenter
                    anchors.right: parent.right
                    anchors.leftMargin: 0
                    font.bold: true
                    font.pixelSize: 12
                    anchors.left: parent.left
                }
                to: 10
                from: 0
                background: Rectangle {
                    x: control1.leftPadding
                    y: control1.topPadding + control1.availableHeight / 2 - height / 2
                    width: control1.availableWidth
                    height: implicitHeight
                    color: "#bdbebf"
                    radius: 2
                    Rectangle {
                        x: control1.first.visualPosition * parent.width
                        width: control1.second.visualPosition * parent.width - x
                        height: parent.height
                        color: window3.pink
                        radius: 2
                    }
                    implicitWidth: 200
                    implicitHeight: 4
                }
                first.handle: Rectangle {
                    id: r1
                    x: control1.leftPadding + control1.first.visualPosition * (control1.availableWidth - width)
                    y: control1.topPadding + control1.availableHeight / 2 - height / 2
                    color: control1.first.pressed ? window3.pink : "#f6f6f6"
                    radius: 13
                    border.width: 0
                    border.color: window3.pink

                    Text {
                        id: rating1
                        y: 24
                        width: 26
                        height: 24
                        color: window3.pink
                        text: Math.round(control1.first.value)
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        font.bold: true
                        font.pointSize: 9
                    }
                    implicitWidth: 26
                    implicitHeight: 26
                }
                first.onVisualPositionChanged: {
                    var x1 = Math.round(first.value)
                    var x2 = Math.round(second.value)
                    if(Math.abs(x2 - x1)===0){
                        rating1.y = -24
                    }
                    else {
                        //rating1.x = 0
                        rating1.y = 24

                    }
                    if(advancedRating.text.length !== 0){
                        advancedRating.text = advancedRating.text.replace('Rating >= ' + Math.round(val1), 'Rating >= ' + Math.round(first.value))
                    }
                    else{
                        advancedRating.text = 'Rating >= ' + Math.round(first.value) + ' AND Rating <= ' + Math.round(second.value)
                    }

                    val1 = Math.round(first.value)

                }
                second.handle: Rectangle {
                    id: r2
                    x: control1.leftPadding + control1.second.visualPosition * (control1.availableWidth - width)
                    y: control1.topPadding + control1.availableHeight / 2 - height / 2
                    color: control1.second.pressed ? window3.pink : "#f6f6f6"
                    radius: 13
                    border.width: 0
                    Text {
                        id: rating2
                        y: 24
                        width: 26
                        height: 24
                        color: window3.pink
                        text: Math.round(control1.second.value)
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        font.bold: true
                        font.pointSize: 9
                    }
                    implicitWidth: 26
                    implicitHeight: 26
                }

                second.onVisualPositionChanged: {
                    var x1 = Math.round(first.value)
                    var x2 = Math.round(second.value)
                    if(Math.abs(x2 - x1)===0){
                        //rating2.x = (22 - Math.abs(r2.x-r1.x))

                        rating2.y = -24

                    }
                    else {
                        //rating2.x = -1
                        rating2.y = 24
                    }





                    if(advancedRating.text.length !== 0){
                        advancedRating.text = advancedRating.text.replace(' AND Rating <= '+ Math.round(val2),' AND Rating <= ' + Math.round(second.value))
                    }
                    else{
                        advancedRating.text = 'Rating >= ' + Math.round(first.value) + ' AND Rating <= ' + Math.round(second.value)
                    }
                    val2 = Math.round(second.value)

                }


                stepSize: 100
            }
            anchors.right: parent.right
            anchors.leftMargin: 20
            anchors.left: parent.left
        }

        Text {
            id: sortTitle1
            x: -198
            y: 6
            height: 39
            color: "#e70c0c"
            text: qsTr("")
            visible: false
            anchors.rightMargin: 0
            font.preferShaping: true
            font.kerning: true
            textFormat: Text.RichText
            font.underline: true
            anchors.leftMargin: 0
            elide: Text.ElideLeft
            fontSizeMode: Text.Fit
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignRight
            font.pixelSize: 20
            anchors.left: parent.left
            font.bold: true
            wrapMode: Text.WordWrap
            anchors.right: parent.right
        }

    }


    MouseArea {
        id: filterButton
        x: 0
        y: 441
        height: 60
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        hoverEnabled: true
        enabled: true
        anchors.right: parent.right
        anchors.left: parent.left
        cursorShape: containsMouse ? Qt.PointingHandCursor : Qt.ArrowCursor
        onEntered: {
            filterArea.color = 'white'
        }
        onExited:  {
            filterArea.color = window3.pink
        }
        onClicked: {
            console.log('clicked')
            MyApp.submit_filter(advancedYear.text + '|' + advancedRating.text + '|' + advancedGenre.text + '|' + advancedSort.text)
            // filter.destroy()
        }

        Rectangle {
            id: submit
            x: 0
            y: -1
            height: 60
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            gradient: Gradient {
                GradientStop {
                    position: 0
                    color: '#000000'            }



                GradientStop {
                    position: 1
                    color: footerColor

                }
            }


            Text {
                id: filterArea
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                wrapMode: Text.WordWrap
                font.pointSize: 18
                font.bold: true
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.fill: parent
                text: 'FILTER MOVIES'
                color: window3.pink


            }
        }
    }









}




/*##^##
Designer {
    D{i:5;anchors_height:100;anchors_width:200;anchors_x:164;anchors_y:26}D{i:4;anchors_height:100;anchors_width:200;anchors_x:164;anchors_y:26}
D{i:27;anchors_x:66}D{i:24;anchors_height:106;anchors_width:200;anchors_x:0;anchors_y:295}
D{i:23;anchors_height:63;anchors_width:200;anchors_x:0;anchors_y:338}D{i:29;anchors_height:31;anchors_width:50;anchors_y:0}
D{i:28;anchors_height:31;anchors_width:50;anchors_y:0}D{i:69;anchors_height:31}D{i:70;anchors_height:31}
D{i:73;anchors_x:6;anchors_y:6}D{i:72;anchors_x:6;anchors_y:6}D{i:67;anchors_height:31}
D{i:66;anchors_height:31}D{i:77;anchors_y:441}D{i:76;anchors_y:441}
}
##^##*/


