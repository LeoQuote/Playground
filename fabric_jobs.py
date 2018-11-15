from fabric import Connection, Config

logstash_start_script = "sudo -u work -i /home/work/logstash/bin/logstash -f /home/work/logstash/conf/logstash.conf >> /home/work/logstash/nohup.out &"
es_start_script = "sudo -u work -i /home/work/python-build/bin/python /home/work/python-build/bin/supervisord -c /home/work/elasticsearch/es_supervisor.conf"
kibana_start_script = "sudo -u work -i /home/work/python-build/bin/python /home/work/python-build/bin/supervisord -c /home/work/kibana/kibana_supervisor2.ini"
nginx_start_script = "cd /home/work/ufe/nginx/ && sudo -u work -i sbin/nginx && cd -"

logstash_hosts = [
    '10.20.64.14',
    '10.20.64.15',
    '10.20.64.18',
    '10.20.64.19',
    '10.20.64.20',
    '10.20.64.21'
    ]

es_hosts = [
    '10.20.64.51',
    '10.20.64.52',
    '10.20.64.53'
]

kibana_hosts = [
    '10.20.64.13'
    ]

KEY_FILE = r"root.key"

def append_logstash_upstart(c):
    # echo file to /etc/rc.local
    c.run("echo \"{}\" >> /etc/rc.local ".format(logstash_start_script))
    
def append_kibana_upstart(c):
    c.run("echo \"{}\" >> /etc/rc.local ".format(kibana_start_script))

def append_nginx_upstart(c):
    c.run("echo \"{}\" >> /etc/rc.local ".format(nginx_start_script))

def append_es_upstart(c):
    c.run("echo \"{}\" >> /etc/rc.local ".format(es_start_script))

for m in logstash_hosts:
    with Connection(m, user='root',connect_kwargs={'key_filename':KEY_FILE}) as conn:
        # append_logstash_upstart(conn)
        pass

for m in kibana_hosts:
    with Connection(m, user='root', connect_kwargs={'key_filename':KEY_FILE}) as conn:
        append_kibana_upstart(conn)
        append_nginx_upstart(conn)

for m in es_hosts:
    with Connection(m, user='root', connect_kwargs={'key_filename':KEY_FILE}) as conn:
        append_es_upstart(conn)
