#!/bin/bash

idx=0

# Total number of nodes
num_of_total_servers=24

# Node Hostname
HOSTNAME="FailureHandling.nova-PG0.wisc.cloudlab.us"

# Your own user name of cloudlab
USERNAME="NAME"
REMOTE_HOME="/users/${USERNAME}"

# Should be your own github token
GITHUB_TOKEN=""

# Fork our repository and replace this with your own
GITHUB_REPO="https://${GITHUB_TOKEN}:@github.com/flslab/FailureHandling.git"

now=$(date +%d_%b_%H_%M_%S)


# This is only used to setup nodes for the first time.
i=0
server_addr=${USERNAME}@node-$i.${HOSTNAME}
scp -oStrictHostKeyChecking=no ~/.ssh/id_rsa ${server_addr}:${REMOTE_HOME}/.ssh/

# This can be used to delete the .ssh key
#    ssh -oStrictHostKeyChecking=no ${server_addr} "rm ${REMOTE_HOME}/.ssh/id_rsa"

for (( i=0; i<num_of_total_servers; i++ )); do
    server_addr=${USERNAME}@node-$i.${HOSTNAME}
    # This is only used to clone and setup for the first time
    ssh -oStrictHostKeyChecking=no ${server_addr} "git clone ${GITHUB_REPO}" &
#    ssh -oStrictHostKeyChecking=no ${server_addr} "cd FailureHandling && mkdir log && bash setup.sh" &

    # This is for killing all the running processes
#    ssh -oStrictHostKeyChecking=no ${server_addr} "sudo pkill python3" &

    # This can be use to pull updates from the repository
#   ssh -oStrictHostKeyChecking=no ${server_addr} "cd FailureHandling && git pull" &
#   ssh -oStrictHostKeyChecking=no ${server_addr} "cd FailureHandling && git fetch --all && git reset --hard origin/main" &
#   ssh -oStrictHostKeyChecking=no ${server_addr} "cd FailureHandling && git checkout main" &
done
