import copy
import unittest
import atlas

class EvidenceTests(unittest.TestCase):
    def setUp(self): self.s,self.c,self.i=copy.deepcopy(atlas.load())
    def test_valid_graph(self): self.assertTrue(atlas.validate(self.s,self.c,self.i))
    def test_unknown_source(self):
        self.c[0]['source']='invented'
        with self.assertRaisesRegex(ValueError,'Unknown source'): atlas.validate(self.s,self.c,self.i)
    def test_missing_locator(self):
        self.c[0]['locator']=' '
        with self.assertRaisesRegex(ValueError,'locator'): atlas.validate(self.s,self.c,self.i)
    def test_duplicate_id(self):
        self.c.append(self.c[0])
        with self.assertRaisesRegex(ValueError,'Duplicate'): atlas.validate(self.s,self.c,self.i)
    def test_inference_label(self):
        self.i[0]['kind']='fact'
        with self.assertRaisesRegex(ValueError,'labelled'): atlas.validate(self.s,self.c,self.i)
    def test_broken_evidence(self):
        self.i[0]['evidence']=['missing']
        with self.assertRaisesRegex(ValueError,'Broken'): atlas.validate(self.s,self.c,self.i)
    def test_no_invented_review(self):
        self.c[0]['review']='reviewed'
        with self.assertRaisesRegex(ValueError,'Reviewer'): atlas.validate(self.s,self.c,self.i)
    def test_unknown_dimension(self):
        self.c[0]['dimension']='automatic_compliance'
        with self.assertRaisesRegex(ValueError,'dimension'): atlas.validate(self.s,self.c,self.i)

if __name__=='__main__': unittest.main()
