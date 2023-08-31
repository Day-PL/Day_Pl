const searchInput = document.querySelector('.popular-plans-search__input');
const searchClearBtn = document.querySelector('.search-clear__btn');
const popularPlansList = document.querySelector('.popular-plans__list');
const planPlaceList = document.querySelector('.popular-plan-place__list');
const planDetailBox = document.querySelector('.popular-plan-detail__box');

window.addEventListener('DOMContentLoaded', () => {
  getPlans('');
});

searchInput.addEventListener('keyup', () => {
  getPlans(searchInput.value);
  })

searchClearBtn.addEventListener('click', () => {
  searchInput.value = '';
  searchInput.focus();
  getPlans('');
})

popularPlansList.addEventListener('click', event => {
  const targetLi = event.target.closest('a');

  if (targetLi) {
    const planId = targetLi.dataset.id;
    getPlanDetail(planId);
  }
})

planPlaceList.addEventListener('click', (event) => {
  const likePlaceId = event.target.dataset.placelike;

  if (likePlaceId) {
    updatePlaceLike(likePlaceId);
    return;
  }
})

planDetailBox.addEventListener('click', (event) => {
  const likePlanId = event.target.dataset.planlike;
  // TODO: 플랜 공유 버튼 클릭시 이벤트!

  if (likePlanId) {
    updatePlanLike(likePlanId);
    return;
  }
})

function getPlanDetail(planId) {
  fetch(`${planId}/`, {
    method : "GET",
  })
  .then((response) => response.json())
  .then((data) => {
    const planDetailContainer = document.querySelector('.popular-plan-detail__container');
    const placeDetail =  printPlanDetail(data);
    const planPlaceList = printPlanPlaceList(data['plan_places']);

    planDetailContainer.appendChild(placeDetail);
    planDetailContainer.appendChild(planPlaceList);

    printMap(planPlaceList)
  })
}

function printPlanDetail(plan) {
  const planId = plan['plan']['id'];
  const planUuid = plan['plan']['uuid'];
  const title = plan['plan']['name'];
  const nickname = plan['plan']['user'];

  planDetailBox.innerHTML = `
  <span class="popular-plan__title">${title}</span>
  <button class="plan-share__btn btn" data-shareid="${planUuid}" data-bs-toggle="modal" data-bs-target="#exampleModal">
    <i class="fa-solid fa-share-nodes"></i>
  </button>
  `
  printPlanLikeBtn(planId, planDetailBox)
  shareFunction()

  return planDetailBox;
}

function printPlanPlaceList(planPlaces) {
  planPlaceList.innerHTML = '';

  for (let place of planPlaces) {
    let placeId = place['placeid'];
    let name = place['place_name'];
    let lng = place['lng'];
    let lat = place['lat'];

    let li = document.createElement('li');
    li.setAttribute('class', 'place-list');
    li.setAttribute('data-lng', lng);
    li.setAttribute('data-lat', lat);

    let span = document.createElement('span');
    span.setAttribute('class', 'place__name');
    if (placeId === 0) {
      span.innerText = '비어있음';
    } else {
      printPlaceLikeBtn(placeId, li)
      span.innerText = name;
    }
    li.appendChild(span);

    planPlaceList.appendChild(li);
  }
  
  return planPlaceList;
}

function getPlans(searchKeyword) {
  if (searchKeyword === '') {
    searchKeyword = 'none'
  }
  
  fetch(`search/${searchKeyword}/`, {
    method : "GET",
  })
  .then((response) => response.json())
  .then((data) => {
    popularPlansList.innerHTML = '';
    if (!data.length) {
      // 여기 다시 수정
      const list = document.createElement('a');
      list.getAttribute('class', 'popular-plan__box__none');
      list.innerText = '해당하는 정보가 없습니다.'
      popularPlansList.appendChild(list);
    }
    for (let plan of data) {
      let planList = printPopularPlanList(plan);
      popularPlansList.appendChild(planList);
    }
  })
}

function printPopularPlanList(plan) {
  const id = plan['id'];
  const uuid = plan['uuid'];
  const title = plan['title'];
  const count = plan['count'];
  const nickname = plan['nickname'];
  const hashtagArea = plan['hashtag_area'];
  const hashtagType = plan['hashtag_type'];
  const hashtagPick = plan['hashtag_pick'];

  const list = document.createElement('a');
  list.setAttribute('class', 'popular-plan__box list-group-item list-group-item-action');
  list.setAttribute('id', id);
  list.setAttribute('data-id', uuid);
  list.setAttribute('data-name', title);
  list.innerHTML = `
                <div class="popular-plan__detail">
                  <div class="popular-plan__title">${title}</div>
                  <span class="popular-plan__like">
                    <i class="fa-solid fa-heart"></i>
                    <span class="popular-plan__like-count">${count}</span>
                  </span>
                  <span class="popular-plan__nickname">${nickname}</span>
                  <span class="popular-plan__hash area">${hashtagArea}</span>
                  <span class="popular-plan__hash type">${hashtagType}</span>
                  <span class="popular-plan__hash pick">${hashtagPick}</span>
                </div>
                `;
  return list;
}