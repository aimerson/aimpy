#! /usr/bin/env python

import numpy as np
import unittest
from aimpy.utils.significant_figures import SigFig



class TestSigFig(unittest.TestCase):


    def test_fman(self):        
        self.assertAlmostEqual(SigFig.fman(1.03232e6),1.03232)
        self.assertAlmostEqual(SigFig.fman(11.03232e6),1.103232)
        self.assertAlmostEqual(SigFig.fman(-1.03232),-1.03232)
        return

    def test_fexp(self):
        self.assertAlmostEqual(SigFig.fexp(1.03232e6),6)
        self.assertAlmostEqual(SigFig.fexp(-5e10),10)
        self.assertAlmostEqual(SigFig.fexp(-4.0),0)
        self.assertAlmostEqual(SigFig.fexp(-4.0e-6),-6)
        self.assertAlmostEqual(SigFig.fexp(-0.4),-1)
        return

    def test_frexp10(self):
        m,e = SigFig.frexp10(1.03232e6)
        self.assertAlmostEqual(m,1.03232)
        self.assertEqual(e,6)
        m,e = SigFig.frexp10(10.03232e6)
        self.assertAlmostEqual(m,1.003232)
        self.assertEqual(e,7)
        m,e = SigFig.frexp10(-1.03232e-56)
        self.assertAlmostEqual(m,-1.03232)
        self.assertEqual(e,-56)
        m,e = SigFig.frexp10(444.03232e-56)
        self.assertAlmostEqual(m,4.4403232)
        self.assertEqual(e,-54)
        return
    
    def test_count_digits(self):
        self.assertEqual(SigFig.count_digits("10.454e50"),5)
        self.assertEqual(SigFig.count_digits("10.454e3"),5)
        self.assertEqual(SigFig.count_digits("-10.454e3"),5)
        self.assertEqual(SigFig.count_digits("aa"),0)
        with self.assertRaises(TypeError):
            SigFig.count_digits(1.0e344)
            SigFig.count_digits(1)
        return

    def test_locate_nsf(self):
        self.assertEqual(SigFig.locate_nsf(10,3),3)
        self.assertEqual(SigFig.locate_nsf(0.102,4),5)
        self.assertEqual(SigFig.locate_nsf(343.4343,3),2)
        self.assertEqual(SigFig.locate_nsf(-343.4343,3),3)
        self.assertEqual(SigFig.locate_nsf(343.4343,1),0)
        self.assertEqual(SigFig.locate_nsf(343.4343,4),4)                
        self.assertEqual(SigFig.locate_nsf(343.45e4,3),2)
        return

    def test_tidyup(self):
        x = "343.4343"
        loc = SigFig.locate_nsf(x,4)
        self.assertEqual(SigFig.tidyup(list(x),loc),list("343.4"))
        x = "343.4343"
        loc = SigFig.locate_nsf(x,2)
        self.assertEqual(SigFig.tidyup(list(x),loc),list("343"))
        x = "-343.4343"
        loc = SigFig.locate_nsf(x,4)
        self.assertEqual(SigFig.tidyup(list(x),loc),list("-343.4"))        

        return


    def test_round_up_9s(self):
        x = "9999.9999"
        nsf = 4
        loc0 = SigFig.locate_nsf(x,nsf)
        result,loc = SigFig.round_up_9s(list(x),loc0)
        self.assertEqual(result,list("10000.9999"))
        self.assertEqual(loc,loc0)
        x = "-343.99943"
        nsf = 3
        loc0 = SigFig.locate_nsf(x,nsf)
        result,loc = SigFig.round_up_9s(list(x),loc0)
        self.assertEqual(result,list(x))
        self.assertEqual(loc,loc0)
        x = "-343.99943"
        nsf = 5
        loc0 = SigFig.locate_nsf(x,nsf)
        result,loc = SigFig.round_up_9s(list(x),loc0)
        self.assertEqual(result,list("-344.00943"))
        self.assertEqual(loc,loc0)
        x = "-39.99943"
        nsf = 3
        loc0 = SigFig.locate_nsf(x,nsf)
        result,loc = SigFig.round_up_9s(list(x),loc0)
        self.assertEqual(result,list("-40.09943"))
        self.assertEqual(loc,loc0)
        x = "999.99943"
        nsf = 3
        loc0 = SigFig.locate_nsf(x,nsf)
        result,loc = SigFig.round_up_9s(list(x),loc0)
        self.assertEqual(result,list("1000.99943"))
        self.assertEqual(loc,loc0)
        x = "-999.99943"
        nsf = 3
        loc0 = SigFig.locate_nsf(x,nsf)
        result,loc = SigFig.round_up_9s(list(x),loc0)
        self.assertEqual(result,list("-1000.99943"))
        self.assertEqual(loc,loc0)
        x = "-2999.99943"
        nsf = 4
        loc0 = SigFig.locate_nsf(x,nsf)
        result,loc = SigFig.round_up_9s(list(x),loc0)
        self.assertEqual(result,list("-3000.99943"))
        self.assertEqual(loc,loc0)
        x = "999.9932"
        nsf = 4
        loc = SigFig.locate_nsf(x,nsf)
        result,loc = SigFig.round_up_9s(list(x),loc0)
        self.assertEqual(result,list("1000.0932"))
        self.assertEqual(loc,loc0-1)
        x = "999.9932"
        nsf = 5
        loc0 = SigFig.locate_nsf(x,nsf)
        result,loc = SigFig.round_up_9s(list(x),loc0)
        self.assertEqual(result,list("1000.0032"))
        self.assertEqual(loc,loc0)
        return

    def test_count_sf(self):
        self.assertEqual(SigFig.count_sf(10.0),3)
        self.assertEqual(SigFig.count_sf(10.0e57),3)
        self.assertEqual(SigFig.count_sf(10003.0),6)
        self.assertEqual(SigFig.count_sf(-10003.0),6)
        self.assertEqual(SigFig.count_sf(0.00012),2)
        self.assertEqual(SigFig.count_sf(-0.00012),2)
        self.assertEqual(SigFig.count_sf(1343),4)
        return


    def test_modify_number(self):
        x = "10.02"
        nsf = 4
        self.assertEqual(SigFig.modify_number(x,nsf),"10.02")
        x = "-10.02"
        nsf = 4
        self.assertEqual(SigFig.modify_number(x,nsf),"-10.02")
        x = "10"
        nsf = 4
        self.assertEqual(SigFig.modify_number(x,nsf),"10.00")
        x = "-10"
        nsf = 4
        self.assertEqual(SigFig.modify_number(x,nsf),"-10.00")
        x = "0.00102"
        nsf = 4
        self.assertEqual(SigFig.modify_number(x,nsf),"0.001020")
        x = "-0.00102"
        nsf = 4
        self.assertEqual(SigFig.modify_number(x,nsf),"-0.001020")
        x = "343.4343"
        nsf = 4
        self.assertEqual(SigFig.modify_number(x,nsf),"343.4")
        x = "-343.4343"
        nsf = 4
        self.assertEqual(SigFig.modify_number(x,nsf),"-343.4")
        x = "343.99943"
        nsf = 5
        self.assertEqual(SigFig.modify_number(x,nsf),"344.00")
        x = "-343.99943"
        nsf = 5
        self.assertEqual(SigFig.modify_number(x,nsf),"-344.00")
        x = "999.9932"
        nsf = 4
        self.assertEqual(SigFig.modify_number(x,nsf),"1000")
        x = "999.9992"
        nsf = 5
        self.assertEqual(SigFig.modify_number(x,nsf),"1000.0")
        x = "1.000000"
        nsf = 4
        self.assertEqual(SigFig.modify_number(x,nsf),"1.000")
        x = "0.10024454"
        nsf = 4
        self.assertEqual(SigFig.modify_number(x,nsf),"0.1002")
        x = "0.10024454"
        nsf = 3
        self.assertEqual(SigFig.modify_number(x,nsf),"0.100")
        x = "0.10029454"
        nsf = 4
        self.assertEqual(SigFig.modify_number(x,nsf),"0.1003")
        x = "-0.10029454"
        nsf = 4
        self.assertEqual(SigFig.modify_number(x,nsf),"-0.1003")
        return

    def round(self):
        x = "9999.9999e-99"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"10000e-99")
        x = "10.02"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"10.02")
        x = "-10.02"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"-10.02")
        x = "10"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"10.00")
        x = "-10"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"-10.00")
        x = "0.00102"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"0.001020")
        x = "-0.00102"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"-0.001020")
        x = "343.4343"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"343.4")
        x = "-343.4343"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"-343.4")
        x = "343.99943"
        nsf = 5
        self.assertEqual(SigFig.round(x,nsf),"344.00")
        x = "-343.99943"
        nsf = 5
        self.assertEqual(SigFig.round(x,nsf),"-344.00")
        x = "999.9932"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"1000")
        x = "999.9992"
        nsf = 5
        self.assertEqual(SigFig.round(x,nsf),"1000.0")
        x = "1.000000"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"1.000")
        x = "0.10024454"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"0.1002")
        x = "0.10024454"
        nsf = 3
        self.assertEqual(SigFig.round(x,nsf),"0.100")
        x = "0.10029454"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"0.1003")
        x = "-0.10029454"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"-0.1003")
        x = "-0.10029454e5"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"-0.1003e5")
        x = "-0.10029454e3"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"-0.1003e3")
        x = "1002.9454e-32"
        nsf = 4
        self.assertEqual(SigFig.round(x,nsf),"1003e-32")
        return


    def test_force_float(self):        
        self.assertEqual(SigFig.force_float(-1.023e3),"-1023.0")
        self.assertEqual(SigFig.force_float(-1.023e16),"-1023000000000000")
        self.assertEqual(SigFig.force_float(1.023e16),"1023000000000000")
        self.assertEqual(SigFig.force_float(1.023e-5),"0.00001023")
        self.assertEqual(SigFig.force_float(1.023e-2),"0.01023")
        self.assertEqual(SigFig.force_float(-1.023e-5),"-0.00001023")
        self.assertEqual(SigFig.force_float(-1.023e-2),"-0.01023")
        return


    def test_latex(self):
        self.assertEqual(SigFig.latex("1000.0"),"1000.0")
        self.assertEqual(SigFig.latex("-1000.0"),"-1000.0")
        self.assertEqual(SigFig.latex("-0.001"),"-0.001")
        self.assertEqual(SigFig.latex("-0.001e-10"),"-0.001\,\\times\,10^{-10}")
        self.assertEqual(SigFig.latex("1.034e23"),"1.034\,\\times\,10^{23}")        
        return




if __name__ == "__main__":
    unittest.main()


              
