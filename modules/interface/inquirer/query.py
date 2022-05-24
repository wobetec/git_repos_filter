from __future__ import print_function, unicode_literals
import regex

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError


style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


def run(edit = True, placeholder = {'keyInc': '', 'keyExc': '', 'parInc': '', 'parExc': '', 'pag_count': 1, 'all_pages': False, 'more_filters': '', 'others': ''}):

    if edit:
        print("Edit query: ")
    else:
        print("Create the query: ")
    questions = [
        {
            'type': 'input',
            'name': 'keyInc',
            'default': placeholder['keyInc'],
            'message': 'Keywords to include:',
        },
        {
            'type': 'input',
            'name': 'keyExc',
            'default': placeholder['keyExc'],
            'message': 'Keywords to exclude:',
        },
        {
            'type': 'input',
            'name': 'parInc',
            'default': placeholder['parInc'],
            'message': 'Parameters to include:',
        },
        {
            'type': 'input',
            'name': 'ParExc',
            'default': placeholder['parExc'],
            'message': 'Parameters to exclude:',
        },
        {
            'type': 'input',
            'name': 'pag_count',
            'default': placeholder['pag_count'],
            'message': 'Results per page:',
            'validate': NumberValidator,
            'filter': lambda val: int(val)
        },
        {
            'type': 'confirm',
            'name': 'all_pages',
            'default': placeholder['all_pages'],
            'message': 'Get all pages?',
            'default': False
        },
        {
            'type': 'input',
            'name': 'more_filters',
            'default': placeholder['more_filters'],
            'message': 'More filters:',
        },
        {
            'type': 'input',
            'name': 'others',
            'default': placeholder['others'],
            'message': 'Others:',
        },
    ]

    answers = prompt(questions, style=style)
    print(answers)
    return answers
