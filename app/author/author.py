from flask import Flask, render_template, request, flash, redirect, url_for
from .. import authormanagement as am
from . import author_bp
import re
from flask_login import login_required


@author_bp.route('/author', methods=('GET', 'POST'))
@login_required
def author():
    exisitingBirthyear=''
    exisitingDeathyear=''
    exisitingComment=''
    exisitingFullname=''
    id=0
    if request.method == 'POST':
        if request.form['action']=='Add':
            authorFullname = str(request.form['author_fullname'])
            comment = str(request.form['author_comment'])
            birthyear = str(request.form['author_birthyear'])
            deathyear = str(request.form['author_deathyear'])
            id=int(request.form['author_id'])
            if not authorFullname:
                flash('Name required!')
                return redirect(url_for('author_bp.author'))
            ## search existing authors to confirm no double entry
            am.saveAuthor(authorFullname,birthyear,deathyear,comment,id)
        elif re.search("Edit*",request.form['action']):
            id=re.findall(r'\d+',request.form['action'])[0]
            existingAuthor=am.loadAuthor(id)
            exisitingBirthyear=existingAuthor['birthyear']
            exisitingDeathyear=existingAuthor['deathyear']
            exisitingComment=existingAuthor['comment']
            exisitingFullname=existingAuthor['fullname']
        elif request.form['action'] == 'Delete':
            am.deleteAuthors(request.form.getlist('delete-checks'))
    authorList=am.listAuthors()
    return render_template('author.html', authors=authorList, author_birthyear=exisitingBirthyear, author_deathyear=exisitingDeathyear, author_comment=exisitingComment, author_fullname=exisitingFullname, author_id=id)

