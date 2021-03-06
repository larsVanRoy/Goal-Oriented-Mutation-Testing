class Node:
    def __init__(self, node_id, node_name):
        self.node_id = node_id
        self.node_name = node_name
        self.inc = list()
        self.out = list()
        self.context = None
        self.arguments = list()
        self.final = False
        self.assertion = False
        self.start = False
        self.test_var = False
        self.mutator_function = False

    def __str__(self):
        if self.final:
            return "{}[label=\"{}\", shape=doublecircle]".format(self.node_id, self.node_name)
        return "{}[label=\"{}\"]".format(self.node_id, self.node_name)

    def set_name(self, name):
        self.node_name = name

    def get_name(self):
        return self.node_name

    def get_id(self):
        return self.node_id

    def set_final(self):
        self.final = True

    def set_test(self):
        self.start = True

    def is_test(self):
        return self.start

    def is_mutator(self):
        return self.mutator_function

    def set_mutator(self):
        self.mutator_function = True

    def set_assertion(self):
        self.assertion = True

    def is_assertion(self):
        return self.assertion

    def set_test_var(self):
        self.test_var = True

    def is_test_var(self):
        return self.test_var

    def add_argument(self, argument):
        self.arguments.append(argument)

    def get_arguments(self):
        return self.arguments

    def set_context(self, context):
        self.context = context

    def get_context(self):
        return self.context

    def add_inc(self, node):
        self.inc.append(node)

    def get_incs(self):
        return self.inc

    def add_out(self, node):
        self.out.append(node)

    def get_outs(self):
        return self.out
