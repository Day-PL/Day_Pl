
function getAddress(status, response) {
    if (status === naver.maps.Service.Status.ERROR) {
        return alert('Something Wrong!');
    }
    var items = response.v2.results,
        address = '';
        
    for (var i=0, ii=items.length, item, addrType; i<ii; i++) {
        item = items[i];
        address = makeAddress(item) || '';
        addrType = item.name === 'roadaddr' ? '[도로명 주소]' : '[지번 주소]';
        if (addrType == '[도로명 주소]'){
            document.getElementById('div3').dataset.address = address;
            console.log(document.getElementById('div3').dataset.address);
        }
    }
    //! 도로명 주소 : address
}

//! 위도,경도 객체 -> 주소
function searchCoordinateToAddress(latlng) {
    naver.maps.Service.reverseGeocode({
        coords: latlng,
        orders: [
            naver.maps.Service.OrderType.ADDR,
            naver.maps.Service.OrderType.ROAD_ADDR
        ].join(',')
    }, getAddress);
    
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
//! 사용자 위치 권한 사용가능한지 브라우저에게 물어보기
$(document).ready(function(){
    if ("geolocation" in navigator) {	/* geolocation 사용 가능 */
        // console.log('사용 가능!');
        navigator.geolocation.getCurrentPosition(function(data) {
            var latitude = data.coords.latitude;
            var longitude = data.coords.longitude;
            searchCoordinateToAddress({
                'y' : latitude, 
                '_lat': latitude, 
                'x': longitude, 
                '_lng': longitude
            });
            console.log(document.getElementById('div3'));
        }, function(error) {
            alert(error);
        }, {
            enableHighAccuracy: true,
            timeout: Infinity,
            maximumAge: 0
        });

    } else {
        alert('geolocation 사용 불가능');
    }
    
});

var HOME_PATH = window.HOME_PATH || '.';

window.addEventListener('DOMContentLoaded', getFilteredPlace);
const selectElement = document.querySelector('.search_place_filter');

function getFilteredPlace(){
    const placeContainer = document.querySelector('.place_container');
    placeContainer.innerHTML = '';
    const selectedPlace = selectElement.options[selectElement.selectedIndex].value;
    fetch(`get-filter/${selectedPlace}/`, {
        method : "get",
    })
    .then((response) => response.json())
    .then((data) => {
        // 가져온 데이터로 html에 뿌려주는 코드
        console.log('data 길이: ', data.length)

        //! 네이버 지도에 마커 찍기
        var map = new naver.maps.Map(document.getElementById('map'), {
            zoom: 16,
            center: new naver.maps.LatLng(37.5737109, 126.9896893),
            zoomControl: true,
            zoomControlOptions: {
                style: naver.maps.ZoomControlStyle.SMALL,
                position: naver.maps.Position.TOP_RIGHT
            }
        });
        var markerList = new Array();
        var infoWindows = new Array();

        function getClickHandler(seq) {
            return function(e) {  // 마커를 클릭하는 부분
                var marker = markerList[seq], // 클릭한 마커의 시퀀스로 찾는다.
                    infoWindow = infoWindows[seq]; // 클릭한 마커의 시퀀스로 찾는다

                if (infoWindow.getMap()) {
                    infoWindow.close();
                } else {
                    infoWindow.open(map, marker); // 표출
                }
            }
        }

        
        //! 위도,경도 어레이(latlngs)로 넣기
        for (let i=0; i<data.length; i++) {
            let placeBox = showPlace(data[i]);
            placeContainer.appendChild(placeBox);

            let name = data[i]['fields']['name'];
            let addressGu = data[i]['fields']['address_gu']
            let addressLo = data[i]['fields']['address_lo']
            
            let url = `https://map.naver.com/v5/directions/-/14129228.684381623,4517601.068035996,${addressGu} ${addressLo} ${name},1151030658,PLACE_POI/-/transit?c=15,0,0,0,dh&isCorrectAnswer=true`
            let lng = data[i]['fields']['lng'];
            let lat = data[i]['fields']['lat'];
            let latlng = new naver.maps.LatLng(lng, lat);
            marker = new naver.maps.Marker({
                position: latlng,
                map: map,
                title: name
            });
            let infoWindow = new naver.maps.InfoWindow({
                content: 
                `<div style="text-align:center;padding:10px;"><b><font size=2>
                    <a href="${url}">
                        ${name}
                    </a>
                </font></b></div>`
            }); //! 클릭했을 때 띄워줄 정보 입력
            marker.set('seq', i);

            markerList.push(marker);
            infoWindows.push(infoWindow); 
            
            icon = null;
            marker = null;

            let placeBoxBody = placeBox.querySelector('.card-body')
            let placeId = data[i]['pk']
            printLikeBtn(placeId, placeBoxBody)
            
            naver.maps.Event.addListener(markerList[i], 'click', getClickHandler(i)); // 클릭한 마커 핸들러
        }
        console.log('after markerList: ', markerList);

        const placeNames = document.querySelectorAll('.placeName');
        console.log('placeName 클래스 찾은 것: ', placeNames);
        placeNames.forEach(placeName => {
            placeName.addEventListener('click', function(){
                //! 모두 안 보이게 하기
                placeNames.forEach(place => {
                    var placeId = place.id
                    document.getElementById('detail_' + placeId).style.display='none';
                    console.log(place, '닫기');
                });
                //! 클릭한 것만 보이게 하기
                var place_id = placeName.id
                document.getElementById('div3').style.display='none';
                document.getElementById('div4').style.display='block';
                document.getElementById('detail_' + place_id).style.display='block';
                console.log(place_id, '열기')
        
            });
        });
        const placeDetails = document.querySelectorAll('.close-detail');
        placeDetails.forEach(placeDetail => {
            placeDetail.addEventListener('click', function(){
                placeDetail.parentElement.style.display='none';
                document.getElementById('div3').style.display='block';
                document.getElementById('div4').style.display='none';
            });
        });
    })
}

function createLikeButton(isLiked, placeId) {
    let likeBtn = document.createElement('button');
    likeBtn.setAttribute('class', 'place-like__btn');
    let likeIcon = document.createElement('i');
    
    if (isLiked) {
        likeIcon.setAttribute('class', 'fa-solid fa-star');
    } else {
        likeIcon.setAttribute('class', 'fa-regular fa-star');
    }

    likeBtn.setAttribute('data-placelike', placeId);
    likeBtn.appendChild(likeIcon);
    return likeBtn;
}

function checkIsLiked(placeId) {
    return new Promise((resolve) => {
        fetch(`check-like/${placeId}/`, {
            method: 'GET',
        })
        .then((response) => response.json())
        .then((data) => {
            resolve(data.is_liked);
        })
    })
}

function printLikeBtn(placeId, placeBoxBody) {
    checkIsLiked(placeId)
    .then(result => { 
        let isPlaceLiked = result;
        let likeBtn = createLikeButton(isPlaceLiked, placeId);
        placeBoxBody.insertBefore(likeBtn, placeBoxBody.firstChild)
    });
}

function showPlace(place){
    const placeId   = place['pk'];
    const placeInfo = place['fields'];
    
    const name          = placeInfo['name'];
    const rating        = placeInfo['rating'];
    const reviewTotal   = placeInfo['review_total'];
    const addressGu     = placeInfo['address_gu'];
    const addressLo     = placeInfo['address_lo'];
    const addressDetail = placeInfo['address_detail'];
    
    const div = document.createElement('div');
    div.setAttribute('class', 'card');
    div.innerHTML = 
    // style="height:90px; width: 18rem;"
    `
        <div id="place_${placeId}" class="card">
            <div class="card-body">
                <h6 class="card-title">
                    <span class="placeName" id="${placeId}">
                        <font size=2>${name}</font>
                    </span>
                    &nbsp;
                    <a href="https://map.naver.com/v5/search/${addressGu} ${addressLo} ${name}/place" target="_blank">
                        <font size=1>네이버플레이스</font>
                    </a>
                    &nbsp;
                    <a href="https://map.naver.com/v5/directions/-/14129228.684381623,4517601.068035996,${addressGu} ${addressLo} ${name},1151030658,PLACE_POI/-/transit?c=15,0,0,0,dh&isCorrectAnswer=true" target="_blank">
                        <font size=1>길찾기</font>
                    </a>
                </h6>   
                <font size=1>
                    <p class="card-text">
                        별점: ${rating}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;리뷰수: ${ reviewTotal }
                    </p>
                </font>
                <font size=1>
                    <p class="card-text">
                        ${addressGu} ${addressLo} ${addressDetail}
                    </p>
                </font>
                <button data-place="${placeId}">플랜에 추가</button>
            </div>
        </div>
    `;
    return div;
}

selectElement.addEventListener('change', getFilteredPlace);


