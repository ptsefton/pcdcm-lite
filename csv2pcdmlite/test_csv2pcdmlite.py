"""
(c) University of Technology Sydney 2016

This file is part of pcdmlite.

    Pddmlite is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Netta is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Netta.  If not, see <http://www.gnu.org/licenses/>.

"""
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from builtins import open
from future import standard_library

import unittest
from csv2pcdmlite import Field, CSVData, item_from_row, relation_from_row


class TestLoading(unittest.TestCase):
        
  def test_basic_field_stuff(self):
      f = Field("dc:identifier")
      self.assertEqual(f.type, Field.TEXT)
     
      f = Field("dc:type")
      self.assertEqual(f.type, Field.ITEM_TYPE)

      f = Field("pcdm:Collection")
      self.assertEqual(f.type, Field.IN_COLLECTION)

      f = Field("FILE:+")
      self.assertEqual(f.type, Field.FILE)
      self.assertTrue(f.repeats)

  def test_row_loading(self):
      row = {'dc:title': 'People', 'dc:type': 'pcdm:Collection', 'dc:identifier': '123'}
      item = item_from_row(row)
      self.assertEqual(item.id, '123')
      self.assertTrue(item.is_collection)

      print(item.serialize_RDF())

  def test_CSV(self):
      csv = CSVData(open("sample-data/first-fleet-maps.csv"))
      csv.get_items()
      self.assertEqual(len(csv.items), 27)
      self.assertEqual(len(csv.collections), 2)

  def test_relations(self):
      row = {'subject': '12345', 'predicate': 'dc:type', 'object': '34352'}
      relation = relation_from_row(row)
      self.assertEqual(relation.predicate, "http://purl.org/dc/elements/1.1/type")

      row = {'subject': '12345', 'predicate': 'http://purl.org/dc/elements/1.1/type', 'object': '34352'}
      relation = relation_from_row(row)
      self.assertEqual(relation.predicate, "http://purl.org/dc/elements/1.1/type")
      
  def test_relations_CSV(self):
      csv = CSVData(open('sample-data/relations.csv'))
      csv.get_relations()
      self.assertEqual(len(csv.relations),2)
      
if __name__ == '__main__':
    unittest.main()
