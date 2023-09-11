const commentSubmitBtns = document.querySelectorAll('.comment-submit__btn')
const commentLists = document.querySelectorAll('.place-comments__list')

newPlanPlaceContainer.addEventListener('click', event => {
  const placeId = event.target.dataset.placename
  if (placeId) {
    getComments(placeId)
  }
})

commentSubmitBtns.forEach(commentSubmitBtn => {
  commentSubmitBtn.closest('form').addEventListener('submit', event => {
    event.preventDefault()
    const commentPlaceId = commentSubmitBtn.dataset.commentplaceid
    if (commentPlaceId) {
      createComment(commentPlaceId)
    }
  })
})

commentLists.forEach(commentList => {
  commentList.addEventListener('click', event => {
    const modifyCommentId = event.target.dataset.modifycommentid
    const modifyCommentPlaceId = event.target.dataset.modifyplaceid
    if (modifyCommentId) {
      const originalComment = document.querySelector(`.content-${modifyCommentId}`).innerText
      const commentContentLi = document.querySelector(`[data-comment="${modifyCommentId}"]`)
      commentContentLi.innerHTML = `
      <form class="comment-modify__form d-flex justify-content-between">
      <div class="form-floating">
        <textarea class="comment-modify-${modifyCommentId} form-control" placeholder="Leave a comment here" id="floatingTextarea2">${originalComment}</textarea>
        <label for="floatingTextarea2">Comments</label>
      </div>
      <button type="button" onclick="modifyComment(${modifyCommentId}, ${modifyCommentPlaceId})" class="comment-modify-submit__btn btn btn-primary">수정</button>
      </form>
      `
    }

    const deleteCommentId = event.target.dataset.deletecommentid
    const deleteCommentPlaceId = event.target.dataset.deleteplaceid
    if (deleteCommentId) {
      deleteComment(deleteCommentId, deleteCommentPlaceId)
    }
  })
})

function deleteComment(commentId, placeId) {
  const placeComments = document.querySelector(`.place-comments-${placeId}`);
  fetch('comment/', {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      comment_id: commentId,
    }),
  })
  .then((response) => response.json())
  .then((data) => {
    if (data.status === 'success') {
      placeComments.innerHTML = ''
      getComments(placeId)
    }
  })
}

function modifyComment(commentId, placeId) {
  const placeComments = document.querySelector(`.place-comments-${placeId}`);
  const newCommentContent = document.querySelector(`.comment-modify-${commentId}`).value
  fetch('comment/', {
    method: 'PUT',
    headers: {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      comment_id: commentId,
      comment: newCommentContent,
    }),
  })
  .then((response) => response.json())
  .then((data) => {
    if (data.status === 'success') {
      placeComments.innerHTML = ''
      getComments(placeId)
    } 
  })
}

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
  const isAuthor = comment['is_current_user_author']
  const placeComments = document.querySelector(`.place-comments-${placeId}`);

  const li = document.createElement('li')
  li.setAttribute('class', 'place-comment d-flex flex-row justify-content-between')
  li.setAttribute('data-comment', commentId)
  li.innerHTML = `
  <div class="comment_description">
    <div class="comment_author">${commentAuthor}</div>
    <div class="comment_content content-${commentId}">${commentContent}</div>
    <div class="comment_date">${commentDate}</div>
  </div>
  `
  const div = document.createElement('div')
  div.setAttribute('class', 'comment__btns d-flex flex-column')
  if (isAuthor) {
    div.innerHTML = `
    <button type="button" class="comment-modify__btn btn btn-outline-primary" data-modifycommentid=${commentId} data-modifyplaceid=${placeId}>수정</button>
    <button type="button" class="comment-delete__btn btn btn-outline-primary" data-deletecommentid=${commentId} data-deleteplaceid=${placeId}>삭제</button>
    `
    li.appendChild(div)
  }
  placeComments.appendChild(li)
}