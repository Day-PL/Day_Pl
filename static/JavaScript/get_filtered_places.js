var HOME_PATH = window.HOME_PATH || '.';

window.addEventListener('DOMContentLoaded', getFilteredPlace)
const selectElement = document.querySelector('.search_place_filter');

function getFilteredPlace(){
    const placeContainer = document.querySelector('.place_container')
    placeContainer.innerHTML = ''
    console.log('실행됨');
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

        // var latlngs = new Array();
        // console.log('before latlngs: ', latlngs);
        //! 위도,경도 어레이(latlngs)로 넣기
        for (let i=0; i < data.length; i++) {
            let placeBox = showPlace(data[i]);
            placeContainer.appendChild(placeBox);

            var lng = data[i]['fields']['lng'];
            var lat = data[i]['fields']['lat'];
            // latlngs.push(new naver.maps.LatLng(lng, lat));
            var latlng = new naver.maps.LatLng(lng, lat);
        }
        // console.log('after latlngs:', latlngs);

        var markerList = new Array();
        var infoWindows = new Array();
        // console.log('before markerList: ', markerList)

        for (let j=0; j<latlngs.length; j++) {
            marker = new naver.maps.Marker({
                position: latlngs[j],
                map: map,
                title: ""
                // icon: {
                //     // url: './img/pin_default.png', // HOME_PATH +'/img/example/sp_pins_spot_v3.png', //! 얜 어디에..?
                //     size: new naver.maps.Size(24, 37),
                //     anchor: new naver.maps.Point(12, 37),
                //     origin: new naver.maps.Point(j * 29, 0)
                // }
            });
            marker.set('seq', j);

            markerList.push(marker);
            
            icon = null;
            marker = null;
        }
        console.log('after markerList: ', markerList)
    })
}

function showPlace(place){
    const placeId = place['id'];

    const placeInfo     = place['fields'];
    const name          = placeInfo['name'];
    const rating        = placeInfo['rating'];
    const reviewTotal   = placeInfo['review_total'];
    const addressGu     = placeInfo['address_gu'];
    const addressLo     = placeInfo['address_lo'];
    const addressDetail = placeInfo['address_detail'];
    
    const div = document.createElement('div');
    div.setAttribute('class', 'card');
    div.innerHTML = 
    `
        <div id="place_${placeId}" class="card" style="height:90px; width: 18rem;">
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