#!/usr/bin/env bash
dropdb recommend_app_test

psql << EOF
create database recommend_app_test;
EOF


