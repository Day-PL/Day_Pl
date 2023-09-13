const planSubmitBtn = document.querySelector('.plan-submit__btn');
const modalSubmitBtn = document.querySelector('.plan-modal-submit__btn');
const placeContainer = document.querySelector('.place_container');
const heartBtn = document.querySelector('.heart__btn');
const selectedPlaceContainer = document.querySelector('.selected-place__container');


// uuid 기반으로 비워두기 실행하기 때문에 아무 정보도 없어도 비워두기 가능하도록 uuid 넣어줌 
//! url에 따라 처리
window.addEventListener('DOMContentLoaded', () => {
  const planBoxes = selectedPlaceContainer.querySelectorAll('.place__box')
  planBoxes.forEach(box => {
    if (! box.dataset.place){
      const uuid = self.crypto.randomUUID();
      const blankBtn = box.querySelector('.plan-blank__btn');
      box.setAttribute('data-id', uuid);
      box.setAttribute('data-blank', uuid);
      box.setAttribute('data-place', '');
      blankBtn.setAttribute('data-blank', uuid);
    }
  })
})

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

let place_current = 4;
const PLACE_TOTAL = 10;

function addPlaceItem(placeName, placeId) {
  let uuid = self.crypto.randomUUID();
  // placeid를 이용하지 않고 uuid를 사용하는 이유 :
  // uuid 기반으로 삭제되기 때문에 같은 장소 두 번 추가해도 선택한 값만 삭제되도록 하기 위해
  const placeBox = document.createElement('li');
  placeBox.setAttribute('class', 'place__box');
  placeBox.setAttribute('draggable', 'true');
  placeBox.setAttribute('data-id', uuid);
  placeBox.setAttribute('data-place', placeId);
  placeBox.setAttribute('data-blank', uuid);

  const div = document.createElement('div')
  div.setAttribute('class', 'place__item')
  div.innerHTML = `
      <span class="place__name">${placeName}</span>
      <button class="plan-blank__btn" data-blank=${uuid} data-state="filled">비워두기</button>
      <button class="place-remove__btn">
        <i class="fa-solid fa-xmark" data-id=${uuid}></i>
      </button>
    `
  placeBox.appendChild(div)
  printPlaceLikeBtn(placeId, div)
  return placeBox
}

selectedPlaceContainer.addEventListener('click', event => {
  const id = event.target.dataset.id;
  const likePlaceId = event.target.dataset.placelike;
  const blankItemId = event.target.dataset.blank;
  
  if (id) {
    const toBeDeleted = document.querySelector(`.place__box[data-id="${id}"]`);
    toBeDeleted.remove();
    place_current--;
    return;
  }
  
  if (likePlaceId) {
    updatePlaceLike(likePlaceId);
    return;
  }

  // 비워두기 버튼 관련 처리
  if (blankItemId) {
    const toBeBlanked = document.querySelector(`.place__box[data-blank="${blankItemId}"]`)
    const blankBtn = toBeBlanked.querySelector('.plan-blank__btn')
    const blankStatus = blankBtn.dataset.state
    
    if (blankItemId && blankStatus === 'filled') {
      blankPlanPlace(blankItemId, toBeBlanked)
    } else if (blankItemId && blankStatus === 'blanked') {
      const content = toBeBlanked.querySelector('.place__name')
      content.innerText = '장소를 선택해주세요.'
      blankBtn.innerText = '비워두기'
      blankBtn.dataset.state = 'filled'
    }
    return;
  }
})

placeContainer.addEventListener('click', event => {
  const placeId = event.target.dataset.place;
  if (placeId && place_current < PLACE_TOTAL) {
    const placeName = document.getElementById(`${placeId}`).innerText;

    printSelectedPlace(placeName, placeId)
  }

  const likePlaceId = event.target.dataset.placelike;
  if (likePlaceId) {
    updatePlaceLike(likePlaceId)
  }
})

function printSelectedPlace(placeName, placeId) {
  const listArr = [...selectedPlaceContainer.children]
  let foundEmptySlot = false;

  listArr.forEach(list => {
    const blankStatus = list.querySelector('.plan-blank__btn')
    const dataPlace = list.dataset.place

    if (blankStatus.dataset.state === 'filled' && !dataPlace && !foundEmptySlot) {
      foundEmptySlot = true;
      const placeItem = list.querySelector('.place__item');
      printPlaceLikeBtn(placeId, placeItem);
      list.dataset.place = placeId;
      const newPlaceName = list.querySelector('.place__name');
      newPlaceName.innerText = placeName;
      return;
    }
  })

  if (!foundEmptySlot) {
    placeBox = addPlaceItem(placeName, placeId)
    selectedPlaceContainer.appendChild(placeBox);
    place_current++;
  }
}

function blankPlanPlace(blankItemId, toBeBlanked) {
  const liArr = [...selectedPlaceContainer.children]
  const itemIndex = liArr.indexOf(toBeBlanked)

  toBeBlanked.dataset.place = ''
  toBeBlanked.innerHTML = ''
  const placeItemDiv = document.createElement('div')
  placeItemDiv.setAttribute('class', 'place__item')
  placeItemDiv.innerHTML = `
    <span class="place__name">비워두었습니다.</span>
    <button class="plan-blank__btn" data-blank="${blankItemId}" data-state="blanked">채우기</button>
    `

  const removeBtn = toBeBlanked.querySelector('.place-remove__btn')
  if (!removeBtn && itemIndex >= 4) {
    const button = document.createElement('button')
    button.setAttribute('class', 'place-remove__btn')
    button.innerHTML = `
    <i class="fa-solid fa-xmark" data-id=${blankItemId}></i>
    `
    placeItemDiv.appendChild(button)
  }
  toBeBlanked.appendChild(placeItemDiv)
}

// 해시태그
const input = document.querySelector('input[name=hashtags]')
let tagify = new Tagify(input, {
  maxTags: 3,
});

function getHashtags() {
  let values = tagify.value
  const valueArr = []
  for (let value of values) {
    valueArr.push(value['value'])
  }
  return valueArr
}

if (modalSubmitBtn) {
  modalSubmitBtn.addEventListener('click', () => {
    const planTitle = getPlanTitle()
    const placeBoxItems = selectedPlaceContainer.querySelectorAll('.place__box');
    const placeIds = Array.from(placeBoxItems).map(item => item.dataset.place);
    console.log(placeIds);
    const hashtags = getHashtags()
    // 이 중 undefined 일 때도 처리해야 함
    const hashtagArea = hashtags[0]
    const hashtagType = hashtags[1]
    const hashtagPick = hashtags[2]
    // true, false로 구분
    const isPublic = document.querySelector('.new-plan__public ').checked
  
    fetch('', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json',
      },
      body : JSON.stringify({ 
        plantitle: planTitle,
        placeids: placeIds,
        isliked: isLiked,
        hashtag_area: hashtagArea,
        hashtag_type: hashtagType,
        hashtag_pick: hashtagPick,
        ispublic: isPublic, }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data)
        if (data.status === 'success') {
          location.reload()
        } else {
          console.log('에러 발생')
        }
      })
  })
}

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
  let listArr = [...currentItem.parentElement.children];
  const dropItemIndex = listArr.indexOf(currentDropItem);
  
  if (currentItemIndex < dropItemIndex) {
    currentDropItem.after(currentItem)
  } else {
    currentDropItem.before(currentItem)
  }

  listArr = [...currentItem.parentElement.children];
  handleRemoveBtn(listArr)
});

function handleRemoveBtn(listArr) {
  for (let [idx, item] of listArr.entries()) {
    let placeItem = item.querySelector('.place__item');
    let removeBtn = placeItem.querySelector('.place-remove__btn');
    if (removeBtn && idx < 4) {
      removeBtn.remove()
    } else if (!removeBtn && idx >= 4) {
      let currenItemUuid = item.dataset.id
      let button = document.createElement('button')
      button.setAttribute('class', 'place-remove__btn')
      button.innerHTML = `
      <i class="fa-solid fa-xmark" data-id="${currenItemUuid}"></i>
      `
      placeItem.appendChild(button)
    }
  }
}