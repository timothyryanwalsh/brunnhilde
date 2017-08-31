# encoding: utf-8

from __future__ import (print_function, unicode_literals)

import datetime
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from os.path import join as j


logging.basicConfig(filename='test.log', level=logging.DEBUG)
stderr = logging.StreamHandler()
stderr.setLevel(logging.WARNING)
logging.getLogger().addHandler(stderr)

def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0


class SelfCleaningTestCase(unittest.TestCase):
    """TestCase subclass which cleans up self.tmpdir after each test"""

    def setUp(self):
        super(SelfCleaningTestCase, self).setUp()

        # tempdir for brunnhilde outputs
        self.dest_tmpdir = tempfile.mkdtemp()
        if not os.path.isdir(self.dest_tmpdir):
            os.mkdirs(self.dest_tmpdir)

    def tearDown(self):
        if os.path.isdir(self.dest_tmpdir):
            shutil.rmtree(self.dest_tmpdir)

        super(SelfCleaningTestCase, self).tearDown()


class TestBrunnhildeIntegration(SelfCleaningTestCase):
    """
    Integration tests. sf (Siegfried) must be installed on user's system for tests to work.
    """

    def test_integration_outputs_created(self):
        subprocess.call('python brunnhilde.py -n ./test-data/files/ "%s" test' % (self.dest_tmpdir), 
            shell=True)
        # siegfried csv and sqlite db
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'siegfried.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'siegfried.sqlite')))
        # html report
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'test.html')))
        # csv reports
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'duplicates.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'errors.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'formats.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'formatVersions.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'mimetypes.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'unidentified.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'warnings.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'years.csv')))
        # tree.txt
        if not sys.platform.startswith('win'):
            self.assertTrue(os.path.isfile(j(self.dest_tmpdir, 'test', 
                'tree.txt')))

    def test_integration_outputs_created_diskimage(self):
        subprocess.call('python brunnhilde.py -nd ./test-data/diskimages/sample-floppy-fat.dd "%s" test' % (self.dest_tmpdir), 
            shell=True)
        # siegfried csv and sqlite db
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'siegfried.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'siegfried.sqlite')))
        # html report
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'test.html')))
        # csv reports
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'duplicates.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'errors.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'formats.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'formatVersions.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'mimetypes.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'unidentified.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'warnings.csv')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'years.csv')))
        # tree.txt
        if not sys.platform.startswith('win'):
            self.assertTrue(os.path.isfile(j(self.dest_tmpdir, 'test', 
                'tree.txt')))
        # dfxml
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'dfxml.xml')))
        # carved_files
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'carved_files', 'file1.txt.txt')))
        self.assertTrue(is_non_zero_file(j(self.dest_tmpdir, 'test', 
            'carved_files', 'Tulips.jpg')))
    
    def test_integration_temp_files_deleted(self):
        subprocess.call('python brunnhilde.py -n ./test-data/files/ "%s" test' % (self.dest_tmpdir), 
            shell=True)
        # temp.html
        self.assertFalse(os.path.isfile(j(self.dest_tmpdir, 'test', 
            'temp.html')))
        # uniqueyears.csv
        self.assertFalse(os.path.isfile(j(self.dest_tmpdir, 'test', 
            'csv_reports', 'uniqueyears.csv')))

    def test_integration_clamav(self):
        subprocess.call('python brunnhilde.py ./test-data/files/ "%s" test' % (self.dest_tmpdir), 
            shell=True)
        # virus log correctly written
        virus_log = j(self.dest_tmpdir, 'test', 'logs', 'viruscheck-log.txt')
        with open(virus_log, 'r') as f:
            self.assertTrue("Scanned files: 4" in f.read())
        with open(virus_log, 'r') as f:
            self.assertTrue("Infected files: 0" in f.read())

    def test_integration_clamav_diskimage(self):
        subprocess.call('python brunnhilde.py -d ./test-data/diskimages/sample-floppy-fat.dd "%s" test' % (self.dest_tmpdir), 
            shell=True)
        # virus log correctly written
        virus_log = j(self.dest_tmpdir, 'test', 'logs', 'viruscheck-log.txt')
        with open(virus_log, 'r') as f:
            self.assertTrue("Scanned files: 2" in f.read())
        with open(virus_log, 'r') as f:
            self.assertTrue("Infected files: 0" in f.read())


if __name__ == '__main__':
    unittest.main()
