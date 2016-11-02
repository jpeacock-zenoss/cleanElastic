## cleanElastic

These scripts have been written to help remove services from an install with the
Zookeeper problem "zk: buffer too small", preventing any removal of services from
Control Center.

### Running the script

Copy the two files to the CC master
run gen.py while serviced is running: python gen.py

You'll be presented with a numbered service tree to select which services you want
to remove from Control Center:

```
  1. [ ] Zenoss.resmgr [deadjil7v454osr4biaza0x1v]
  2.   [ ] Infrastructure [80ymizlk9gsznjzcsfgbk3g3c]
  3.     [ ] redis [8jcb032ofbr2f45f1s8l1so4b]
  4.     [ ] RabbitMQ [w54rf4xi47ha2ajqlrvs2u9w]
  5.     [ ] mariadb-model [7ymdbtpy958a7ull3eym9d985]
  6.     [ ] zencatalogservice [39hh3p44i6ajz735scp8l7m67]
  7.     [ ] mariadb-events [5l4adpj8o1qvmtmnjw3m5ry5l]
  8.     [ ] memcached [uutfagv95ko3f3io96vicxpv]
  9.     [ ] opentsdb [eovaurpeqetd6wfduvh7cbxj7]
 10.       [ ] reader [459589hx7brjmqxj54uotao0g]
 11.       [ ] writer [cw5lr6fb5t27dzljlm46t7ri8]
 12.     [ ] HBase [cakf4s87acaqpnyomro5vzlf5]
 13.       [ ] HMaster [c0g87yd2tfkjpquzfb51ha9on]
 14.       [ ] RegionServer [cwvhj2squhchv28iq8fscunqc]
 15.       [ ] ZooKeeper [ex020ehq7ldt5tohwsp0j7keu]
 16.   [ ] Zenoss [7t53amlt7acfu9yklolij1icq]
 17.     [ ] Collection [59aedxqo99limb46da2x9tds2]
 18.       [ ] localhost [4kcz96d7f5gr9iawnirszq7vq]
 19.         [ ] col1 [d2k6xj03h9b05k7mwe0maze6k]
 20.           [ ] zensyslog [djwhudmt95ko1bpq344ulk67c]
 21.           [ ] zenpython [582xqfthbaruwz2nxar5bomh]
 22.           [ ] zenmail [evmqbe2b6ibqxbh7hh2vmwwel]
 23.           [ ] zenvsphere [67qr816lelufbemzijfb1inc5]
 24.           [ ] zenjmx [9m8ui2qjm8zlh4kiqj4v63ro1]
 25.           [ ] zenucsevents [48ch3sbhekcrh10yp7oqqkf0q]
 26.           [ ] zentrap [8fmspsflqinded28gvepbeqsf]
 27.           [ ] zenmodeler [bxsw3nwokprnkrtcg9nkh4glz]
 28.           [ ] zenstatus [5enbnl3sj4d6ndsg5db0c1821]
 29.           [ ] zenping [2ykf3ts12snl7jvr3pv5w16q]
 30.           [ ] zenperfsnmp [2i7jv2cej1tj9mu9ymv74oeh7]
 31.           [ ] zenprocess [3qb7slfkos70maoo0ybkr6e9j]
 32.           [ ] zenwebtx [5mngmwqkss9fu3ydb1ez10yqv]
 33.           [ ] zenmailtx [96qrke3akjrzq64xcfhz8qnuw]
 34.           [ ] MetricShipper [33d7acmd1wlrntmr863eyewyy]
 35.           [ ] zminion [8qzfrlidehusx38ph3jd77sdq]
 36.           [ ] collectorredis [4wrsimd9ysj21i2hmbj1gl54w]
 37.           [ ] zencommand [8lwf3r0cpjasoqvvav04xux5i]
 38.           [ ] zenpropertymonitor [bss1thnamns82tm1eqm2ni7f]
 39.           [ ] zenpop3 [154rtq9e8rytqrkcig2ea5unn]
...
 82.         [ ] zenhub [e92y5mn929av69gnibjioduik]
 83.         [ ] localhost [e52d2p4zk7qbaf52ekhfuqqzp]
 84.           [ ] zenpop3 [4hiqrneeuhhlimn8ubqk01zc0]
 85.           [ ] zenmail [h9wgn99qixa8na9byhhifdla]
 86.           [ ] zensyslog [c6x4vstcjv6u8c6z66c39hwgy]
 87.           [ ] zenpython [3w92lzdvf9ctaw30kv8m71qq0]
 88.           [ ] zenvsphere [a93c02mc8x2m9tuwsqbh5eavz]
 89.           [ ] zenjmx [e099vy5pq1htf9o2prs2c6nwm]
 90.           [ ] zenucsevents [1ysgxubyj7rqmnzhr5musz72x]
 91.           [ ] zenstatus [btjc9dzr5wup22xwaaqapecye]
 92.           [ ] zentrap [3uihszj0bx9nt2lg8fscsxdwf]
 93.           [ ] zenmodeler [49zefdtu7yjoq7ublrk3gf27n]
 94.           [ ] zenping [1avtx229dmeoi7a45056ba5mq]
 95.           [ ] zenperfsnmp [96ctxktjefkdmbqkhs8ihqccp]
 96.           [ ] zenprocess [3af5k7hlaxxffwoj6g9i40oy2]
 97.           [ ] zenwebtx [9yel4g4ec477aoquz3azv4pgq]
 98.           [ ] MetricShipper [10bnnkt9h6pk8778llaogcr80]
 99.           [ ] zenmailtx [311x303abayaakrxor1qkq7ie]
100.           [ ] zminion [1bilpist8678a9dy02d9lxzgh]
101.           [ ] collectorredis [azvnbimn76myk6ttgfbxxeo5]
102.           [ ] zencommand [ckyuiraa6jgzvxy35so5o6gzr]
103.           [ ] zenpropertymonitor [cfbxyonnkjww2hliv24nfyyk7]
103.           [ ] zenpropertymonitor [cfbxyonnkjww2hliv24nfyyk7]
104.     [ ] Events [dfiq6ldxsuf7rdyge3s2t8suy]
105.       [ ] zeneventd [df344ws5bkev1wrbd7beajeo4]
106.       [ ] zenactiond [2d5im0o6op2ephjn1271o0xpe]
107.       [ ] zeneventserver [98gk7kas0lvtx67d7560zxdbq]
108.     [ ] Metrics [91mw319kug0tcmg6hp01zfjrn]
109.       [ ] MetricConsumer [2p3l6w168hpe6kcngy2qmpwc4]
110.       [ ] CentralQuery [1wzvajhc6u4qor864prorhei4]
111.       [ ] MetricShipper [dhquuzgxbglf5t5iu91soy9d0]
112.     [ ] User Interface [1j0ugbb4wjn20eazwxbh439jr]
113.       [ ] Zope [c8vh8ahw90h8jsi76lq6liiiw]
114.       [ ] Zauth [eo34ufbfq7j2felntqcbyqbss]
115.       [ ] zenjobs [3s6yo9vyapl4s431wrnfa4c1f]
116.       [ ] zenjserver [abz1ueew1giod48hgwnabxp7v]

Select a service by number, 'p' to process the items, 'quit' or 'exit' to abort: 19
```

Toggle services to remove by entering the numbers.  When you have all services you want to remove
selected, enter 'p' to generate scripts and inspect the running serviced.

You'll be presented with a set of steps to run to perform the cleanup:
```
Steps to clean services from Elastic:

  1) Stop serviced: sudo systemctl stop serviced (on all hosts)
  2) run: docker run  -v /opt/serviced/var/isvcs/elasticsearch-serviced/data:/opt/elasticsearch-0.90.9/data -v /opt/serviced/isvcs/resources:/usr/local/serviced/resources -v /tmp/startElastic.sh:/tmp/startElastic.sh -v /home/zenny/
removeService.py:/tmp/removeService.py -v /tmp/removeServices.sh:/tmp/removeServices.sh -it f18c53e2acb34e266d9d3b595cf7cf998c7efc5248e4d9083ab50776718cc64b bash
    a) In the container: bash /tmp/startElastic.sh (wait for 'recovered [1] indices into cluster_state')
       * Note: If you don't see '[1] indices', check to make sure all serviced are stopped and try again
    b) In the container: bash /tmp/removeServices.sh
    c) Exit the container: exit
  3) run: sudo rm -rf /opt/serviced/var/isvcs/zookeeper *for ALL hosts*
  4) Start serviced: sudo systemctl start serviced (master first, then delegates)
```

Follow the steps above to remove the services from Control Center.

## What does it do?

1. shuts down serviced on all hosts.

2. runs a docker container with Elastic, mapping the generated scripts into the container.

2a. Starts Elastic in the container.

2b. Removes the selected services from Elastic.

3. Blows away the isvcs Zookeeper data.

4. Starts Control Center.  Zookeeper will reload itself from Elastic, without the removed services.

## How are the services removed?

The service document is removed using curl:

```curl -XDELETE 'http://localhost:9200/controlplane/service/serviceid'```

The address assignments are removed:

```curl -XDELETE 'http://localhost:9200/controlplane/addressassignment/serviceid'```

Each service config is removed by querying for all service configs with a path ending in this serviceid:

```curl -H "Content-Type: application/json" -XGET -d '{"fields": ["_id"], "query": {"wildcard": { "ServicePath":  "*/serviceid" }}}' http://localhost:9200/_search```

For each document id found, it gets removed:

```curl -XDELETE 'http://localhost:9200/controlplane/svcconfigfile/docid'```
