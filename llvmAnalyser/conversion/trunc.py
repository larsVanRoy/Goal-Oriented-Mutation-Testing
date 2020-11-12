from llvmAnalyser.types import get_type
from llvmAnalyser.llvmStatement import LlvmStatement


class TruncAnalyzer:
    def __init__(self):
        pass

    @staticmethod
    def analyze_trunc(tokens):
        trunc = Trunc()

        # pop potential assignment sequence
        while tokens[0] != "trunc":
            tokens.pop(0)

        # pop the trunc instruction
        tokens.pop(0)

        # pop the original type
        _, tokens = get_type(tokens)

        # get the value
        value = ""
        while tokens[0] != "to":
            value += tokens.pop(0)
        trunc.set_value(value)

        # get the final type
        final_type, tokens = get_type(tokens)
        trunc.set_final_type(final_type)

        return trunc


class Trunc(LlvmStatement):
    def __init__(self):
        super().__init__()
        self.value = None
        self.final_type = None

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def set_final_type(self, final_type):
        self.final_type = final_type

    def get_final_type(self):
        return self.final_type

    def get_used_variables(self):
        return [self.value]
