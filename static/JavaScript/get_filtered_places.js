const newPlanPlaceContainer = document.querySelector('.place_container');
const placeSearchInput = document.querySelector('.new-plan-place-search__input')
const searchClearBtn = document.querySelector('.search-clear__btn');

getUserAddress()

window.addEventListener('DOMContentLoaded', () => {
    getFilteredPlace('')
}); //! 모두 로딩되고 보내준 장소 데이터들 가져와서 네이버 지도에 마커 표시 및 관련 기능(좋아요,추가)

const selectElement = document.querySelector('.search_place_filter'); 
selectElement.addEventListener('change',  () => {
    getFilteredPlace('')
}); //! (필터가) 바뀔 때마다 장소 데이터들 가져와서 네이버 지도에 마커 표시 및 관련 기능(좋아요,추가)
let userAddress = '';

placeSearchInput.addEventListener('keyup', () => {
    getFilteredPlace(placeSearchInput.value)
})

searchClearBtn.addEventListener('click', () => {
    placeSearchInput.value = '';
    placeSearchInput.focus();
    getFilteredPlace('');
})

//! 사용자 위치 권한 사용가능한지 브라우저에게 물어보기 (가장 먼저 실행, 가장 마지막에 끝)
function getUserAddress(){
    window.addEventListener('DOMContentLoaded', function(){
        console.log('유저 위치 정보 가져오기 시작')
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(function(data) {
                let latitude = data.coords.latitude;
                let longitude = data.coords.longitude;
                console.log(latitude, longitude);
                
                getDetailedAddress(latitude, longitude)
                .then(result => {
                    console.log(result);
                    userAddress = result;
                    return userAddress;
                })
                .catch(error => {
                    console.error('Error:', error);
                    userAddress = '';
                });
                
            }, function(error) {
                // alert(error);
            }, {
                enableHighAccuracy: true,
                timeout: Infinity,
                maximumAge: 0
            });
        } else {
            alert('geolocation 사용 불가능');
        }
    });
}
async function getDetailedAddress(lat, lng) {
    console.log('getDetailedAddress 실행');
    const latlng = new naver.maps.LatLng(lat, lng);
    try {
        const response = await new Promise((resolve, reject) => {
            naver.maps.Service.reverseGeocode({
                coords: latlng,
                orders: [
                    naver.maps.Service.OrderType.ADDR,
                    naver.maps.Service.OrderType.ROAD_ADDR
                ].join(',')
            }, (status, response) => {
                if (status === naver.maps.Service.Status.ERROR) {
                    reject('Error while reverse geocoding');
                } else {
                    resolve(response);
                }
            });
        });

        const items = response.v2.results;
        for (let i = 0; i < items.length; i++) {
            const item = items[i];
            if (item.name === 'roadaddr') {
                const address = makeAddress(item) || '';
                return address;
            }
        }
        return '';
    } catch (error) {
        console.error('Error:', error);
        return '';
    }
}
function makeAddress(item) { //! 위도,경도 객체 -> 주소
    console.log('makeAddress 실행');
    if (!item) {
        return;
    }
    var name   = item.name,
        region = item.region,
        land   = item.land,
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

function getFilteredPlace(placeSearchKeyword){
    if (placeSearchKeyword === '') {
        placeSearchKeyword = 'none'
    }
    console.log('getFilteredPlace 실행');
    newPlanPlaceContainer.innerHTML = '';
    const encodedKeyword = encodeURIComponent(placeSearchKeyword)
    const selectedPlace = selectElement.options[selectElement.selectedIndex].value;
    fetch(`/get-filter/${selectedPlace}/${encodedKeyword}/`, {
        method : "GET",
    })
    .then((response) => response.json())
    .then((data) => {
        console.log('data 길이: ', data.length)
        if (!data.length) {
            newPlanPlaceContainer.innerHTML = '';
            const div = document.createElement('div');
            div.innerText = '해당하는 정보가 없습니다'
            newPlanPlaceContainer.appendChild(div)
        }
        newPlanPlaceContainer.innerHTML = '';
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
            let placeBox = printPlace(data[i]);
            newPlanPlaceContainer.appendChild(placeBox);

            let name = data[i]['fields']['name'];
            let addressGu = data[i]['fields']['address_gu']
            let addressLo = data[i]['fields']['address_lo']
            
            let url = data[i]['fields']['url'];
            let lng = data[i]['fields']['lng'];
            let lat = data[i]['fields']['lat'];
            let latlng = new naver.maps.LatLng(lng, lat);

            let marker = new naver.maps.Marker({
                position: latlng,
                map: map,
                title: name
            });

            let infoWindow = new naver.maps.InfoWindow({
                content: 
                `
                <div style="text-align:center;padding:10px;">
                    <b>
                        <font size=2>
                            <a href="${url}" target="_blank">
                                ${name}
                            </a>
                        </font>
                    </b>
                </div>`
            }); //! 클릭했을 때 띄워줄 정보 입력
            marker.set('seq', i);

            markerList.push(marker);
            infoWindows.push(infoWindow); 

            marker = null;
            
            naver.maps.Event.addListener(markerList[i], 'click', getClickHandler(i)); // 클릭한 마커 핸들러
            

            let placeBoxBody = placeBox.querySelector('.card-title')

            let placeId = data[i]['pk']
            printPlaceLikeBtn(placeId, placeBoxBody)
        }

        const placeNames = document.querySelectorAll('.place_name');
        console.log('placeName 클래스 찾은 것: ', placeNames);
        placeNames.forEach(placeName => {
            placeName.addEventListener('click', function(){
                //! 모두 안 보이게 하기
                placeNames.forEach(place => {
                    var placeId = place.id
                    document.getElementById('detail_' + placeId).style.display='none';
                });
                //! 클릭한 것만 보이게 하기
                var place_id = placeName.id
                document.getElementById('div3').style.display='none';
                document.getElementById('div4').style.display='block';
                document.getElementById('detail_' + place_id).style.display='block';
        
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
function printPlace(place){
    const placeInfo     = place['fields'];
    const placeId       = place['pk'];
    const typeCode      = placeInfo['type_code'];
    const name          = placeInfo['name'];
    const rating        = placeInfo['rating'];
    const reviewTotal   = placeInfo['review_total'];
    const addressGu     = placeInfo['address_gu'];
    const addressLo     = placeInfo['address_lo'];
    const addressDetail = placeInfo['address_detail'];
    const placeUrl      = placeInfo['url'];
    const naverPlaceId  = placeInfo['naver_place_id'];
    
    const cardBox = document.createElement('div');
    cardBox.setAttribute('class', 'card p-3 mb-2');
    cardBox.setAttribute('id', `place_${placeId}`)
    if (typeCode === 21) {
        if (name.includes("]")) {
            const nameSplit = name.split("]")
            const nameFirst = nameSplit[0] + "]"
            const nameRest = nameSplit.slice(1).join(" ")
            cardBox.innerHTML = 
            `
            <div class="card-title">
                <a class="place_name fs-5 fw-bold" id="${placeId}" data-placename="${placeId}">${nameFirst}</br>${nameRest}</a>
            </div>
            <div class="card-body p-0">
                <div class="place__links py-2">
                    <a href="${placeUrl}" target="_blank">예매하기</a>
                    <a href="https://map.naver.com/p/directions/-/,,,${naverPlaceId},PLACE_POI/-/walk?c=13.00,0,0,0,dh" target="_blank">길찾기</a>   
                </div>
                <p class="card-text">${addressGu} ${addressLo} ${addressDetail}</p>
                <div class="mt-2 text-center">
                    <button class="add-plan__btn btn btn-primary btn-sm fw-bold" data-place="${placeId}">플랜에 추가하기</button>
                </div>
            </div>
        `;
        } else {
            cardBox.innerHTML = 
        `
        <div class="card-title">
            <a class="place_name fs-5 fw-bold" id="${placeId}" data-placename="${placeId}">${name}</a>
        </div>
        <div class="card-body p-0">
            <div class="place__links py-2">
                <a href="${placeUrl}" target="_blank">예매하기</a>
                <a href="https://map.naver.com/p/directions/-/,,,${naverPlaceId},PLACE_POI/-/walk?c=13.00,0,0,0,dh" target="_blank">길찾기</a>
            </div>
            <p class="card-text">${addressGu} ${addressLo} ${addressDetail}</p>
            <div class="mt-2 text-center">
                <button class="add-plan__btn btn btn-primary btn-sm fw-bold" data-place="${placeId}">플랜에 추가하기</button>
            </div>
        </div>
    `;}
    } else {
        cardBox.innerHTML = 
    `
        <div class="card-title">
            <a class="place_name fs-5 fw-bold" id="${placeId}" data-placename="${placeId}">${name}</a>
        </div>
        <div class="card-body p-0">
            <div class="place__links py-2">
                <a class="me-1 fs-6 fw-semibold" href="${placeUrl}" target="_blank">네이버플레이스</a>
                <a class="fs-6 fw-semibold" href="https://map.naver.com/p/directions/-/,,,${naverPlaceId},PLACE_POI/-/walk?c=13.00,0,0,0,dh" target="_blank">길찾기</a>
            </div>
            <p class="card-text">별점: ${rating}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;리뷰수: ${ reviewTotal }</p>
            <p class="card-text">${addressGu} ${addressLo} ${addressDetail}</p>
            <div class="mt-2 text-center">
                <button class="add-plan__btn btn btn-primary btn-sm fw-bold" data-place="${placeId}">플랜에 추가하기</button>
            </div>
        </div>
    `;
    }
    return cardBox;
}
