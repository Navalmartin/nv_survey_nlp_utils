import unittest
from src.utils.survey_item_type_enum import get_survey_item_strings_human_read, SURVEY_ITEM_TYPE_STRS


class TestMiscellenaous(unittest.TestCase):

    def test_get_survey_item_strings_human_read(self):

        items = get_survey_item_strings_human_read()
        self.assertEqual(len(SURVEY_ITEM_TYPE_STRS), len(items))
        expected = ['cathodic protection', 'deck superstructure cockpit',
                    'domestic equipment', 'deck equipment',
                    'safety equipment', 'hull shell',
                    'keels ballast', 'internal structure members', 'through hull fittings',
                    'steering', 'rig and sails', 'propulsion machinery',
                    'electrical and electronics', 'bilge pumps', 'safety equipment', 'interior exterior outfit']
        self.assertEqual(expected, items)


if __name__ == '__main__':
    unittest.main()
