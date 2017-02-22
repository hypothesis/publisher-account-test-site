(function () {
  const openLoginPopup = function openLoginPopup() {
    const width  = 400;
    const height = 400;
    const left   = window.screenX + ((window.innerWidth / 2)  - (width  / 2));
    const top    = window.screenY + ((window.innerHeight / 2) - (height / 2));

    window.open(
      '/login',
      'loginWindow',
      `left=${left},top=${top},width=${width},height=${height}`
    );
  };

  window.hypothesisConfig = function () {
    return {
      services: [{
        authority: 'partner.org',
        grantToken: hypothesisGrantToken,
      }],
      onLogin: openLoginPopup,
    };
  };

  document.querySelectorAll('.js-popup-login').forEach((item) => {
    item.addEventListener('click', (event) => {
      event.preventDefault();
      openLoginPopup();
    });
  });
})()
