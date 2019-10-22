import unittest
from lex_navigator_lambda_validator import *


class test_lex_routines(unittest.TestCase):

    def testHIDvalid_full_honeywell(self):
        self.assertEqual(isvalid_hid_honeywell("H306101"), True, "Not starting with H or E")
        self.assertEqual(isvalid_hid_honeywell("E306101"), True, "Not starting with H or E")
        self.assertEqual(isvalid_hid_honeywell("S306101"), False)
        self.assertEqual(isvalid_hid_honeywell("H30610"), False)
        self.assertEqual(isvalid_hid_honeywell("H3061000"), False)
        self.assertEqual(isvalid_hid_honeywell("H30AB01"), False)

    def test_hid_short(self):
        self.assertEqual(isvalid_hid_num("H306101"), False, "Not valid")
        self.assertEqual(isvalid_hid_num("E306101"), False, "Not valid")
        self.assertEqual(isvalid_hid_num("C306101"), False, "Not valid")
        self.assertEqual(isvalid_hid_num("306101"), True)
        self.assertEqual(isvalid_hid_num("000000"), True)
        self.assertEqual(isvalid_hid_num("954632"), True)
        self.assertEqual(isvalid_hid_num("30610"), False)
        self.assertEqual(isvalid_hid_num("30610245"), False)

    def test_contact_detail(self):
       self.assertEqual(get_employee_detail("Pollard")['Surname'], "Pollard", "Not valid")
       self.assertEqual(get_employee_detail("Pollard")['Name'], "Aidan", "Not valid")
       self.assertEqual(get_employee_detail("Pollard")['Phone'], "(01) 4297 6430", "Not valid")
       self.assertEqual(get_employee_detail("Pollard")['Email'], "dictum.eleifend.nunc@et.co.uk", "Not valid")
       self.assertEqual(get_employee_detail("John")['Surname'], "Stuart", "Not valid")


if __name__ == '__main__':
    unittest.main()
