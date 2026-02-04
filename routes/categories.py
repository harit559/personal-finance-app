"""
Category Routes - Manage transaction categories.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Category, Transaction, Account

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/')
@login_required
def list_categories():
    """List all categories for the current user."""
    expense_categories = Category.query.filter_by(
        user_id=current_user.id, 
        category_type='expense'
    ).all()
    
    income_categories = Category.query.filter_by(
        user_id=current_user.id, 
        category_type='income'
    ).all()
    
    # Count transactions per category
    for cat in expense_categories + income_categories:
        cat.transaction_count = Transaction.query.filter_by(category_id=cat.id).count()
    
    return render_template('categories/list.html',
                           expense_categories=expense_categories,
                           income_categories=income_categories)


@categories_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_category():
    """Add a new category."""
    if request.method == 'POST':
        category = Category(
            user_id=current_user.id,
            name=request.form['name'],
            category_type=request.form['category_type'],
            icon=request.form.get('icon', '📦'),
            color=request.form.get('color', '#6366f1')
        )
        
        db.session.add(category)
        db.session.commit()
        
        flash('Category created!', 'success')
        return redirect(url_for('categories.list_categories'))
    
    return render_template('categories/add.html')


@categories_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    """Edit a category."""
    category = db.session.get(Category, id)
    if not category:
        return "Not found", 404
    
    # Make sure this category belongs to the current user
    if category.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('categories.list_categories'))
    
    if request.method == 'POST':
        category.name = request.form['name']
        category.category_type = request.form['category_type']
        category.icon = request.form.get('icon', '📦')
        category.color = request.form.get('color', '#6366f1')
        
        db.session.commit()
        flash('Category updated!', 'success')
        return redirect(url_for('categories.list_categories'))
    
    return render_template('categories/edit.html', category=category)


@categories_bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_category(id):
    """
    Delete a category.
    If transactions exist, ask user to migrate them to another category first.
    """
    category = db.session.get(Category, id)
    if not category:
        return "Not found", 404
    
    # Make sure this category belongs to the current user
    if category.user_id != current_user.id:
        flash('Access denied.', 'error')
        return redirect(url_for('categories.list_categories'))
    
    # Count transactions using this category
    transaction_count = Transaction.query.filter_by(category_id=id).count()
    
    if request.method == 'POST':
        # Handle migration if user selected a new category
        new_category_id = request.form.get('new_category_id')
        
        if transaction_count > 0:
            if new_category_id == 'none':
                # Set transactions to no category
                Transaction.query.filter_by(category_id=id).update({'category_id': None})
            elif new_category_id:
                # Migrate to selected category
                Transaction.query.filter_by(category_id=id).update({'category_id': int(new_category_id)})
        
        # Delete the category
        db.session.delete(category)
        db.session.commit()
        
        flash('Category deleted!', 'info')
        return redirect(url_for('categories.list_categories'))
    
    # GET request - show confirmation page with migration options
    # Get other categories of the same type for migration
    other_categories = Category.query.filter(
        Category.user_id == current_user.id,
        Category.id != id,
        Category.category_type == category.category_type
    ).all()
    
    return render_template('categories/delete.html',
                           category=category,
                           transaction_count=transaction_count,
                           other_categories=other_categories)
