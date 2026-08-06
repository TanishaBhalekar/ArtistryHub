from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Commission, CommissionStatus, PaymentStatus

commissions = Blueprint('commissions', __name__, url_prefix='/commissions')

KANBAN_STAGES = [
    CommissionStatus.REQUESTED.value,
    CommissionStatus.ACCEPTED.value,
    CommissionStatus.SKETCH.value,
    CommissionStatus.COLORING.value,
    CommissionStatus.REVISION.value,
    CommissionStatus.DELIVERED.value
]

@commissions.route('/', methods=['GET'])
@login_required
def index():
    """Kanban dashboard view sorting active commissions by status columns."""
    all_commissions = Commission.query.filter_by(artist_id=current_user.id).order_by(Commission.created_at.desc()).all()
    
    # Group commissions by status column
    kanban_columns = {stage: [] for stage in KANBAN_STAGES}
    total_value = 0.0

    for comm in all_commissions:
        stage_key = comm.status.value if isinstance(comm.status, CommissionStatus) else str(comm.status)
        if stage_key in kanban_columns:
            kanban_columns[stage_key].append(comm)
        else:
            kanban_columns[CommissionStatus.REQUESTED.value].append(comm)
        
        if comm.cost:
            total_value += float(comm.cost)

    return render_template(
        'commissions/index.html',
        kanban_columns=kanban_columns,
        stages=KANBAN_STAGES,
        total_commissions=len(all_commissions),
        total_value=total_value
    )


@commissions.route('/create', methods=['POST'])
@login_required
def create():
    """Create a new client commission."""
    title = request.form.get('title', '').strip()
    client_name = request.form.get('client_name', '').strip()
    client_email = request.form.get('client_email', '').strip()
    client_notes = request.form.get('client_notes', '').strip()
    description = request.form.get('description', '').strip()
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

    # Map status enum
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


@commissions.route('/<int:commission_id>/status', methods=['POST'])
@login_required
def update_status(commission_id):
    """Update a commission card's current status (supports JSON or Form POST)."""
    comm = Commission.query.filter_by(id=commission_id, artist_id=current_user.id).first_or_404()
    
    if request.is_json:
        data = request.get_json()
        new_status_str = data.get('status')
    else:
        new_status_str = request.form.get('status')

    if not new_status_str:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Status parameter missing.'}), 400
        flash('Status parameter missing.', 'danger')
        return redirect(url_for('commissions.index'))

    matched_status = None
    for s in CommissionStatus:
        if s.value == new_status_str:
            matched_status = s
            break

    if not matched_status:
        if request.is_json:
            return jsonify({'success': False, 'error': 'Invalid status value.'}), 400
        flash('Invalid status value.', 'danger')
        return redirect(url_for('commissions.index'))

    comm.status = matched_status
    comm.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        if request.is_json:
            return jsonify({'success': True, 'id': comm.id, 'new_status': comm.status.value})
        flash(f'Updated "{comm.title}" status to {comm.status.value}.', 'success')
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({'success': False, 'error': 'Database commit failed.'}), 500
        flash('Failed to update status.', 'danger')

    return redirect(url_for('commissions.index'))


@commissions.route('/<int:commission_id>/update', methods=['POST'])
@login_required
def update_details(commission_id):
    """Update estimated project delivery pricing, client details, revision count, or payment status."""
    comm = Commission.query.filter_by(id=commission_id, artist_id=current_user.id).first_or_404()

    title = request.form.get('title', '').strip()
    client_name = request.form.get('client_name', '').strip()
    client_email = request.form.get('client_email', '').strip()
    client_notes = request.form.get('client_notes', '').strip()
    description = request.form.get('description', '').strip()
    cost_val = request.form.get('cost', '').strip()
    revision_count_val = request.form.get('revision_count', '').strip()
    deadline_str = request.form.get('deadline', '').strip()
    payment_status_str = request.form.get('payment_status', '').strip()

    if title:
        comm.title = title
    if client_name:
        comm.client_name = client_name
    if client_email:
        comm.client_email = client_email
    if client_notes is not None:
        comm.client_notes = client_notes
    if description is not None:
        comm.description = description

    if cost_val:
        try:
            comm.cost = float(cost_val)
        except ValueError:
            pass

    if revision_count_val:
        try:
            comm.revision_count = int(revision_count_val)
        except ValueError:
            pass

    if deadline_str:
        try:
            comm.deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
        except ValueError:
            pass

    if payment_status_str:
        for ps in PaymentStatus:
            if ps.value == payment_status_str or ps.name.lower() == payment_status_str.lower():
                comm.payment_status = ps
                break

    comm.updated_at = datetime.utcnow()

    try:
        db.session.commit()
        flash(f'Updated commission details for "{comm.title}".', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to update commission details.', 'danger')

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
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete commission.', 'danger')

    return redirect(url_for('commissions.index'))
