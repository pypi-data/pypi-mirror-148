import copy
import functools
import json
import pprint
import random
import time
import types
from threading import Timer

import jsonpickle
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QThread, forcepoint, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

"""
naming conventions 
s... string
s_var_name = 'asdf'
n... number
n_var_name = 1123
n_var_name = -1123
n_var_name = 11.23
n_var_name = -11.23
a... array
a_var_name = [...]
o...
o_var_name = {}
o_var_name = My_class()
dict or pyhton class instance

if the datatype is unknow or variable , dont mention it at all 
for example 
for attr_val in dict 
    print(attr_val)
"""


def rsetattr(obj, attr, val):
    pre, _, post = attr.rpartition(".")
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


def rgetattr(obj, str_attr, *args):
    """
    gets you an nested property value with a str , for example
    rgetattr(o_test, 'a.b.0.e.2'), arrays can be accessed via number

    o_class_or_dict {
        a : 1,
        b : {
            a: [
                0,
                1,
                2,
                {
                    a : True
                },
                [
                    0,
                    1,
                    2
                ]
            ]
        }
    }
    use it like this

    rgetattr(o_class_or_dict, 'a') # returns  a
    rgetattr(o_class_or_dict, 'b.a') # returns object
    rgetattr(o_class_or_dict, 'b.a.2') # returns 2
    rgetattr(o_class_or_dict, 'b.a.3.a') # returns True
    rgetattr(o_class_or_dict, 'b.a.3.4.1') # returns 1


    Args:
        obj: dict or object
        attr:
    Returns:
        any
    """

    def _getattr(obj, str_attr):
        if type(obj) is list and str_attr.isnumeric():
            return obj[int(str_attr)]
        if type(obj) is dict:
            return obj.get(str_attr, *args)

        return getattr(obj, str_attr, *args)

    return functools.reduce(_getattr, [obj] + str_attr.split("."))


def remove_nested_dicts_or_class_instances_from_dict_or_class_instance(obj):
    """
    removes shallow
    """
    arr_attrs_to_delete = []
    # obj.__class__.__module__ == 'builtins' checks if obj is user defined class via 'class my_class_name:...'
    if obj.__class__.__module__ != "builtins":
        # loop over class instance attrs
        for str_attr in dir(obj):
            # ignore the builtin python attributes
            if str_attr.startswith("__"):
                continue
            attr = getattr(obj, str_attr)
            if attr.__class__.__module__ != "builtins" or type(attr) is dict:
                arr_attrs_to_delete.append(str_attr)

    if type(obj) is dict:
        # loop over dict attrs
        for str_attr, attr in obj.items():
            if attr.__class__.__module__ != "builtins" or type(attr) is dict:
                arr_attrs_to_delete.append(str_attr)

    for str_attr_to_delete in arr_attrs_to_delete:
        if obj.__class__.__module__ != "builtins":
            delattr(obj, str_attr_to_delete)
        if type(obj) is dict:
            del obj[str_attr_to_delete]


class Pyqt5_view_object:
    instances = []

    @staticmethod
    def delete_instances_object_path_dot_notation_starts_with_string(string):

        instances_to_delete = []
        for instance in Pyqt5_view_object.instances:

            if instance.dict_object["object_path_dot_notation"].startswith(string):
                instances_to_delete.append(instance)

        for instance_to_delete in instances_to_delete:

            del Pyqt5_view_object.instances[Pyqt5_view_object.instances.index(instance_to_delete)]

    @classmethod
    def get_root_instance(self):
        # for obj in gc.get_objects():
        #     if isinstance(obj, self):
        #         print(obj)
        for obj in self.instances:
            # print(obj['dict_object']['object_path_dot_notation'])
            if obj.dict_object["object_path_dot_notation"] == "":
                return obj

    @staticmethod
    def get_instance_by_object_path_dot_notation(str_object_path_dot_notation):
        for obj in Pyqt5_view_object.instances:
            if obj.dict_object["object_path_dot_notation"] == str_object_path_dot_notation:
                return obj

    @staticmethod
    def remove_from_layout_by_object_path_dot_notation(str_object_path_dot_notation):
        instance = Pyqt5_view_object.get_instance_by_object_path_dot_notation(
            str_object_path_dot_notation
        )
        instance.remove_from_layout()

    qt_layout_class_names = ["QHBoxLayout", "QVBoxLayout"]
    qt_input_events = [
        "event",
        "closeEvent",
        "focusInEvent",
        "focusOutEvent",
        "enterEvent",
        "keyPressEvent",
        "keyReleaseEvent",
        "leaveEvent",
        "mouseDoubleClickEvent",
        "mouseMoveEvent",
        "mousePressEvent",
        "mouseReleaseEvent",
        "moveEvent",
        "paintEvent",
        "resizeEvent",
        "sliderMoved",
    ]
    qt_input_events_special = ["textChanged", "valueChanged"]
    qt_class_names_with_setText = [
        "QLabel",
        "QPushButton",
        "QLineEdit",
    ]
    qt_class_names_with_setValue = ["QSlider"]

    def __init__(self, dict_object, data):

        self.__class__.instances.append(self)

        self.data = data

        # prevent pyqt5 error 'QLayout::addChildLayout: layout "" already has a parent'
        self.connect_with_parent_pyqt5_view_object_executed = False

        # we only must use the first dimension of this dict_object
        remove_nested_dicts_or_class_instances_from_dict_or_class_instance(dict_object)
        self.dict_object = dict_object

        self.qt_constructor = dict_object["qt_constructor"]
        self.qt_layout_added = False
        if self.qt_constructor.find("(") == -1:
            self.qt_constructor = self.qt_constructor + "()"
        self.qt_class_name = self.get_qt_class_name_by_constructor(self.qt_constructor)
        # self.qt_object = globals()[self.qt_class_name]()
        self.qt_constructor_instance_varname = "tmp_qt_constructor_instance"
        self.qt_object = exec(self.qt_constructor_instance_varname + " = " + self.qt_constructor)
        # since we cannot set background color or .hide / .show on QHBoxlayout and QVBoxlayout
        # we neet a wrapper of this kind
        # q_layout
        #   q_widget <- can be visible toggled with .show / .hide , can have bg color with setStylesheet backgroun-color...
        #       q_layout
        #           qt_object <- instance of actual object from view.. label or input or layout or widget ,

        # why 4 additional qt_objects ?
        # because the qt_object type is dynamic: layout or qwidget
        # and qt allows only the following behaviour with addWidget or addLayout or setLayout
        # -------------------------------
        # possible      possible
        # qt_layout     qt_layout
        #   qt_laout        qt_widget
        # possible      not possible
        # qt_widget     qt_widget
        #   qt_layout       qt_widget
        self.qt_object = locals()[self.qt_constructor_instance_varname]

        self.qt_layout_great_grand_parent = QVBoxLayout()
        self.qt_widget_grand_parent = QWidget()
        self.qt_layout_parent = QVBoxLayout()
        self.qt_layout_great_grand_parent.addWidget(self.qt_widget_grand_parent)
        self.qt_widget_grand_parent.setLayout(self.qt_layout_parent)

        self.qt_layout_great_grand_parent.setSpacing(0)
        # self.qt_layout_great_grand_parent.setMargin(0)

        self.qt_layout_parent.setSpacing(0)
        # self.qt_layout_parent.setMargin(0)

        if self.is_qt_layout_class_name():
            self.qt_layout_parent.addLayout(self.qt_object)
        else:
            self.qt_layout_parent.addWidget(self.qt_object)

        # self.qt_object = exec(self.qt_constructor)
        self.code_statements_before_string_evaluation = []
        self.code_statements_after_string_evaluation = []

        if "c" in dict_object:
            self.c = dict_object["c"]  # c is shor for children, can be string, or data path
        else:
            self.c = None

        if "code_statements_before_string_evaluation" in self.dict_object:
            self.code_statements_before_string_evaluation = self.dict_object[
                "code_statements_before_string_evaluation"
            ]
        if "code_statements_after_string_evaluation" in self.dict_object:
            self.code_statements_after_string_evaluation = self.dict_object[
                "code_statements_after_string_evaluation"
            ]

        self.synced_o_data_path = None
        self.render_function = None

        self.init_event_listeners()

    def get_parent_pyqt5_view_object(self):

        if self.dict_object["object_path_dot_notation"] == "":
            return None

        # ...{arrayindex}.c.3 -> ...{arrayindex}
        parts = self.dict_object["object_path_dot_notation"].split(".")

        parent_pyqt5_view_object = None
        while parent_pyqt5_view_object == None:
            parts.pop(-1)
            parts.pop(-1)
            parent_object_path_dot_notation = ".".join(parts)
            print(parent_object_path_dot_notation)
            parent_pyqt5_view_object = Pyqt5_view_object.get_instance_by_object_path_dot_notation(
                parent_object_path_dot_notation
            )

        print("parent_pyqt5_view_object")
        print(parent_pyqt5_view_object)
        return parent_pyqt5_view_object
        print(parent_pyqt5_view_object)
        # # ...{arrayindex}.c.3 -> ...{arrayindex}
        # parts = self.dict_object['object_path_dot_notation'].split('.')
        # parts.pop(-1)
        # parts.pop(-1)
        # parent_object_path_dot_notation = ".".join(parts)

        # # print('self')
        # # print(self.dict_object['object_path_dot_notation'])
        # # print('parent')
        # # print(parent_object_path_dot_notation)
        # #time.sleep(2)
        # return Pyqt5_view_object.get_instance_by_object_path_dot_notation(
        #     parent_object_path_dot_notation
        # )

    def connect_with_parent_pyqt5_view_object(self):
        # prevent pyqt5 error 'QLayout::addChildLayout: layout "" already has a parent'
        if not self.connect_with_parent_pyqt5_view_object_executed or True:

            self.connect_with_parent_pyqt5_view_object_executed = True

            parent_pyqt5_view_object = self.get_parent_pyqt5_view_object()

            if parent_pyqt5_view_object == None:
                return True

            parent_pyqt5_view_object.qt_object.addLayout(self.qt_layout_great_grand_parent)

    def remove_from_layout(self):
        self.c = '""'

        parent_pyqt5_view_object = self.get_parent_pyqt5_view_object()

        Pyqt5_app.delete_items_of_pyqt5_layout(self.qt_layout_great_grand_parent)

        # self.qt_layout_great_grand_parent.setParent(None)
        # return True

    def init_event_listeners(self):

        if self.is_qt_layout_class_name() == False:
            self.qt_object.setMouseTracking(True)

        for i in self.dict_object:
            if hasattr(self.qt_object, i):
                function_body = self.data.get_void_function_by_string(
                    self.dict_object[i],
                    self.code_statements_before_string_evaluation,
                    self.code_statements_after_string_evaluation + ["Pyqt5_app.re_render_view()"],
                )
                is_qt_input_event = False
                if i in Pyqt5_view_object.qt_input_events:
                    is_qt_input_event = True
                    setattr(self.qt_object, i, function_body)
                if i in Pyqt5_view_object.qt_input_events_special:
                    # function_body = self.data.get_void_function_by_string(self.dict_object[i], self.code_statements_before_string_evaluation, self.code_statements_after_string_evaluation)
                    is_qt_input_event = True
                    # self.qt_object.event = self.qt_object_event_function
                    localattrname = (
                        "i_cannot_connect_this_function_directly_thats_why_i_set_this_attribute_"
                        + str(i)
                    )
                    setattr(self.qt_object, localattrname, function_body)
                    qt_event_function = getattr(self.qt_object, i)
                    qt_event_function.connect(getattr(self.qt_object, localattrname))
                    # self.qt_object.valueChanged.connect(
                    #     lambda val: function_body(val)
                    # )
                    # qt_object_fun = getattr(self.qt_object, i)
                    # qt_object_fun.connect(getattr(self.qt_object, localattrname))

                if is_qt_input_event == False:
                    function_body = self.data.get_return_function_by_string(
                        self.dict_object[i],
                        self.code_statements_before_string_evaluation,
                        self.code_statements_after_string_evaluation,
                    )
                    attr = getattr(self.qt_object, i)
                    if callable(attr):
                        function_return = function_body()
                        # print(attr)
                        attr(function_return)
                        # print(attr)

    def update_evaluated_properties_for_parent_widget_or_layout(self, qt_widget_or_layout):
        for i in self.dict_object:
            if i in Pyqt5_view_object.qt_input_events:
                # we skip the event handlers since we initialize them in an other place
                continue
            else:
                if hasattr(qt_widget_or_layout, i):
                    qt_function_or_property = getattr(qt_widget_or_layout, i)

                    evaluated_return = self.get_evaluated_return_by_string(self.dict_object[i])

                    if callable(qt_function_or_property):
                        qt_function_or_property(evaluated_return)
                    else:
                        setattr(qt_widget_or_layout, i, evaluated_return)

    def get_evaluated_return_by_string(self, function_string):
        function_body = self.data.get_return_function_by_string(
            function_string,
            self.code_statements_before_string_evaluation,
            self.code_statements_after_string_evaluation,
        )
        try:
            evaluated_return = function_body()
        except:
            print("!-!-! error !-!-!")
            print('"c or code_statements" attrbute is invalid')
            print(
                "code_statements_before_string_evaluation:"
                + str(self.code_statements_before_string_evaluation)
            )
            print("c:" + str(self.c))
            print(
                "code_statements_after_string_evaluation:"
                + str(self.code_statements_after_string_evaluation)
            )

            print("data:")
            pprint.pprint(self.data.__dict__)
            raise
        return evaluated_return

    def update_evaluated_properties(self):
        #  not only the 'c' property wants to be evaluated, for example there are properties like
        #  (widget).setStyleSheet or (layout).setSpacing
        #  so we have to try to evaluate those as well
        self.update_evaluated_properties_for_parent_widget_or_layout(self.qt_widget_grand_parent)
        self.update_evaluated_properties_for_parent_widget_or_layout(
            self.qt_layout_great_grand_parent
        )

        if self.wants_to_be_evaluated():

            evaluated_return = str(self.get_evaluated_return_by_string(self.c))

            self.set_evaluated_return(evaluated_return)

    def set_evaluated_return(self, evaluated_return):
        if self.qt_class_name in Pyqt5_view_object.qt_class_names_with_setText:
            self.qt_object.setText(evaluated_return)

        if self.qt_class_name in Pyqt5_view_object.qt_class_names_with_setValue:
            self.qt_object.setValue(int(evaluated_return))

    def get_qt_class_name_by_constructor(self, string):
        parts = string.split("(")
        qt_class_name = parts.pop(0)
        return qt_class_name

    def has_c_property(self):
        return "c" in self.dict_object

    def has_children(self):
        return type(self.c) == list
        # self.type = 'has_children'
        # has children

    def wants_to_be_synced(self):
        try:
            rgetattr(self.data, self.c)
            return True
        except:
            return False
            # wants to be synced
            # self.type = 'wants_to_be_synced'
            # c is the path of a data object which has to be synced
            # for example data.cameras[0]

    def wants_to_be_evaluated(self):
        return (
            self.is_qt_layout_class_name() == False
            and self.has_children() == False
            and self.has_c_property() == True
            and self.wants_to_be_synced() == False
        )
        # self.type = 'wants_to_be_evaluated'
        # wants to be evaluated

    def is_qt_layout_class_name(self):
        return self.qt_class_name in Pyqt5_view_object.qt_layout_class_names

    def if_condition_is_true(self):
        # if condition is true or non existsing
        if "if" in self.dict_object:
            condition = self.dict_object["if"]
            function_body = self.data.get_return_function_by_string(
                condition,
                self.code_statements_before_string_evaluation,
                self.code_statements_after_string_evaluation,
            )
            condition_result = function_body()
            return condition_result
        else:
            return True

    def re_render_qt_object(self):
        # ensure the layout is connected
        self.connect_with_parent_pyqt5_view_object()

        if self.if_condition_is_true():
            self.qt_widget_grand_parent.show()
            self.update_evaluated_properties()
        else:
            self.qt_widget_grand_parent.hide()

    # def __repr__(self):
    #     return self.toJSON()
    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #         sort_keys=True, indent=4)


class View_object:
    def __init__(self, parent_view_object, original_object, data):
        self.child_view_objects = []
        # self.parent_view_object = parent_view_object
        self.parent_view_object = None
        self.original_object = original_object
        self.data = data
        self.for_statement = None
        self.pyqt5_view_objects = []

        self.update_pyqt5_view_objects()

    def get_parent_view_object_pyqt5_view_objects(self):
        if self.parent_view_object != None:
            arr = self.parent_view_object.pyqt5_view_objects
        else:
            arr = []

        return arr

    def handle_for_statement_update_pyqt5_view_objects(self):
        if "index_in_array" in self.original_object:
            print("self.original_object['index_in_array']")
            print(self.original_object["index_in_array"])

        parts = str(self.original_object["for"]).split(" in ")
        self.array_var_name_in_for_statement = parts.pop(len(parts) - 1)
        parts = parts.pop(0).split(",")
        self.value_var_name_in_for_statement = parts.pop(0).strip()
        self.index_var_name_in_for_statement = parts.pop(0).strip()

        code_statements_before_string_evaluation = (
            self.get_code_statements_before_string_evaluation_by_array_index(0)
        )
        print(code_statements_before_string_evaluation)

        evaluated_array_var_len = self.data.get_return_function_by_string(
            "len(" + self.array_var_name_in_for_statement + ")",
            code_statements_before_string_evaluation,
        )()

        print(str(evaluated_array_var_len) + ": length of array_var_name_in_for")
        print(str(len(self.pyqt5_view_objects)) + ": length of actual array")
        if evaluated_array_var_len == len(self.pyqt5_view_objects):
            return False
        # print(length)
        # exit()

        for key in range(len(self.pyqt5_view_objects), evaluated_array_var_len):
            original_object_copy = self.original_object.copy()

            original_object_copy["index_in_array"] = key

            #  code_statements_before_string_evaluation = self.get_code_statements_before_string_evaluation_by_array_index(key)

            original_object_copy[
                "code_statements_before_string_evaluation"
            ] = code_statements_before_string_evaluation + [
                str(self.value_var_name_in_for_statement)
                + " = "
                + str(self.array_var_name_in_for_statement)
                + "["
                + str(key)
                + "]"
            ]

            pyqt5_view_object = Pyqt5_view_object(original_object_copy, self.data)
            self.pyqt5_view_objects.append(pyqt5_view_object)
            # print(value)

    def has_parent_view_object(self):
        return self.parent_view_object != None

    def get_code_statements_before_string_evaluation_by_array_index(self, array_index):

        arr = []

        if self.has_parent_view_object():
            # print(len(self.parent_view_object.pyqt5_view_objects))
            parent_view_object_pyqt5_view_object = self.parent_view_object.pyqt5_view_objects[
                array_index
            ]
            if (
                "code_statements_before_string_evaluation"
                in parent_view_object_pyqt5_view_object.dict_object
            ):
                # print(parent_view_object_pyqt5_view_object.dict_object['code_statements_before_string_evaluation'])
                arr = parent_view_object_pyqt5_view_object.dict_object[
                    "code_statements_before_string_evaluation"
                ]

        return arr

    def update_pyqt5_view_objects(self):

        # print('json or original_object')
        # print(json.dumps(self.original_object))
        # print(type(self.original_object['qt_constructor']))
        # if the original_object has a for property we have to handle it here
        if "for" in self.original_object:
            self.handle_for_statement_update_pyqt5_view_objects()
        else:
            self.original_object[
                "code_statements_before_string_evaluation"
            ] = self.get_code_statements_before_string_evaluation_by_array_index(0)
            self.original_object["index_in_array"] = 0
            self.pyqt5_view_objects = [Pyqt5_view_object(self.original_object, self.data)]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class View_template:
    """
    1. str_view_json to o_view_dict
    2. convert "for" attr in each object into for_statement_objects : [...]
    3. foreach obj in dict create corresponding pyqt5 object

    """

    def __init__(self, data):

        self.data = data
        self.str_view_json = """
            {
                "qt_constructor" : "QVBoxLayout", 
                "setStyleSheet": "'background-color: '+random_color()",
                "setSpacing": "n_slider_val.value",
                "setContentMargins": "n_slider_val.value",
                "c": [
                    {
                        "setStyleSheet": "'background-color: '+random_color()",
                        "qt_constructor" : "QHBoxLayout", 
                        "c":[
                            { 
                                "qt_constructor": "QPushButton",  
                                "c": "a_button_texts[int(random.random()*len(a_button_texts))]", 
                                "mousePressEvent" : "print('printing to console')"
                            },
                            { 
                                "qt_constructor": "QPushButton",  
                                "c": "a_button_texts[0]", 
                                "mousePressEvent" : "print('printing to console')"
                            },
                            { 
                                "qt_constructor": "QPushButton",  
                                "c": "str(s_btn_text_by_hy.value)", 
                                "mousePressEvent" : "by_and_hy(s_btn_text_by_hy)"
                            }
                        ]
                    },
                    {
                        "qt_constructor" : "QHBoxLayout", 
                        "c":[

                                { 
                                    "qt_constructor": "QSlider(Qt.Horizontal)", 
                                    "c": "n_slider_val.value",
                                    "valueChangedasdf": "print('value '+str(event)+' changed at:'+str(time.time()))",
                                    "valueChanged": "n_slider_val._value = event",
                                    "sliderMovedasdf": "print('value '+str(event)+' changed at:'+str(time.time()))",
                                    "setMinimum" : "1", 
                                    "setMaximum" : "10" 
                                },
                                { 
                                    "qt_constructor": "QLabel", 
                                    "c":"'slider val : '+str(n_slider_val.value)"
                                }, 
                                { 
                                    "qt_constructor": "QPushButton",  
                                    "c": "'reset slider val to 5'", 
                                    "mousePressEvent" : "n_slider_val.value = 5"
                                }

                        ]
                    },
                    {
                        "qt_constructor" : "QHBoxLayout", 
                        "c":[
                                { 
                                    "qt_constructor": "QLineEdit",  
                                    "c": "s_input_text.value", 
                                    "textChanged": "s_input_text._value = event"
                                },
                                { 
                                    "qt_constructor": "QLabel",  
                                    "c": "'text is :'+str(s_input_text.value)" 
                                },
                                {
                                    "qt_constructor" : "QHBoxLayout", 
                                    "c":[
                                            { 
                                                "qt_constructor": "QPushButton",  
                                                "c": "'reset text above'", 
                                                "mousePressEvent" : "s_input_text.value = 'reseetet text'"
                                            },
                                            { 
                                                "qt_constructor": "QPushButton",  
                                                "c": "'print to console'", 
                                                "mousePressEvent" : "print('printing to console')"
                                            },

                                            { 
                                                "qt_constructor": "QPushButton",  
                                                "c": "'click me'", 
                                                "mousePressEvent": "test_synced_obj()", 
                                                "mouseMoveEvent" : "print('damn mouse moved on butto')"
                                            }
                                    ]
                                }


                        ]
                    },
                    {
                    "qt_constructor_qwidget_is_not_allowed_use_qwdiget_property_to_render_on_widget": "QWidget",  
                    "setStyleSheet": "'background-color: '+random_color()",
                    "c": [
                        { 
                            "qt_constructor_this_wont_be_possible_since_qwidget_cannot_directly_be_child_of_qwidget": "QLabel",  
                            "c": "'qlabel directly child of qwidget'" 
                        },
                        {
                        "qt_constructor": "QHBoxLayout",  
                        "c": [
                            {
                                "qt_constructor" : "QVBoxLayout"
                            }
                        ]
                        }
                    ]
                    },
                    { 
                        "qt_constructor": "QPushButton",  
                        "c": "'len(cameras)'+str(len(cameras))", 
                        "mousePressEvent": "Pyqt5_app.re_render_view()" ,
                        "mousePressEventdisabled": "print('lel whz is this alreadz called')" 
                    },
                    {
                        "qt_constructor" : "QHBoxLayout", 
                        "c":[
                                { 
                                    "qt_constructor": "QPushButton",  
                                    "c": "'add cam'", 
                                    "mousePressEvent": "cameras.append(1)"       
                                },
                                { 
                                    "qt_constructor": "QPushButton",  
                                    "c": "'remove cam'", 
                                    "mousePressEvent": "cameras.pop(0)"       
                                }
                        ]
                    },
                    {
                        "if": "len(cameras) > 2",
                        "qt_constructor": "QHBoxLayout",  
                        "c":[
                            {
                                "if": "len(cameras) > 3", 
                                "qt_constructor": "QLabel",  
                                "c": "str(time.time())+' i show because cameras is bigger 3'"           
                            },
                            {
                                "if": "len(cameras) > 1", 
                                "qt_constructor": "QLabel",  
                                "c": "str(time.time())+' i show because cameras is bigger 1'"           
                            },
                            {
                                "qt_constructor": "QLabel",  
                                "c": "str(time.time())+' i show because cameras is bigger 2'"           
                            }
                        ]
                    },
                    {
                        "qt_constructor": "QHBoxLayout", 
                        "c":[
                                { 
                                    "qt_constructor": "QPushButton",  
                                    "c": "'add to string array'", 
                                    "mousePressEvent": "a_strings.append(Synced_data_obj('more txt'+str(len(a_strings))))"       
                                },
                                { 
                                    "qt_constructor": "QPushButton",  
                                    "c": "'remove from string array'", 
                                    "mousePressEvent": "a_strings.pop(1)"       
                                }

                        ]
                    },
                    {
                        "qt_constructor":"QHBoxLayout", 
                        "c": [
                                { 
                                    "qt_constructor": "QLabel",  
                                    "c": "'len(a_strings):'+str(len(a_strings))" 
                                },
                                { 
                                    "qt_constructor": "QLabel",  
                                    "c": "'str(a_strings):'+str(str(a_strings))" 
                                }
                        ]
                    },
                    {
                        "qt_constructor": "QLabel",  
                        "c": "str(time.time())+'i want to get rendered'"
                    },
                    {
                        "qt_constructor": "QLabel",  
                        "c": "len(cameras)"
                    },
                    {
                        "qt_constructor": "QVBoxLayout",  
                        "c": [
                            {
                                "qt_constructor" : "QHBoxLayout", 
                                "for": "val1, key in a_strings",
                                "c":[
                                    {
                                        "for": "value_asdf_test, key in a_strings",
                                        "qt_constructor":"QLabel", 
                                        "c":"str(value_asdf_test.value)"
                                    }
                                ]
                            }
                            ]
                    },
                    {
                        "qt_constructor": "QLabel",  
                        "c": "s_text.value"
                    }
                ]
            }
        """
        self.str_view_json_test_arrays = """
        
                {
                    "qt_constructor": "QVBoxLayout",  
                    "c": [
                        {
                            "qt_constructor" : "QHBoxLayout", 
                            "for": "val1, key in a_strings",
                            "c":[
                                {
                                    "for": "value_asdf_test, key in a_strings",
                                    "qt_constructor":"QLabel", 
                                    "c":"'str arr val '+str(value_asdf_test.value)"
                                }
                            ]
                        }
                        ]
                }

            
        """
        self.str_view_json_test_nesting = """
        
                {
                    "qt_constructor": "QVBoxLayout",  
                    "c": [
                            {
                                "qt_constructor": "QLabel",  
                                "c": "'asdf'"
                            }, 
                            {
                                "qt_constructor": "QVBoxLayout",  
                                "c": [
                                        {
                                            "qt_constructor": "QLabel",  
                                            "c": "'asdf'"
                                        }, 
                                        {
                                            "qt_constructor": "QVBoxLayout",  
                                            "c": [
                                                    {
                                                        "qt_constructor": "QLabel",  
                                                        "c": "'asdf'"
                                                    }
                                                ]
                                        }
                                    ]
                            }
                        ]
                }    
        """

        self.str_view_json_test_array_1d = """
        
                {
                    "qt_constructor": "QVBoxLayout",  
                    "c": [
                            {
                                "qt_constructor" : "QHBoxLayout", 
                                "for": "val1, key in a_strings",
                                "c": [
                                    {
                                        "qt_constructor": "QLabel",  
                                        "c": "val1.value"
                                    }
                                ]
                            }
                        ]
                }

        """
        self.str_view_json_test_array_2d = """
                        {
                    "qt_constructor": "QVBoxLayout",  
                    "c": [
                        {
                            "qt_constructor" : "QHBoxLayout", 
                            "for": "val1, key in a_strings",
                            "c":[
                                {
                                    "for": "value_asdf_test, key in a_strings",
                                    "qt_constructor":"QLabel", 
                                    "c":"'for loop 2 '+str(value_asdf_test.value)"
                                }
                            ]
                        }
                        ]
                }
        """
        self.o_view_dict = None

    def render_view_without_reset(self):
        """
        renders the view without reseting it
            1. recursive update for statement objects
            2. foreach pyqt5_view_object instance .re_render_qt_object()
        """

        self.recursive_update_for_statement_objects(self.o_view_dict)

        for instance in Pyqt5_view_object.instances:
            instance.re_render_qt_object()

    def get_rendered_root_pyqt5_qt_object(self):
        """
        converts json to dict and renders it
            1. convert json to dict
            2. rendering the view
        Raises:
            Error when str_view_json is not correct
        """
        self.o_view_dict = json.loads(self.str_view_json)

        if type(self.o_view_dict) != dict:
            raise Exception(
                "root of str_view_json has to be one single object {...}, not an array"
            )
        if "for" in self.o_view_dict:
            raise Exception('root of str_view_json must not contain a "for" property')

        self.render_view_without_reset()

        # self.test_recursive_update_for_statement_objects()

        root_pyqt5_view_object = Pyqt5_view_object.get_root_instance()

        return root_pyqt5_view_object.qt_layout_great_grand_parent

    def test_recursive_update_for_statement_objects(self):
        """
        testing the rendering of the for_statement_objects
        """

        print("-------------------")
        print("testing list.append")
        print("-------------------")
        print("")
        self.data.a_strings.append(Synced_data_obj("a_strings text 3"))
        self.data.a_strings.append(Synced_data_obj("a_strings text 4"))

        self.write_o_view_dict_to_json(self.o_view_dict)
        self.render_view_without_reset()

        print("-------------------")
        print("testing list.pop")
        print("-------------------")
        print("")
        self.data.a_strings.pop(0)
        self.data.a_strings.pop(2)

        self.write_o_view_dict_to_json(self.o_view_dict)
        self.render_view_without_reset()

        print("-------------------")
        print("testing list = ... / setattr")
        print("-------------------")
        print("")
        self.data.a_strings = [
            Synced_data_obj("txt 1"),
            Synced_data_obj("text 2"),
            Synced_data_obj("str 3"),
            Synced_data_obj("str 3"),
            Synced_data_obj("str 3"),
        ]
        self.write_o_view_dict_to_json(self.o_view_dict)
        self.render_view_without_reset()

    def write_o_view_dict_to_json(self, obj):
        """
        writes the object formatted/beautified to json file
        filename time.time()+{functionname}.json
        """
        f = open(str(time.time()) + "write_o_view_dict_to_json.json", "w")

        f.write(
            json.dumps(
                json.loads(jsonpickle.encode(obj, unpicklable=False)), indent=4, sort_keys=True
            )
        )
        f.close()

        print("file written")

    def recursive_update_for_statement_objects(
        self, object, parent_object=None, parent_object_path_dot_notation=None
    ):
        """
            updates the "for" attr in every object,
            before
            {
                ...
                "for": "num_index, o_val in data_array"
                "a": 1,
                "b": 1,
                "c": [
                    {},...
                ],
            }
            after
            {
                ...
                "for": "num_index, o_val in data_array"
                "a": 1,
                "b": 1,
                "c": [
                    {},...
                ],
                "for_statement_objects": [
                    "a": 1,
                    "b": 1,
                    "c": [
                        {},...
                    ],
                ]
            }
        Args:

        """
        if not "qt_constructor" in object:
            print("skipping dict_object, no qt_constructor property is set!")
            return object
        if parent_object == None:
            code_statements_before_string_evaluation = []
            object_path_dot_notation = ""
        else:
            code_statements_before_string_evaluation = parent_object[
                "code_statements_before_string_evaluation"
            ].copy()
            object_path_dot_notation = parent_object_path_dot_notation

        # carry down
        if "code_statements_before_string_evaluation" not in object:
            object[
                "code_statements_before_string_evaluation"
            ] = code_statements_before_string_evaluation

        if "for" in object:

            parts = str(object["for"]).split(" in ")
            array_var_name_in_for_statement = parts.pop(len(parts) - 1)
            parts = parts.pop(0).split(",")
            value_var_name_in_for_statement = parts.pop(0).strip()
            index_var_name_in_for_statement = parts.pop(0).strip()

            # get the evaluated length of data array
            evaluated_array_var_len = self.data.get_return_function_by_string(
                "len(" + array_var_name_in_for_statement + ")",
                code_statements_before_string_evaluation,
            )()

            if "for_statement_objects" not in object:
                object["for_statement_objects"] = []

            if evaluated_array_var_len > len(object["for_statement_objects"]):

                for key in range(len(object["for_statement_objects"]), evaluated_array_var_len):

                    # important use deepcopy to copy the object
                    object_copy = copy.deepcopy(object)

                    # remove some attrs to prevent circular reference
                    del object_copy["for_statement_objects"]
                    del object_copy["for"]

                    # add parts of the for statement
                    object_copy[
                        "array_var_name_in_for_statement"
                    ] = array_var_name_in_for_statement
                    object_copy[
                        "value_var_name_in_for_statement"
                    ] = value_var_name_in_for_statement
                    object_copy[
                        "index_var_name_in_for_statement"
                    ] = index_var_name_in_for_statement
                    object_copy["index_number_in_for_loop"] = key

                    # carry down and extend code_statements_before_string_evaluation
                    object_copy[
                        "code_statements_before_string_evaluation"
                    ] = code_statements_before_string_evaluation + [
                        str(value_var_name_in_for_statement)
                        + " = "
                        + str(array_var_name_in_for_statement)
                        + "["
                        + str(key)
                        + "]"
                    ]

                    # insert into for_statement_objects list
                    object["for_statement_objects"].insert(key, object_copy)

            if evaluated_array_var_len < len(object["for_statement_objects"]):
                # data_array is smaller than for_statement_object
                # objects were removed from data array
                o_for_statement_object_to_delete = []

                for num_index, o_for_statement_object in enumerate(
                    object["for_statement_objects"]
                ):

                    if num_index >= evaluated_array_var_len:
                        o_for_statement_object_to_delete.append(o_for_statement_object)

                for o_for_statement_object in o_for_statement_object_to_delete:

                    num_index = object["for_statement_objects"].index(o_for_statement_object)
                    pyqt5_view_object_to_delete = (
                        Pyqt5_view_object.get_instance_by_object_path_dot_notation(
                            o_for_statement_object["object_path_dot_notation"]
                        )
                    )

                    pyqt5_view_object_to_delete.remove_from_layout()

                    # to delete all children objects we can delete all instances beginning with the
                    Pyqt5_view_object.delete_instances_object_path_dot_notation_starts_with_string(
                        o_for_statement_object["object_path_dot_notation"]
                    )

                    del object["for_statement_objects"][num_index]

        # ----- start create pyqt5_view_object -----
        # create the pyqt5_view_object instance and reference it on the dict, pass if available parent object pyqt5_view_object reference
        object["object_path_dot_notation"] = str(object_path_dot_notation)

        if "has_instance_of_pyqt5_view_object" not in object:

            if "for_statement_objects" not in object:

                object_copy = copy.deepcopy(object)

                # flag the existance of an instance of Pyqt5_view_object for this o_dict_view_object
                object["has_instance_of_pyqt5_view_object"] = True

                # unfortunately we cannot reference the instance on the o_dict_view_object
                # object['pyqt5_view_object'] = Pyqt5_view_object... # not working
                # deepcopy makes trouble...
                Pyqt5_view_object(object_copy, self.data)

        # ----- end  create pyqt5_view_object -----

        # we could get rid of the 'c' in this original object with the 'for' , but we need it for future for_statement_objects, since we make deepcopy for new data_array objects
        if "for_statement_objects" in object:

            for fstoindex, for_statement_object in enumerate(object["for_statement_objects"]):
                # carry down and extend object_path_dot_notation
                for_statement_object["object_path_dot_notation"] = (
                    object["object_path_dot_notation"]
                    + ".for_statement_objects"
                    + "."
                    + str(fstoindex)
                )

                for_statement_object = self.recursive_update_for_statement_objects(
                    for_statement_object, object, for_statement_object["object_path_dot_notation"]
                )

        if "for_statement_objects" not in object:

            if "c" in object:

                if type(object["c"]) == list:
                    for oindex, child_object in enumerate(object["c"]):
                        # carry down and extend object_path_dot_notation
                        object_path_dot_notation_o = (
                            object["object_path_dot_notation"] + ".c" + "." + str(oindex)
                        )
                        child_object = self.recursive_update_for_statement_objects(
                            child_object, object, object_path_dot_notation_o
                        )

        return object

    # def recursive_foreach_object(self, object, callback):
    # """
    # loop over each object that has a corresponding pyqt5_view_object
    # this could be used if the object_path_dot_notation would not have to be set
    # """
    #     if('for_statement_objects' in object):
    #         for for_statement_object in object['for_statement_objects']:
    #             if 'c' in for_statement_object:
    #                 if(type(for_statement_object['c']) == list):
    #                     for child_object in for_statement_object['c']:
    #                         object = child_object
    #                         parent_object = for_statement_object
    #                         callback(self, object, parent_object)
    #     else:
    #         if 'c' in object:
    #             if(type(object['c']) == list):
    #                 for child_object in object['c']:
    #                     callback(child_object, object)

    #     return object


class Synced_data_obj:
    """
    used to have a observed object
    when .value changes, the corresponding pyqt5_view_objects have to be updated
    as an easy but more resource hungry solution for now
    just every pyqt5_view_object is being re rendered / re evaluated

    test = Synced_data_obj('example value str')
    test.value # returns 'example value str'

    Attrs:
        value: any datatype

    """

    intern_propname_prefix = "_"

    def __init__(self, value):
        self._value = value

    def __setattr__(self, str_attr, value) -> None:
        """
        before
        setattr(obj, 'test') or obj.test = ...
        after
        setattr(obj, '_test') or obj._test = ...
        """
        if str_attr.startswith(Synced_data_obj.intern_propname_prefix) == False:
            super().__setattr__(Synced_data_obj.intern_propname_prefix + str_attr, value)
            Pyqt5_app.re_render_view()
        else:
            super().__setattr__(str_attr, value)

    def __getattribute__(self, str_attr):
        """
        before
        getattr(obj, 'test')
        after
        getattr(obj, '_test')
        """
        if str_attr.startswith(Synced_data_obj.intern_propname_prefix) == False:
            return super().__getattribute__(str(Synced_data_obj.intern_propname_prefix + str_attr))
        else:
            return super().__getattribute__(str_attr)
        # re rendering is only neccessary when setter is called ... Pyqt5_app.re_render_view()


class Yet_more_nested:
    """
    test class
    """

    def __init__(self, id) -> None:
        self.id = id
        self.whichstring = Synced_data_obj("im Yet_more_nested, my id is" + str(self.id))


class Some_deep_nested_shit:
    """
    test class
    """

    def __init__(self, id) -> None:
        self.id = id
        self.whichstring = Synced_data_obj("im Some_deep_nested_shit, my id is" + str(self.id))
        self.aha = Synced_data_obj("asdf")
        self.yet_more_nested_array = [Yet_more_nested(1), Yet_more_nested(2)]


class Camera:
    """
    test class
    """

    def __init__(self) -> None:
        self.fps = Synced_data_obj(100)  # will be data.cameras.fps.value
        # self.xyz = ...
        # self.xyz = ...
        # self.xyz = ...
        # and so on


class Data:
    """
    the data class
    all data for the application has to be referenced here
    to syncronize an object with a view_object
    Synced_data_obj has to be used

    the class can contain function which can be accessed via their name
    """

    def __init__(self) -> None:
        self.cameras = []
        self.s_text = Synced_data_obj("this is text data")
        self.s_input_text = Synced_data_obj("INIT TEXT")
        self.a_button_texts = [
            "Push me!",
            "Smash me!",
            "Click me!",
            "Hit me!",
            "Press me!",
            "clink me!",
            "clack me!",
            "chink me!",
            "snick me!",
            "tick me!",
            "snap me!",
        ]
        self.s_btn_text_by_hy = Synced_data_obj("Try me!")
        self.a_strings = [
            Synced_data_obj("a_strings text 1"),
            Synced_data_obj("a_strings text 2"),
        ]
        self.a_some_deep_nested_shits = [
            Some_deep_nested_shit(1),
            Some_deep_nested_shit(2),
        ]
        self.n_slider_val = Synced_data_obj(1)

    def test_synced_obj(self):
        """
        testing rendering behaviour
        when using time.sleep()
        """
        self.s_text.value = "test 1"
        time.sleep(1)
        self.s_text.value = "test 2"
        time.sleep(1)
        self.s_text.value = "test 3"
        time.sleep(1)
        self.s_text.value = "test 4"
        time.sleep(1)

    def by_and_hy(self, synced_obj):

        synced_obj.value = "by by ..."

        def hy(arg1, synced_obj):
            print(arg1)
            synced_obj.value = "Hy, im back ;->"
            print("")

        r = Timer(1.0, hy, ("has_to_be_passed_idk_why", synced_obj))
        r.start()

    def random_color(self):
        r = lambda: random.randint(0, 255)
        rc = "#%02X%02X%02X" % (r(), r(), r())
        return str(rc)

    def get_return_function_by_string(
        self,
        string,
        code_statements_before_string_evaluation=[],
        code_statements_after_string_evaluation=[],
    ):
        return self.get_function_by_string(
            string,
            True,
            code_statements_before_string_evaluation,
            code_statements_after_string_evaluation,
        )

    def get_void_function_by_string(
        self,
        string,
        code_statements_before_string_evaluation=[],
        code_statements_after_string_evaluation=[],
    ):
        return self.get_function_by_string(
            string,
            False,
            code_statements_before_string_evaluation,
            code_statements_after_string_evaluation,
        )

    def get_function_by_string(
        self,
        string,
        return_evaluated=False,
        code_statements_before_string_evaluation=[],
        code_statements_after_string_evaluation=[],
    ):
        """
        creates a function by string,
        provides every attribute as a local reference
        this makes it more convenient to get access to a data attribute
        for example
        self.test_arr[2].test_data -> test_arr[2].test_data

        Attrs:
            string: string is one single statement
            code_statements_before_string_evaluation: array multiple code statements
            code_statements_after_string_evaluation: array multiple code statements
        """
        str_funname = "fun_" + str((int(time.time())))
        str_fun_str = ""
        arr_fun_str_lines = []
        arr_fun_str_lines.append("def " + str(str_funname) + "(self,event=None,**kvargs):")

        arr_fun_str_lines.append("    for key, value in kvargs.items():")
        arr_fun_str_lines.append("        exec(key+'=value')")

        # provide attributes as local scope references
        for property in dir(self):
            arr_fun_str_lines.append("    " + property + "=" + "self." + property)

        for statement in code_statements_before_string_evaluation:
            arr_fun_str_lines.append("    " + str(statement))

        # create a unique temporary variable name
        if return_evaluated:
            str_varname = "var_" + str((int(time.time())))
            arr_fun_str_lines.append("    " + str_varname + "=" + string)
        else:
            arr_fun_str_lines.append("    " + string)

        for statement in code_statements_after_string_evaluation:
            arr_fun_str_lines.append("    " + str(statement))

        if return_evaluated:
            arr_fun_str_lines.append("    return " + "(" + str_varname + ")")

        str_fun_str = "\n".join(arr_fun_str_lines)

        exec(str_fun_str)

        functionbody = locals()[str_funname]
        # we have to bind the method to the class in order to automatically
        # get the first parameter 'self'
        # simply setattr wont work
        # setattr(self, fname, lambda: functionbody(self))
        # this will bind the method to the self
        setattr(self, str_funname, types.MethodType(functionbody, self))

        return getattr(self, str_funname)


class Pyqt5_app(QWidget):
    arr_instances = []

    @staticmethod
    def delete_items_of_pyqt5_layout(layout):
        """
        og: https://stackoverflow.com/questions/37564728/pyqt-how-to-remove-a-layout-from-a-layout
        user: TheTrowser
        recursively deletes every item of pyqt5 layout
        """
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    Pyqt5_app.delete_items_of_pyqt5_layout(item.layout())

    @staticmethod
    def re_render_view():
        """
        foreach instance
        render_view_without_reset
        """
        for obj in Pyqt5_app.arr_instances:
            obj.render_view_without_reset()

    def __init__(self):
        self.__class__.arr_instances.append(self)

        super().__init__()

        self.initialize_gui()

    def initialize_gui(self):

        self.setWindowTitle("Object Sync")

        self.data = Data()

        # initialize pyqt5_view
        self.view_template = View_template(self.data)

        # most outer layout , is not affected by rendering of view
        self.q_h_box_layout = QHBoxLayout()
        #
        self.render_view = self.view_template.get_rendered_root_pyqt5_qt_object()

        self.q_h_box_layout.addLayout(self.render_view)

        self.setLayout(self.q_h_box_layout)
        self.show()

    def render_view_without_reset(self):
        self.view_template.render_view_without_reset()
