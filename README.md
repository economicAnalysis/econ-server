data is stored in the format


```js
 {
   date: month_year,
   pce_avghr: {
     [
       {average_hour_value: value,
        pce_value: value,
        date: date
        },
        {average_hour_value: value,
        pce_value: value,
        date: date
        },...
      ]
   },
   
 }
```

####Useful information
The server listens on port 5000

the link command takes the form `--link name:alias`

######ssh into the container

```
ssh root@localhost -p 50002 -i econapp_docker_rsa
```

######linking to localhost

The following code controls how the server in the container is mapped to the 
host. When we're running on localhost the port, which is port 5000 in the 
container, is mapped to the variable `port_db` on localhost. In the default
`sample.yml` file the value for `port_db` is 50001. Hence, the app is available
at url: http://localhost:50001

```
-p {{ port_db }}:5000
```