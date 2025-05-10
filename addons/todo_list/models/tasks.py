from odoo import models, fields, api  # type: ignore


class Tasks(models.Model):
    _name = 'todo_list.tasks'
    _description = 'todo_list.tasks'

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    status = fields.Selection(
        [('not_started', 'Not Started'),
         ('in_progress', 'In Progress'),
         ('completed', 'Completed')],
        string="Status",
        default='not_started'
    )
    priority = fields.Selection(
        [('low', 'Low'),
         ('medium', 'Medium'),
         ('high', 'High')],
        string="Priority",
        default='medium'
    )
    people_id = fields.Many2one("todo_list.people", string="Assigned To")
    calendar_event_id = fields.Many2one('calendar.event', string='Calendar Event', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super().create(vals_list)
        for task in tasks:
            calendar_event = self.env['calendar.event'].create({
                'name': task.name,
                'description': task.description,
                'start': task.start_date,
                'stop': task.end_date or task.start_date,
                'user_id': self.env.user.id,
            })
            task.calendar_event_id = calendar_event
        return tasks

    def write(self, vals):
        result = super().write(vals)
        for task in self:
            if task.calendar_event_id:
                task.calendar_event_id.write({
                    'name': task.name,
                    'description': task.description,
                    'start': task.start_date,
                    'stop': task.end_date or task.start_date,
                })
        return result

    def unlink(self):
        for task in self:
            if task.calendar_event_id:
                task.calendar_event_id.unlink()
        return super().unlink()
