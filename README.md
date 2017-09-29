# Proyecto-GestionOSWebservices
Flask webservice packing into a Dockerfile

git clone https://github.com/AndresHerrera/Proyecto-GestionOSWebservices.git

## Video (asciinema)

https://asciinema.org/a/QLPaAvjKPNz79U4eOlCOIFHBd


## Build a  Docker container

$docker build -t oswebservice:latest .

## Start Docker microservice as a daemon

$docker run -d -p 6060:5000 -v $(pwd):/app oswebservice

## Usage  ( Complete command list ) :

$ curl -i http://localhost:6060/

## Extended list

<table style='width:100%'><tr><th>METHOD</th><th>URL</th><th>JSON Response</th></tr><tr><td colspan=3 align=center><b>WHO</b></td></tr><tr><td>GET</td><td>curl http://localhost:6060/who</td><td>show who is logged on</td></tr><tr><td>GET</td><td>curl http://localhost:6060/who/user</td><td>check if user is logged on</td></tr><tr><td colspan=3 align=center><b>CPU</b></td></tr><tr><td>GET</td><td>curl http://localhost:6060/cpu/us</td><td>Time spent running non-kernel code.  (user time, including nice time)</td></tr><tr><td>GET</td><td>curl http://localhost:6060/cpu/sy</td><td>Time spent running kernel code.  (system time)</td></tr><tr><td>GET</td><td>curl http://localhost:6060/cpu/id</td><td>Time spent idle.</td></tr><tr><td>GET</td><td>curl http://localhost:6060/cpu/wa</td><td>Time spent waiting for IO.</td></tr><tr><td>GET</td><td>curl http://localhost:6060/cpu/st</td><td>Time stolen from a virtual machine.</td></tr><tr><td colspan=3 align=center><b>OS</b></td></tr><tr><td>GET</td><td>curl http://localhost:6060/os/kernel</td><td>kernel name.</td></tr><tr><td>GET</td><td>curl http://localhost:6060/os/release</td><td>release.</td></tr><tr><td>GET</td><td>curl http://localhost:6060/os/nodename</td><td>nodename.</td></tr><tr><td>GET</td><td>curl http://localhost:6060/os/kernelversion</td><td>kernelversion.</td></tr><tr><td>GET</td><td>curl http://localhost:6060/os/machine</td><td>machine.</td></tr><tr><td>GET</td><td>curl http://localhost:6060/os/processor</td><td>processor.</td></tr><tr><td>GET</td><td>curl http://localhost:6060/os/operatingsystem</td><td>operatingsystem.</td></tr><tr><td>GET</td><td>curl http://localhost:6060/os/hardware</td><td>hardware.</td></tr><tr><td colspan=3 align=center><b>MEMORY</b></td></tr><tr><td>GET</td><td>curl http://localhost:6060/mem/swpd</td><td>shows the amount of virtual memory used.</td></tr><tr><td>GET</td><td>curl http://localhost:6060/mem/free</td><td>shows the amount of idle memory.</td></tr><tr><td>GET</td><td>curl http://localhost:6060/mem/buff</td><td>shows the amount of memory used as buffers.</td></tr><tr><td>GET</td><td>curl http://localhost:6060/mem/cache</td><td>shows the amount of memory used as cache.</td></tr><tr><td colspan=3 align=center><b>MISC</b></td></tr><tr><td>GET</td><td>curl http://localhost:6060/misc/uptime</td><td>Tell how long the system has been running.</td></tr><tr><td>GET</td><td>curl http://localhost:6060/misc/battery</td><td>Shows battery status and capacity.</td></tr><tr><td>POST</td><td>curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Docker"}' http://localhost:6060//misc/locate</td><td>Find files by name </td></tr></table>



