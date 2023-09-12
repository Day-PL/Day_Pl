const FULL_PATH = 'http://127.0.0.1:8000'
const findIdForm = document.querySelector('.find-id__form')
const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value

findIdForm.addEventListener('submit', event => {
  event.preventDefault()
  const email = document.querySelector('#email').value
  checkValidId(email)
})

function checkValidId(email) {
  fetch('', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email,
    }),
  })
  .then((response) => response.json())
  .then((data) => {
    if (data.status === 'error') {
      const result = document.querySelector('.find-id__result')
      result.classList.remove('invisible')
      result.innerText = data.message
    }
    else if (data.status === 'success') {
      const statusIcon = document.querySelector('.status')
      statusIcon.classList.remove('invisible')
      setTimeout(() => {
        window.location.href = `${FULL_PATH}/users/login/`
      }, 3000);
      openModal();
    }
  })
}

function openModal() {
  const modal = new bootstrap.Modal(document.querySelector('.modal'))
  modal.show();
}