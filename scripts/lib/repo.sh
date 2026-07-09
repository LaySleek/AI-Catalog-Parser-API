#!/bin/bash

sync_repo() {

    local dir="$1"
    local cmd="$2"

    if [ -d "$dir/.git" ]; then

        if [[ "$UPDATE_REPOS" == true ]]; then
            info "Updating repository ${CYAN}$dir${NC}"

            sudo -u "$OWNER_USER" bash -c "
                cd '$dir'
                git fetch --all
                git pull
            "
        else
            warn "$dir already exists, skipping"
        fi

        return
    fi

    info "Cloning repository ${CYAN}$dir${NC}"

    mkdir -p "$dir"

    sudo -u "$OWNER_USER" bash -c "
        cd '$dir'
        $cmd
    "
}