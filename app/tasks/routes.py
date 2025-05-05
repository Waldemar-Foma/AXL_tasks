from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Task, Project, User
from app.tasks.forms import TaskForm
from app import db
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/project/<int:project_id>/create', methods=['GET', 'POST'])
@login_required
def create_task(project_id):
    project = Project.query.get_or_404(project_id)
    form = TaskForm()
    
    # Заполняем список исполнителей
    form.assignee_id.choices = [(u.id, u.username) for u in User.query.order_by('username')]
    
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            priority=form.priority.data,
            deadline=form.deadline.data,
            project_id=project.id,
            assignee_id=form.assignee_id.data
        )
        db.session.add(task)
        db.session.commit()
        flash('Задача успешно создана!', 'success')
        return redirect(url_for('projects.project_detail', project_id=project.id))
    
    return render_template('tasks/create.html', 
                         project=project, 
                         form=form)


@tasks_bp.route('/<int:task_id>/complete')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.assignee_id != current_user.id and not current_user.is_admin:
        flash('Вы не можете завершить эту задачу', 'error')
        return redirect(url_for('projects.project_detail', project_id=task.project_id))
    
    task.status = 'completed'
    db.session.commit()
    flash('Задача отмечена как выполненная!', 'success')
    return redirect(url_for('projects.project_detail', project_id=task.project_id))