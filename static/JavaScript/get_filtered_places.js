var HOME_PATH = window.HOME_PATH || '.';

window.addEventListener('DOMContentLoaded', getFilteredPlace)
const selectElement = document.querySelector('.search_place_filter');

window.addEventListener('DOMContentLoaded', getFilteredPlace)

function getFilteredPlace(){
    const placeContainer = document.querySelector('.place_container')
    placeContainer.innerHTML = ''
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
            var name = data[i]['fields']['name'];
            var lng = data[i]['fields']['lng'];
            var lat = data[i]['fields']['lat'];
            var latlng = new naver.maps.LatLng(lng, lat);
            marker = new naver.maps.Marker({
                position: latlng,
                map: map,
                title: name
            });
            var infoWindow = new naver.maps.InfoWindow({
                content: `<div style="text-align:center;padding:10px;"><b><font size=2>${name}</font></b></div>`
            }); // 클릭했을 때 띄워줄 정보 입력
            marker.set('seq', i);

            markerList.push(marker);
            infoWindows.push(infoWindow); 
            
            icon = null;
            marker = null;
            
            naver.maps.Event.addListener(markerList[i], 'click', getClickHandler(i)); // 클릭한 마커 핸들러
            

            let placeBoxBody = placeBox.querySelector('.card-body')

            let placeId = data[i]['pk']
            printLikeBtn(placeId, placeBoxBody)
        }
        console.log('after markerList: ', markerList)
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
    const placeInfo = place['fields'];
    const placeId = place['pk'];
    const name = placeInfo['name'];
    const rating = placeInfo['rating'];
    const reviewTotal = placeInfo['review_total'];
    const addressGu = placeInfo['address_gu'];
    const addressLo = placeInfo['address_lo'];
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


