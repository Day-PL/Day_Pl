const placeNames = document.querySelectorAll('.placeName');
placeNames.forEach(placeName => {
    placeName.addEventListener('click', function(){
        var place_id = placeName.id
        console.log('detail_' + place_id)
        document.getElementById('div3').style.display='none';
        // document.getElementById('div4').style.display='block'; 
        document.getElementById('detail_' + place_id).style.display='block'
    });
});

const placeDetails = document.querySelectorAll('.close-detail');
placeDetails.forEach(placeDetail => {
    placeDetail.addEventListener('click', function(){
        placeDetail.parentElement.style.display='none';
        document.getElementById('div3').style.display='block';
    });
});