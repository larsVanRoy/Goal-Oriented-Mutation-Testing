import unittest

from yaml import load
from llvmAnalyser.analyser import LLVMAnalyser

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

config = load(open('config.yml').read(), Loader=Loader)


def get_focal_methods(llvm_path, depth):
    analyzer = LLVMAnalyser()
    analyzer.config["graph"] = False
    analyzer.config["max_depth"] = depth

    analyzer.get_relevant_functions(llvm_path)

    return analyzer.get_focal_methods()


class TestTool(unittest.TestCase):
    def test_stack(self):
        llvm_path = "exampleProjects/stack/llvm/linked.ll"

        focal_methods = get_focal_methods(llvm_path, 2)

        self.assertEqual(len(focal_methods), 1)
        self.assertEqual(len(focal_methods["@_ZN19StackTest_push_Test8TestBodyEv"]), 2)
        self.assertTrue("@_ZN5Stack4pushEi" in focal_methods["@_ZN19StackTest_push_Test8TestBodyEv"])

    def test_profile(self):
        llvm_path = "exampleProjects/profile/llvm/linked.ll"

        focal_methods = get_focal_methods(llvm_path, 5)

        self.assertEqual(len(focal_methods), 1)
        self.assertEqual(len(focal_methods["@_ZN31ProfileTester_setFirstName_Test8TestBodyEv"]), 1)
        self.assertTrue("@_ZN7Profile12getFirstNameB5cxx11Ev" in
                        focal_methods["@_ZN31ProfileTester_setFirstName_Test8TestBodyEv"])

    def test_dict(self):
        llvm_path = "exampleProjects/dict/llvm/linked.ll"

        focal_methods = get_focal_methods(llvm_path, 5)

        self.assertEqual(len(focal_methods), 1)
        self.assertEqual(len(focal_methods["@_ZN20DictTest_add_el_Test8TestBodyEv"]), 1)
        self.assertTrue("@_ZN4Dict6get_elEi" in focal_methods["@_ZN20DictTest_add_el_Test8TestBodyEv"])
