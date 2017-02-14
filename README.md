# Hypothesis Publisher Account Demo Site

This is an example application showing how content publishers can use
[Hypothesis](https://hypothes.is)' Publisher Account feature to add annotation functionality to their pages which is integrated with their existing account system.

Publishers who just want to add the Hypothesis client to their pages and allow users to annotate using Hypothesis accounts can simply [embed Hypothesis](https://hypothes.is/for-publishers/).

----

## Setup

First, you will need to create a couple of things on the Hypothesis service:

1. A set of credentials (an "authclient") for managing annotations and users
   associated with your domain.

2. A group associated with your domain to which users can post annotations.
   Annotations from this group will be displayed when the Hypothesis client
   loads on your pages.

In [Hypothesis development environments](http://h.readthedocs.io/en/latest/developing/install/), you can do this using the `hypothesis` CLI tool:

```sh
# 1. Create an OAuth client which can manage annotations and users belonging
# to partner.org
./bin/hypothesis --dev authclient add --name Partner --authority partner.org

# 2. Create an admin user for partner.org. This is needed because groups must
# have a creator.
./bin/hypothesis --dev user add --authority partner.org --username admin --email admin@localhost --password secret

# 3. Create the main group for annotations on partner.org
./bin/hypothesis --dev groups add-publisher-group --authority partner.org --name Partner --creator admin
```

Step 1 will give you a client ID and secret which can be used to create accounts
on the Hypothesis service via the API, and generate _grant tokens_ which can be
used to identify the logged-in user to the Hypothesis client.

Once you have a client ID and secret, you can run the example site as follows:

```
pip install -r requirements.txt
export HYPOTHESIS_SERVICE="http://127.0.0.1:5000" # Point to the local H service
export HYPOTHESIS_AUTHORITY=$AUTHORITY  # Domain name used when registering publisher account
export HYPOTHESIS_CLIENT_ID=$CLIENT_ID
export HYPOTHESIS_CLIENT_SECRET=$CLIENT_SECRET
make run
```

Once the web app is running:

1. Go to [http://localhost:5050](http://localhost:5050) to view the example
page.
2. Enter a username and click "Sign up" to create an account on the publisher site.
The first time you log in with a particular username, a corresponding account will
be created on the Hypothesis service.

After logging in, you can annotate content in the article by selecting text and clicking the "Annotate" or "Highlight" buttons that appear.

## How it works

When you "Sign up" on the example site, a request is made to the [Create user API](http://h.readthedocs.io/en/latest/api/#operation/createUser) to create an account with the given username within the namespace of your publisher account. When the page loads, it creates a [JWT token](https://jwt.io/) for the logged-in user, using the client ID and secret, and embeds it in the generated page.

When the Hypothesis client runs, it calls the `window.hypothesisConfig()` function to fetch the configuration for the annotation client and reads the grant token. It then exchanges this grant token for an access token which allows the client to create annotations using this username.
