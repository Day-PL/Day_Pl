const FULL_PATH = 'http://127.0.0.1:8000'
const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value

export function printPlaceLikeBtn(placeId, placeBoxBody) {
  checkPlaceIsLiked(placeId)
  .then(result => { 
      let isPlaceLiked = result;
      let likeBtn = createPlaceLikeButton(isPlaceLiked, placeId);
      placeBoxBody.insertBefore(likeBtn, placeBoxBody.firstChild)
  });
}

export function updatePlaceLike(PlaceId) {
  if (PlaceId) {
    fetch('', {
      method: 'PUT',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ placeid: PlaceId }),
    })
    .then((response) => response.json())
    .then((data) => {
      const placeLikeBtn = document.querySelectorAll(`.place-like__btn[data-placelike="${PlaceId}"]`)
      placeLikeBtn.forEach(btn => {
        if (data.isliked === true) {
          btn.innerHTML = `<i data-placelike="${PlaceId}" class="fa-solid fa-star"></i>`
        } else {
          btn.innerHTML = `<i data-placelike="${PlaceId}" class="fa-regular fa-star"></i>`
        }
      })

    })
  }
}

function createPlaceLikeButton(isLiked, placeId) {
  let likeBtn = document.createElement('button');
  likeBtn.setAttribute('class', 'place-like__btn');
  let likeIcon = document.createElement('i');
  
  if (isLiked) {
      likeIcon.setAttribute('class', 'fa-solid fa-star');
      likeIcon.setAttribute('data-placelike', placeId);
  } else {
      likeIcon.setAttribute('class', 'fa-regular fa-star');
      likeIcon.setAttribute('data-placelike', placeId);
  }

  likeBtn.setAttribute('data-placelike', placeId);
  likeBtn.appendChild(likeIcon);
  return likeBtn;
}

function checkPlaceIsLiked(placeId) {
  return new Promise((resolve) => {
      fetch(`${FULL_PATH}/check-place-like/${placeId}/`, {
          method: 'GET',
      })
      .then((response) => response.json())
      .then((data) => {
          resolve(data.is_liked);
      })
  })
}

// 인기 플랜 / 나의 기록 중 남의 기록 ➡️ 하트 버튼 관련 function
export function printPlanLikeBtn(planId, planBoxBody) {
  checkPlanIsLiked(planId)
  .then(result => { 
      let isPlanLiked = result;
      let likeBtn = createPlanLikeButton(isPlanLiked, planId);
      planBoxBody.insertBefore(likeBtn, planBoxBody.firstChild)
  });
}

export function updatePlanLike(planId) {
  if (planId) {
    fetch('', {
      method: 'PUT',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ planid: planId }),
    })
    .then((response) => response.json())
    .then((data) => {
      const planLikeBtn = document.querySelectorAll(`.plan-like__btn[data-planlike="${planId}"]`)
      planLikeBtn.forEach(btn => {
        if (data.isliked === true) {
          btn.innerHTML = `<i data-planlike="${planId}" class="fa-solid fa-heart"></i>`
        } else {
          btn.innerHTML = `<i data-planlike="${planId}" class="fa-regular fa-heart"></i>`
        }
      })

    })
  }
}

function createPlanLikeButton(isLiked, planId) {
  let likeBtn = document.createElement('button');
  likeBtn.setAttribute('class', 'plan-like__btn');
  let likeIcon = document.createElement('i');

  if (isLiked) {
    likeIcon.setAttribute('class', 'fa-solid fa-heart');
    likeIcon.setAttribute('data-planlike', planId);
  } else {
    likeIcon.setAttribute('class', 'fa-regular fa-heart');
    likeIcon.setAttribute('data-planlike', planId);
  }
  
  likeBtn.setAttribute('data-planlike', planId);
  likeBtn.appendChild(likeIcon);
  return likeBtn;
}

function checkPlanIsLiked(planId) {
  return new Promise((resolve) => {
    fetch(`${FULL_PATH}/check-plan-like/${planId}/`, {
      method: 'GET',
    })
    .then((response) => response.json())
    .then((data) => {
        resolve(data.is_liked)
    })
  })
}