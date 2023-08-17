const placeNames = document.querySelectorAll('.placeName');

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