from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models import Project, Document
from app.projects.forms import ProjectForm, DocumentForm
from app import db
import os
from datetime import datetime
from werkzeug.utils import secure_filename

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/')
@login_required
def list_projects():
    projects = Project.query.order_by(Project.updated_at.desc()).all()
    return render_template('projects/list.html', projects=projects)

@projects_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if not current_user.is_admin:
        flash('Только администратор может создавать проекты', 'error')
        return redirect(url_for('projects.list_projects'))
    
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            project_url=form.project_url.data
        )
        
        if form.cover_image.data:
            filename = secure_filename(form.cover_image.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'projects', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            form.cover_image.data.save(filepath)
            project.cover_image = filename
        
        db.session.add(project)
        db.session.commit()
        flash('Проект успешно создан!', 'success')
        return redirect(url_for('projects.list_projects'))
    
    return render_template('projects/create.html', form=form)

@projects_bp.route('/<int:project_id>')
@login_required
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('projects/detail.html', project=project)

@projects_bp.route('/<int:project_id>/add_document', methods=['GET', 'POST'])
@login_required
def add_document(project_id):
    if not current_user.is_admin:
        flash('Только администратор может добавлять документы', 'error')
        return redirect(url_for('projects.project_detail', project_id=project_id))
    
    project = Project.query.get_or_404(project_id)
    form = DocumentForm()
    
    if form.validate_on_submit():
        document = Document(
            name=form.name.data,
            project_id=project.id
        )
        
        if form.file.data:
            filename = secure_filename(form.file.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], 'documents', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            form.file.data.save(filepath)
            document.file_path = filename
        elif form.url.data:
            document.url = form.url.data
        
        db.session.add(document)
        db.session.commit()
        flash('Документ успешно добавлен!', 'success')
        return redirect(url_for('projects.project_detail', project_id=project.id))
    
    return render_template('projects/add_document.html', project=project, form=form)