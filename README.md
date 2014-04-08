# Memcached Tools
## About
This is a utility container designed to perform dump and restore of memcached
data.  


## Usage

This cointainer takes (at a minimum) one environment variable, 
`MEMCACHED_SERVERS`.  This value should be a string of the form "host:port"

Additionally, this container can make use of the **link** feature of Docker
leveraging a destination value of `MC`.  Examples are shown below.  There are
three primitives available to the container:
- dump - Dump all data in the remote memcached server to /tmp/memcache
- load - Load all data from the path /tmp/memcache to the remote memcached server
- sample - Generate 899 sample keys of the form mykeyXXX and add them to the server

```
$ mkdir /tmp/test
$ docker run --rm -e MEMCACHED_SERVERS=192.168.1.101:11211 -v /tmp/test:/tmp/memcache brianredbeard/memcache-tools dump
```

## Examples

In this example we will create a memcached container, load it with sample data,
verify we can see the values, flush the cache, reload our data, and finally
verify that the values match.

### Install the memcached server:

```
$ docker run -p 11211 -d --name memcached jacksoncage/memcache
```

### Load sample data into the container, utilizing a docker link

```
$ mkdir /tmp/test
$ docker run --rm --link memcached:mc -v /tmp/test:/tmp/memcache brianredbeard/memcache-tools sample
```

### Verify that the data is there

```
$ docker ps 
CONTAINER ID        IMAGE                         COMMAND             CREATED             STATUS              PORTS                      NAMES
f053e93d69e2        jacksoncage/memcache:latest   bash start.sh       44 seconds ago      Up 41 seconds       0.0.0.0:49154->11211/tcp   memcache  
$ telnet 127.0.0.1 49154
Trying ::1...
Connected to localhost.
Escape character is '^]'.
stats items
STAT items:3:number 899
STAT items:3:age 10
STAT items:3:evicted 0
STAT items:3:evicted_nonzero 0
STAT items:3:evicted_time 0
STAT items:3:outofmemory 0
STAT items:3:tailrepairs 0
STAT items:3:reclaimed 0
STAT items:3:expired_unfetched 0
STAT items:3:evicted_unfetched 0
END
get mykey600
VALUE mykey600 1 49
(dp1
S'lang'
p2
S'python'
p3
sS'value'
p4
I448
s.
END
```
Here we see that on slab 3 we have 899 values in the cache and that the key
**mykey600** has the integer value *448* stored inside it's object.

### Dump the contents of the cache

```
$ docker run --rm --link memcached:mc -v /tmp/test:/tmp/memcache brianredbeard/memcache-tools dump
```

You will find that in /tmp/test there will be 899 files, each with the name of
a key.  The contents of each file correlate to the respective key on the 
memcached server.

### Flushing the memcached cache

```
$ telnet 127.0.0.1 49154
Trying ::1...
Connected to localhost.
Escape character is '^]'.
flush_all 1
OK
get mykey600
END
```

This sets all values to immediately have a one second TTL, effectively expiring
the entire cache.  Attempting to retrieve the value of **mykey600** results in 
no data returned.

### Reload our sample data

```
$ docker run --rm --link memcached:mc -v /tmp/test:/tmp/memcache brianredbeard/memcache-tools load
```

At this point our data should be reloaded.

### Verification of data
```
$ telnet 127.0.0.1 49154
Trying ::1...
Connected to localhost.
Escape character is '^]'.
get mykey600
VALUE mykey600 1 49
(dp1
S'lang'
p2
S'python'
p3
sS'value'
p4
I448
s.
END
```

