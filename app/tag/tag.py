from flask import render_template, request, flash, redirect, url_for
from .. import helperfunctions as hf
from .. import tagmanagement as tm
from . import tag_bp


@tag_bp.route('/tag', methods=('GET', 'POST'))
def tag():
    conn = hf.get_db_connection()
    cur=conn.cursor(dictionary=True) 
    if request.method == 'POST':
        if request.form['action']=='Add':
            tag = request.form['tag']
            if not tag:
                flash('Tag is required!')
                return redirect(url_for('tag'))
            sql='insert into notetag(tag,entry_datetime, update_datetime) VALUES (?, now(), now())'
            cur.execute(sql,(tag,))
        if request.form['action']=='Delete':
            tm.deleteTagsById(request.form.getlist('delete-checks'))
        conn.commit()
        conn.close()
    tags=tm.listTagsFull()
    return render_template('tag.html', items=tags)
