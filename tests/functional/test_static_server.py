import unittest
import shutil
import tempfile
import os
from webob import Request
import pybald
from pybald import context
from pybald.util.static_serve import StaticServer

import logging
log = logging.getLogger(__name__)

# binary data for a tiny png file
binary_file_data = b'''\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00!\x00\x00\x00\x1a\x08\x03\x00\x00\x00\x0e\x87\xc53\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x01\xecPLTEGpL\xbc\xbc\xbb\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xe3\xe3\xe3\xff\xff\xff\x00\x00\x00]]]\x00\x00\x00\xc2\xc2\xc1\xfe\xff\xff\xfb\xfb\xfb\x96\x96\x96\xff\xff\xff\xba\xba\xba\xeb\xea\xeb\x14\x14\x14\xbe\xbe\xbe\x1d\x1d\x1d\xe0\xe0\xe0\xf8\xf8\xf8\xf8\xf8\xf7\xba\xc7\xae\xee\xee\xee\xf3\xf4\xf2\xd9\xd9\xd9\xc0\xc0\xc0\xae\xae\xae\xe1\xe1\xe1\xb9\xb9\xb7\xf1\xf1\xf1\xc9\xd3\xc0\xe7\xe7\xe7\xd3\xdb\xcd\xfe\xfe\xfe\xc4\xcf\xb9\xd2\xd2\xd2\xd7\xd7\xd7\xd3\xd3\xd3\xf4\xf4\xf4```\x85\x85\x85\xe2\xe2\xe2\xdb\xdb\xdb\xf6\xf6\xf6\xda\xda\xda\xeb\xeb\xeb\xf7\xf7\xf7\xf4\xf4\xf4\xef\xef\xef\xd7\xd7\xd7\xfe\xfe\xfe\xfa\xfa\xfaDDD\xed\xed\xec\x00\x00\x00\xec\xec\xec\x00\x00\x00\xec\xec\xec\xbf\xbf\xbf\xe1\xe7\xdc\xa5\xb8\x95\xe8\xed\xe5\xce\xce\xce\xec\xec\xec\xeb\xeb\xeb\xe9\xe9\xe9\xe7\xe7\xe7\xe4\xe4\xe4\xe3\xe3\xe3\xec\xe6\xe7\xf5\xf5\xf5\xdb\xdb\xdb\xe5\xda\xdb\xd6\xd6\xd6\xef\xee\xee\xd8\xd8\xd8\xac\xac\xac\xcd\xcd\xcd\xaa\xaa\xa4\xb4\xb4\xb4\xe2\xe2\xe2\xe5\xe7\xe7\xde\xde\xde\xcc\xcc\xcc\xec\xec\xec\xcb\xcb\xcb\xc0\xc0\xc0\xd6\xd6\xd6\xd7\xd7\xd7\x89\x8e\x8e\xd8\xd8\xd8\xa9\xa9\xa5\xe2\xe2\xe2\xc0\xc0\xc0\xdc\xdc\xdc\xe6\xe6\xe6\xf2\xf2\xf2hhh\x00\x00\x00\xf0\xf0\xf0\xb2\xb2\xb2\xb4\xb4\xb4\xae\xbe\xa1\x8b\xa5ru\x97S\xff\xff\xff\xfe\xfe\xfe\xef\xef\xf0\xf1\xf1\xf1\xfc\xfc\xfc\xed\xed\xed\xf5\xf5\xf5\xf2\xf3\xf3\xfd\xfe\xfd\xf4\xf4\xf4\xfa\xfa\xf9\xfa\xfb\xf9\xf8\xf8\xf8\xb1\xc1\xa3\xdf\xdf\xdfz\x9aZ\x98\xae\x85\xe9\xe9\xe9\xa9\xbb\x99\xd6\xde\xcf\xd9\xe0\xd3\xed\xf0\xe9\xf6\xf8\xf4\x83\x9fg\xce\xd8\xc6\xee\xef\xef\xef\xf2\xec\x92\xab|\xc1\xcd\xb6\xc6\xd1\xbc\xdc\xe3\xd6\xde\xe5\xd9\xe2\xe2\xe2\xe4\xe5\xe4\xbb\xc9\xb0\xe9\xee\xe5r\x96Lw\x98R\xa0\xb4\x8di\x90;\x8c\xa5u\x87\xa2m\xb6\xc5\xa8\xe2\xd1\xd3\xd6\xb6\xb9\xd7\xd7\xd7\xcd\xcd\xcdo\x94C\xb6\xc2\xac\x7f\x9dc\x8e\xa7ua\x8b*(s\x00\x92\xa9\x7fj\x8f?S_`q\x00\x00\x00\x8etRNS\x00\xba\xfb\xfc\xfd\x03\xfc\x02\xfe\x0e\'\x199\xfe\xfe\x01\xfa\xba\xe0\x10\xba\x04\x80\xf7\xfd\xfe\xeb\xfce4#y/\xe9\xfc\xfe\xfe\xfc\xfeTbY\xe2\x1b\x1a\xec\x07\xfbq\xc1\xef\xf0\xe1\xc2\xf8\xef\x1c\xfa\n\xdd\x08\xea\xc1\xfe\xfe\xfcI\xc9\xc9\xaf\xa0\xad\x93\xfa\xf6\xa1\xfb}\xd3\xe6(Q*\\\xf0\x95u}\xb3\x89\x8a{Z4\xb1G\xdf\xfe\x9b\xd8\xf8 \x15\xee\xa6\x99\xfc\xfc\xfc\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfe\xff\xfe\xcb\x14\xdbZ\x00\x00\x02VIDAT(\xcfu\x90\x07S"A\x10\x85[jY\xe6\x14\x84\x13I\x87Y\x8ce,\x15\xc3\x19/\xe7\x9cs\xce\xbd\x01\t.Q\xd2*`\x8e\x97\xe3\x1f\xbda\x17,\xbc+_\xd5\x84\xea\xfe\xe6Mw\x03\xec\x93N\x0bPW\x7f\xa7\xff\xae\x19\x8c\xfb3`\xd4*\x02\x18\xb9\xd7\xcdq>\xbc\r=\xc6\x7f\x9f*\xea\xbax\x191\xe0v\xe3}\x1a\xd4\x95\x00\x00\x96\x86cm\x1d\xedg:9QS\xc9{\x03\xdeG\x0f\xba\x94x\x11\x18\xaf9n\xf3a^\xce^\x94B\x9f\xbf,#6Z\xc7\x8b\x88\x0ejO(Y\xc2\xb0\xac\xb4,\x13z\xf3\xf72\x88\xa7-j\xb9Z\xa8kD\x8d\x89!\x84\x88\x12\xef\xf1\xf0Q\xa7f\xb4\xf9)ob\xb0\r\xb4*aEw\x0b\xad\xcf+{d\x7f%1\xb5\xc8\x18\x8dF\x9bE\x16\xeb\x15\x82\xfa\x9cD\x96COH\x08\xe4\x7f\xa2kv\xe8\xd90\xca\x02\xc1\x1a\xd5\xc3\x08\xa7\x90%(\t\x82,\x0b~\xe9\\\x7f_\x1d\xc0\xc3\x1b\x9f.\xa0]\xaf\x96\xaa\x85vd8D\xf4UJ~A\xe8>\xdfWSo\xbdi\xfbx\x16/\x8d\xa9\x84\x0e\xcc\x83\xe8F\x0e\xd5~\xb0 \x83\t\xad\x85n\xb5=\xd0\x81\xc8\x10N\x11\xcd1\x0c\xed\x9a\xd3\xe0\xc0\x15\xe8\xd9\x1b\xf6\xd5\xce\xbd\xd7\x9c\xc1` \x84#\x0c\xde*$-\rz\xbd\xfe\xda\xf5\xa1Q\xbf$\x8a>_\xf1\x13\x16\x9f<\xae\xd5\xd7\xea\x1b,\xf0\xea9\xda\xec\xf6\xe1\x01\'\x1fj\x96\xa9x\xaf$\x06$:\x9b\x174l\xe3\xaa^B\xc5`\xd1_\xa2\xf3\xe4\xa3+\xa1\x15z\xce\x06\nn\xaf\xcb\xa1\xe2(\xba\r\x0c\x93\xa78\x8c\x7fS\xe3s\xab\t$\xad\xf3\x8c\x1b\'(Q\x85-\xb80\x15_X[\x10\x13\x99\xef\xf1\xc4\\\xdc\x95L\xfe\\\x9as}]\xa5\x99#\x05"\xb8\xb1\x18\xd9\x0c\xce\xff\xc8\x86#\xe1\\&\xbc\xbd\xb6\xed\x8a,\xae\xb7\x96\x101Gr#\xbb\x18N\xbb"\x98\nfc\xe1\\$\x98\xf2M;J=~\xc7R\x81\xcd_\xc9\xf4\xd6\xeeN\xecOl=\xbe\x93I\x05\xb7\x8a\x04\xad\x94}\xf7!3\xc3N\xbfg\x13M\x8e){\xb6\xc9\xe5t9s\x8e\xa6\x19\xd6\x84\x8d\x94\x98@\xc4t\x9an\xbbK\xf8\x9f\xc8h9\x98\xdfN\x96U\x97\x1d\xce\xabZ9\xd5\xa5D\xaa\xcb&\xdf\x8c\x00\x8c\x9b\x0f\x1d,\xf3\x98\xf1/\xdd\xa1\xd3/;\\G\x8c\x00\x00\x00\x00IEND\xaeB`\x82'''

test_conf = dict(env_name="SampleTestProjectEnvironment",
                 debug=False)


class TestStaticServer(unittest.TestCase):
    def setUp(self):
        context._reset()
        self.test_dir = tempfile.mkdtemp()
        with open(os.path.join(self.test_dir, "pybald.png"), "wb") as image:
            image.write(binary_file_data)

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)
        context._reset()

    def test_serve_png_file(self):
        "Serve a file from a static asset path (temporary)"
        pybald.configure(config_object=test_conf)
        app = StaticServer(application=None, path=self.test_dir)

        resp = Request.blank('/pybald.png').get_response(app)
        self.assertEqual(resp.headers['Content-Type'], 'image/png')
        self.assertEqual(resp.headers['Content-Length'], '1342')
        print(type(resp.body))
        print(type(binary_file_data))
        self.assertEqual(resp.body, binary_file_data)



if __name__ == "__main__":
    unittest.main()
