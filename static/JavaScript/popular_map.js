const defaultLat = 126.9896893;
const defaultLng = 37.5737109;
const defaultZoom = 14;

let map = new naver.maps.Map(document.getElementById('map'), {
    zoom: defaultZoom,
    center: new naver.maps.LatLng(defaultLng, defaultLat),
    zoomControl: true,
    zoomControlOptions: {
        style: naver.maps.ZoomControlStyle.SMALL,
        position: naver.maps.Position.TOP_RIGHT
    }
});

function printMap(placeList) {
  map = new naver.maps.Map(document.getElementById('map'), {
    zoom: defaultZoom,
    center: new naver.maps.LatLng(defaultLng, defaultLat),
    zoomControl: true,
    zoomControlOptions: {
      style: naver.maps.ZoomControlStyle.SMALL,
      position: naver.maps.Position.TOP_RIGHT,
    },
  })

  var polyline = new naver.maps.Polyline({
    map: map,
    path: [],
    strokeColor: '#5347AA',
    strokeWeight: 2
  });

  let placeLis = placeList.querySelectorAll('.place-list');

  let latAvg = 0;
  let lngAvg = 0;
  let len = placeLis.length;

  var markerList = new Array();
  var infoWindows = new Array();

  for (let i=0; i<placeLis.length; i++) {
    var placeLi = placeLis[i]
    let lat     = placeLi.dataset.lat;
    let lng     = placeLi.dataset.lng;
    let url     = placeLi.dataset.url;
    let name    = placeLi.dataset.name;
    
    var point = new naver.maps.LatLng(lng, lat);
    var path = polyline.getPath();
    path.push(point);

    latAvg += lat;
    lngAvg += lng;

    let marker = new naver.maps.Marker({
      position: new naver.maps.LatLng(lng, lat),
      map: map,
      title: 1
    });

    //! 클릭했을 때 띄워줄 정보 입력
    let infoWindow = new naver.maps.InfoWindow({
      content: `
                <div style="text-align:center;padding:10px;">
                  <b>
                    <font size=2>
                      <a href="${url}" target="_blank">
                        ${name}
                      </a>
                    </font>
                  </b>
                </div>
                `
    });
    marker.set('seq', i);
    markerList.push(marker);
    infoWindows.push(infoWindow); 
    marker = null
    naver.maps.Event.addListener(markerList[i], 'click', getClickHandler(markerList, infoWindows, i)); // 클릭한 마커 핸들러
  }
  lngAvg /= len;
  latAvg /= len;
  map.setOptions("center", new naver.maps.LatLng(lngAvg, latAvg));
}


function getClickHandler(markerList, infoWindows, seq) {
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