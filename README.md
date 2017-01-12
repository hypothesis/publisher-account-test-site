# Hypothesis Publisher Account Demo Site

This is an example application showing how content publishers can use
[Hypothesis](https://hypothes.is)' Publisher Account feature to add annotation functionality to their pages which is integrated with their existing account system.

Publishers who just want to add the Hypothesis client to their pages and allow users to annotate using Hypothesis accounts can simply [embed Hypothesis](https://hypothes.is/for-publishers/).

----

## Setup

First, you will need to create a publisher account on the Hypothesis service [TODO: Add information on how to do this].

This will give you a client ID and secret which can be used to create accounts
on the Hypothesis service via the API, and generate _grant tokens_ which can be
used to identify the logged-in user to the Hypothesis client.

Once you have a client ID and secret, you can run the example site as follows:

```
pip install -r requirements.txt
export HYPOTHESIS_AUTHORITY=$AUTHORITY  # Domain name used when registering publisher account
export HYPOTHESIS_CLIENT_ID=$CLIENT_ID
export HYPOTHESIS_CLIENT_SECRET=$CLIENT_SECRET
make run
```

Once the app is running, go to [http://localhost:5050](http://localhost:5050) to view the example
page.  Enter a username and click "Sign up" to register an account on the
Hypothesis service, associated with your publisher account, and "Login" to log
in to the example site.

After logging in, you can annotate content in the article by selecting text and clicking the "Annotate" or "Highlight" buttons that appear.

## How it works

When you "Sign up" on the example site, a request is made to the [Create user API](http://h.readthedocs.io/en/latest/api/#operation/createUser) to create an account with the given username within the namespace of your publisher account. When the page loads, it creates a [JWT token](https://jwt.io/) for the logged-in user, using the client ID and secret, and embeds it in the generated page.

When the Hypothesis client runs, it calls the `window.hypothesisConfig()` function to fetch the configuration for the annotation client and reads the grant token. It then exchanges this grant token for an access token which allows the client to create annotations using this username.
