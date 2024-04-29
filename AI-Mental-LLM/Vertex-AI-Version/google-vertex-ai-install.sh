# # Option  1 install

# apt-get update
# apt-get install apt-transport-https ca-certificates gnupg curl

# # add key 
# curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg

# echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list


# apt-get update && apt-get install google-cloud-cli


# option 2 install
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-473.0.0-linux-x86_64.tar.gz
tar -xf google-cloud-cli-473.0.0-linux-x86_64.tar.gz
./google-cloud-sdk/install.sh




