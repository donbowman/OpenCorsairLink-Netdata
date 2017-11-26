# -*- coding: utf-8 -*-
# Description: OpenCorsairLink netdata python module
# Author: Don Bowman (db@donbowman.ca)

#from bases.FrameworkServices.ExecutableService import ExecutableService
from base import ExecutableService

# default module values (can be overridden per job in `config`)
update_every = 5
priority = 60000
retries = 5

# charts order (can be overridden if you want less charts, or different order)
ORDER = ['temp', 'input_voltage', 'output_wattage',
 'out_v', 'out_a', 'out_w',
]

CHARTS = {
    # id: {
    #     'options': [name, title, units, family, context, charttype],
    #     'lines': [
    #         [unique_dimension_name, name, algorithm, multiplier, divisor]
    #     ]}
    'temp': {
        'options': [None, "PSU Temp0", "C", 'psu', 'psu.temp0', 'line'],
        'lines': [
            ['temp0',   'temp0', 'absolute', 1, 100],
            ['temp1',   'temp1', 'absolute', 1, 100]
        ]},
    'input_voltage': {
        'options': [None, "PSU Input Voltage", "V", 'psu', 'psu.input_voltage', 'line'],
        'lines': [
            ['input_voltage',   'input_voltage', 'absolute', 1, 100]
        ]},
    'output_wattage': {
        'options': [None, "PSU Output Wattage", "V", 'psu', 'psu.output_wattage', 'line'],
        'lines': [
            ['output_wattage',   'output_wattage', 'absolute', 1, 100]
        ]},
    'out_v': {
        'options': [None, "PSU Voltage", "V", 'psu', 'psu.out_v', 'line'],
        'lines': [
            ['out_12v_v',   'out_12v_v', 'absolute', 1, 100],
            ['out_5v_v',   'out_5v_v', 'absolute', 1, 100],
            ['out_3v_v',   'out_3v_v', 'absolute', 1, 100]
        ]},
    'out_a': {
        'options': [None, "PSU Amperage", "A", 'psu', 'psu.out_a', 'line'],
        'lines': [
            ['out_12v_a',   'out_12v_a', 'absolute', 1, 100],
            ['out_5v_a',   'out_5v_a', 'absolute', 1, 100],
            ['out_3v_a',   'out_3v_a', 'absolute', 1, 100]
        ]},
    'out_w': {
        'options': [None, "PSU Wattage", "W", 'psu', 'psu.out_w', 'line'],
        'lines': [
            ['out_12v_w',   'out_12v_w', 'absolute', 1, 100],
            ['out_5v_w',   'out_5v_w', 'absolute', 1, 100],
            ['out_3v_w',   'out_3v_w', 'absolute', 1, 100]
        ]},
}

class Service(ExecutableService):
    def __init__(self, configuration=None, name=None):
        ExecutableService.__init__(self, configuration=configuration, name=name)
        self.command = "OpenCorsairLink.elf --device 0"
        self.order = ORDER
        self.definitions = CHARTS

    def _get_data(self):
        """
        Format data received from shell command
        :return: dict
        """
        raw_data = self._get_raw_data()
        self.debug('raw_data: <<%s>>' % raw_data)
        if not raw_data:
            return None

        ckeys = {}
        ckeys['Temperature 0'] = 'temp0'
        ckeys['Temperature 1'] = 'temp1'
        ckeys['Supply Voltage'] = 'input_voltage'
        ckeys['Total Watts'] = 'output_wattage'
        ckeys['Output 12v'] = '12v'
        ckeys['Output 5v'] = '5v'
        ckeys['Output 3.3v'] = '3v'

        data = {}
        lm = ''
        raw_data = ''.join(raw_data)
        self.debug('==================================')
        for l in raw_data.split('\n'):
            l = ''.join(l.strip())
            self.debug('l: <<%s>>' % l)
            fields = l.split(':')
            if len(fields) > 1:
                keyn = ''.join(fields[0]).strip()
                keyv = ''.join(fields[1]).strip()
                if keyn in ckeys:
                    x = ckeys.get(keyn,"None")
                    if len(keyv):
                        keyv = keyv.split(' ')[0]
                        data[x] = int ( float(keyv) * 100)
                    lm = x
            elif len(lm) > 0:
                fields = l.split(' ')
                if (fields[0] == 'Voltage'):
                    data['out_%s_v' % lm] = int( float(fields[-1]) * 100)
                elif (fields[0] == 'Amps'):
                    data['out_%s_a' % lm] = int( float(fields[-1]) * 100)
                elif (fields[0] == 'Watts'):
                    data['out_%s_w' % lm] = int( float(fields[-1]) * 100)

        self.debug('data: <<%s>>' % data)
        return data

#    def check(self):
#        return True
