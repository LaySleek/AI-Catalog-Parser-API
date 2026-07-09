#!/bin/bash

create_user() {

    local user="$1"

    if id "$user" &>/dev/null; then
        warn "User $user exists"
        return
    fi

    sudo useradd \
        --create-home \
        --shell /bin/bash \
        "$user"

    echo "$user:$user" | sudo chpasswd
}