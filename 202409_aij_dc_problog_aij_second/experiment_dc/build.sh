#!/bin/bash
set -exu
docker build --tag local/dc_problog -f Dockerfile ./
