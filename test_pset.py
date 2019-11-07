#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pset_4` package."""

from unittest import TestCase
from luigi import build
from pset_4.tasks.stylize import Stylize


class Dummy_Test(TestCase):
    def test_dummy(self):
        self.assertEqual(0, 0)


# class Luigi_Download_Tests(TestCase):
# TODO - not implementing this test because it would download files during every travis test
# def test_ContentImage(self):
#     x = build([
#         Stylize(
#             model='udnie.pth',
#             image='luigi.jpeg'
#         )], local_scheduler=True)
#     self.assertEqual(x, True)
