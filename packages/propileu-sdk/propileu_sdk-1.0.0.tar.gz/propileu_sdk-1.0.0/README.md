# Propileu SDK

[![Build Status](https://travis-ci.com/juntossomosmais/propileu-sdk.svg?token=cfB1EHQmosyKPne1bPRP&branch=master)](https://travis-ci.com/juntossomosmais/propileu-sdk)
[![Maintainability](https://api.codeclimate.com/v1/badges/b8056e184a75503d3a5f/maintainability)](https://codeclimate.com/repos/5c76824edd77990240012db0/maintainability) 
[![Test Coverage](https://api.codeclimate.com/v1/badges/b8056e184a75503d3a5f/test_coverage)](https://codeclimate.com/repos/5c76824edd77990240012db0/test_coverage)

---

SDK based on DRF and other services configure on [Propileu](https://github.com/juntossomosmais/propileu).

## How to use it

You must set the following environment properties:

- `PROPILEU_SDK_AUTH`: Sample value is `http://localhost:8081/api/v1/api-token-auth/`
- `PROPILEU_SDK_READ_WRITE_HOST`: Sample value is `http://localhost:8081/api/v1/`
- `PROPILEU_USERNAME`: Username which was created on Django
- `PROPILEU_PASSWORD`: Password bound to the previous user

These ones are optional:

- `PROPILEU_SDK_READ_HOST`: If there is a specific host to only READ DATA
- `REQUESTS_TIMEOUT`: its default value is 30
- `REQUESTS_MAX_RETRIES`: its default value is 3

## Important notice

The purpose of this App and even this README is not fully closed.
