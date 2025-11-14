import os, sys, importlib


dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
print("Set path to: "+parent_dir_path)

import unittest
import BaseAccess as Ba
import Helper as He


Ba.setDBName("dbiu.bayern")


class NormalizeQuery_test(unittest.TestCase):

    maxDiff = None


    def readFile(self,path: str):

        with open(path, 'r') as file:
            return file.read()

    def helperEqual(self, nr: str):
        He.setup("sql_testing_tools/tests/v1/a"+nr+".sql", "sql_testing_tools/tests/v2/a"+nr+".sql")
        print("\n\nTest "+nr+"------------------------------")
        print("V1: "+He.sql)
        print("V2: "+He.sol)
        print("-------------------------------------\n\n")
        if He.sol != He.sql:
            self.fail("\n" + He.sol + "\n" + He.sql)

        col = He.checkColumns()
        tab = He.checkTables()
        grp = He.checkGroup()
        ord = He.checkOrder()

        if(col != "" or tab != "" or grp != "" or ord != ""):
            self.fail("\n" + col + "\n" + tab + "\n" + grp + "\n" + ord)
            
    def helperUnequal(self, nr:str):
        td = Ba.getTableDict()
        q1 = He.normalizeSQLQuery(self.readFile("sql_testing_tools/tests/v1/a"+nr+".sql"), td)
        q2 = He.normalizeSQLQuery(self.readFile("sql_testing_tools/tests/v2/a"+nr+".sql"), td)
        print("\n\nTest "+nr+"------------------------------")
        print("V1: "+He.sql)
        print("V2: "+He.sol)
        print("-------------------------------------\n\n")
        if q1 == q2:
            self.fail("\n" + q1 + "\n" + q1)
        

    def test_a01_oneCondition(self):
        nr = '01'
        self.helperEqual(nr)
    


    def test_a02_oneOR(self):
        nr = '02'
        self.helperEqual(nr)



    def test_a03_twoOR(self):
        nr = '03'
        self.helperEqual(nr)



    def test_a04_twoOR_withBrackets(self):
        nr = '04'
        self.helperEqual(nr)



    def test_a05_twoOR_withWithoutBrackets(self):
        nr = '05'
        self.helperEqual(nr)



    def test_a06_AND_inBrackets_OR_outside(self):
        nr = '06'
        self.helperEqual(nr)



    def test_a07_AND_inOutsideBrackets_OR_outside(self):
        nr = '07'
        self.helperEqual(nr)



    def test_a08_OR_inBrackets_AND_outside(self):
        nr = '08'
        self.helperEqual(nr)



    def test_a09_GROUP_CountSumAvg(self):
        nr = '09'
        self.helperEqual(nr)



    def test_a10_GROUP_twoCols(self):
        nr = '10'
        self.helperEqual(nr)
            


    def test_a11_BUG(self):
        nr = '11'
        self.helperEqual(nr)
            


    def test_a12_BUG(self):
        nr = '12'
        self.helperEqual(nr)
            


    def test_a13_BUG(self):
        nr = '13'
        self.helperEqual(nr)
            


    def test_a14_BUG(self):
        nr = '14'
        self.helperEqual(nr)



    def test_a15_ORDER_BY(self):
        nr = '15'
        self.helperEqual(nr)



    def test_a16_LIMIT(self):
        nr = '16'
        self.helperEqual(nr)



    def test_a17_LIKE(self):
        nr = '17'
        self.helperEqual(nr)



    def test_a18_Semicolon(self):
        nr='18'
        self.helperEqual(nr)
    
    

    def test_a19_OrderBy_withWithoutASC(self):
        nr='19'
        self.helperEqual(nr)
    
    

    def test_a20_OrderBy_ASCandDESC(self):
        nr='20'
        self.helperEqual(nr)
    
    

    def test_a21_OrderBy_AscDesc_Unequal(self):
        nr='21'
        self.helperUnequal(nr)

    def test_a22_GroupIsolated(self):
        nr='22'
        res = He.checkGroup("sql_testing_tools/tests/v1/a"+nr+".sql", "sql_testing_tools/tests/v2/a"+nr+".sql")

        if res == "":
            self.fail("Different grouping not recognized")

    def test_a23_not_equal(self):
        nr = '23'
        self.helperEqual(nr)

    def test_a24_not_equal(self):
        nr = '24'
        self.helperEqual(nr)

    def test_a25_anton(self):
        nr = '25'
        self.helperEqual(nr)

    def test_a26_anton2(self):
        nr = '26'
        self.helperEqual(nr)

    def test_a27_detailCheckWrongOrder(self):
        nr = '27'
        He.setup("sql_testing_tools/tests/v1/a"+nr+".sql", "sql_testing_tools/tests/v2/a"+nr+".sql")

        col = He.checkColumns()
        tab = He.checkTables()
        grp = He.checkGroup()
        ord = He.checkOrder()

        msg = "\n\n"

        if(col==""):
            msg += "Spalten werden als richtig angezeigt, obwohl falsch\n"

        if(tab != "" or grp != "" or ord != ""):
            msg += tab + "\n" + grp + "\n" + ord

        if msg != "\n\n":
            self.fail(msg)
            

    def test_a28_kreuzproduktA1(self):
        nr = '28'
        self.helperEqual(nr)
        
        
    def test_a29_kreuzproduktA5(self):
        
        nr = '27'
        He.setup("sql_testing_tools/tests/v1/a"+nr+".sql", "sql_testing_tools/tests/v2/a"+nr+".sql")

        col = He.checkColumns()
        tab = He.checkTables()
        cond = He.checkCondition()
        grp = He.checkGroup()
        ord = He.checkOrder()

        msg = "\n\n"

        if(cond==""):
            msg += "Bedingungen werden als korrekt angezeigt, obwohl falsch\n"
            

        if(col != "" or tab != "" or grp != "" or ord != ""):
            msg += tab + "\n" + grp + "\n" + ord

        if msg != "\n\n":
            self.fail(msg)