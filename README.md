# Hypothesis Publisher Account Test Site

This is a web app to test how content publishers can use
[Hypothesis](https://hypothes.is)' Publisher Account feature to add annotation
functionality to their pages which is integrated with their existing account
system.

Note that this is only intended for us at Hypothesis to test the integration
functionality internally, it's not intended as a demo or example for
publishers.

Publishers who just want to add the Hypothesis client to their pages and allow users to annotate using Hypothesis accounts can simply [embed Hypothesis](https://hypothes.is/for-publishers/).

## Installing the publisher account test site in a development environment

### You will need

* The publisher account test site integrates with h and the Hypothesis client,
  so you will need to set up development environments for each of those before
  you can develop the publisher account test site:

  * https://h.readthedocs.io/en/latest/developing/install/
  * https://h.readthedocs.io/projects/client/en/latest/developers/developing/

* [Git](https://git-scm.com/)

* [pyenv](https://github.com/pyenv/pyenv)
  Follow the instructions in the pyenv README to install it.
  The Homebrew method works best on macOS.

### Clone the Git repo

    git clone https://github.com/hypothesis/publisher-account-test-site.git

This will download the code into a `publisher-account-test-site` directory in
your current working directory. You need to be in the
`publisher-account-test-site` directory from the remainder of the installation
process:

    cd publisher-account-test-site

### Create the development data and settings

Create the database contents and environment variable settings needed to get
publisher-account-test-site working nicely with your local development
instances of the rest of the Hypothesis apps:

    make devdata

This requires you to have a git SSH key set up that has access to the private
https://github.com/hypothesis/devdata repo. Otherwise `make devdata` will
crash.

### Start the development server

    make dev

The first time you run `make dev` it might take a while to start because it'll
need to install the application dependencies and build the client assets.

This will start the server on port 5050 (http://localhost:5050), reload the
application whenever changes are made to the source code, and restart it should
it crash for some reason.

**That's it!** You’ve finished setting up your publisher account test site
development environment. Run `make help` to see all the commands that're
available for linting etc.

### Using the app

Once the development server is running:

1. Go to [http://localhost:5050](http://localhost:5050) to view the test page.
2. Enter a username and click "Sign up" to create an account on the publisher site.

The first time you log in with a particular username, a corresponding account
will be created on the Hypothesis service.

After logging in, you can annotate content in the article by selecting text and
clicking the "Annotate" or "Highlight" buttons that appear.

## How it works

When you "Sign up" on the test site, a request is made to the [Create user API](http://h.readthedocs.io/en/latest/api/#operation/createUser) to create an account with the given username within the namespace of your publisher account. When the page loads, it creates a [JWT token](https://jwt.io/) for the logged-in user, using the client ID and secret, and embeds it in the generated page.

When the Hypothesis client runs, it calls the `window.hypothesisConfig()` function to fetch the configuration for the annotation client and reads the grant token. It then exchanges this grant token for an access token which allows the client to create annotations using this username.
