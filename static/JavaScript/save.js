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

const planNames = document.querySelectorAll('.popular-plan__title');  //! 클릭할 부분
planNames.forEach(function(planName) {
    const a_tag = planName.parentElement.parentElement;
    a_tag.addEventListener('click', function(event){   //! 클릭시 이벤트
        event.stopPropagation();
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
                
                var polyline = new naver.maps.Polyline({
                    map: map,
                    path: [],
                    strokeColor: '#5347AA',
                    strokeWeight: 2
                });
                
                // let markerList = new Array();
                let labels = planDiv.querySelectorAll('label');

                let latAvg = 0;
                let lngAvg = 0;
                let len = labels.length;
                labels.forEach(function(label){
                    let lat = label.dataset.lat;
                    let lng = label.dataset.lng;

                    latAvg += lat;
                    lngAvg += lng;

                    var point = new naver.maps.LatLng(lng, lat);

                    var path = polyline.getPath();
                    path.push(point);

                    let marker = new naver.maps.Marker({
                        position: new naver.maps.LatLng(lng, lat),
                        map: map,
                        title: 1,
                        // icon: {
                        //     url   : '../img/purple_marker.png',
                        //     size  : new naver.maps.Size(50, 52),
                        //     origin: new naver.maps.Point(0, 0),
                        //     anchor: new naver.maps.Point(25, 26)
                        // }
                    });
                    
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
                    status1 = $('input:checkbox[id="' + label.getAttribute('for') + '"]').is(':checked');
                })
                lngAvg /= len;
                latAvg /= len;
                map.setOptions("center", new naver.maps.LatLng(lngAvg, latAvg));
            } else if (! planDiv.classList.contains('hide-plan')){  //! 클릭하지 않은 것들 중 보이는 장소들은 안 보이게 하기
                planDiv.classList.add('hide-plan');
            }
        });
    });
});

const hearts = document.querySelectorAll('.heart'); //! 변경

hearts.forEach(function(heart){
    const planId = heart.dataset.planid;
    const planTitle = heart.dataset.plantitle;
    const a = heart.parentElement.parentElement.parentElement;
    const planType = heart.dataset.plantype;
    const modifyPlan = a.querySelectorAll('#modifyPlan');
    const removePlan = a.querySelectorAll('#removePlan');
    heart.addEventListener('click', function(event){
        event.stopPropagation();
        if (heart.classList.contains('fa-solid')) {
            heart.classList.remove('fa-solid');
            heart.classList.add('fa-regular');
            fetch(`${planId}/like/remove`, {
                method : "get",
            })
        }else {
            heart.classList.remove('fa-regular');
            heart.classList.add('fa-solid');
            fetch(`${planId}/like/add`, {
                method : "get",
            })
        }
    });
    if (modifyPlan.length) {
        modifyPlan[0].addEventListener('click', function(event){
            event.stopPropagation();
            fetch(`${planId}/modify`, {
                method : 'get',
            })
            .then(window.location.href = `/saves/${planId}/modify`)
        });
        removePlan[0].addEventListener('click', function(event){
            event.stopPropagation();
            fetch(`${planId}/remove`, {
                method : 'get',
            })
            .then(() => {
                alert(`플랜명 : "${planTitle}" 삭제`)
            })
            .then(location.reload())
        });
    }
});
