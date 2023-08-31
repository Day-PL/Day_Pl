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
  let placeLis = placeList.querySelectorAll('.place-list');

  let latAvg = 0;
  let lngAvg = 0;
  let len = placeLis.length;
  placeLis.forEach((placeLi) => {
    let lat = placeLi.dataset.lat;
    let lng = placeLi.dataset.lng;

    latAvg += lat;
    lngAvg += lng;

    let marker = new naver.maps.Marker({
      position: new naver.maps.LatLng(lng, lat),
      map: map,
      title: 1
    });
    marker = null
  })
  lngAvg /= len;
  latAvg /= len;
  map.setOptions("center", new naver.maps.LatLng(lngAvg, latAvg));
}
