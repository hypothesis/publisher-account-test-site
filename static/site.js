(function () {
  const openPopup = (url) => {
    const width  = 400;
    const height = 400;
    const left   = window.screenX + ((window.innerWidth / 2)  - (width  / 2));
    const top    = window.screenY + ((window.innerHeight / 2) - (height / 2));

    window.open(
      url,
      'loginWindow',
      `left=${left},top=${top},width=${width},height=${height}`
    );
  };

  const openLoginPopup = () => openPopup('/login');

  window.hypothesisConfig = function () {
    return {
      branding: {
        // Match the body's background color.
        appBackgroundColor: '#ddd',

        // Match the header's background and foreground colors.
        accentColor: '#444',
        ctaBackgroundColor: '#444',
        ctaTextColor: 'white',

        // Match the body text of the article.
        annotationFontFamily: 'serif',
        selectionFontFamily: 'serif',
      },
      services: [{
        authority: 'partner.org',
        grantToken: hypothesisGrantToken,
        icon: 'https://openclipart.org/download/272629/sihouette-animaux-10.svg',
        onLoginRequest: openLoginPopup,
        onLogoutRequest: () => window.location = '/logout',
        onSignupRequest: () => openPopup('/signup'),
        onProfileRequest: () => window.location = '/profile',
        onHelpRequest: () => window.location = '/help',
      }],
    };
  };

  document.querySelectorAll('.js-popup-login').forEach((item) => {
    item.addEventListener('click', (event) => {
      event.preventDefault();
      openLoginPopup();
    });
  });
})()
