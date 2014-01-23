#!/usr/bin/env python
import urllib
import socket
import json

class DynamicIp:
    def __init__(self, record_id, token, email, name, zone):
        self.record_id = record_id
        self.token = token
        self.email = email
        self.name = name
        self.zone = zone

    def get_live_ip(self):
        try:
            return socket.gethostbyname(self.name + '.' + self.zone)
        except IOError:
            return None

    def get_current_ip(self):
        try:
            return urllib.urlopen('http://ipecho.net/plain').read()
        except:
            return None

    def update_record(self):
        cur_ip = self.get_current_ip()
        last_ip = self.get_live_ip()

        if cur_ip is None:
            return False

        if last_ip is None:
            return False

        if cur_ip != last_ip:
            data = urllib.urlencode({
                'a': 'rec_edit',
                'type': 'A',
                'service_mode': '0',
                'ttl': '1',
                'tkn': self.token,
                'id': self.record_id,
                'email': self.email,
                'z': self.zone,
                'name': self.name,
                'content': cur_ip
            })

            try:
                response = urllib.urlopen('https://www.cloudflare.com/api_json.html/?%s' % data)
                result = json.loads(response.read())
            except:
                return False

            if result['result'] == 'success':
                return True
            return False

        return True


if __name__ == '__main__':
    dns = DynamicIp(
        'rec_id',   # 8273429
        'token',    # 8afbe6dea02407989af4dd4c97bb6e25
        'mail',     # mail@example.com
        'name',     # sub
        'zone'      # example.com
    )

    dns.update_record()