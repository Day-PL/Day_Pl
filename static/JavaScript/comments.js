const commentSubmitBtns = document.querySelectorAll('.comment-submit__btn')

newPlanPlaceContainer.addEventListener('click', event => {
  const placeId = event.target.dataset.placename
  getComments(placeId)
})

commentSubmitBtns.forEach(commentSubmitBtn => {
  commentSubmitBtn.closest('form').addEventListener('submit', event => {
    event.preventDefault()
    const commentPlaceId = commentSubmitBtn.dataset.commentplaceid
    createComment(commentPlaceId)
  })
})

function createComment(placeId) {
  const commentTextArea = document.querySelector(`.comment-content-${placeId}`)
  const placeComments = document.querySelector(`.place-comments-${placeId}`);
  fetch(`comment/`, {
    method: "POST",
    headers: {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      place_id: placeId,
      comment: commentTextArea.value,}),
  })
  .then((response) => response.json())
  .then((data) => {
    if (data.status === 'success') {
      commentTextArea.value = '';
      placeComments.innerHTML = ''
      getComments(placeId)
    }
  })
}

function getComments(placeId) {
  const placeComments = document.querySelector(`.place-comments-${placeId}`);
  fetch(`comment/${placeId}/`, {
    method: "GET",
  })
  .then((response) => response.json())
  .then((datas) => {
    placeComments.innerHTML = ''
    for (let data of datas) {
      printComments(data, placeId)
    }
  })
}

function printComments(comment, placeId) {
  const commentId = comment['id']
  const commentAuthor = comment['comment_author']
  const commentContent = comment['comment']
  const commentDate = comment['created_at']
  const placeComments = document.querySelector(`.place-comments-${placeId}`);

  const li = document.createElement('li')
  li.setAttribute('class', 'place-comment d-flex flex-row justify-content-between')
  li.innerHTML = `
  <div class="comment_description">
    <div class="comment_author">${commentAuthor}</div>
    <div class="comment_content">${commentContent}</div>
    <div class="comment_date">${commentDate}</div>
  </div>
  <div class="comment__btns d-flex flex-column">
    <button type="button" class="comment-modify__btn btn btn-outline-primary" data-commentmodify=${commentId}>수정</button>
    <button type="button" class="comment-delete__btn btn btn-outline-primary" data-commentdelete=${commentId}>삭제</button>
  </div>
  `
  placeComments.appendChild(li)
}