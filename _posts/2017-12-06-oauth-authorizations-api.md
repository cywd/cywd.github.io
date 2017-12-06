---
layout: post
title: OAuth Authorizations API
excerpt: ""
categories: [GitHub]
tags: [GitHub, API]
date: 2017-12-06
comments: true
---

* TOC
{:toc}
---

You can use this API to manage the access OAuth applications have to your account. You can only access this API via [Basic Authentication](https://developer.github.com/v3/auth#basic-authentication) using your username and password, not tokens.

Make sure you understand how to [work with two-factor authentication](https://developer.github.com/v3/auth/#working-with-two-factor-authentication) if you or your users have two-factor authentication enabled.

## List your grants

You can use this API to list the set of OAuth applications that have been granted access to your account. Unlike the [list your authorizations](https://developer.github.com/v3/oauth_authorizations/#list-your-authorizations) API, this API does not manage individual tokens. This API will return one entry for each OAuth application that has been granted access to your account, regardless of the number of tokens an application has generated for your user. The list of OAuth applications returned matches what is shown on [the application authorizations settings screen within GitHub](https://github.com/settings/applications#authorized). The `scopes` returned are the union of scopes authorized for the application. For example, if an application has one token with `repo` scope and another token with `user` scope, the grant will return `["repo", "user"]`.

```
GET /applications/grants

```

### Response

```
Status: 200 OK
Link: <https://api.github.com/resource?page=2>; rel="next",
      <https://api.github.com/resource?page=5>; rel="last"

```

```
[
  {
    "id": 1,
    "url": "https://api.github.com/applications/grants/1",
    "app": {
      "url": "http://my-github-app.com",
      "name": "my github app",
      "client_id": "abcde12345fghij67890"
    },
    "created_at": "2011-09-06T17:26:27Z",
    "updated_at": "2011-09-06T20:39:23Z",
    "scopes": [
      "public_repo"
    ]
  }
]

```

## Get a single grant

```
GET /applications/grants/:id

```

### Response

```
Status: 200 OK

```

```
{
  "id": 1,
  "url": "https://api.github.com/applications/grants/1",
  "app": {
    "url": "http://my-github-app.com",
    "name": "my github app",
    "client_id": "abcde12345fghij67890"
  },
  "created_at": "2011-09-06T17:26:27Z",
  "updated_at": "2011-09-06T20:39:23Z",
  "scopes": [
    "public_repo"
  ]
}

```

## Delete a grant

Deleting an OAuth application's grant will also delete all OAuth tokens associated with the application for your user. Once deleted, the application has no access to your account and is no longer listed on [the application authorizations settings screen within GitHub](https://github.com/settings/applications#authorized).

```
DELETE /applications/grants/:id

```

### Response

```
Status: 204 No Content

```

## List your authorizations

```
GET /authorizations

```

### Response

```
Status: 200 OK
Link: <https://api.github.com/resource?page=2>; rel="next",
      <https://api.github.com/resource?page=5>; rel="last"

```

```
[
  {
    "id": 1,
    "url": "https://api.github.com/authorizations/1",
    "scopes": [
      "public_repo"
    ],
    "token": "",
    "token_last_eight": "12345678",
    "hashed_token": "25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8",
    "app": {
      "url": "http://my-github-app.com",
      "name": "my github app",
      "client_id": "abcde12345fghij67890"
    },
    "note": "optional note",
    "note_url": "http://optional/note/url",
    "updated_at": "2011-09-06T20:39:23Z",
    "created_at": "2011-09-06T17:26:27Z",
    "fingerprint": "jklmnop12345678"
  }
]

```

## Get a single authorization

```
GET /authorizations/:id

```

### Response

```
Status: 200 OK

```

```
{
  "id": 1,
  "url": "https://api.github.com/authorizations/1",
  "scopes": [
    "public_repo"
  ],
  "token": "",
  "token_last_eight": "12345678",
  "hashed_token": "25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8",
  "app": {
    "url": "http://my-github-app.com",
    "name": "my github app",
    "client_id": "abcde12345fghij67890"
  },
  "note": "optional note",
  "note_url": "http://optional/note/url",
  "updated_at": "2011-09-06T20:39:23Z",
  "created_at": "2011-09-06T17:26:27Z",
  "fingerprint": "jklmnop12345678"
}

```

## Create a new authorization

If you need a small number of personal access tokens, implementing the [web flow](https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/) can be cumbersome. Instead, tokens can be created using the OAuth Authorizations API using [Basic Authentication](https://developer.github.com/v3/auth#basic-authentication). To create personal access tokens for a particular OAuth application, you must provide its client ID and secret, found on the OAuth application settings page, linked from your [OAuth applications listing on GitHub](https://github.com/settings/developers).

If your OAuth application intends to create multiple tokens for one user, use `fingerprint` to differentiate between them.

You can also create OAuth tokens through the web UI via the [personal access tokens settings](https://github.com/settings/tokens). Read more about these tokens on the [GitHub Help site](https://help.github.com/articles/creating-an-access-token-for-command-line-use).

Organizations that enforce SAML SSO require personal access tokens to be whitelisted. Read more about whitelisting tokens on the [GitHub Help site](https://help.github.com/articles/about-identity-and-access-management-with-saml-single-sign-on).

```
POST /authorizations

```

### Parameters

| Name            | Type     | Description                              |
| --------------- | -------- | ---------------------------------------- |
| `scopes`        | `array`  | A list of scopes that this authorization is in. |
| `note`          | `string` | **Required**. A note to remind you what the OAuth token is for. Tokens not associated with a specific OAuth application (i.e. personal access tokens) must have a unique note. |
| `note_url`      | `string` | A URL to remind you what app the OAuth token is for. |
| `client_id`     | `string` | The 20 character OAuth app client key for which to create the token. |
| `client_secret` | `string` | The 40 character OAuth app client secret for which to create the token. |
| `fingerprint`   | `string` | A unique string to distinguish an authorization from others created for the same client ID and user. |

```
{
  "scopes": [
    "public_repo"
  ],
  "note": "admin script"
}

```

### Response

```
Status: 201 Created
Location: https://api.github.com/authorizations/1

```

```
{
  "id": 1,
  "url": "https://api.github.com/authorizations/1",
  "scopes": [
    "public_repo"
  ],
  "token": "abcdefgh12345678",
  "token_last_eight": "12345678",
  "hashed_token": "25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8",
  "app": {
    "url": "http://my-github-app.com",
    "name": "my github app",
    "client_id": "abcde12345fghij67890"
  },
  "note": "optional note",
  "note_url": "http://optional/note/url",
  "updated_at": "2011-09-06T20:39:23Z",
  "created_at": "2011-09-06T17:26:27Z",
  "fingerprint": ""
}

```

## Get-or-create an authorization for a specific app

This method will create a new authorization for the specified OAuth application, only if an authorization for that application doesn't already exist for the user. The URL includes the 20 character client ID for the OAuth app that is requesting the token. It returns the user's existing authorization for the application if one is present. Otherwise, it creates and returns a new one.

```
PUT /authorizations/clients/:client_id

```

### Parameters

| Name            | Type     | Description                              |
| --------------- | -------- | ---------------------------------------- |
| `client_secret` | `string` | **Required**. The 40 character OAuth app client secret associated with the client ID specified in the URL. |
| `scopes`        | `array`  | A list of scopes that this authorization is in. |
| `note`          | `string` | A note to remind you what the OAuth token is for. |
| `note_url`      | `string` | A URL to remind you what app the OAuth token is for. |
| `fingerprint`   | `string` | A unique string to distinguish an authorization from others created for the same client and user. If provided, this API is functionally equivalent to [Get-or-create an authorization for a specific app and fingerprint](https://developer.github.com/v3/oauth_authorizations/#get-or-create-an-authorization-for-a-specific-app-and-fingerprint). |

```
{
  "client_secret": "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcd",
  "scopes": [
    "public_repo"
  ],
  "note": "admin script"
}

```

### Response if returning a new token

```
Status: 201 Created
Location: https://api.github.com/authorizations/1

```

```
{
  "id": 1,
  "url": "https://api.github.com/authorizations/1",
  "scopes": [
    "public_repo"
  ],
  "token": "abcdefgh12345678",
  "token_last_eight": "12345678",
  "hashed_token": "25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8",
  "app": {
    "url": "http://my-github-app.com",
    "name": "my github app",
    "client_id": "abcde12345fghij67890"
  },
  "note": "optional note",
  "note_url": "http://optional/note/url",
  "updated_at": "2011-09-06T20:39:23Z",
  "created_at": "2011-09-06T17:26:27Z",
  "fingerprint": ""
}

```

### Response if returning an existing token

```
Status: 200 OK
Location: https://api.github.com/authorizations/1

```

```
{
  "id": 1,
  "url": "https://api.github.com/authorizations/1",
  "scopes": [
    "public_repo"
  ],
  "token": "",
  "token_last_eight": "12345678",
  "hashed_token": "25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8",
  "app": {
    "url": "http://my-github-app.com",
    "name": "my github app",
    "client_id": "abcde12345fghij67890"
  },
  "note": "optional note",
  "note_url": "http://optional/note/url",
  "updated_at": "2011-09-06T20:39:23Z",
  "created_at": "2011-09-06T17:26:27Z",
  "fingerprint": ""
}

```

## Get-or-create an authorization for a specific app and fingerprint

This method will create a new authorization for the specified OAuth application, only if an authorization for that application and fingerprint do not already exist for the user. The URL includes the 20 character client ID for the OAuth app that is requesting the token. `fingerprint` is a unique string to distinguish an authorization from others created for the same client ID and user. It returns the user's existing authorization for the application if one is present. Otherwise, it creates and returns a new one.

```
PUT /authorizations/clients/:client_id/:fingerprint

```

### Parameters

| Name            | Type     | Description                              |
| --------------- | -------- | ---------------------------------------- |
| `client_secret` | `string` | **Required**. The 40 character OAuth app client secret associated with the client ID specified in the URL. |
| `scopes`        | `array`  | A list of scopes that this authorization is in. |
| `note`          | `string` | A note to remind you what the OAuth token is for. |
| `note_url`      | `string` | A URL to remind you what app the OAuth token is for. |

```
{
  "client_secret": "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcd",
  "scopes": [
    "public_repo"
  ],
  "note": "admin script"
}

```

### Response if returning a new token

```
Status: 201 Created
Location: https://api.github.com/authorizations/1

```

```
{
  "id": 1,
  "url": "https://api.github.com/authorizations/1",
  "scopes": [
    "public_repo"
  ],
  "token": "abcdefgh12345678",
  "token_last_eight": "12345678",
  "hashed_token": "25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8",
  "app": {
    "url": "http://my-github-app.com",
    "name": "my github app",
    "client_id": "abcde12345fghij67890"
  },
  "note": "optional note",
  "note_url": "http://optional/note/url",
  "updated_at": "2011-09-06T20:39:23Z",
  "created_at": "2011-09-06T17:26:27Z",
  "fingerprint": "jklmnop12345678"
}

```

### Response if returning an existing token

```
Status: 200 OK
Location: https://api.github.com/authorizations/1

```

```
{
  "id": 1,
  "url": "https://api.github.com/authorizations/1",
  "scopes": [
    "public_repo"
  ],
  "token": "",
  "token_last_eight": "12345678",
  "hashed_token": "25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8",
  "app": {
    "url": "http://my-github-app.com",
    "name": "my github app",
    "client_id": "abcde12345fghij67890"
  },
  "note": "optional note",
  "note_url": "http://optional/note/url",
  "updated_at": "2011-09-06T20:39:23Z",
  "created_at": "2011-09-06T17:26:27Z",
  "fingerprint": "jklmnop12345678"
}

```

## Update an existing authorization

```
PATCH /authorizations/:id

```

### Parameters

| Name            | Type     | Description                              |
| --------------- | -------- | ---------------------------------------- |
| `scopes`        | `array`  | Replaces the authorization scopes with these. |
| `add_scopes`    | `array`  | A list of scopes to add to this authorization. |
| `remove_scopes` | `array`  | A list of scopes to remove from this authorization. |
| `note`          | `string` | A note to remind you what the OAuth token is for. Tokens not associated with a specific OAuth application (i.e. personal access tokens) must have a unique note. |
| `note_url`      | `string` | A URL to remind you what app the OAuth token is for. |
| `fingerprint`   | `string` | A unique string to distinguish an authorization from others created for the same client ID and user. |

You can only send one of these scope keys at a time.

```
{
  "add_scopes": [
    "repo"
  ],
  "note": "admin script"
}

```

### Response

```
Status: 200 OK

```

```
{
  "id": 1,
  "url": "https://api.github.com/authorizations/1",
  "scopes": [
    "public_repo"
  ],
  "token": "",
  "token_last_eight": "12345678",
  "hashed_token": "25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8",
  "app": {
    "url": "http://my-github-app.com",
    "name": "my github app",
    "client_id": "abcde12345fghij67890"
  },
  "note": "optional note",
  "note_url": "http://optional/note/url",
  "updated_at": "2011-09-06T20:39:23Z",
  "created_at": "2011-09-06T17:26:27Z",
  "fingerprint": "jklmnop12345678"
}

```

## Delete an authorization

```
DELETE /authorizations/:id

```

### Response

```
Status: 204 No Content

```

## Check an authorization

OAuth applications can use a special API method for checking OAuth token validity without running afoul of normal rate limits for failed login attempts. Authentication works differently with this particular endpoint. You must use [Basic Authentication](https://developer.github.com/v3/auth#basic-authentication) when accessing it, where the username is the OAuth application `client_id` and the password is its `client_secret`. Invalid tokens will return `404 NOT FOUND`.

```
GET /applications/:client_id/tokens/:access_token

```

### Response

```
Status: 200 OK

```

```
{
  "id": 1,
  "url": "https://api.github.com/authorizations/1",
  "scopes": [
    "public_repo"
  ],
  "token": "abcdefgh12345678",
  "token_last_eight": "12345678",
  "hashed_token": "25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8",
  "app": {
    "url": "http://my-github-app.com",
    "name": "my github app",
    "client_id": "abcde12345fghij67890"
  },
  "note": "optional note",
  "note_url": "http://optional/note/url",
  "updated_at": "2011-09-06T20:39:23Z",
  "created_at": "2011-09-06T17:26:27Z",
  "fingerprint": "jklmnop12345678",
  "user": {
    "login": "octocat",
    "id": 1,
    "avatar_url": "https://github.com/images/error/octocat_happy.gif",
    "gravatar_id": "",
    "url": "https://api.github.com/users/octocat",
    "html_url": "https://github.com/octocat",
    "followers_url": "https://api.github.com/users/octocat/followers",
    "following_url": "https://api.github.com/users/octocat/following{/other_user}",
    "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
    "organizations_url": "https://api.github.com/users/octocat/orgs",
    "repos_url": "https://api.github.com/users/octocat/repos",
    "events_url": "https://api.github.com/users/octocat/events{/privacy}",
    "received_events_url": "https://api.github.com/users/octocat/received_events",
    "type": "User",
    "site_admin": false
  }
}

```

## Reset an authorization

OAuth applications can use this API method to reset a valid OAuth token without end user involvement. Applications must save the "token" property in the response, because changes take effect immediately. You must use [Basic Authentication](https://developer.github.com/v3/auth#basic-authentication) when accessing it, where the username is the OAuth application `client_id` and the password is its `client_secret`. Invalid tokens will return `404 NOT FOUND`.

```
POST /applications/:client_id/tokens/:access_token

```

### Response

```
Status: 200 OK

```

```
{
  "id": 1,
  "url": "https://api.github.com/authorizations/1",
  "scopes": [
    "public_repo"
  ],
  "token": "abcdefgh12345678",
  "token_last_eight": "12345678",
  "hashed_token": "25f94a2a5c7fbaf499c665bc73d67c1c87e496da8985131633ee0a95819db2e8",
  "app": {
    "url": "http://my-github-app.com",
    "name": "my github app",
    "client_id": "abcde12345fghij67890"
  },
  "note": "optional note",
  "note_url": "http://optional/note/url",
  "updated_at": "2011-09-06T20:39:23Z",
  "created_at": "2011-09-06T17:26:27Z",
  "fingerprint": "jklmnop12345678",
  "user": {
    "login": "octocat",
    "id": 1,
    "avatar_url": "https://github.com/images/error/octocat_happy.gif",
    "gravatar_id": "",
    "url": "https://api.github.com/users/octocat",
    "html_url": "https://github.com/octocat",
    "followers_url": "https://api.github.com/users/octocat/followers",
    "following_url": "https://api.github.com/users/octocat/following{/other_user}",
    "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
    "organizations_url": "https://api.github.com/users/octocat/orgs",
    "repos_url": "https://api.github.com/users/octocat/repos",
    "events_url": "https://api.github.com/users/octocat/events{/privacy}",
    "received_events_url": "https://api.github.com/users/octocat/received_events",
    "type": "User",
    "site_admin": false
  }
}

```

## Revoke an authorization for an application

OAuth application owners can revoke a single token for an OAuth application. You must use [Basic Authentication](https://developer.github.com/v3/auth#basic-authentication) for this method, where the username is the OAuth application `client_id`and the password is its `client_secret`.

```
DELETE /applications/:client_id/tokens/:access_token

```

### Response

```
Status: 204 No Content

```

## Revoke a grant for an application

OAuth application owners can revoke a grant for their OAuth application and a specific user. You must use [Basic Authentication](https://developer.github.com/v3/auth#basic-authentication) for this method, where the username is the OAuth application `client_id` and the password is its `client_secret`. You must also provide a valid token as `:token`and the grant for the token's owner will be deleted.

Deleting an OAuth application's grant will also delete all OAuth tokens associated with the application for the user. Once deleted, the application will have no access to the user's account and will no longer be listed on [the application authorizations settings screen within GitHub](https://github.com/settings/applications#authorized).

```
DELETE /applications/:client_id/grants/:access_token

```

### Response

```
Status: 204 No Content

```

## More Information

It can be a little tricky to get started with OAuth. Here are a few links that might be of help:

- [OAuth 2 spec](http://tools.ietf.org/html/rfc6749)
- [Facebook Login API](http://developers.facebook.com/docs/technical-guides/login/)
- [Ruby OAuth2 lib](https://github.com/intridea/oauth2)
- [Simple Ruby/Sinatra example](https://gist.github.com/9fd1a6199da0465ec87c)
- [Python Flask example](https://gist.github.com/ib-lundgren/6507798) using [requests-oauthlib](https://github.com/requests/requests-oauthlib)
- [Simple Python example](https://gist.github.com/e3fbd47fbb7ee3c626bb) using [python-oauth2](https://github.com/dgouldin/python-oauth2)
- [Ruby OmniAuth example](https://github.com/intridea/omniauth)
- [Ruby Sinatra extension](https://github.com/atmos/sinatra_auth_github)
- [Ruby Warden strategy](https://github.com/atmos/warden-github)
- [Personal access tokens and SAML SSO](https://developer.github.com/v3/auth#authenticating-for-saml-sso)