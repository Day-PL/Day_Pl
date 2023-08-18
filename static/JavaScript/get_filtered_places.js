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
        for(i=0; i < data.length; i++) {
            let placeBox = showPlace(data[i])
            placeContainer.appendChild(placeBox)
        }
    })
}

function showPlace(place){
    const placeInfo = place['fields'];
    const placeId = place['id'];
    const name = placeInfo['name'];
    const rating = placeInfo['rating'];
    const reviewTotal = placeInfo['review_total'];
    const addressGu = placeInfo['address_gu'];
    const addressLo = placeInfo['address_lo'];
    const addressDetail = placeInfo['address_detail'];
    
    const div = document.createElement('div')
    div.setAttribute('class', 'card')
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
    `
    return div
}

selectElement.addEventListener('change', getFilteredPlace)
