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
        console.log(data)
        for(i=0; i < data.length; i++) {
            let placeBox = showPlace(data[i])
            placeContainer.appendChild(placeBox)
        }
    })
}

function showPlace(place){
    const placeInfo = place['fields'];
    
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
        <div class="card-body">
        <a href="https://map.naver.com/v5/search/${addressGu} ${addressLo} ${name}/place" target="_blank"><h6 class="card-title">${name}</h6></a>
        <p class="card-text">별점: ${rating}  리뷰수: ${ reviewTotal }</p>
        <p class="card-text">${addressGu} ${addressLo} ${addressDetail}</p>
        <a href="https://map.naver.com/v5/directions/-/14129228.684381623,4517601.068035996,${addressGu} ${addressLo} ${name},1151030658,PLACE_POI/-/transit?c=15,0,0,0,dh&isCorrectAnswer=true" target="_blank">길찾기</a>
    `
    return div
}

selectElement.addEventListener('change', getFilteredPlace)
