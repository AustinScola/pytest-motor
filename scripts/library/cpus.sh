#!/bin/bash

function get_number_of_cpus() {
    local NUMBER_OF_CPUS="$(nproc)"
    echo "${NUMBER_OF_CPUS}"
}
