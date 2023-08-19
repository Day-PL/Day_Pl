const planSubmitBtn = document.querySelector('.plan-submit__btn')
const selectedPlaceContainer = document.querySelector('.selected-place__container')
const placeContainer = document.querySelector('.place_container')
const heartBtn = document.querySelector('.heart__btn')

let isLiked = false
heartBtn.addEventListener('click', () => {
  if (isLiked == true) {
    heartBtn.innerHTML = '<i class="fa-regular fa-heart"></i>'
    isLiked = false
  } else {
    heartBtn.innerHTML = '<i class="fa-solid fa-heart"></i>'
    isLiked = true
  }
})

let place_current = 1;
const PLACE_TOTAL = 10;

function addPlaceItem(placeName, placeId) {
  let uuid = self.crypto.randomUUID();

  // placeid를 이용하지 않고 uuid를 사용하는 이유 :
  // uuid 기반으로 삭제되기 때문에 같은 장소 두 번 추가해도 선택한 값만 삭제되도록 하기 위해
  const placeBox = document.createElement('li');
  placeBox.setAttribute('class', 'place__box');
  placeBox.setAttribute('draggable', 'true');
  placeBox.setAttribute('data-id', uuid);
  placeBox.setAttribute('data-place', `${placeId}`);
  placeBox.innerHTML = `
    <div class="place__item">
      <span class="place__name">${placeName}</span>
      <button class="place-remove__btn">
        <i class="fa-solid fa-xmark" data-id=${uuid}></i>
      </button>
    </div>
    `
  printLikeBtn(placeId, placeBox)
  return placeBox
}

selectedPlaceContainer.addEventListener('click', event => {
  const id = event.target.dataset.id;
  if (id) {
    const toBeDeleted = document.querySelector(`.place__box[data-id="${id}"]`);
    toBeDeleted.remove();
    place_current--;
    return;
  }

  const likePlaceId = event.target.dataset.placelike;
  if (likePlaceId) {
    updatePlaceLike(likePlaceId)
  }
})

placeContainer.addEventListener('click', event => {
  const placeId = event.target.dataset.place;
  if (placeId && place_current < PLACE_TOTAL) {
    const placeName = document.getElementById(`${placeId}`).innerText;
    const placeBox = addPlaceItem(placeName, placeId)
    selectedPlaceContainer.appendChild(placeBox)
    place_current++;
    return;
  }

  const likePlaceId = event.target.dataset.placelike;
  if (likePlaceId) {
    updatePlaceLike(likePlaceId)
  }
})

function updatePlaceLike(likePlaceId) {
  if (likePlaceId) {
    fetch('', {
      method: 'PUT',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ placeid: likePlaceId }),
    })
    .then((response) => response.json())
    .then((data) => {
      const placeLikeBtn = document.querySelectorAll(`.place-like__btn[data-placelike="${likePlaceId}"]`)
      placeLikeBtn.forEach(btn => {
        if (data.isliked === true) {
          btn.innerHTML = '<i class="fa-solid fa-star"></i>'
        } else {
          btn.innerHTML = '<i class="fa-regular fa-star"></i>'
        }
      })

    })
  }
}

planSubmitBtn.addEventListener('click', () => {
  const planTitle = getPlanTitle()
  const placeBoxItems = selectedPlaceContainer.querySelectorAll('.place__box');
  const placeIds = Array.from(placeBoxItems).map(item => item.dataset.place);
  console.log(placeIds)

  fetch('', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
    },
    body : JSON.stringify({ 
      plantitle: planTitle,
      placeids: placeIds,
      isliked: isLiked, }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === 'success') {
        location.reload()
      } else {
        console.log('에러 발생')
      }
    })
})

function getPlanTitle() {
  const planTitleInput = document.querySelector('.plan-title');
  let planTitle = ''
  if (planTitleInput.value === '') {
    planTitle = planTitleInput.getAttribute('placeholder');
  } else {
    planTitle = planTitleInput.value;
  }
  return planTitle
}

// drag & drop event
let currentItemIndex = null;
let currentItem = null;

selectedPlaceContainer.addEventListener('dragstart', event => {
  currentItem = event.target.closest('li');
  const listArr = [...currentItem.parentElement.children];
  currentItemIndex = listArr.indexOf(currentItem);
});

selectedPlaceContainer.addEventListener('dragover', event => {
  event.preventDefault();
});

selectedPlaceContainer.addEventListener('drop', event => {
  event.preventDefault();

  const currentDropItem = event.target.closest('li');
  const listArr = [...currentItem.parentElement.children];
  const dropItemIndex = listArr.indexOf(currentDropItem);
  
  if (currentItemIndex < dropItemIndex) {
    currentDropItem.after(currentItem)
  } else {
    currentDropItem.before(currentItem)
  }
});
