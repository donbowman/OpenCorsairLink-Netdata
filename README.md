# CorsairLink and Netdata

This is an integration between [OpenCorsairLink](https://github.com/audiohacked/OpenCorsairLink)
and [Netdata](https://github.com/firehol/netdata).

To install:

1. cp 50-corsair.rules /lib/udev/rules.d/50-corsair.rules
2. systemctl restart systemd-udevd.service
3. udevadm trigger
4. cp opencorsairlink.chart.py /usr/libexec/netdata/python.d
5. systemctl restart netdata

See [my blog](https://blog.donbowman.ca/2017/11/26/the-new-corsair-supply-and-netdata/) for more.
