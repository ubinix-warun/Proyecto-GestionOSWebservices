#!/usr/bin/python
#
# El siguiente programa permite obtener algunos valores de un sistema operativo
# Linux pero que se accede a la informacion a traves de Web Services.
#  
# Basado en el ejemplo de curso Fundamentos de Sistemas Distribuidos
# DS-Fall 2007 -  Docente : John Sanabria - john.sanabria@correounivalle.edu.co   
#
# Alumnos:  Fabio Andres Herrera - fabio.herrera@correounivalle.edu.co
#                  Mario Castillo - mario.castillo@correounivalle.edu.co
#
#
#
 
# Librerias que se requieren para correr la aplicacion
from flask import Flask, jsonify, make_response,  request
import subprocess

 
app = Flask(__name__)


@app.route('/')
@app.route('/index.htm')
@app.route('/index.html')
def index():
    request_host=request.host
    output = "<html><head><style>table,th,td{border:1px solid black;border-collapse:collapse;}</style></head><body>" 
    output += "<h2>OS WebService</h2>"
    output +="<h3>By:<br>Andres Herrera - fabio.herrera@correounivalle.edu.co"
    output +="<br>Mario Castillo - mario.castillo@correounivalle.edu.co</h3>"
    output +="<h3>Usage:</h3>"
    output +="<table style='width:100%'><tr><th>METHOD</th><th>URL</th><th>JSON Response</th></tr>"
    output +="<tr><td colspan=3 align=center><b>WHO</b></td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/who</td><td>show who is logged on</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/who/user</td><td>check if user is logged on</td></tr>"
    output +="<tr><td colspan=3 align=center><b>CPU</b></td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/cpu/us</td><td>Time spent running non-kernel code.  (user time, including nice time)</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/cpu/sy</td><td>Time spent running kernel code.  (system time)</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/cpu/id</td><td>Time spent idle.</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/cpu/wa</td><td>Time spent waiting for IO.</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/cpu/st</td><td>Time stolen from a virtual machine.</td></tr>"
    output +="<tr><td colspan=3 align=center><b>OS</b></td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/os/kernel</td><td>kernel name.</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/os/release</td><td>release.</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/os/nodename</td><td>nodename.</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/os/kernelversion</td><td>kernelversion.</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/os/machine</td><td>machine.</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/os/processor</td><td>processor.</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/os/operatingsystem</td><td>operatingsystem.</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/os/hardware</td><td>hardware.</td></tr>"
    output +="<tr><td colspan=3 align=center><b>MEMORY</b></td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/mem/swpd</td><td>shows the amount of virtual memory used.</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/mem/free</td><td>shows the amount of idle memory.</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/mem/buff</td><td>shows the amount of memory used as buffers.</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/mem/cache</td><td>shows the amount of memory used as cache.</td></tr>"
    output +="<tr><td colspan=3 align=center><b>MISC</b></td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/misc/uptime</td><td>Tell how long the system has been running.</td></tr>"
    output +="<tr><td>GET</td><td>curl http://"+request_host+"/misc/battery</td><td>Shows battery status and capacity.</td></tr>"
    output +="<tr><td>POST</td><td>curl -i -H \"Content-Type: application/json\" -X POST -d '{\"name\":\"Docker\"}' http://"+request_host+"/misc/locate</td><td>Find files by name </td></tr>"
    output +="</table>"
    output +="</body></html>"
    return output
    
    

# ###################################
#
# Este metodo se usa para determinar que personas estan conectadas usando el 
# comando 'who'. 
#
# 'who | cut -d ' ' -f 1 | uniq'
#
# curl http://localhost:5000/who
#
# ###################################

@app.route('/who',methods = ['GET'])
def who():
        who = subprocess.Popen(['who'], stdout = subprocess.PIPE)
        cut = subprocess.Popen(['cut', '-d', ' ', '-f', '1'], stdin = who.stdout, stdout = subprocess.PIPE)
        output = subprocess.check_output(('uniq'), stdin = cut.stdout)
        return jsonify({'users': output})
 
# ################################### 
#
# Este metodo permite determinar si un usuario en particular esta conectado.
#
# 'who | cut -d ' ' -f 1 | grep ${USERNAME} | uniq'
#
# curl http://localhost:5000/who/john
#
# ###################################

@app.route('/who/<string:useri>',methods = ['GET'])
def whou(useri):
        who = subprocess.Popen(['who'], stdout = subprocess.PIPE)
        cut = subprocess.Popen(['cut', '-d', ' ', '-f', '1'], stdin = who.stdout, stdout = subprocess.PIPE)
        user = subprocess.Popen(['grep', useri], stdin = cut.stdout, stdout = subprocess.PIPE)
        output = subprocess.check_output(('uniq'), stdin = user.stdout)
        if output =='':
            return make_response(jsonify({'error': 'user-> %s not logged in' % useri }), 404)
        else:
            return jsonify({'loggedin': output})
    
# ###################################
# Este metodo es usado para determinar el uso de la CPU. 
#
# Si quiere saber mas detalles de este comando, desde la terminal, ejecute el
# comando 'man vmstat' o visite https://linux.die.net/man/8/vmstat 
#
# 14: tiempo invertido en la ejecucion de codigo que no es del kernel
# 15: tiempo invertido en la ejecucion de codigo del kernel
# 16: tiempo inactivo 
# 17: tiempo invertido en la espera de operaciones de IO
# 18: tiempo que se toma desde una maquina virtual
#
# vmstat | tail -n +3 | tr -s ' ' | cut -d ' ' -f n
#
# curl http://localhost:5000/cpu/us (valor 14)
# curl http://localhost:5000/cpu/sy (valor 15)
# curl http://localhost:5000/cpu/id (valor 16)
# curl http://localhost:5000/cpu/wa (valor 17)
# curl http://localhost:5000/cpu/st (valor 18)
#
# ###################################

@app.route('/cpu/<string:param>', methods = ['GET'])
def cpuwa(param):
        vmstat = subprocess.Popen(['vmstat'], stdout = subprocess.PIPE)
        tail = subprocess.Popen(['tail','-n','+3'], stdin = vmstat.stdout, stdout = subprocess.PIPE)
        tr = subprocess.Popen(['tr', '-s', ' '], stdin = tail.stdout, stdout = subprocess.PIPE)
        
        choices = {'us': 14, 'sy': 15,  'id':16 ,  'wa':17,  'st':18}
        value = choices.get(param, 'default')
        if value=='default':
            return make_response(jsonify({'error': 'Unknown param use -> us, sy, id, wa, st'}), 404)
        else:
            output = subprocess.check_output(['cut', '-d', ' ', '-f', str(value)], stdin = tr.stdout)
            return jsonify({'cpu %s' % param: output})
            
# ###################################
#
# Web service que entrega informacion relativa a esta maquina
#
# curl http://localhost:5000/os
#
# ###################################

@app.route('/os',methods=['GET'])
def os():
        kernel = subprocess.check_output(['uname','-s'])
        release = subprocess.check_output(['uname','-r'])
        nodename = subprocess.check_output(['uname','-n'])
        kernelv = subprocess.check_output(['uname','-v'])
        machine = subprocess.check_output(['uname','-m'])
        processor = subprocess.check_output(['uname','-p'])
        os = subprocess.check_output(['uname','-o'])
        hardware = subprocess.check_output(['uname','-i'])
        return jsonify({'kernel': kernel,
                        'release': release,
                        'node_name': nodename,
                        'kernel_version': kernelv,
                        'machine': machine,
                        'processor': processor,
                        'operating_system': os,
                        'hardware_platform': hardware})
 
# ###################################
# Funcion que recupera informacion relativa a un parametro especifico del host
#
# Posibles valores
#
# - kernel
# - release
# - nodename
# - kernelversion
# - machine
# - processor
# - operatingsystem
# - hardware
#
# Metodo de acceso
# curl http://localhost:5000/os/kernel
# curl http://localhost:5000/os/release
# curl http://localhost:5000/os/nodename
# curl http://localhost:5000/os/kernelversion
# curl http://localhost:5000/os/machine
# curl http://localhost:5000/os/processor
# curl http://localhost:5000/os/operatingsystem
# curl http://localhost:5000/os/hardware
#
# ###################################

@app.route('/os/<string:param>',methods=['GET'])
def osp(param):
        key = param
        value = ""
        if (param == "kernel"):
                value = subprocess.check_output(['uname','-s'])
        elif (param == "release"):
                value = subprocess.check_output(['uname','-r'])
        elif (param == "nodename"):
                value = subprocess.check_output(['uname','-n'])
        elif (param == "kernelversion"):
                value = subprocess.check_output(['uname','-v'])
        elif (param == "machine"):
                value = subprocess.check_output(['uname','-m'])
        elif (param == "processor"):
                value = subprocess.check_output(['uname','-p'])
        elif (param == "operatingsystem"):
                value = subprocess.check_output(['uname','-o'])
        elif (param == "hardware"):
                value = subprocess.check_output(['uname','-i'])
        else:
                return make_response(jsonify({'error': 'Bad parameter. Valid parameters: \'kernel\', \'release\' \'nodename\' \'kernelversion\' \'machine\' \'processor\' \'operatingsystem\' \'hardware\''}), 404)
 
        return jsonify({key: value})
 
# ###################################
#
# Metodo usado para determinar el uso de memoria. 
#
# Posibles metodos de acceso
#
# curl http://localhost:5000/mem/swpd
# curl http://localhost:5000/mem/free
# curl http://localhost:5000/mem/buff
# curl http://localhost:5000/mem/cache
#
# ###################################

@app.route('/mem/<string:param>', methods = ['GET'])
def mem(param):
        vmstat = subprocess.Popen(['vmstat'], stdout = subprocess.PIPE)
        tail = subprocess.Popen(['tail','-n','+3'], stdin = vmstat.stdout, stdout = subprocess.PIPE)
        tr = subprocess.Popen(['tr', '-s', ' '], stdin = tail.stdout, stdout = subprocess.PIPE)
        
        choices = {'swpd': 4, 'free': 5,  'buff':6 ,  'cache':7}
        value = choices.get(param, 'default')
        if value=='default':
            return make_response(jsonify({'error': 'Unknown param use -> swpd, free, buff, cache '}), 404)
        else:
            output = subprocess.check_output(['cut', '-d', ' ', '-f', str(value)], stdin = tr.stdout)
        return jsonify({'mem %s' % param: output})
 
 # ###################################
#
# Comandos varios
#
# Posibles metodos de acceso
#
# curl http://localhost:5000/misc/uptime
# curl http://localhost:5000/misc/battery
#
# ###################################

#acpi -V | grep Bat | tr -s ' ' | cut -d ':' -f 2

#tell how long the system has been running
@app.route('/misc/<string:param>',methods=['GET'])
def misc(param):
        key = param
        value = ""
        json=""
        if (param == "uptime"):
                value = subprocess.check_output(['uptime','-p'])
                json = jsonify({key: value})
        elif (param == "battery"):
                value1 =  subprocess.check_output(['acpi','-V'])
                acpi =  subprocess.Popen(['acpi', '-V'], stdout = subprocess.PIPE) 
                grep = subprocess.Popen(['grep','Bat'], stdin = acpi.stdout, stdout = subprocess.PIPE)
                awk = subprocess.Popen(['awk','{print substr($0,12,50)}'], stdin = grep.stdout, stdout = subprocess.PIPE)
                value1 = subprocess.check_output(['head','-n' , '1'], stdin = awk.stdout  ) 
                
                acpi =  subprocess.Popen(['acpi', '-V'], stdout = subprocess.PIPE) 
                grep = subprocess.Popen(['grep','Bat'], stdin = acpi.stdout, stdout = subprocess.PIPE)
                awk = subprocess.Popen(['awk','{print substr($0,12,50)}'], stdin = grep.stdout, stdout = subprocess.PIPE)
                value2 = subprocess.check_output(['tail','-n' , '1'], stdin = awk.stdout  )
               
                json = jsonify({'status': value1,  'capacity': value2})
        else:
                return make_response(jsonify({'error': 'Bad parameter. Valid parameters: \'uptime\' '}), 404)
        return json

#Find files by name
#curl -i -H "Content-Type: application/json" -X POST -d '{"name":"Docker"}' http://localhost:5000/misc/locate       
@app.route('/misc/locate', methods = ['POST'])
def locate():
        param= request.json['name']
        if not request.json or not 'name' in request.json:
            return make_response(jsonify({'error': 'You must set a name parammeter '}), 404)
        else:
            try:
                output= subprocess.check_output(['locate', str(param)])
                list = output.split('\n')
            except Exception:
                list="Not found"
        return jsonify({'results': list }) , 201      
#
# Este es el punto donde arranca la ejecucion del programa
#
if __name__ == '__main__':
        app.run(debug = True, host='0.0.0.0')

