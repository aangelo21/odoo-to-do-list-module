from odoo import models, fields, api  # type: ignore


class People(models.Model):
    _name = 'todo_list.people'
    _description = 'todo_list.people'

    name = fields.Char(string="Name")
    surname = fields.Char(string="Surname")
    birth_date = fields.Date(string="Birth Date")
    task_ids = fields.One2many("todo_list.tasks", "people_id", string="Tasks")

