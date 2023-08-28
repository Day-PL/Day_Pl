const defaultLat = 126.9896893;
const defaultLng = 37.5737109;
const defaultZoon = 14;

let map = new naver.maps.Map(document.getElementById('map'), {
    zoom: defaultZoon,
    center: new naver.maps.LatLng(defaultLng, defaultLat),
    zoomControl: true,
    zoomControlOptions: {
        style: naver.maps.ZoomControlStyle.SMALL,
        position: naver.maps.Position.TOP_RIGHT
    }
});

const planNames = document.querySelectorAll('.planName');  //! 클릭할 부분들
 
planNames.forEach(function(planName) {
    planName.addEventListener('click', function(){   //! 클릭시 이벤트
        let planId = planName.id;
        let planDivs = document.querySelectorAll('.plan');

        planDivs.forEach(function(planDiv) {

            if (planDiv.classList.contains('plan_' + planId) & planDiv.classList.contains('hide-plan')){  //! 클릭한 플랜의 장소들 토글하기
                planDiv.classList.toggle('hide-plan');
                map = new naver.maps.Map(document.getElementById('map'), {
                    zoom: defaultZoon,
                    center: new naver.maps.LatLng(defaultLng, defaultLat),
                    zoomControl: true,
                    zoomControlOptions: {
                        style: naver.maps.ZoomControlStyle.SMALL,
                        position: naver.maps.Position.TOP_RIGHT
                    }
                });
                // let markerList = new Array();
                let labels = planDiv.querySelectorAll('label');

                let latAvg = 0;
                let lngAvg = 0;
                let len = labels.length;
                labels.forEach(function(label){
                    console.log(label);
                    let lat = label.dataset.lat;
                    let lng = label.dataset.lng;

                    latAvg += lat;
                    lngAvg += lng;

                    let marker = new naver.maps.Marker({
                        position: new naver.maps.LatLng(lng, lat),
                        map: map,
                        title: 1
                    });
                    // markerList.push(marker);
                    marker = null;
                })
                lngAvg /= len;
                latAvg /= len;
                map.setOptions("center", new naver.maps.LatLng(lngAvg, latAvg));
            }else if (planDiv.classList.contains('plan_' + planId) & !planDiv.classList.contains('hide-plan')){
                planDiv.classList.toggle('hide-plan');
                map = new naver.maps.Map(document.getElementById('map'), {
                    zoom: defaultZoon,
                    center: new naver.maps.LatLng(defaultLng, defaultLat),
                    zoomControl: true,
                    zoomControlOptions: {
                        style: naver.maps.ZoomControlStyle.SMALL,
                        position: naver.maps.Position.TOP_RIGHT
                    }
                });
                let labels = planDiv.querySelectorAll('label');
                let latAvg = 0;
                let lngAvg = 0;
                let len = labels.length;
                labels.forEach(function(label){
                    let lat = label.dataset.lat;
                    let lng = label.dataset.lng;
                    latAvg += lat;
                    lngAvg += lng;
                })
                lngAvg /= len;
                latAvg /= len;
                map.setOptions("center", new naver.maps.LatLng(lngAvg, latAvg));
            }else if (! planDiv.classList.contains('hide-plan')){  //! 클릭하지 않은 것들 중 보이는 장소들은 안 보이게 하기
                planDiv.classList.add('hide-plan');
            }
        });
    });
});