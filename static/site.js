(function () {
  window.hypothesisConfig = function () {
    return {
      services: [{
        authority: 'partner.org',
        grantToken: hypothesisGrantToken,
      }],
    };
  };
})()
