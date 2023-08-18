var HOME_PATH = window.HOME_PATH || '.';

//! 지도의 옵션
var mapOptions = {
    center: new naver.maps.LatLng(37.5713, 126.9883),
    zoom: 15, //! 지도의 초기 줌 레벨
    minZoom: 11, //! 지도의 최소 줌 레벨
    zoomControl: true, // 줌 컨트롤의 표시 여부
    zoomControlOptions: { // 줌 컨트롤의 옵션
        position: naver.maps.Position.TOP_RIGHT
    },
    mapTypeControl: true
}

var map = new naver.maps.Map('map', mapOptions);
// naver.maps.Event.addListener(map, 'zoom_changed', function (zoom) {
//     console.log('zoom:' + zoom);
// });

//! 지도 인터랙션 옵션
$("#interaction").on("click", function(e) {
    e.preventDefault();
    if (map.getOptions("draggable")) {
        map.setOptions({ //지도 인터랙션 끄기
            draggable: false,
            pinchZoom: false,
            scrollWheel: false,
            keyboardShortcuts: false,
            disableDoubleTapZoom: true,
            disableDoubleClickZoom: true,
            disableTwoFingerTapZoom: true
        });
        $(this).removeClass("control-on");
    } else {
        map.setOptions({ //지도 인터랙션 켜기
            draggable: true,
            pinchZoom: true,
            scrollWheel: true,
            keyboardShortcuts: true,
            disableDoubleTapZoom: false,
            disableDoubleClickZoom: false,
            disableTwoFingerTapZoom: false
        });

        $(this).addClass("control-on");
    }
});

//! 타일 fadeIn 효과
$("#tile-transition").on("click", function(e) {
    e.preventDefault();

    if (map.getOptions("tileTransition")) {
        map.setOptions("tileTransition", false); //타일 fadeIn 효과 끄기
        $(this).removeClass("control-on");
    } else {
        map.setOptions("tileTransition", true); //타일 fadeIn 효과 켜기
        $(this).addClass("control-on");
    }
});
//! min/max 줌 레벨
$("#min-max-zoom").on("click", function(e) {
    e.preventDefault();

    if (map.getOptions("minZoom") === 10) {
        map.setOptions({
            minZoom: 7,
            maxZoom: 21
        });
        $(this).val(this.name + ': 7 ~ 21');
    } else {
        map.setOptions({
            minZoom: 10,
            maxZoom: 21
        });
        $(this).val(this.name + ': 10 ~ 21');
    }
});

//! 지도 컨트롤
$("#controls").on("click", function(e) {
    e.preventDefault();

    if (map.getOptions("scaleControl")) {
        map.setOptions({ //모든 지도 컨트롤 숨기기
            scaleControl: false,
            logoControl: false,
            mapDataControl: false,
            zoomControl: false,
            mapTypeControl: false
        });
        $(this).removeClass('control-on');
    } else {
        map.setOptions({ //모든 지도 컨트롤 보이기
            scaleControl: true,
            logoControl: true,
            mapDataControl: true,
            zoomControl: true,
            mapTypeControl: true
        });
        $(this).addClass('control-on');
    }
});

$("#interaction, #tile-transition, #controls").addClass("control-on");


var infoWindow = new naver.maps.InfoWindow({
    anchorSkew: true
});

map.setCursor('pointer');

var cityhall = new naver.maps.LatLng(37.5666805, 126.9784147),
    map = new naver.maps.Map('map', {
        center: cityhall.destinationPoint(0, 500),
        zoom: 15
    }),
    marker = new naver.maps.Marker({
        map: map,
        position: cityhall
    });

function searchCoordinateToAddress(latlng) {

    infoWindow.close();

    naver.maps.Service.reverseGeocode({
        coords: latlng,
        orders: [
            naver.maps.Service.OrderType.ADDR,
            naver.maps.Service.OrderType.ROAD_ADDR
        ].join(',')
    }, function(status, response) {
        if (status === naver.maps.Service.Status.ERROR) {
            return alert('Something Wrong!');
        }

        var items = response.v2.results,
            address = '',
            htmlAddresses = [];

        for (var i=0, ii=items.length, item, addrType; i<ii; i++) {
            item = items[i];
            address = makeAddress(item) || '';
            addrType = item.name === 'roadaddr' ? '[도로명 주소]' : '[지번 주소]';

            htmlAddresses.push((i+1) +'. '+ addrType +' '+ address);
        }

        infoWindow.setContent([
            '<div style="padding:10px;min-width:200px;line-height:150%;">',
            '<h4 style="margin-top:5px;">검색 좌표</h4><br />',
            htmlAddresses.join('<br />'),
            '</div>'
        ].join('\n'));

        infoWindow.open(map, latlng);
    });
}
//! 좌표계 변환하기
function initGeocoder() {
    var tm128 = (310917, 552751);
    var naverCoord = naver.maps.TransCoord.fromTM128ToNaver(tm128); // TM128 -> NAVER

    infoWindow = new naver.maps.InfoWindow({
        content: ''
    });
    console.log('NAVER: ' + naverCoord.toString());
}
naver.maps.onJSContentLoaded = initGeocoder;

function searchAddressToCoordinate(address) {
    naver.maps.Service.geocode({
        query: address
    }, function(status, response) {
        if (status === naver.maps.Service.Status.ERROR) {
            return alert('Something Wrong!');
        }
        if (response.v2.meta.totalCount === 0) {
            return alert('totalCount' + response.v2.meta.totalCount);
        }
        var htmlAddresses = [],
            item = response.v2.addresses[0],
            point = new naver.maps.Point(item.x, item.y);
        if (item.roadAddress) {
            htmlAddresses.push('[도로명 주소] ' + item.roadAddress);
        }

        //! 마커 표시
        var marker = new naver.maps.Marker({
            position: new naver.maps.LatLng(37.5713, 126.9883),
            map: map
        });

        infoWindow.setContent([
            '<font size=1><div style="padding:10px;min-width:100px;line-height:150%;">',
            // '<h6 style="margin-top:5px;">검색 주소 : '+ address +'</h6><br />',
            htmlAddresses.join('<br />'),
            '</div></font>'
        ].join('\n'));

        map.setCenter(point);
        infoWindow.open(map, point);
    });
}
//! 맨 처음 주소
function initGeocoder() {
    map.addListener('click', function(e) {
        searchCoordinateToAddress(e.coord);
    });

    $('#address').on('keydown', function(e) {
        var keyCode = e.which;

        if (keyCode === 13) { // Enter Key
            searchAddressToCoordinate($('#address').val());
        }
    });

    $('#submit').on('click', function(e) {
        e.preventDefault();

        searchAddressToCoordinate($('#address').val());
    });
    //! 주소 들어가는 곳
    searchAddressToCoordinate('종로 3가');
}

function makeAddress(item) {
    if (!item) {
        return;
    }

    var name = item.name,
        region = item.region,
        land = item.land,
        isRoadAddress = name === 'roadaddr';

    var sido = '', sigugun = '', dongmyun = '', ri = '', rest = '';
    if (hasArea(region.area1)) {
        sido = region.area1.name;
    }
    if (hasArea(region.area2)) {
        sigugun = region.area2.name;
    }
    if (hasArea(region.area3)) {
        dongmyun = region.area3.name;
    }
    if (hasArea(region.area4)) {
        ri = region.area4.name;
    }
    if (land) {
        if (hasData(land.number1)) {
            if (hasData(land.type) && land.type === '2') {
                rest += '산';
            }
            rest += land.number1;
            if (hasData(land.number2)) {
                rest += ('-' + land.number2);
            }
        }
        if (isRoadAddress === true) {
            if (checkLastString(dongmyun, '면')) {
                ri = land.name;
            } else {
                dongmyun = land.name;
                ri = '';
            }
            if (hasAddition(land.addition0)) {
                rest += ' ' + land.addition0.value;
            }
        }
    }
    return [sido, sigugun, dongmyun, ri, rest].join(' ');
}

function hasArea(area) {
    return !!(area && area.name && area.name !== '');
}

function hasData(data) {
    return !!(data && data !== '');
}

function checkLastString (word, lastString) {
    return new RegExp(lastString + '$').test(word);
}

function hasAddition (addition) {
    return !!(addition && addition.value);
}

naver.maps.onJSContentLoaded = initGeocoder;