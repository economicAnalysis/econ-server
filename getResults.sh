echo "-----------src/node-std*------------" > RESULTS.log
ssh root@localhost -p 50002 -i econapp_docker_rsa 'cat /var/log/supervisor/node-std*' >> RESULTS.log
echo "-----------src/ls*------------" >> RESULTS.log
ssh root@localhost -p 50002 -i econapp_docker_rsa 'cd /src; ls' >> RESULTS.log
echo "-----------test.txt------------" >> RESULTS.log
ssh root@localhost -p 50002 -i econapp_docker_rsa 'cat /test.txt' >> RESULTS.log
=======
echo "" >> RESULTS.log


cat RESULTS.log