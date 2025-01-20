describe('CXFacturatie module E2E test', () => {
  it('Logs in using Auth0', function () {
    cy.visit('/');

    cy.origin('https://dev-icv5ncp4ozs145pe.eu.auth0.com', () => {
      cy.get('input#username')
        .type('user_test1@example.nl');

      cy.get('input[name="password"]')
        .type('Test123@', { log: false });

      cy.get('div.c21f9f2f0')
      .find('button[data-action-button-primary="true"]')
      .click();
    });

    cy.url().should('include', '/tabs/home');
  });

  it('View settings page and get the phone number', function () {
    cy.visit('/tabs/settings');
    cy.get('#phone_number').invoke('text').then((phonenumber) => {
      cy.log(`Phone number is: ${phonenumber}`)
    })
  })

  // TODO: for the history, home, facturen & profiel tests, add invoice viewer.
  describe('Historie page tests', () => {
    it('View historie page', () => {
      cy.visit('/tabs/historie');
    });
  });
  
  describe('Home page tests', () => {
    it('View home page', () => {
      cy.visit('/tabs/home');
    });
  });

  describe('Facturen page tests', () => {
    it('View facturen page', () => {
      cy.visit('/tabs/facturen');
    });
  });

  describe('Profiel page tests', () => {
    it('View profiel page', () => {
      cy.visit('/tabs/profiel');
    });
    it('Logging out', () => {
      cy.visit('/tabs/profiel');

      cy.get('#logout_btn')
      .click();
    });
  });
  

});
