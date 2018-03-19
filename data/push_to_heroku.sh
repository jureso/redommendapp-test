#!/usr/bin/env bash
# If needed run first:
# heroku pg:reset DATABASE_URL --app recommendapp-test
heroku pg:push postgresql://localhost/recommend_app_test DATABASE_URL --app recommendapp-test