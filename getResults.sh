echo "-----------src/node-std*------------" > RESULTS.log
ssh root@localhost -p 50002 -i econapp_docker_rsa 'cat /var/log/supervisor/node-std*' >> RESULTS.log
echo "" >> RESULTS.log


cat RESULTS.log