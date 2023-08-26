// import * as module from './get_filtered_places';

module.getUserAddress();

let clickElements = document.getElementsByClassName('planName');
let placeElements = document.getElementsByClassName('plan');

Array.from(clickElements).forEach(function(clickElement) {
    let clickPlanId = clickElement.id;
    
    clickElement.addEventListener('click', function(){
        // 모두 숨기고 클릭한 것만 보여주기
        Array.from(placeElements).forEach(function(placeElement) {
            if(placeElement.classList.contains('plan_' + clickPlanId)){
                placeElement.classList.toggle('hide-plan');
            }else if (! placeElement.classList.contains('hide-plan')){
                placeElement.classList.add('hide-plan')
            }
        });
    });
});

const div = document.createElement('div');
div.setAttribute('class', 'card');
div.innerHTML = 
`
<div id="place_${placeId}" class="card">
    <div class="card-body">

        <h6 class="card-title">
            <span class="placeName" id="${placeId}">
                <font size=2>${name}</font>
            </span>
            &nbsp;
            <a href="https://map.naver.com/v5/search/${addressGu} ${name}/place" target="_blank">
                <font size=1>네이버플레이스</font>
            </a>
            &nbsp;
            <a href="https://map.naver.com/v5/directions/-/14129228.684381623,4517601.068035996,${addressGu} ${name},1151030658,PLACE_POI/-/transit?c=15,0,0,0,dh&isCorrectAnswer=true" target="_blank">
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