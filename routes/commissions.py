import os
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Commission, CommissionStatus, PaymentStatus, CommissionDeliverable
from services.image_processing import allowed_file

commissions = Blueprint('commissions', __name__, url_prefix='/commissions')

# 4 Clean Kanban Pipeline Categories as requested in Prompt 3
KANBAN_PIPELINE = [
    {
        'id': 'requests',
        'title': 'New Requests',
        'badge_class': 'bg-warning-subtle text-warning border-warning-subtle',
        'statuses': [CommissionStatus.REQUESTED.value]
    },
    {
        'id': 'in_progress',
        'title': 'In Progress (Sketch/Color)',
        'badge_class': 'bg-primary-subtle text-info border-info-subtle',
        'statuses': [CommissionStatus.ACCEPTED.value, CommissionStatus.SKETCH.value, CommissionStatus.COLORING.value]
    },
    {
        'id': 'revisions',
        'title': 'Under Review / Revisions',
        'badge_class': 'bg-danger-subtle text-danger border-danger-subtle',
        'statuses': [CommissionStatus.REVISION.value]
    },
    {
        'id': 'completed',
        'title': 'Completed / Delivered',
        'badge_class': 'bg-success-subtle text-success border-success-subtle',
        'statuses': [CommissionStatus.DELIVERED.value]
    }
]

@commissions.route('/', methods=['GET'])
@login_required
def index():
    """Kanban pipeline view with 4 clean columns and prominent + Create Commission button."""
    all_commissions = Commission.query.filter_by(artist_id=current_user.id).order_by(Commission.created_at.desc()).all()
    
    # Organize into 4 columns
    columns = {col['id']: [] for col in KANBAN_PIPELINE}
    total_value = 0.0

    for comm in all_commissions:
        status_val = comm.status.value if isinstance(comm.status, CommissionStatus) else str(comm.status)
        
        if status_val == CommissionStatus.REQUESTED.value:
            columns['requests'].append(comm)
        elif status_val in [CommissionStatus.ACCEPTED.value, CommissionStatus.SKETCH.value, CommissionStatus.COLORING.value]:
            columns['in_progress'].append(comm)
        elif status_val == CommissionStatus.REVISION.value:
            columns['revisions'].append(comm)
        elif status_val == CommissionStatus.DELIVERED.value:
            columns['completed'].append(comm)
        else:
            columns['requests'].append(comm)

        if comm.cost:
            total_value += float(comm.cost)

    return render_template(
        'commissions/index.html',
        pipeline=KANBAN_PIPELINE,
        columns=columns,
        total_commissions=len(all_commissions),
        total_value=total_value
    )


@commissions.route('/<int:commission_id>', methods=['GET'])
@login_required
def detail(commission_id):
    """Detailed Commission View with Milestones, Deliverable Uploads, Client Info, Financials & Activity Timeline."""
    comm = Commission.query.filter_by(id=commission_id, artist_id=current_user.id).first_or_404()
    deliverables = CommissionDeliverable.query.filter_by(commission_id=comm.id).order_by(CommissionDeliverable.created_at.desc()).all()
    
    return render_template(
        'commissions/detail.html',
        commission=comm,
        deliverables=deliverables
    )


@commissions.route('/create', methods=['POST'])
@login_required
def create():
    """Create a new client commission from modal."""
    title = request.form.get('title', '').strip()
    client_name = request.form.get('client_name', '').strip()
    client_email = request.form.get('client_email', '').strip()
    client_notes = request.form.get('client_notes', '').strip()
    description = request.form.get('description', '').strip()
    medium = request.form.get('medium', 'Digital 2D').strip()
    priority = request.form.get('priority', 'Normal').strip()
    cost_val = request.form.get('cost', '0.00').strip()
    deadline_str = request.form.get('deadline', '').strip()
    status_str = request.form.get('status', CommissionStatus.REQUESTED.value)

    if not title or not client_name or not client_email:
        flash('Title, Client Name, and Client Email are required.', 'danger')
        return redirect(url_for('commissions.index'))

    try:
        cost = float(cost_val) if cost_val else 0.00
    except ValueError:
        cost = 0.00

    deadline = None
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
        except ValueError:
            pass

    status_enum = CommissionStatus.REQUESTED
    for s in CommissionStatus:
        if s.value == status_str:
            status_enum = s
            break

    new_comm = Commission(
        artist_id=current_user.id,
        title=title,
        client_name=client_name,
        client_email=client_email,
        client_notes=client_notes,
        description=description,
        medium=medium,
        priority=priority,
        cost=cost,
        deadline=deadline,
        status=status_enum
    )

    try:
        db.session.add(new_comm)
        db.session.commit()
        flash(f'Commission "{title}" for {client_name} created successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to create commission. Please try again.', 'danger')

    return redirect(url_for('commissions.index'))


@commissions.route('/<int:commission_id>/upload-deliverable', methods=['POST'])
@login_required
def upload_deliverable(commission_id):
    """Upload a sketch or final deliverable iteration with versioning (v1, v2, final)."""
    comm = Commission.query.filter_by(id=commission_id, artist_id=current_user.id).first_or_404()
    version_tag = request.form.get('version_tag', 'v1').strip()
    notes = request.form.get('notes', '').strip()
    file = request.files.get('file')

    if not file or file.filename == '':
        flash('Please select a file to upload.', 'danger')
        return redirect(url_for('commissions.detail', commission_id=comm.id))

    if not allowed_file(file.filename):
        flash('Invalid file format. Please upload PNG, JPG, JPEG, or WEBP.', 'danger')
        return redirect(url_for('commissions.detail', commission_id=comm.id))

    upload_folder = current_app.config.get('UPLOAD_FOLDER')
    filename = secure_filename(file.filename)
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    saved_filename = f"comm_{comm.id}_{version_tag}_{timestamp}_{filename}"
    filepath = os.path.join(upload_folder, saved_filename)
    
    file.save(filepath)

    deliverable = CommissionDeliverable(
        commission_id=comm.id,
        filename=saved_filename,
        version_tag=version_tag,
        notes=notes
    )

    # Automatically increment revision count
    if version_tag != 'final':
        comm.revision_count = comm.revision_count + 1

    try:
        db.session.add(deliverable)
        db.session.commit()
        flash(f'Deliverable iteration {version_tag.upper()} uploaded successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to save deliverable record.', 'danger')

    return redirect(url_for('commissions.detail', commission_id=comm.id))


@commissions.route('/<int:commission_id>/milestones', methods=['POST'])
@login_required
def update_milestones(commission_id):
    """Update milestone checklist status."""
    comm = Commission.query.filter_by(id=commission_id, artist_id=current_user.id).first_or_404()
    comm.accepted_done = True if request.form.get('accepted_done') else False
    comm.sketch_done = True if request.form.get('sketch_done') else False
    comm.render_done = True if request.form.get('render_done') else False
    comm.delivered_done = True if request.form.get('delivered_done') else False

    try:
        db.session.commit()
        flash('Milestone checklist updated.', 'success')
    except Exception:
        db.session.rollback()
        flash('Failed to update milestones.', 'danger')

    return redirect(url_for('commissions.detail', commission_id=comm.id))


@commissions.route('/<int:commission_id>/action', methods=['POST'])
@login_required
def quick_action(commission_id):
    """Execute quick workflow actions: Submit for Review, Request Payment, Mark Delivered."""
    comm = Commission.query.filter_by(id=commission_id, artist_id=current_user.id).first_or_404()
    action = request.form.get('action', '').strip()

    if action == 'submit_review':
        comm.status = CommissionStatus.REVISION
        flash(f'"{comm.title}" submitted for client review!', 'info')
    elif action == 'request_payment':
        comm.payment_status = PaymentStatus.DEPOSIT_PAID
        flash(f'Payment request sent for "{comm.title}". Deposit marked as pending.', 'success')
    elif action == 'mark_delivered':
        comm.status = CommissionStatus.DELIVERED
        comm.payment_status = PaymentStatus.PAID_IN_FULL
        comm.delivered_done = True
        flash(f'"{comm.title}" marked as Delivered & Paid in Full!', 'success')

    comm.updated_at = datetime.utcnow()

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        flash('Action update failed.', 'danger')

    return redirect(url_for('commissions.detail', commission_id=comm.id))


@commissions.route('/<int:commission_id>/status', methods=['POST'])
@login_required
def update_status(commission_id):
    """Update status (supports JSON or Form POST for Kanban drag/drop or clicks)."""
    comm = Commission.query.filter_by(id=commission_id, artist_id=current_user.id).first_or_404()
    
    if request.is_json:
        data = request.get_json()
        new_status_str = data.get('status')
    else:
        new_status_str = request.form.get('status')

    matched_status = None
    for s in CommissionStatus:
        if s.value == new_status_str:
            matched_status = s
            break

    if matched_status:
        comm.status = matched_status
        comm.updated_at = datetime.utcnow()
        try:
            db.session.commit()
            if request.is_json:
                return jsonify({'success': True, 'id': comm.id, 'new_status': comm.status.value})
            flash(f'Updated "{comm.title}" status to {comm.status.value}.', 'success')
        except Exception:
            db.session.rollback()

    return redirect(url_for('commissions.index'))


@commissions.route('/<int:commission_id>/delete', methods=['POST'])
@login_required
def delete(commission_id):
    """Delete a commission record."""
    comm = Commission.query.filter_by(id=commission_id, artist_id=current_user.id).first_or_404()
    try:
        db.session.delete(comm)
        db.session.commit()
        flash(f'Commission "{comm.title}" deleted.', 'info')
    except Exception:
        db.session.rollback()
        flash('Failed to delete commission.', 'danger')

    return redirect(url_for('commissions.index'))
