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