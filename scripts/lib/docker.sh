#!/bin/bash

########################################
# Utility Functions
########################################

image_exists() {
    local tag="$1"
    docker image inspect "$tag" > /dev/null 2>&1
}

build_image() {

    local dir="$1"
    local tag="${2:-}"

    if [ ! -d "$dir" ]; then
        warn "$dir missing"
        return
    fi

    cd "$dir"

    if [[ -n "$tag" ]] && [[ "$FORCE_REBUILD" != true ]]; then
        if image_exists "$tag"; then
            warn "Image exists, skipping: ${CYAN}$tag${NC}"
            return
        fi
    fi

    if [ -f docker-compose.yml ]; then

        info "docker compose build $dir"

        docker compose pull --ignore-pull-failures
        docker compose build --pull

    elif [ -f Dockerfile ]; then

        if [ -n "$tag" ]; then
            info "docker build ${CYAN}$tag${NC}"
            docker build -t "$tag" .
        else
            info "docker build $dir"
            docker build .
        fi

    else
        warn "No docker build config in $dir"
    fi
}