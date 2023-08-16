const plusBtn = document.querySelector('.place-plus__btn')
const placeContainer = document.querySelector('.place__container')

// TODO: 하드코딩 변수 옮기기
PLACE_CURRENT = 1;
PLACE_TOTAL = 10;

function addPlaceItem(placeName) {
  let uuid = self.crypto.randomUUID();

  const placeBox = document.createElement('li');
  placeBox.setAttribute('class', 'place__box');
  placeBox.setAttribute('data-id', uuid)
  placeBox.innerHTML = `
    <div class="place__item">
      <span class="place-like__btn">
        <i class="fa-solid fa-star"></i>
      </span>
      <span class="place__name">${placeName}</span>
      <button class="place-remove__btn">
        <i class="fa-solid fa-xmark" data-id=${uuid}></i>
      </button>
    </div>
    `
  return placeBox
}

// TODO: 이름 가져오는 코드 추가 구현 필요
plusBtn.addEventListener('click', () => {
  if (PLACE_CURRENT < PLACE_TOTAL) {
    const placeBox = addPlaceItem('장소')
    placeContainer.appendChild(placeBox)
    PLACE_CURRENT++;
  }
});

placeContainer.addEventListener('click', event => {
  const id = event.target.dataset.id;
  if (id) {
    const toBeDeleted = document.querySelector(`.place__box[data-id="${id}"]`);
    toBeDeleted.remove();
    PLACE_CURRENT--;
  }
})