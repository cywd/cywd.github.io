---
layout: post
title: About authorization options for OAuth Apps
excerpt: ""
categories: [GitHub]
tags: [GitHub, API]
date: 2017-12-06
comments: true
---

* TOC
{:toc}
---

## Web Application Flow

The flow to authorize users for your app is:

- Users are redirected to request their GitHub identity
- Users are redirected back to your site by GitHub
- Your app accesses the API with the user's access token

### 1. Users are redirected to request their GitHub identity

```
GET https://github.com/login/oauth/authorize

```

**Parameters**

| Name           | Type     | Description                              |
| -------------- | -------- | ---------------------------------------- |
| `client_id`    | `string` | **Required**. The client ID you received from GitHub when you [registered](https://github.com/settings/applications/new). |
| `redirect_uri` | `string` | The URL in your application where users will be sent after authorization. See details below about [redirect urls](https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/#redirect-urls). |
| `scope`        | `string` | A space-delimited list of [scopes](https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-scopes-for-oauth-apps/). If not provided, `scope`defaults to an empty list for users that have not authorized any scopes for the application. For users who have authorized scopes for the application, the user won't be shown the OAuth authorization page with the list of scopes. Instead, this step of the flow will automatically complete with the set of scopes the user has authorized for the application. For example, if a user has already performed the web flow twice and has authorized one token with `user` scope and another token with `repo`scope, a third web flow that does not provide a `scope` will receive a token with `user` and `repo` scope. |
| `state`        | `string` | An unguessable random string. It is used to protect against cross-site request forgery attacks. |
| `allow_signup` | `string` | Whether or not unauthenticated users will be offered an option to sign up for GitHub during the OAuth flow. The default is `true`. Use `false` in the case that a policy prohibits signups. |

### 2. Users are redirected back to your site by GitHub

If the user accepts your request, GitHub redirects back to your site with a temporary `code` in a code parameter as well as the state you provided in the previous step in a `state` parameter. If the states don't match, the request was created by a third party and the process should be aborted.

Exchange this `code` for an access token:

```
POST https://github.com/login/oauth/access_token

```

**Parameters**

| Name          | Type   | Description                              |
| ------------- | ------ | ---------------------------------------- |
| client_id     | string | **Required.** The client ID you received from GitHub for your GitHub App. |
| client_secret | string | **Required.** The client secret you received from GitHub for your GitHub App. |
| code          | string | **Required.** The code you received as a response to Step 1. |
| redirect_uri  | string | The URL in your application where users are sent after authorization. |
| state         | string | The unguessable random string you provided in Step 1. |

**Response**

By default, the response takes the following form:

`access_token=e72e16c7e42f292c6912e7710c838347ae178b4a&token_type=bearer`

You can also receive the content in different formats depending on the Accept header:

```
Accept: application/json
{"access_token":"e72e16c7e42f292c6912e7710c838347ae178b4a", "scope":"repo,gist", "token_type":"bearer"}

Accept: application/xml
<OAuth>
  <token_type>bearer</token_type>
  <scope>repo,gist</scope>
  <access_token>e72e16c7e42f292c6912e7710c838347ae178b4a</access_token>
</OAuth>

```

### 3. Use the access token to access the API

The access token allows you to make requests to the API on a behalf of a user.

GET <https://api.github.com/user?access_token=>...

You can pass the token in the query params as shown above, but a cleaner approach is to include it in the Authorization header.

Authorization: token OAUTH-TOKEN

For example, in curl you can set the Authorization header like this:

```
curl -H "Authorization: token OAUTH-TOKEN" https://api.github.com/user

```

## Non-Web Application Flow

Use [Basic Authentication](https://developer.github.com/v3/auth#basic-authentication) to create an OAuth2 token using the [interface](https://developer.github.com/v3/oauth_authorizations/#create-a-new-authorization). With this technique, a username and password doesn't need to be permanently stored and the user can revoke access at any time.

**Note:** When using the non-web application flow to create an OAuth2 token, make sure to understand how to [work with two-factor authentication](https://developer.github.com/v3/auth/#working-with-two-factor-authentication) if you or your users have two-factor authentication enabled.

## Redirect URLs

The `redirect_uri` parameter is optional. If left out, GitHub will redirect users to the callback URL configured in the OAuth Application settings. If provided, the redirect URL's host and port must exactly match the callback URL. The redirect URL's path must reference a subdirectory of the callback URL.

```
CALLBACK: http://example.com/path

GOOD: http://example.com/path
GOOD: http://example.com/path/subdir/other
BAD:  http://example.com/bar
BAD:  http://example.com/
BAD:  http://example.com:8080/path
BAD:  http://oauth.example.com:8080/path
BAD:  http://example.org
```