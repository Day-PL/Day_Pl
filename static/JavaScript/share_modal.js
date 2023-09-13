Kakao.init('b29a5aad96c55485af88e2910393db7d');

function shareFunction(plantitle) {
  const shareBtn = document.querySelector('.plan-share__btn')
  const planUuid = shareBtn.dataset.shareid
  const facebookShareBtn = document.querySelector('.share-facebook')
  const twitterShareBtn = document.querySelector('.share-twitter')
  const kakaoShareBtn = document.querySelector('.share-kakao')
  const urlShareBtn = document.querySelector('.share-urlcopy__btn')
  const thisUrl = `${FULL_PATH}/populars/detail/${planUuid}`

  facebookShareBtn.addEventListener('click', () => {
    let url = "http://www.facebook.com/sharer/sharer.php?u="+encodeURIComponent(thisUrl);
    window.open(url, "", "width=500, height=300");
  })
  
  twitterShareBtn.addEventListener('click', () => {
    let url = "http://twitter.com/share?url="+encodeURIComponent(thisUrl);
    window.open(url, "tweetPop", "width=500, height=700, scrollbars=yes");
  })

  kakaoShareBtn.addEventListener('click', () => {
    kakaoShareMessage(plantitle, thisUrl)
  })

  urlShareBtn.addEventListener('click', () => {
  navigator.clipboard.writeText(thisUrl)
    .then(() => {
      // 복사 성공 관련 창
      console.log('복사에 성공하였습니다')},
      // 복사 실패 관련 창
      () => {console.log('복사에 실피했습니다.')})
  })
}

function kakaoShareMessage(plantitle, url) {
  Kakao.Share.sendDefault({
    objectType: 'feed',
    content: {
      title: '[DAY\'PL] 플랜을 확인해 보세요.',
      description: `${plantitle}`,
      imageUrl:
        // TODO: 이미지 추후 변경
        'https://postfiles.pstatic.net/MjAyMzA5MTNfNDEg/MDAxNjk0NjA0OTc2Nzcz.OzGmoj1JiWHxqcSlxMSERBfUNqNfxqsJQWIg_sFSwUog.qF5DXok7pS1I3K-xmXGVpBtuE2oX27UCRfAw3KeZdKAg.PNG.m0522j/DayPl_logo-removebg-preview.png?type=w773',
      link: {
        webUrl: url,
      },
    },
    buttons: [
      {
        title: '자세히 보기',
        link: {
          webUrl: url,
        },
      },
    ],
  });
}