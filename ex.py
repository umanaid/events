@app.route('/message/<id1>/<e_id>', methods=['GET', 'POST'])
def message(id1,e_id):
    if session.get('user') or session.get('vendor'):  # Allow both users and vendors
        if session.get('user'):
            user_type = 'sender'  # User is sender
        else:
            user_type = 'reviver'  # Vendor is receiver

        cursor = mydb.cursor(buffered=True)
        cursor.execute('SELECT user_id FROM users WHERE username=%s', [session.get('user')]) if session.get('user') else cursor.execute('SELECT vendor_id FROM vendors WHERE name=%s', [session.get('vendor')])
        user_id = cursor.fetchone()[0]
        cursor.close()

        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT message_body, DATE_FORMAT(sent_at,'%h:%i %p') AS date, user_id FROM communications WHERE (user_id = %s AND sent_to = %s and event_id=%s) OR (user_id = %s AND sent_to = %s and event_id=%s) ORDER BY sent_at", (id1, user_id, e_id,user_id, id1,e_id))
        messages = cursor.fetchall()
        cursor.close()
        print(messages)

        sender = [(msg[0], msg[1],msg[2]) for msg in messages if msg[2] == user_id]
        receiver = [(msg[0], msg[1],msg[2]) for msg in messages if msg[2] != user_id]

        if request.method == 'POST':
            message = request.form['Message']
            subject = request.form['subject']
            cursor = mydb.cursor(buffered=True)
            cursor.execute('INSERT INTO communications (user_id, sent_to, message_body, user_type,event_id,message_subject) VALUES (%s, %s, %s, %s,%s,%s)', (id1, user_id, message, user_type,e_id,subject))
            mydb.commit()
            cursor.close()

            cursor = mydb.cursor(buffered=True)
            cursor.execute("SELECT message_body, DATE_FORMAT(sent_at,'%h:%i %p') AS date, user_id FROM communications WHERE (user_id = %s AND sent_to = %s and event_id=%s) OR (user_id = %s AND sent_to = %s and event_id=%s) ORDER BY sent_at", (user_id, id1,e_id, id1, user_id,e_id))
            messages = cursor.fetchall()
            cursor.close()

            sender = [(msg[0], msg[1],msg[2]) for msg in messages if msg[2] == user_id]
            receiver = [(msg[0], msg[1],msg[2]) for msg in messages if msg[2] != user_id]

        return render_template('chatbox.html', sender=sender, receiver=receiver, user_type=user_type,user_id=user_id)
    return redirect(url_for('login'))
@app.route('/umessage/<id1>/<e_id>', methods=['GET', 'POST'])
def umessage(id1,e_id):
    if session.get('user') or session.get('vendor'):  # Allow both users and vendors
        if session.get('user'):
            user_type = 'sender'  # User is sender
        else:
            user_type = 'reviver'  # Vendor is receiver

        cursor = mydb.cursor(buffered=True)
        cursor.execute('SELECT user_id FROM users WHERE username=%s', [session.get('user')]) if session.get('user') else cursor.execute('SELECT vendor_id FROM vendors WHERE name=%s', [session.get('vendor')])
        user_id = cursor.fetchone()[0]
        cursor.close()

        cursor = mydb.cursor(buffered=True)
        cursor.execute("SELECT message_body, DATE_FORMAT(sent_at,'%h:%i %p') AS date, user_id FROM communications WHERE (user_id = %s AND sent_to = %s and event_id=%s) OR (user_id = %s AND sent_to = %s and event_id=%s) ORDER BY sent_at", (id1, user_id, e_id,user_id, id1,e_id))
        messages = cursor.fetchall()
        cursor.close()
        print(messages)

        sender = [(msg[0], msg[1],msg[2]) for msg in messages if msg[2] == user_id]
        receiver = [(msg[0], msg[1],msg[2]) for msg in messages if msg[2] != user_id]

        if request.method == 'POST':
            message = request.form['Message']
            subject = request.form['subject']
            cursor = mydb.cursor(buffered=True)
            cursor.execute('INSERT INTO communications (user_id, sent_to, message_body, user_type,event_id,message_subject) VALUES (%s, %s, %s, %s,%s,%s)', (user_id, id1, message, user_type,e_id,subject))
            mydb.commit()
            cursor.close()

            cursor = mydb.cursor(buffered=True)
            cursor.execute("SELECT message_body, DATE_FORMAT(sent_at,'%h:%i %p') AS date, user_id FROM communications WHERE (user_id = %s AND sent_to = %s and event_id=%s) OR (user_id = %s AND sent_to = %s and event_id=%s) ORDER BY sent_at", (user_id, id1,e_id, id1, user_id,e_id,))
            messages = cursor.fetchall()
            cursor.close()

            sender = [(msg[0], msg[1],msg[2]) for msg in messages if msg[2] == user_id]
            receiver = [(msg[0], msg[1],msg[2]) for msg in messages if msg[2] != user_id]

        return render_template('chatbox.html', sender=sender, receiver=receiver, user_type=user_type,user_id=user_id)
    return redirect(url_for('login'))




app.run(debug=True,use_reloader=True)