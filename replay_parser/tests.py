from replay_parser import ReplayParser

import os
import struct
import unittest


class TestReplayParser(unittest.TestCase):

    folder_path = '{}/example_replays/'.format(
        os.path.dirname(os.path.realpath(__file__))
    )

    def test_104_replay(self):
        """
        A replay from version 1.04.
        """

        parser = ReplayParser()

        with open(self.folder_path + '1.04.replay', 'rb') as f:
            response = parser.parse(f)
            self.assertIsInstance(response, dict)
            self.assertEqual(response['header']['Id'], '0AB18BAB4CCE97201B7753A84B358D48')

    def test_105_replay(self):
        """
        A replay from version 1.05.
        """

        parser = ReplayParser()

        with open(self.folder_path + '1.05.replay', 'rb') as f:
            response = parser.parse(f)
            self.assertIsInstance(response, dict)
            self.assertEqual(response['header']['Id'], '56E7708C45ED1CF3B9E51EBF1ADF4431')

    def test_broken_replay(self):
        """
        This replay file was purposefully broken by deleting a large portion
        of the data.
        """

        parser = ReplayParser()

        with open(self.folder_path + 'broken.replay', 'rb') as f:
            with self.assertRaises(struct.error):
                parser.parse(f)

    def test_keyframes_missing_replay(self):
        """
        For some reason, this replay is missing the key frames from when goals
        were scored, so that data is not available to a parser. This is a good
        test to ensure the parser can handle odd scenarios.
        """

        parser = ReplayParser()

        with open(self.folder_path + 'keyframes_missing.replay', 'rb') as f:
            response = parser.parse(f)
            self.assertIsInstance(response, dict)
            self.assertEqual(response['header']['Id'], '50D5031342FF90D9F25BE5A0152E56B8')

    def test_keyframes_2s_replay(self):
        """
        For some reason, this replay is missing the key frames from when goals
        were scored, so that data is not available to a parser. This is a good
        test to ensure the parser can handle odd scenarios.
        """

        parser = ReplayParser()

        with open(self.folder_path + '2s.replay', 'rb') as f:
            response = parser.parse(f)
            self.assertIsInstance(response, dict)
            self.assertEqual(response['header']['Id'], '016D2CB946676AFDC11D29BFD84C9CB3')

    def test_file_attr(self):
        class Obj:
            class File:
                path = self.folder_path + '2s.replay'

            file = File()

        parser = ReplayParser()

        response = parser.parse(Obj())
        self.assertIsInstance(response, dict)
        self.assertEqual(response['header']['Id'], '016D2CB946676AFDC11D29BFD84C9CB3')

    def test_file_exception(self):
        parser = ReplayParser()

        with self.assertRaises(TypeError):
            parser.parse(None)
