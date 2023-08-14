const csrfToken = document.querySelector('[name="csrfmiddlewaretoken"]').value

function checkUsernameDuplicate() {
  const username = document.querySelector('#username');

  fetch('check-username/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username: username.value }),
  })
    .then((response) => response.json())
    .then((data) => {
      const resultElement = document.querySelector('.username-result');
      if (data.status === 'fail') {
        resultElement.innerText = data.message;
        resultElement.style.color = 'red';
      } else if (data.status === 'error') {
        resultElement.innerText = data.message;
        resultElement.style.color = 'red';
      } else {
        resultElement.innerText = data.message;
        resultElement.style.color = 'green';
        username.setAttribute('readonly', 'true');
      }
    })
    .catch((error) => console.error('Error:', error));
}

// 비밀번호
const pwd1Input = document.querySelector('#password1');
const pwd2Input = document.querySelector('#password2');
const pwdResult = document.querySelector('.pwd-result');

function checkPwdValidate() {
  const passwordReg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$!%*?&])[A-Za-z\d@#$!%*?&]{8,}$/;
  if (!passwordReg.test(pwd1Input.value)) {
    pwdResult.textContent = '8자 이상의 영문 대문자, 소문자, 숫자, 특수문자를 사용해 주세요.';
    pwdResult.style.color = 'red';
    pwd2Input.setAttribute('readonly', 'true')
  } else {
    pwdResult.textContent = '';
    pwd2Input.removeAttribute('readonly')
  }
}

pwd1Input.addEventListener('blur', checkPwdValidate);

function checkPwdsMatch() {
  if (pwd1Input.value === pwd2Input.value) {
    pwdResult.textContent = '비밀번호가 일치합니다.';
    pwdResult.style.color = 'green';
  } else {
    pwdResult.textContent = '비밀번호가 일치하지 않습니다.';
    pwdResult.style.color = 'red';
  }
}

pwd2Input.addEventListener('input', checkPwdsMatch);

function checkMailDuplicate() {
  const mailInput = document.querySelector('.mail');
  const mailResult = document.querySelector('.mail-result');
  
  const mailReg = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!mailReg.test(mailInput.value)) {
    mailResult.innerText = '이메일 주소가 정확한지 확인해 주세요.';
    mailResult.style.color = 'red';
  } else {
    fetch('check-mail/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ mail: mailInput.value }),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status === 'fail') {
          mailResult.innerText = data.message;
          mailResult.style.color = 'red';
        } else if (data.status === 'error') {
          mailResult.innerText = data.message;
          mailResult.style.color = 'red';
        } else {
          mailResult.textContent = '사용 가능한 이메일입니다.';
          mailResult.style.color = 'green';
          mailInput.setAttribute('readonly', 'true')
        }
      })
      .catch((error) => {
        console.error('Error checking email:', error);
      });
  }
}

const phoneInput = document.querySelector('#phone');
const phoneResult = document.querySelector('.phone-result');

phoneInput.addEventListener('input', function() {
  formatPthoneNumber(this);
});

function formatPthoneNumber(input) {
  const phoneNumber = input.value.replace(/-/g, "");

  if (phoneNumber/length <= 3) {
    input.value = phoneNumber
  } else if (phoneNumber.length <= 7) {
    input.value = phoneNumber.substring(0, 3) + '-' + phoneNumber.substring(3);
  } else {
    input.value
    = phoneNumber.substring(0, 3) + '-'
    + phoneNumber.substring(3, 7) + '-'
    + phoneNumber.substring(7);
  }
}

function checkPhoneValidate() {
  const phoneReg = /^01[0-9]-\d{4}-\d{4}$/;
  if (!phoneReg.test(phoneInput.value)) {
    phoneResult.textContent = '휴대전화번호가 정확한지 확인해 주세요.';
    phoneResult.style.color = 'red';
  } else {
    phoneResult.textContent = '';
  }
}

phoneInput.addEventListener('blur', checkPhoneValidate);

// TODO: 아이디와 이메일 주소가 readonly일 때만 회원가입 버튼 활성화