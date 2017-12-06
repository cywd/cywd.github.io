---
layout: post
title: Other Authentication Methods
excerpt: ""
categories: [GitHub]
tags: [GitHub, API]
date: 2017-12-06
comments: true
---

* TOC
{:toc}
---


- [Basic Authentication](https://developer.github.com/v3/auth/#basic-authentication)
- [Working with two-factor authentication](https://developer.github.com/v3/auth/#working-with-two-factor-authentication)

While the API provides multiple methods for authentication, we strongly recommend using [OAuth](https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/)for production applications. The other methods provided are intended to be used for scripts or testing (i.e., cases where full OAuth would be overkill). Third party applications that rely on GitHub for authentication should not ask for or collect GitHub credentials. Instead, they should use the [OAuth web flow](https://developer.github.com/apps/building-integrations/setting-up-and-registering-oauth-apps/about-authorization-options-for-oauth-apps/).

## Basic Authentication

The API supports Basic Authentication as defined in [RFC2617](http://www.ietf.org/rfc/rfc2617.txt) with a few slight differences. The main difference is that the RFC requires unauthenticated requests to be answered with `401 Unauthorized` responses. In many places, this would disclose the existence of user data. Instead, the GitHub API responds with `404 Not Found`. This may cause problems for HTTP libraries that assume a `401 Unauthorized` response. The solution is to manually craft the `Authorization` header.

### Via Username and Password

To use Basic Authentication with the GitHub API, simply send the username and password associated with the account.

For example, if you're accessing the API via [cURL](http://curl.haxx.se/), the following command would authenticate you if you replace `<username>` with your GitHub username. (cURL will prompt you to enter the password.)

```
curl -u username https://api.github.com/user

```

### Via OAuth Tokens

Alternatively, you can use [personal access tokens](https://github.com/blog/1509-personal-api-tokens) or OAuth tokens instead of your password.

```
curl -u username:token https://api.github.com/user

```

This approach is useful if your tools only support Basic Authentication but you want to take advantage of OAuth access token security features.

### Authenticating for SAML SSO

**Note:** Integrations and Oauth applications that generate tokens on behalf of others are automatically whitelisted.

If you're using the API to access an organization that enforces [SAML SSO](https://help.github.com/articles/about-identity-and-access-management-with-saml-single-sign-on) for authentication, you'll need to create a personal access token (PAT) and [whitelist the token](https://help.github.com/articles/authorizing-a-personal-access-token-for-use-with-a-saml-single-sign-on-organization/) for that organization. Visit the URL specified in `X-GitHub-SSO` to whitelist the token for the organization.

```
curl -v -H "Authorization: token TOKEN" https://api.github.com/repos/octodocs-test/test

X-GitHub-SSO: required; url=https://github.com/orgs/octodocs-test/sso?authorization_request=AZSCKtL4U8yX1H3sCQIVnVgmjmon5fWxks5YrqhJgah0b2tlbl9pZM4EuMz4
{
  "message": "Resource protected by organization SAML enforcement. You must grant your personal token access to this organization.",
  "documentation_url": "https://help.github.com"
}

```

When requesting data that could come from multiple organizations (for example, [requesting a list of issues created by the user](https://developer.github.com/v3/issues/#list-issues)), the `X-GitHub-SSO` header indicates which organizations require whitelisting:

```
curl -v -H "Authorization: token TOKEN" https://api.github.com/user/issues

X-GitHub-SSO: partial-results; organizations=21955855,20582480

```

The value `organizations` is a comma-separated list of organization IDs for organizations that require whitelisting.

## Working with two-factor authentication

For users with two-factor authentication enabled, Basic Authentication requires an extra step. When you attempt to authenticate with Basic Authentication, the server will respond with a `401`and an `X-GitHub-OTP: required; :2fa-type` header. This indicates that a two-factor authentication code is needed (in addition to the username and password). The `:2fa-type` in this header indicates whether the account receives its two-factor authentication codes via SMS or via an application.

In addition to the Basic Authentication credentials, you must send the user's authentication code (i.e., one-time password) in the `X-GitHub-OTP` header. Because these authentication codes expire quickly, we recommend using the Authorizations API to [create an access token](https://developer.github.com/v3/oauth_authorizations/#create-a-new-authorization) and using that token to [authenticate via OAuth](https://developer.github.com/v3/#authentication) for most API access.

Alternately, you can create access tokens from the Personal Access Token [settings page](https://github.com/settings/tokens).